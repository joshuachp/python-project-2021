"""Analyzes an input data to give a sentiment score."""

import copy
import csv
from math import ceil
from multiprocessing import Pool
from pathlib import Path

import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn

from .config import config
from .input_data import InputData

POOL_SIZE = 6


class Analyzer():
    def __init__(self, input_data: InputData) -> None:
        input = copy.deepcopy(input_data)
        input.tokenize()
        input.filter()
        self.tokens_list: list[list[str]] = input.tokens_list
        self.sentiment_values: list[tuple[int, int, int]] = []

    @staticmethod
    def penn_to_wn(tag: str) -> str:
        if tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('R'):
            return wn.ADV
        elif tag.startswith('V'):
            return wn.VERB
        return ''

    @staticmethod
    def get_sentiment(word, tag) -> tuple[float, float, float]:
        """Restituisce il punteggio pos, neg e neutro in una tupla."""
        wn_tag = Analyzer.penn_to_wn(tag)
        if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
            return (0, 0, 0)

        synsets = wn.synsets(word, pos=wn_tag, lang=config['lang_code'])
        if not synsets:
            return (0, 0, 0)
        synset = synsets[0]
        swn_synset = swn.senti_synset(synset.name())
        return (swn_synset.pos_score(), swn_synset.neg_score(),
                swn_synset.obj_score())

    @staticmethod
    def get_tokens_sentiments(
            tokens_list: list[list[str]]) -> list[tuple[int, int, int]]:
        result = []
        for tokens in tokens_list:
            values = [
                Analyzer.get_sentiment(token, tag)
                for (token, tag) in nltk.pos_tag(tokens)
            ]
            pos_count = 0
            neg_count = 0
            obj_count = 0
            for (pos, neg, obj) in values:
                if pos > neg and pos > obj:
                    pos_count += 1
                elif neg > pos and neg > obj:
                    neg_count += 1
                else:
                    obj_count += 1
            result.append((pos_count, neg_count, obj_count))
        return result

    def get_sentiment_values(self) -> None:
        print("Start analysis")
        # Check the length of the token list if it is useful to use multiple processes
        if len(self.tokens_list) <= POOL_SIZE:
            self.sentiment_values = self.get_tokens_sentiments(
                self.tokens_list)
        else:
            values = []
            tokens_chunks = []
            n_tokens = ceil(len(self.tokens_list) / POOL_SIZE)
            # Divide the token list into chunks to pass to the pool
            for i in range(POOL_SIZE - 1):
                start = i * n_tokens
                end = start + n_tokens
                tokens_chunks.append(self.tokens_list[start:end])
            start = (POOL_SIZE - 1) * n_tokens
            tokens_chunks.append(self.tokens_list[start:])

            with Pool(POOL_SIZE) as pool:
                pool_results = pool.map(self.get_tokens_sentiments,
                                        tokens_chunks)
            for results in pool_results:
                for value in results:
                    values.append(value)
            self.sentiment_values = values

    def print(self) -> None:
        pos_count = 0
        neg_count = 0
        obj_count = 0
        for (i, [pos, neg, obj]) in enumerate(self.sentiment_values):
            if pos > neg:
                pos_count += 1
                print(f"{i}. Positive frase 🙂")
            elif neg > pos:
                neg_count += 1
                print(f"{i}. Negative frase 🙁")
            else:
                obj_count += 1
                print(f"{i}. Neutral frase 😐")
        print(
            f"There were: {pos_count} positive, {neg_count} negative, {obj_count} neutral reviews."
        )

    def save_csv(self, path: Path, ids=None) -> None:
        if ids is None:
            ids = range(len(self.tokens_list))
        with open(path, "x") as file:
            csv_file = csv.writer(file)
            for (i, [pos, neg, obj]) in zip(ids, self.sentiment_values):
                if pos > neg and pos > obj:
                    res = 'positive'
                elif neg > pos and neg > obj:
                    res = 'negative'
                else:
                    res = 'neutral'
                csv_file.writerow([i, res, pos, neg, obj])

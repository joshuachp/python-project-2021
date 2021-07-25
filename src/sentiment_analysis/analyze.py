"""Analyzes an input data to give a sentiment score."""

import copy

import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn

from .config import config
from .input_data import InputData


class Analyzer():
    def __init__(self, input_data: InputData) -> None:
        input = copy.deepcopy(input_data)
        input.tokenize()
        input.filter()
        self.tokens: list[str] = input.tokens

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

    def get_sentiment_values(self) -> tuple[int, int, int]:
        values = [
            self.get_sentiment(token, tag)
            for (token, tag) in nltk.pos_tag(self.tokens)
        ]
        pos_count = 0
        neg_count = 0
        obj_count = 0
        for (pos, neg, obj) in values:
            if pos > neg and pos > obj:
                pos_count += 1
            elif neg > pos and obj:
                neg_count += 1
            else:
                obj += 1
        return (pos_count, neg_count, obj_count)

    def print(self) -> None:
        [pos, neg, obj] = self.get_sentiment_values()
        if pos > neg and pos > obj:
            print("Positive frase 🙂")
        elif neg > pos and neg > obj:
            print("Negative frase 🙁")
        else:
            print("Neutral frase 😐")
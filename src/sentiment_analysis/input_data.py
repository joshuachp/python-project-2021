"""
Module to fetch and prepare the input data for analysis.

Classes: InputData
"""

import nltk

from .config import config

STOP_WORDS = nltk.corpus.stopwords.words(config["language"])


class InputData():
    """Generic input data class."""
    def __init__(self,
                 data: list[str] = [],
                 tokens: list[list[str]] = []) -> None:
        self.data: list[str] = data
        self.tokens_list: list[list[str]] = tokens

    def tokenize(self) -> None:
        """Tokenize the text in an array of words."""
        tokens_list = []
        for text in self.data:
            tokens = []
            for s in nltk.sent_tokenize(text, language=config['language']):
                for w in nltk.word_tokenize(s, language=config['language']):
                    tokens.append(w)
            tokens_list.append(tokens)
        self.tokens_list = tokens_list

    def filter(self) -> None:
        """Sanitize the input data filtering the stop words and symbols."""
        for (i, tokens) in enumerate(self.tokens_list):
            self.tokens_list[i] = [
                w.lower() for w in tokens
                if w.isalnum() and w.lower() not in STOP_WORDS
            ]

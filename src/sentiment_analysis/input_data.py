"""
Module to fetch and prepare the input data for analysis.

Classes: InputData
"""

import nltk

from .config import config

STOP_WORDS = nltk.corpus.stopwords.words(config["language"])


class InputData():
    """Generic input data class."""
    def __init__(self, text='', tokens=list()) -> None:
        self.text: str = text
        self.tokens: list[str] = tokens

    def tokenize(self) -> None:
        """Tokenize the text in an array of words."""
        tokens = []
        for s in nltk.sent_tokenize(self.text, language=config['language']):
            for w in nltk.word_tokenize(s, language=config['language']):
                tokens.append(w)
        self.tokens = tokens

    def filter(self) -> None:
        """Sanitize the input data filtering the stop words and symbols."""
        self.tokens = [
            w.lower() for w in self.tokens
            if w.isalnum() and w.lower() not in STOP_WORDS
        ]

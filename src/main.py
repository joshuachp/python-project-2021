#!/usr/bin/env python
"""Main file with the example."""

from sentiment_analysis.analyze import Analyzer
from sentiment_analysis.input_data import InputData

if __name__ == '__main__':
    input = InputData("This is a terrible review.")
    analyze = Analyzer(input)
    analyze.print()

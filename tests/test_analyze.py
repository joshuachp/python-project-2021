from src.sentiment_analysis.analyze import Analyzer
from src.sentiment_analysis.input_data import InputData


def test_init():
    input = InputData(["This is terribly bad."])
    analyze = Analyzer(input)
    assert input.tokens_list == []
    assert analyze.tokens_list == [['terribly', 'bad']]


def test_penn_to_wn():
    assert Analyzer.penn_to_wn('JJR') == 'a'


def test_get_sentiment():
    [pos, neg, obj] = Analyzer.get_sentiment('terrible', 'JJ')
    assert neg > pos and neg > obj


def test_get_sentiment_values():
    input = InputData(["This is terribly bad."])
    analyzer = Analyzer(input)
    analyzer.get_sentiment_values()
    assert len(analyzer.sentiment_values) == 1
    (pos, neg, obj) = analyzer.sentiment_values[0]
    assert neg > pos and neg > obj

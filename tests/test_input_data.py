from src.sentiment_analysis.input_data import InputData


def test_tokenize():
    input = InputData("Hello, World!")
    input.tokenize()
    assert input.tokens == ['Hello', ',', 'World', '!']


def test_filter():
    input = InputData("No, but maybe Yes! I Or bad.")
    input.tokenize()
    input.filter()
    assert input.tokens == ['maybe', 'yes', 'bad']

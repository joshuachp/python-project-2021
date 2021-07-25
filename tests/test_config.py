from src.sentiment_analysis.config import config


def test_config():
    assert config['language'] == 'english'

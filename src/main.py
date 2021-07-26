#!/usr/bin/env python
"""Main file with the example."""

from pathlib import Path

from sentiment_analysis.amazon_input import AmazonJsonFile
from sentiment_analysis.analyze import Analyzer
from sentiment_analysis.input_data import InputData
from sentiment_analysis.tripadvs_input import TripAdvisorFile


def print_menu():
    print('''Select option:
    1. Use input text
    2. Use Amazon reviews json file
    3. Use Trip advisor reviews csv file
''')


def input_text():
    text = input("> ")
    analyzer = Analyzer(InputData([text]))
    analyzer.get_sentiment_values()
    analyzer.print()


def amazon_file():
    path = input("path to the json > ")
    analyzer = Analyzer(AmazonJsonFile(Path(path)))
    analyzer.get_sentiment_values()
    analyzer.print()
    path = input("save csv as > ")
    analyzer.save_csv(path)


def trip_advisor_file():
    path = input("path to the csv > ")
    input_data = TripAdvisorFile(Path(path))
    analyzer = Analyzer(input_data)
    analyzer.get_sentiment_values()
    analyzer.print()
    path = input("save csv as > ")
    analyzer.save_csv(path, input_data.ids)


if __name__ == '__main__':
    while (True):
        print_menu()
        try:
            option = int(input('[1-5]> '))
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            print(e)
            continue

        if option == 1:
            input_text()
        elif option == 2:
            amazon_file()
        elif option == 3:
            trip_advisor_file()
        else:
            print('Option not recognized')

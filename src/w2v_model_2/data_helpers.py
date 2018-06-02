import numpy as np
import csv
import pandas
from builtins import range


def load_data():
    """
    Loads and preprocessed data for the dataset.
    Returns input vectors, labels, vocabulary, and inverse vocabulary.
    """
    examples = list(open("./../forumpedia_csv/char_model_train.txt", "r", encoding='utf-8').readlines())
    examples = [s.strip() for s in examples]
    examples_tag = [s.split(':')[0] for s in examples]
    positive_labels = [0 for _ in range(0, examples_tag.count('0'))]
    negative_labels = [1 for _ in range(0, examples_tag.count('1'))]
    y = np.concatenate([positive_labels, negative_labels], 0)
    maximal_length = 0
    x_test_row_int = []
    x_test = []
    list_ex = []
    list_examples = []
    y_test_row = []
    examples = [s.split(':')[1] for s in examples]
    examples = [s.split(' ') for s in examples]
    for example in examples:
        for x in example:
            list_ex.append(int(x))
        list_examples.append(list_ex)
        list_ex = []
    examples = np.array(list_examples)
    for example in examples:
        maximal_length = max(maximal_length, len(example))
    for idx, example in enumerate(examples):
        x_test_row = example
        for x in range(0, maximal_length - len(example)):
            x_test_row.append(0)
        x_test.append(np.array(x_test_row))
    x_test = np.array(x_test)
    return x_test, y, maximal_length

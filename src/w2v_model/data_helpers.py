import numpy as np


def load_data():
    """
    Loads and preprocessed data for the dataset.
    Returns input vectors, labels, vocabulary, and inverse vocabulary.
    """
    # Load and preprocess data
    positive_examples = list(open("./../forumpedia_csv/w2v_model_train.txt", "r", encoding='utf-8').readlines())
    examples = [s.strip().replace(',100', '') for s in positive_examples]
    examples_tag = [s.split(':')[0] for s in examples]
    examples = [s.split(':')[1] for s in examples]
    examples = np.array([s.split('\n') for s in examples])
    examples = np.array([[s1.split(',') for s1 in s] for s in examples])
    examples = [np.array([np.array([s2.split(' ') for s2 in s1]) for s1 in s]) for s in examples]
    array = []

    for sentace in examples:
        array.append(sentace[0])
    examples = np.array(array)

    x_text = examples


    labels = []
    # positive_labels = [[0, 1] for _ in range(0, examples_tag.count('0'))]
    # negative_labels = [[1, 0] for _ in range(0, examples_tag.count('1'))]
    # y = np.concatenate([positive_labels, negative_labels], 0)
    for tag in examples_tag:
        if tag[0] == '0':
            labels.append([0, 1])
        elif tag[0] == '1':
            labels.append([1, 0])
        else:
            AssertionError
    y = np.array(labels)
    sentace_lengths_list = []

    for idx, sentace in enumerate( x_text):
        sentace_lengths_list.append(sentace.shape[0])
        for word in sentace:
            if len(word) != 100:
                print(word)

        #     print(word.shape)
    padding_value = []
    for x in range(0, 100):
        padding_value.append(0)
    padding_value = np.array([np.array(padding_value)])
    X_test = []
    for sentace in x_text:
        sentace_with_padding = sentace
        for x in range(sentace.shape[0], max(sentace_lengths_list)):
            #print(sentace_with_padding.shape)
            if 100 not in sentace_with_padding.shape:
                print('wolabogacosiedzieje')
            sentace_with_padding = np.vstack((sentace_with_padding, padding_value))
        X_test.append(sentace_with_padding)
    X_test = np.array(X_test)
    sentace_lengths_list = []
    for sentace in X_test:
        sentace_lengths_list.append(sentace.shape[0])

    return [X_test, y,  max(sentace_lengths_list)]

import os
from tqdm import tqdm
import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split
from bert.tokenization.bert_tokenization import FullTokenizer

BUG_PAIRS_FILE = 'esn_pairs.json'

BERT_MODEL_NAME = 'uncased_L-12_H-768_A-12'

BERT_CKPT_DIRECTORY = os.path.join('bert_model/', BERT_MODEL_NAME)
BERT_CKPT_FILE = os.path.join(BERT_CKPT_DIRECTORY, 'bert_model.ckpt')
BERT_CONFIG_FILE = os.path.join(BERT_CKPT_DIRECTORY, 'bert_config.json')

def main():
    data = pd.read_json(BUG_PAIRS_FILE)
    train_data, test_data = train_test_split(data, test_size=0.2)
    tokenizer = FullTokenizer(vocab_file=os.path.join(BERT_CKPT_DIRECTORY, 'vocab.txt'))
    bug_pairs_data = BugPairsData(train_data, test_data, tokenizer)
    
class BugPairsData:
    def __init__(self, train_data, test_data, tokenizer: FullTokenizer, max_sequence_length=192):
        self.tokenizer = tokenizer
        self.max_sequence_length = max_sequence_length
        ((self.train_x_1, self.train_x_2, self.train_y), (self.test_x_1, self.test_x_2, self.test_y)) = map(self._prepare_data, [train_data, test_data])
        self.train_x_1, self.train_x_2, self.test_x_1, self.test_x_2 = map(self._apply_padding, [self.train_x_1, self.train_x_2, self.test_x_1, self.test_x_2])


    def _prepare_data(self, dataframe):
        x_1, x_2, y = [], [], []
        for _, row in tqdm(dataframe.iterrows()):
            description_1, description_2, label = row['description_1'], row['description_2'], row['label']
            tokens_1, tokens_2 = self._tokenize(description_1), self._tokenize(description_2)
            token_ids_1, token_ids_2 = self.tokenizer.convert_tokens_to_ids(tokens_1), self.tokenizer.convert_tokens_to_ids(tokens_2)        
            x_1.append(token_ids_1)
            x_2.append(token_ids_2)
            y.append(label)
        return np.array(x_1, dtype=object), np.array(x_2, dtype=object), np.array(y, dtype=object)

    def _apply_padding(self, ids):
        x = []
        for input_ids in ids:
            cut_point = min(len(input_ids), self.max_sequence_length - 2)
            input_ids = input_ids[:cut_point]
            input_ids = input_ids + [0] * (self.max_sequence_length - len(input_ids))
            x.append(np.array(input_ids))
        return np.array(x)


    def _tokenize(self, text):
        tokens = self.tokenizer.tokenize(text)
        tokens = ['[CLS]'] + tokens + ['[SEP]']
        return tokens

if __name__ == '__main__':
    main()
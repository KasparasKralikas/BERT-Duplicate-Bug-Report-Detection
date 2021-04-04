import os
from tqdm import tqdm
import pandas as pd
import numpy as np
import datetime

import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split

import bert
from bert import BertModelLayer
from bert.loader import StockBertConfig, map_stock_config_to_params, load_stock_weights
from bert.tokenization.bert_tokenization import FullTokenizer

BUG_PAIRS_FILE = 'esn_pairs.json'

BERT_MODEL_NAME = 'uncased_L-12_H-768_A-12'

BERT_CKPT_DIRECTORY = os.path.join('bert_model', BERT_MODEL_NAME)
BERT_CKPT_FILE = os.path.join(BERT_CKPT_DIRECTORY, 'bert_model.ckpt')
BERT_CONFIG_FILE = os.path.join(BERT_CKPT_DIRECTORY, 'bert_config.json')

LOG_DIRECTORY = os.path.join('logs', 'duplicate_bug_report_detection_' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))

def main():
    data = pd.read_json(BUG_PAIRS_FILE)
    train_data, test_data = train_test_split(data, test_size=0.2)
    tokenizer = FullTokenizer(vocab_file=os.path.join(BERT_CKPT_DIRECTORY, 'vocab.txt'))
    bug_pairs_data = BugPairsData(train_data, test_data, tokenizer)
    classification_model = ClassificationModel()
    classification_model.create_model(192, BERT_CONFIG_FILE, BERT_CKPT_FILE)
    classification_model.compile_model()
    print('fitting ===============')
    classification_model.fit_model(bug_pairs_data.train_x_1, bug_pairs_data.train_x_2, bug_pairs_data.train_y, LOG_DIRECTORY)
    
class ClassificationModel:
    def create_model(self, max_sequence_length, bert_config_file, bert_ckpt_file):
        with tf.io.gfile.GFile(bert_config_file, 'r') as reader:
            bert_config = StockBertConfig.from_json_string(reader.read())
            bert_params = map_stock_config_to_params(bert_config)
            bert_params.adapter_size = None
            bert = BertModelLayer.from_params(bert_params, name='bert')

        input_ids_1 = keras.layers.Input(shape=(max_sequence_length, ), dtype='int32', name='input_ids_1')
        input_ids_2 = keras.layers.Input(shape=(max_sequence_length, ), dtype='int32', name='input_ids_2')
        bert_output_1 = bert(input_ids_1)
        bert_output_2 = bert(input_ids_2)

        classes_output_1 = keras.layers.Lambda(lambda seq: seq[:, 0, :])(bert_output_1)
        classes_output_2 = keras.layers.Lambda(lambda seq: seq[:, 0, :])(bert_output_2)

        concatenated_output = keras.layers.Concatenate(axis=-1)([classes_output_1, classes_output_2])
        concatenated_output = keras.layers.Dropout(0.5)(concatenated_output)

        logits = keras.layers.Dense(units=1536, activation='tanh')(concatenated_output)
        logits = keras.layers.Dropout(0.5)(logits)
        logits = keras.layers.Dense(units=1, activation='sigmoid')(logits)

        model = keras.Model(inputs=[input_ids_1, input_ids_2], outputs=logits)
        model.build(input_shape=(None, max_sequence_length, max_sequence_length))
        load_stock_weights(bert, bert_ckpt_file)
        
        self.model = model

    def compile_model(self):
        self.model.compile(
            optimizer=keras.optimizers.Adam(1e-5),
            loss=keras.losses.BinaryCrossentropy(),
            metrics=[keras.metrics.Accuracy(name='accuracy'), keras.metrics.Recall(name='recall'), keras.metrics.Precision(name='precission')]
        )
    
    def fit_model(self, train_x_1, train_x_2, train_y, log_directory):
        tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_directory)
        history = self.model.fit(
            x=[train_x_1, train_x_2],
            y=train_y,
            validation_split=0.1,
            batch_size=16,
            shuffle=True,
            epochs=5,
            callbacks=[tensorboard_callback]
        )

    

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
        return np.array(x_1, dtype=object), np.array(x_2, dtype=object), np.array(y, dtype='float32')

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
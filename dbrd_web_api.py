from flask import Flask, request
from sentence_transformers import SentenceTransformer
import os.path as path
import pandas as pd
import numpy as np
import pickle
import json

MODEL_PATH = 'model/paraphrase-distilroberta-dbrd-ooall-40000'

ISSUES_FILE = 'ooall_latest.csv'

EMBEDDINGS_OUTPUT = 'embeddings/ooall_embeddings.pkl'

model = None

issue = None

embeddings = None

PORT = 5000

app = Flask(__name__)

@app.route('/get_duplicates', methods=['POST'])
def get_duplicates():
    body = request.get_json(silent=True)
    description = body['description']
    return 'Hello World of Bugs'

def load_model():
    print('Loading model...')
    model = SentenceTransformer(MODEL_PATH)
    print('Model loaded successfully')
    return model

def load_issues():
    print('Loading issuess...')
    issues = pd.read_csv(ISSUES_FILE)
    issues['full_description'] = issues['short_desc'].astype(str) + '\n' + issues['description'].astype(str)
    print('Loaded {} issues'.format(len(issues)))
    return issues

def generate_embeddings(model, issues):
    embeddings = None
    print('Checking if previously calculated embeddings exist...')
    if path.exists(EMBEDDINGS_OUTPUT):
        embeddings = pickle.load(open(EMBEDDINGS_OUTPUT, 'rb'))
        if len(embeddings) == len(issues):
            print('Found previously calculated embeddings')
            return embeddings
    print('No previously calculated embeddings were found')
    print('Calculating embeddings...')
    embeddings = model.encode(np.array(issues['full_description']), convert_to_tensor=True)
    print('Embeddings calculated successfully')
    print('Saving embeddings...')
    pickle.dump(embeddings, open(EMBEDDINGS_OUTPUT, 'wb'))
    print('Embeddings saved')
    return embeddings

if __name__ == '__main__':
    model = load_model()
    issues = load_issues()
    embeddings = generate_embeddings(model, issues)
    app.run(port=PORT)

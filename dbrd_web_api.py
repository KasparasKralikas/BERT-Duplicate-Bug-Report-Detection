from flask import Flask, request
from sentence_transformers import SentenceTransformer, util
from flask_cors import CORS
import os.path as path
import pandas as pd
import numpy as np
import pickle
import json
import time

MODEL_PATH = 'model/paraphrase-distilroberta-dbrd-ooall-40000'

ISSUES_FILE = 'ooall_latest.csv'

EMBEDDINGS_OUTPUT = 'embeddings/ooall_embeddings.pkl'

model = None

issue = None

embeddings = None

PORT = 5000

app = Flask(__name__)
CORS(app)

@app.route('/get_duplicates/', methods=['POST'])
def get_duplicates():
    body = request.get_json(silent=True)
    description = body['description']
    top_k = body['top_k']
    similar_issues = retrieve_top_k_similar_issues(model, issues, embeddings, description, top_k)
    return {
        'similar_issues': similar_issues
    }

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

def retrieve_top_k_similar_issues(model, issues, embeddings, description, top_k):
    print('Retrieving top-{} similar issues...'.format(top_k))
    start_time = time.time()
    description_embedding = model.encode(description, convert_to_tensor=True)
    results = util.semantic_search(description_embedding, embeddings, top_k=top_k)[0]
    similar_issues = []
    for result in results:
        result_issue = issues.iloc[result['corpus_id']]
        issue = {
            'id': int(result_issue['bug_id']),
            'description': str(result_issue['full_description']),
            'similarity': float(result['score'])
        }
        similar_issues.append(issue)
    end_time = time.time()
    duration_in_secs = end_time - start_time
    print('Retrieved top-{} similar issues in {} seconds'.format(top_k, round(duration_in_secs, 5)))
    return similar_issues

if __name__ == '__main__':
    model = load_model()
    issues = load_issues()
    embeddings = generate_embeddings(model, issues)
    app.run(port=PORT)

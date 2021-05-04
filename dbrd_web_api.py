from flask import Flask, request
import json
from sentence_transformers import SentenceTransformer

MODEL_PATH = 'model/paraphrase-distilroberta-dbrd-ooall-40000'

ISSUES_PATH = 'ooall_latest.csv'

EMBEDDINGS_OUTPUT = 'embeddings/ooall_embeddings.csv'

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

if __name__ == '__main__':
    load_model()
    app.run(port=PORT)

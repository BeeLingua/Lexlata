from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import tokenize
import os
import pandas as pd

# find dataset file path
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

# convert tokenized object to 2 dimensional list
def list2d(texts):
    result = []
    for law in texts:
        line = []
        for token in law:
            line.append(token)
        result.append(line)
    return result

ds_name = 'kanunum-nlp-doc-analysis-dataset.csv'
ds_fp = find(ds_name, '/')
ds = pd.read_csv(ds_fp)

texts = [tokenize(i) for i in ds['data_text']]
# get data_text column and create a list from tokenized texts
text = list2d(texts)
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(text)]

model = Doc2Vec(documents, vector_size=100, window=4, min_count=1, workers=8, epochs=10)

def run(query: str):
    input_text_embedding = [model.infer_vector(query.split())]
    # compute the embedding of input query

    most_similar_docs = model.docvecs.most_similar(input_text_embedding, topn=5)
    # compare with docs

    results = []
    for doc in most_similar_docs:
        results.append({
            'name': ds['baslik'][doc[0]],
            'date': ds['mevzuat_tarihi'][doc[0]],
            'number': ds['mevzuat_no'][doc[0]],
            'info': ''.join(text[doc[0]]),
            'link': ds['url'][doc[0]]
            })
    return results
# Yüklü değillerse gerekli kütüphanelerin yüklenmesi

#!pip install torch
#!pip install transformers

# Gerekli kütüphanelerin içe aktarılması

from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
import nltk
import torch

# Cümle temsillerinin deserialize edilerek RAM'e alınması

import pickle

embeddings = []

for i in range(0, 501):
    with open(f'embeddings/sbert_embeddings{i}.json', 'rb') as file:
        obj = pickle.load(file)
        embeddings.extend(obj)

# Huggingface servisinde barındırılan BERT modelimizin indirilmesi

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sfurkan/LexBERT-turkish-uncased')

# Veri kümemizin içe aktarılması

TARGETED_DATASET_PATH = r'data.csv'

texts = pd.read_csv(TARGETED_DATASET_PATH)

# Herhangi bir cümlenin indexini alıp içinde bulunduğu dokümanın indexini döndüren dictionary veri yapısının oluşturulması

from tqdm import tqdm

sentenceIndex2DocIndex = {}
lastSentenceIndex = 0
currentDocIndex = 0
for text in tqdm(texts.iloc):
    text = text['data_text']
    sentences = text.strip().split('.')
    
    for idx, sentence in enumerate(sentences):
        sentenceIndex2DocIndex[idx + lastSentenceIndex] = currentDocIndex
    
    lastSentenceIndex += len(sentences)
    currentDocIndex += 1

# Verilen girdi dokümanı kullanarak benzer dokümanları döndüren fonksiyon

from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity

def getSimilarDocuments(inputText, topk=10):
    inputEmbedding = model.encode(inputText)

    documentEmbeddings = []
    embeddingIndex = 0
    for idx, text in tqdm(enumerate(texts.iloc)):
        text = text["data_text"]
        sents = text.strip().split('.')
        sentEmbeddings = []
        for sent in sents:
            sentEmbeddings.append(embeddings[embeddingIndex])
            embeddingIndex += 1
        documentEmbeddings.append(sentEmbeddings)


    documentScores = []    
    for docEmb in documentEmbeddings:
        similarities = cosine_similarity(docEmb, [inputEmbedding])
        meanSim = 0
        for sim in similarities:
            meanSim += sim[0]
        meanSim /= len(similarities)
        documentScores.append(meanSim)

    unfilteredDocuments = []
    maxSim = -1
    for idx, docScore in enumerate(documentScores):
        if docScore > maxSim:
            maxSim = docScore
            unfilteredDocuments.append((texts.iloc[idx], docScore))
    
    documentsToReturn = sorted(unfilteredDocuments, key=lambda x: x[1], reverse=True)[:min(len(unfilteredDocuments), topk)]
    
    documentRows = []
    for document, score in documentsToReturn:
        documentRows.append((*document.values, score))
        
        #dfRows.append(pd.DataFrame([document, pd.Series(score)], columns=texts.columns))
    similarDF = pd.DataFrame(documentRows, columns=[*texts.columns, 'Similarity Score'])
    
    return similarDF

# Örnek kullanım

# INPUT_TEXT = 'Elektronik eşya vergilendirmesi hakkında kanun'

# print(getSimilarDocuments(INPUT_TEXT, topk=5)['baslik'][0])





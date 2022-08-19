# Normal modelimize alternatif olarak oluşturduğumuz bir modeldir. Normal modelimizin aksine burada girdinin doküman türünü sınıflandırıyoruz. Bunun sonucu olarak yalnızca girilen dokümanın türünde çıktılar alınıyor.
# 
# Girdilerin (CSV değerlendirme dosyasının) özelliklerine bağlı olarak 2 modelimizin performansı farklılık gösterebileceğinden dolayı duruma göre birini seçeceğiz.


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
model.max_seq_length = 65536


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


# Doküman türünü çıkarabilen 'text classification' modelimizin indirilmesi

from transformers import pipeline

classificationPipeline = pipeline("text-classification", model="sfurkan/LexBERT-textclassification-turkish-uncased", tokenizer = "sfurkan/LexBERT-textclassification-turkish-uncased")


# Girilen dokümanın BERT tarafından kullanılabilmesi için ilk 512 kelimeyi alacak şekilde kırpılması. (Yalnızca 'text classification' için kullanılır)

def cropDocument(document, cropLimit=512):
    totalWords = []
    sentences = document.replace('\n', '. ').split('.')
    for sent in sentences:
        sent = sent.strip()
        words = sent.split(' ')
        for word in words[:-1]:
            if len(totalWords) >= cropLimit:
                return totalWords
            totalWords.append(word)
        totalWords.append(f"{words[-1]}.")
    return ' '.join(totalWords)


# Girilen dokümanın türünü döndürecek fonksiyon

def getDocumentType(inputText):
    return classificationPipeline(cropDocument(inputText))[0]["label"]


# Doküman içerisindeki cümle temsillerinin organizasyonunun 'liste içinde liste' şeklinde bir veri yapısında sağlanması
documentEmbeddings = []
def initializeDocEmbeddings():
    embeddingIndex = 0
    for idx in tqdm(range(texts.shape[0])):
        text = texts.loc[idx]["data_text"]
        sents = text.strip().split('.')
        sentEmbeddings = []
        for sent in sents:
            sentEmbeddings.append(embeddings[embeddingIndex])
            embeddingIndex += 1
        documentEmbeddings.append(sentEmbeddings)
initializeDocEmbeddings()


# Verilen girdi dokümanı kullanarak benzer dokümanları döndüren fonksiyon

from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity

def getSimilarDocuments(inputText, topk=10):
    # Girdinin doküman türünün belirlenmesi
    docType = getDocumentType(inputText)

    inputEmbedding = model.encode(inputText)

    documentScores = []    
    for idx, docEmb in enumerate(documentEmbeddings):
        # Iterate edilen dokümanın kategorisi, aranan kategori değilse atlanması
        if texts.iloc[idx]["kategori"] != docType:
            continue
        
        similarities = cosine_similarity(docEmb, [inputEmbedding])
        meanSim = 0
        for sim in similarities:
            meanSim += sim[0]
        meanSim /= len(similarities)
        documentScores.append((idx, meanSim))

    unfilteredDocuments = []
    maxSim = -1
    for idx, docScore in documentScores:
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

#INPUT_TEXT = "Elektronik eşya vergilendirmesi hakkında kanun"

#print(getSimilarDocuments(INPUT_TEXT, topk=5))
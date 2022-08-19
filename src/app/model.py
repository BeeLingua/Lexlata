DOCUMENT_COUNT = 4000

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import tokenize
import os
import pandas as pd
import string
import json
from rake_nltk import Rake
import re
import math
import zeyrek

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

analyzer = zeyrek.MorphAnalyzer()

def getLemmatizedWordList(sentence):
    return [x[0].lemma for x in analyzer.analyze(sentence) if len(x) > 0 and x[0].lemma not in [*string.punctuation, 'Unk']]

def getPOSTagList(sentence):
    return [x[0].pos for x in analyzer.analyze(sentence) if len(x) > 0 and x[0].pos not in ['Punc', 'Unk']]

TR_STOP = ["ya da", "yada", "a","acaba","altı","altmış","ama","ancak","arada","artık","asla","aslında","aslında","ayrıca","az","bana","bazen","bazı","bazıları","belki","ben","benden","beni","benim","beri","beş","bile","bilhassa","bin","bir","biraz","birçoğu","birçok","biri","birisi","birkaç","birşey","biz","bizden","bize","bizi","bizim","böyle","böylece","bu","buna","bunda","bundan","bunlar","bunları","bunların","bunu","bunun","burada","bütün","çoğu","çoğunu","çok","çünkü","da","daha","dahi","dan","de","defa","değil","diğer","diğeri","diğerleri","diye","doksan","dokuz","dolayı","dolayısıyla","dört","e","edecek","eden","ederek","edilecek","ediliyor","edilmesi","ediyor","eğer","elbette","elli","en","etmesi","etti","ettiği","ettiğini","fakat","falan","filan","gene","gereği","gerek","gibi","göre","hala","halde","halen","hangi","hangisi","hani","hatta","hem","henüz","hep","hepsi","her","herhangi","herkes","herkese","herkesi","herkesin","hiç","hiçbir","hiçbiri","i","ı","için","içinde","iki","ile","ilgili","ise","işte","itibaren","itibariyle","kaç","kadar","karşın","kendi","kendilerine","kendine","kendini","kendisi","kendisine","kendisini","kez","ki","kim","kime","kimi","kimin","kimisi","kimse","kırk","madem","mi","mı","milyar","milyon","mu","mü","nasıl","ne","neden","nedenle","nerde","nerede","nereye","neyse","niçin","nin","nın","niye","nun","nün","o","öbür","olan","olarak","oldu","olduğu","olduğunu","olduklarını","olmadı","olmadığı","olmak","olması","olmayan","olmaz","olsa","olsun","olup","olur","olur","olursa","oluyor","on","ön","ona","önce","ondan","onlar","onlara","onlardan","onları","onların","onu","onun","orada","öte","ötürü","otuz","öyle","oysa","pek","rağmen","sana","sanki","sanki","şayet","şekilde","sekiz","seksen","sen","senden","seni","senin","şey","şeyden","şeye","şeyi","şeyler","şimdi","siz","siz","sizden","sizden","size","sizi","sizi","sizin","sizin","sonra","şöyle","şu","şuna","şunları","şunu","ta","tabii","tam","tamam","tamamen","tarafından","trilyon","tüm","tümü","u","ü","üç","un","ün","üzere","var","vardı","ve","veya","ya","yani","yapacak","yapılan","yapılması","yapıyor","yapmak","yaptı","yaptığı","yaptığını","yaptıkları","ye","yedi","yerine","yetmiş","yi","yı","yine","yirmi","yoksa","yu","yüz","zaten","zira"]
TR_STOP = set(TR_STOP)
    
WORD_TO_DF_JSON_PATH = r"..\..\word2DocFreq.json"
with open(WORD_TO_DF_JSON_PATH, 'r', encoding="utf8") as word2FreqFile:
    WORD_TO_DF = json.load(word2FreqFile)

VOCABULARY_PATH = r"..\..\turkce_kelime_listesi.txt"
with open(VOCABULARY_PATH, 'r', encoding="utf8") as vocabFile:
    VOCABULARY = json.load(vocabFile, strict=False)

def get_keyword_list(TEXT):
    LEMMATIZED_TEXT = ' '.join(getLemmatizedWordList(TEXT))

    rake = Rake(language="turkish", max_length=6)
    rake.extract_keywords_from_text(TEXT)

    keywordsWithScores = list(set(rake.get_ranked_phrases_with_scores()))

    finalKeywordsWithScores = []
    for kwIndex in range(len(keywordsWithScores)):
        score, kw = keywordsWithScores[kwIndex]
        kw = kw.lower()
        if len(kw) >= 2 and not kw.isdigit():
            words = kw.split(' ')
            docFreq = 1
            OOVCount = 0
            for word in words:
                if not word in VOCABULARY:
                    OOVCount += 1
                docFreq *= WORD_TO_DF.get(word, 1)
            docFreq /= len(words)
            
            # Out of vocabulary (OOV) filtrelemesi:
            if OOVCount / len(words) >= 0.6:
                continue
                
            lemmatizedWords = getLemmatizedWordList(kw)
            
            # TF-IDF etkisinin çarpılması:
            score *= len(re.findall(fr"\b{' '.join(lemmatizedWords)}\b", LEMMATIZED_TEXT)) * math.log(DOCUMENT_COUNT / docFreq, 10)
            
            finalKeywordsWithScores.append((kw, score))

    return sorted(finalKeywordsWithScores, reverse=True, key=lambda elem: elem[1])[:5]

#print(get_keyword_list(ds['data_text'][0]))

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
            'info': ds['data_text'][doc[0]],
            'link': ds['url'][doc[0]],
            'keywords': get_keyword_list(ds['data_text'][doc[0]])
            })
    return results
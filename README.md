# Lexlata
Kamuda mevzuat arama motoru

- Öncelikle doc2vec ve tf-idf modellerini denedik ve projemizin temelini attık, sonrasında BERT modelinin başarımının yüksek olması nedeniyle BERT modelini kullanmaya karar verdik.
- BERT modelini eğitmek çok fazla kaynak gerektirdiğinden önceden eğitilmiş bir modeli (https://huggingface.co/dbmdz/bert-base-turkish-cased) temel aldık.
- BERT modelini bize verilen ve mevzuat.gov.tr sitesinden çektiğimiz veriyle eğittik.
- Elde ettiğimiz kelime temsillerini kosinüs benzerliği kullanarak karşılaştırarak en benzer sonucu elde etmeye çalıştık.

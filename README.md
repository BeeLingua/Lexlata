# Lexlata
Kamuda Mevzuat Arama Motoru

Geliştiren Takım: BeeLingua

## Geliştirme Süreci ve Yöntem
- Öncelikle doc2vec ve tf-idf modellerini denedik ve projemizin temelini attık, sonrasında BERT modelinin başarımının yüksek olması nedeniyle BERT modelini kullanmaya karar verdik.
- BERT modelini eğitmek çok fazla kaynak gerektirdiğinden önceden eğitilmiş bir modeli (https://huggingface.co/dbmdz/bert-base-turkish-cased) temel aldık.
- BERT modelini bize verilen veri kümesiyle ve mevzuat.gov.tr sitesinden çektiğimiz veriyle eğittik.
- SBERT kütüphanesini kullanarak bütün cümlelerin vektör temsillerini elde edip kaydettik.
- Yine SBERT kütüphanesi kullanarak sorgu olarak girilen dokümanın da vektör temsilini elde ettik.
- Girilen dokümanın temsili ile sistemde kayıtlı olan dokümanlar içerisindeki cümlelerin temsillerini kosinüs benzerliği metoduyla karşılaştırdık.
- Bu benzerliğe göre en yakın dokümanları sıraladık.

## Kullanılan Modeller
- Üzerine eğitim yaparak geliştirdiğimiz BERTurk modeli:

  https://huggingface.co/dbmdz/bert-base-turkish-uncased

- Geliştirme süreci sonunda bizim tarafımızdan sunulan model:

  https://huggingface.co/sfurkan/LexBERT-turkish-uncased

- Geliştirdiğimiz 'LexBERT-turkish-uncased' (yukarıdaki linkte bulunan model) modelini 'fine-tune' ederek doküman sınıflandırmasında kullandığımız model:

  https://huggingface.co/sfurkan/LexBERT-textclassification-turkish-uncased

## Kullanılan Veri Kümeleri
- Başlangıçta bize verilen 76 MB'lık veri kümesi

- https://www.mevzuat.gov.tr sitesinden topladığımız dokümanları içeren 131 MB'lık veri kümesi:

  https://huggingface.co/datasets/sfurkan/Kanun-Yonetmelik-Tuzuk

## Bağlılıklar
### Jupyter Notebook ile kurulum yapılacaksa:
```
numpy
pandas
scikit_learn
sentence_transformers
torch
tqdm
transformers
```
### Docker ile kurulum yapılacaksa:
Bütün bağlılıklar imajın içerisindedir. Projeyi çalıştırmak için ek olarak indirilmesi gereken bir şey yoktur.

## Kurulum ve Kullanım
Proje, Jupyter Notebook kullanarak veya Docker konteyneri oluşturularak 2 farklı şekilde kullanılabilir.
### Jupyter Notebook Kullanarak Kurulum
1- Bilgisayarınızda Jupyter Notebook yüklü değilse yükleyin (https://jupyter.org/install). Jupyter Notebook projenin çalıştırılması için gerekli olan tüm modüllere sahiptir. Buna rağmen modülün bulunamadığına dair hata almanız halinde projenin ihtiyaç duyduğu her modülün yüklenmesi için kullanılacak komutlar aşağıdadır.
```
pip install numpy==1.23.2
pip install pandas==1.4.3
pip install scikit_learn==1.1.2
pip install sentence_transformers==2.2.2
pip install torch==1.12.1
pip install tqdm==4.64.0
pip install transformers==4.18.0
```


2- Github reposu üzerindeki 'Releases' kısmından projenin son sürümünü indirin.

3- İndirdiğiniz dosyayı herhangi bir klasöre çıkartın.

3- Jupyter Notebook kullanarak kullanmak istediğiniz modele göre 'Lexlata-Final-Model.ipynb' veya 'Lexlata-Final-Model-Classification-Alternative.ipynb' dosyalarından birini açın.

4- Son hücrede bulunan örnek kullanımı inceleyerek kolayca kullanmaya başlayabilirsiniz.

### Docker Kullanarak Kurulum
1- Yüklü değilse Docker indirip kurun. (https://www.docker.com/products/docker-desktop)

2- Komut satırını açıp aşağıdaki komutları yazın:
```
docker pull sfurkan20/lexlata
docker run -d --name Lexlata -p 0.0.0.0:8501 sfurkan20/lexlata
```
3- Tarayıcınızla aşağıdaki adrese gidin:
```
http://localhost:8501
```

4- Arama yerine sorgunuzu girerek veya doküman yükleyerek arama yapabilirsiniz.

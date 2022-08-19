import streamlit as st
from streamlit.components.v1 import html
from model_final import getSimilarDocuments
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'turkish')

st.set_page_config(
   page_title="Lexlata",
   page_icon="https://media-public.canva.com/RA1JI/MAE0sNRA1JI/1/t.png"
)

st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">""", unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">
      <img src="https://www.svgrepo.com/show/258301/bee.svg" width="30" height="30" class="d-inline-block align-top" alt="">BeeLingua
    </a>
    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
      <li class="nav-item">
        <a class="nav-link active" href="https://drive.google.com/file/d/1M16R_NqWjQn_wGEd_60hteEfs9LitDsC/view">Contact</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://drive.google.com/file/d/1M16R_NqWjQn_wGEd_60hteEfs9LitDsC/view">About</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

#a:-webkit-any-link {color: #2c5e74;}
st.markdown(""" <style>
.st-cl {border-bottom-width: 2px;}
.st-ck {border-top-width: 2px;}
.st-cj {border-right-width: 2px;}
.st-ci {border-left-width: 2px;}
nav.bg-light {background-color: #e6e48c!important;}
.css-10trblm {font-family: sans-serif;}
div.css-zt5igj + span {color: #fff;}
.css-1v3fvcr {background-color: #2c5e74; background-image: url('https://media-public.canva.com/9KIMs/MAEqpM9KIMs/1/tl.png');}
.badge {margin-right: 10px;}
header {visibility: hidden;}
footer {visibility: hidden;}
.card {margin-bottom: 40px;color: black;}
a.btn-primary{color: #fff;}
.btn-primary {color: #ddd; background-color: #2c5e74; border-color: #2c5e74;}
.btn-primary:hover {color: #fff; background-color: #1a3d41; border-color: #1a3d41;}
.modal-content {color: black;}
.btn-primary:not(:disabled):not(.disabled).active:focus, .btn-primary:not(:disabled):not(.disabled):active:focus, .show>.btn-primary.dropdown-toggle:focus {box-shadow: 0 0 0 0.2rem rgb(44 94 116 / 50%);}
</style> """, unsafe_allow_html=True)

st.title('LEXLATA')

def list_keywords(keywords):
  keyword_list = ''
  for keyword in keywords:
    keyword_list += (f"""<span class="badge badge-dark">{keyword[0]}</span>""")
  return keyword_list

input_type = st.radio('Aramak istediğiniz mevzuatı yazarak ya da txt dosyası formatında yükleyerek aratabilirsiniz.',
  options=('Yaz', 'Dosya Yükle'),
  horizontal=True)
res = []
if input_type == 'Yaz':
  search_text = st.text_input('Mevzuat giriniz:',placeholder='Aranacak ifade/sayıyı yazınız...')
  if search_text:
    res = getSimilarDocuments(search_text, topk=5)
if input_type == 'Dosya Yükle':
  container = st.container()
  with container:
    search_file = st.file_uploader("Dosya seçin:")
    button = st.button("Ara")
    if button:
      if search_file:
        res = getSimilarDocuments(search_file.getvalue().decode("utf-8"), topk=5)
laws = ''
for i in range(len(res)):
  laws += (f"""<div class="card text-center">
  <div class="card-header">
    {res['kategori'][i]}
  </div>
  <div class="card-body">
    <p class="card-text">{res['baslik'][i]}</p>
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#{str(i) + '.law'}">İncele</button>
  </div>
  <div class="card-footer text-muted">
    {datetime.strptime(res['mevzuat_tarihi'][i], '%Y-%m-%d').strftime('%d %B %Y') if isinstance(res['mevzuat_tarihi'][i], str) else 'Belirsiz' }
  </div>
  </div>
  <div class="modal fade" tabindex="-1" id="{str(i) + '.law'}" tabindex="-1" aria-labelledby="{str(i) + '.lawLabel'}" style="display: none;" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{res['baslik'][i]}</h5>
          <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>{res['data_text'][i]}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Kapat</button>
          <a type="button" class="btn btn-primary" href="{res['url'][i]}">Kaynağı Görüntüle</a>
        </div>
      </div>
    </div>
  </div>""")
  #list_keywords(res[i]['keywords'])
  #<p class="mb-1">Mevzuat Bilgisi: {str(res[i]['info'][0:15]).join('...')}</p>
  #{res['mevzuat_no'][i]}
st.markdown(f"""<div class="list-group">{laws}</div>""",unsafe_allow_html=True)
script = """<script>
    sources = ['https://code.jquery.com/jquery-3.2.1.slim.min.js', 'https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js', 'https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js']
    integrities = ['sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN', 'sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q', 'sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl']
    for (var i = 0; i < 3; i++) {
      script = parent.document.createElement('script');
      script.setAttribute('src', sources[i]);
      script.setAttribute('integrity', integrities[i]);
      script.setAttribute('crossorigin', 'anonymous');
      parent.document.body.appendChild(script);
    }
  </script>"""
html(f"""{script}""",height=0)

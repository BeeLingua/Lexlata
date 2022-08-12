import streamlit as st
from streamlit.components.v1 import html
from model import run
from datetime import datetime

st.set_page_config(
   page_title="Lexlata",
   page_icon="https://media-public.canva.com/RA1JI/MAE0sNRA1JI/1/t.png"
)

st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"><script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script><script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script><script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>""", unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">
      <img src="https://media-public.canva.com/RA1JI/MAE0sNRA1JI/1/t.png" width="30" height="30" class="d-inline-block align-top" alt="">BeeLingua
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
.css-10trblm {font-family: sans-serif;}
.css-1v3fvcr {background-color: #2c5e74; background-image: url('https://media-public.canva.com/9KIMs/MAEqpM9KIMs/1/tl.png');}
header {visibility: hidden;}
footer {visibility: hidden;}
.card {margin-bottom: 40px;color: black;}
.card-body button {color: #fff;}
</style> """, unsafe_allow_html=True)

st.title('LEXLATA')

input_type = st.radio('Aramak istediğiniz mevzuatı yazarak ya da txt dosyası formatında yükleyerek aratabilirsiniz.',
  options=('Yaz', 'Dosya Yükle'),
  horizontal=True)
res = []
if input_type == 'Yaz':
  search_text = st.text_input('Mevzuat giriniz:',placeholder='Aranacak ifade/sayıyı yazınız...')
  if search_text:
    res = run(search_text)
if input_type == 'Dosya Yükle':
  container = st.container()
  with container:
    search_file = st.file_uploader("Dosya seçin:")
    button = st.button("Ara")
    if button:
      if search_file:
        res = run(search_file.getvalue().decode("utf-8"))
laws = ''
for i in range(len(res)):
  laws += (f"""<div class="card text-center">
  <div class="card-header">
    {res[i]['number']}
  </div>
  <div class="card-body">
    <p class="card-text">{res[i]['name']}</p>
    <button type="button" class="btn btn-primary" onclick="open({str(i) + '.law'})">İncele</button>
  </div>
  <div class="card-footer text-muted">
    {datetime.strptime(res[i]['date'], '%Y-%m-%d').strftime('%d %B %Y') if isinstance(res[i]['date'], str) else 'Belirsiz' }
  </div>
</div>
<div class="modal fade" tabindex="-1" id="{str(i) + '.law'}" tabindex="-1" aria-labelledby="{str(i) + '.lawLabel'}" style="display: none;" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Modal title</h5>
        <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p>Modal body text goes here.</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>""")
  #<p class="mb-1">Mevzuat Bilgisi: {str(res[i]['info'][0:15]).join('...')}</p>
js_open = "(function (){console.log(document.getElementById('0.law'));})();"
html(f"""<div class="list-group">{laws}</div><script>{js_open}</script><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"><script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script><script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script><script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>""")

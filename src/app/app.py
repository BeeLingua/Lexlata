import streamlit as st
import model as md

st.set_page_config(
   page_title="Lexlata",
   page_icon="https://media-public.canva.com/RA1JI/MAE0sNRA1JI/1/t.png"
)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

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
</style> """, unsafe_allow_html=True)

st.title('LEXLATA')
search = st.text_input('Mevzuat giriniz:',placeholder='Aranacak ifade/sayıyı yazınız...')
if search:
    res = md.run(search)
    laws = ''
    for i in range(len(res)):
        laws += (f"""<a href="https://www.mevzuat.gov.tr/" class="list-group-item list-group-item-action flex-column align-items-start" style="margin-bottom:15px;">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">Mevzuat Adı: {res[i]['name']}</h5>
      <small>Mevzuat No: {res[i]['number']}</small>
    </div>
    <p class="mb-1">Mevzuat Bilgisi: {res[i]['info']}</p>
    <small>Kabul Tarihi: {res[i]['date']}</small>
  </a>""")
    st.write(f"""<div class="list-group">{laws}</div>""", unsafe_allow_html=True)
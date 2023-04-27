import os
import streamlit as st
import shutil

from PIL import Image


favicon = Image.open("favicon.png")
st.set_page_config(
    
    page_title="BizGPT Public",
    page_icon=favicon,

)

css= '''
<style>

.css-h5rgaw.egzxvld1
{
    visibility: hidden;
}

</style>
'''
st.markdown(css,unsafe_allow_html=True) #remove css 


st.title("Coming soon")



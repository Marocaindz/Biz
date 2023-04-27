import os
import streamlit as st
import shutil

from PIL import Image


favicon = Image.open("favicon.png")
st.set_page_config(
    
    page_title="BizGPT Public",
    page_icon=favicon,

)

def create_new_folder(path, folder_name):
    new_folder_path = os.path.join(path, folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        st.success(f"Folder '{folder_name}' created successfully!")
    else:
        st.warning(f"Folder '{folder_name}' already exists.")


def delete_folder(folder_path):
    try:
        os.rmdir(folder_path)
        st.success(f"Directory '{folder_path}' deleted successfully.")
    except OSError as e:
        st.error(f"Error deleting directory '{folder_path}': {e}.")
    


folder_path = "folders"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

folders = [f.name for f in os.scandir(folder_path) if f.is_dir()]

selected_folder = st.sidebar.selectbox("Select a folder", folders)
selected_folder_path = os.path.join(folder_path, selected_folder)
num_files = len(os.listdir(selected_folder_path))

st.sidebar.write(f"Selected folder: {selected_folder} [{num_files}]")
if num_files > 0:
    
    for file in os.listdir(selected_folder_path):
        st.sidebar.write(f"- {file}")


# Ask the user to enter a new folder name
new_folder_name = st.sidebar.text_input("Enter a new folder name")

# Create a new folder when the user clicks the button
if st.sidebar.button("Create Folder"):
    create_new_folder(folder_path, new_folder_name)
    

if st.sidebar.button("Delete Folder"):
    confirm_panel = st.expander(f"Are you sure you want to delete **{selected_folder}** folder?", expanded=True)
    with confirm_panel:
        confirmed = st.button("Yes")
        if confirmed:
            delete_folder(selected_folder_path)
            st.success("Folder deleted successfully!")

#script
import os
os.environ["OPENAI_API_KEY"] = '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'

import streamlit as st
from llama_index import download_loader
from llama_index.node_parser import SimpleNodeParser
from llama_index import GPTSimpleVectorIndex
from llama_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper, ServiceContext
from langchain import OpenAI
css= '''
<style>

.css-h5rgaw.egzxvld1
{
    visibility: hidden;
}

</style>
'''
st.markdown(css,unsafe_allow_html=True) #remove css 


doc_path = "./"+selected_folder_path+"/"
index_file = 'index.json'

if 'response' not in st.session_state:
    st.session_state.response = ''

def send_click():
    st.session_state.response  = index.query(st.session_state.prompt)

index = None
st.title("BizGPT Chatbot")

sidebar_placeholder = st.sidebar.container()
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

    doc_files = os.listdir(doc_path)
    for doc_file in doc_files:
        os.remove(doc_path + doc_file)

    bytes_data = uploaded_file.read()
    with open(f"{doc_path}{uploaded_file.name}", 'wb') as f: 
        f.write(bytes_data)

    SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

    loader = SimpleDirectoryReader(doc_path, recursive=True, exclude_hidden=True)
    documents = loader.load_data()
    sidebar_placeholder.header('Current Processing Document:')
    sidebar_placeholder.subheader(uploaded_file.name)
    sidebar_placeholder.write(documents[0].get_text()[:10000]+'...')

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))

    max_input_size = 4096
    num_output = 256
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index = GPTSimpleVectorIndex.from_documents(
        documents, service_context=service_context
    )

    index.save_to_disk(index_file)

elif os.path.exists(index_file):
    index = GPTSimpleVectorIndex.load_from_disk(index_file)

    SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
    loader = SimpleDirectoryReader(doc_path, recursive=True, exclude_hidden=True)
    documents = loader.load_data()
    doc_filename = os.listdir(doc_path)[0]
    sidebar_placeholder.header('Current Processing Document:')
    sidebar_placeholder.subheader(doc_filename)
    sidebar_placeholder.write(documents[0].get_text()[:10000]+'...')

if index != None:
    st.text_input("Ask something: ", key='prompt')
    st.button("Send", on_click=send_click)
    if st.session_state.response:
        st.subheader("Response: ")
        st.success(st.session_state.response, icon= "🤖")




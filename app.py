import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

# Setup AI and Database
embeddings = OllamaEmbeddings(model="llama3.2")
llm = ChatOllama(model="llama3.2", temperature=0)
persist_dir = "ngo_db"

def run_data_upload(uploaded_file):
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        loader = PyPDFLoader("temp.pdf")
        data = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
        chunks = text_splitter.split_documents(data)
        
        # Stamp the ID onto the data
        current_user = st.session_state.get('username', 'Unknown')
        for chunk in chunks:
            chunk.metadata["uploaded_by"] = current_user
        
        vectordb = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings, 
            persist_directory=persist_dir
        )
        st.success(f"File uploaded and indexed by {current_user}!")

def run_emergency_ai():
    st.subheader("AI Emergency Assistant")
    query = st.text_input("What is the emergency?")
    
    if query:
        vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
        # Using MMR search to prevent mixing up unrelated files
        results = vectordb.max_marginal_relevance_search(query, k=5)
        
        context_with_ids = ""
        for doc in results:
            uploader = doc.metadata.get("uploaded_by", "Admin")
            context_with_ids += f"\n[VOLUNTEER: {uploader}] reported: {doc.page_content}\n"

        prompt = f"""
        Strictly use these records to answer. If the records are about different topics, 
        do not mix them. Focus ONLY on matching the request: {query}
        RECORDS: {context_with_ids}
        """
        
        response = llm.invoke(prompt)
        st.info(response.content)
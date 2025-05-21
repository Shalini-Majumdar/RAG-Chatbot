# rag_pipeline.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.embeddings import SentenceTransformerEmbeddings

def build_qa_chain():
    # Load LLM
    model_name = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
    llm = HuggingFacePipeline(pipeline=pipe)

    # Load retriever
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
        "faiss_index", 
        embedding, 
        allow_dangerous_deserialization=True  # Needed for Streamlit + pickle
    )
    retriever = vectorstore.as_retriever()

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


_embeddings = OpenAIEmbeddings()
_vectorstore = None


# =====================
# PROCESSAR PDF
# =====================

def process_pdf(file_path: str):

    global _vectorstore


    loader = PyPDFLoader(file_path)
    documents = loader.load()


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )


    chunks = splitter.split_documents(documents)


    _vectorstore = FAISS.from_documents(
        chunks,
        _embeddings
    )


# =====================
# BUSCAR
# =====================

def search(query: str):

    global _vectorstore


    if _vectorstore is None:
        return []


    retriever = _vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )


    docs = retriever.invoke(query)


    return [doc.page_content for doc in docs]
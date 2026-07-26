import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ingest_pdf():
    if not PDF_PATH:
        print("Erro: A variável PDF_PATH não está definida.")
        return

    print(f"Carregando o arquivo PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print("Quebrando o conteúdo do PDF em partes menores...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    docs = text_splitter.split_documents(documents)

    print(f"Criando embeddings...")
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )

    print("Conectando com o banco de dados...")
    db_url = os.getenv("DATABASE_URL")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME", "my_collection")

    print(f"Armazenando {len(docs)} chunks no banco de dados...")
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=db_url,
        use_jsonb=True,
    )
    
    vectorstore.add_documents(docs)
    print("Ingestão concluída com sucesso!")

if __name__ == "__main__":
    ingest_pdf()
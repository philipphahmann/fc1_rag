import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Lê o template do prompt do arquivo
with open("prompts/search_prompt.txt", "r", encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()

def search_prompt(question):
    if not question:
        return "Pergunta não fornecida."

    db_url = os.getenv("DATABASE_URL")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME", "my_collection")

    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )

    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=db_url,
        use_jsonb=True,
    )

    # Buscar os top 10 chunks similares
    docs_with_scores = vectorstore.similarity_search_with_score(question, k=10)
    
    # Extrair o conteúdo do texto dos chunks recuperados
    contexto = "\n\n".join([doc.page_content for doc, _ in docs_with_scores])

    # Inicializar o ChatOpenAI (LLM)
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini"),
        temperature=0
    )

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm

    response = chain.invoke({
        "contexto": contexto,
        "pergunta": question
    })

    return response.content
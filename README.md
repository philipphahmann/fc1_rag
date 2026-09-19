# Desafio MBA Engenharia de Software com IA - Full Cycle

## Descrição

Este projeto implementa uma solução de RAG (Retrieval-Augmented Generation) para consultas em documentos PDF, utilizando LangChain, OpenAI e PostgreSQL com extensão pgvector.

## Estrutura do Projeto

```
FC1_RAG/
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── data/
│   └── document.pdf
├── prompts/
│   └── system_prompt.txt
└── src/
    ├── chat.py
    ├── ingest.py
    └── search.py
```

## Arquivos Principais

### 1. `.env` e `.env.example`
Arquivos de variáveis de ambiente com as chaves e caminhos para a aplicação.

### 2. `docker-compose.yml`
Gerencia o serviço de banco de dados PostgreSQL com a extensão pgvector.

### 3. `src/ingest.py`
Script para ingestão de documentos PDF (atualmente configurado com um livro de História das Américas):
- Carrega o PDF do diretório `data/`
- Divide em chunks com RecursiveCharacterTextSplitter
- Cria embeddings com OpenAI
- Armazena no PostgreSQL via pgvector

### 4. `src/search.py`
Lógica principal de busca semântica:
- Busca o contexto mais relevante no banco vetorial
- Formata e integra com o LLM (OpenAI) usando o prompt dedicado

### 5. `src/chat.py`
Interface de chat pelo terminal.

### 6. `prompts/system_prompt.txt`
Template de sistema com regras estritas para o modelo. Ele inclui proteções contra prompt injections e garante que a resposta seja baseada unicamente no contexto do documento.

## ⚠️ Aviso Importante sobre o PDF

A aplicação funciona **SOMENTE com um único arquivo PDF por vez** na pasta `/data`. Caso você precise mudar o PDF para fazer consultas sobre um documento diferente, é necessário **resetar o banco de dados** para limpar os dados antigos antes de fazer uma nova ingestão. Para isso, remova os volumes do banco e suba novamente:
```bash
docker-compose down -v
docker-compose up -d
```
Após o reset, coloque o novo PDF na pasta `/data` e rode o script de ingestão novamente.

## Pré-requisitos

- Python (com ambiente virtual configurado)
- Docker e Docker Compose
- Chave de API OpenAI

## Instalação e Execução

1. **Configurar variáveis de ambiente:**
   Crie o seu `.env` com base no `.env.example` inserindo sua API Key:
   ```bash
   cp .env.example .env
   ```

2. **Construir e iniciar os containers do banco de dados:**
   ```bash
   docker-compose up -d
   ```

3. **Ingerir o documento PDF:**
   No seu terminal (com a venv ativada):
   ```bash
   python src/ingest.py
   ```

4. **Iniciar chat:**
   No seu terminal (com a venv ativada):
   ```bash
   python src/chat.py
   ```
   ```
   PERGUNTA: [sua pergunta]
   ```

## Como Testar (Livro de História)

### Exemplos de perguntas que funcionam:

**Pergunta:** "Qual era o livro sagrado dos maias?"
**Resposta:** "O livro sagrado dos maias era chamado de Popol Vuh."

### Exemplos de perguntas que NÃO funcionam (fora do contexto do livro):

**Pergunta:** "Qual é a capital da França?"
**Resposta:** "Não tenho informações necessárias para responder sua pergunta."

## Tecnologias Utilizadas

- **Framework:** LangChain
- **Embeddings:** OpenAI (text-embedding-3-small)
- **LLM:** OpenAI (gpt-4o-mini)
- **Banco de Dados:** PostgreSQL com pgvector
- **Orquestração:** Docker Compose

## Boas Práticas Aplicadas

- **Separação de Responsabilidades:** O projeto divide o fluxo em arquivos distintos para ingestão (`ingest.py`), busca (`search.py`) e interface (`chat.py`).
- **Arquitetura de Papéis (Chat Pattern):** Utiliza o `ChatPromptTemplate` para separar regras de sistema (`SystemMessage`) das mensagens do usuário (`HumanMessage`), otimizando o entendimento do modelo.
- **Desacoplamento e Segurança de Prompt:** O prompt principal foi isolado (`prompts/system_prompt.txt`) e aprimorado com instruções explícitas para mitigar ataques de *Prompt Injection* e desvios de conduta do usuário.
- **Isolamento de Credenciais e Configurações:** Chaves de API e strings de conexão de banco de dados são injetadas exclusivamente através do arquivo `.env`.
- **Infraestrutura Desacoplada e Reprodutível:** O banco vetorial é levantado via Docker, garantindo que o ambiente do banco rode de forma idêntica em qualquer sistema operacional.
- **Organização do Projeto:** Os recursos como PDFs estão estruturados no diretório isolado `/data`.

## Autoria

Desenvolvido como parte do MBA Engenharia de Software com IA - Full Cycle.
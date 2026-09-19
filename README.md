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
├── document.pdf
├── prompts/
│   └── system_prompt.txt
├── shortcuts/
│   └── reset_and_init.sh
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

### 7. `document.pdf`
Arquivo PDF base para a ingestão que deve ficar na raiz do projeto. Se quiser usar outro arquivo, coloque-o aqui com esse exato nome, ou altere a variável `PDF_PATH` no `.env`.

## ⚠️ Aviso Importante sobre o PDF

A aplicação funciona **SOMENTE com um único arquivo PDF por vez** (por padrão, o `document.pdf` na raiz do projeto). Caso você precise mudar o PDF para fazer consultas sobre um documento diferente, é necessário **resetar o banco de dados** para limpar os dados antigos antes de fazer uma nova ingestão. Para isso, rode o atalho:
```bash
bash shortcuts/reset_and_init.sh
```

## Pré-requisitos

- Python (com ambiente virtual configurado)
- Docker e Docker Compose
- Chave de API OpenAI

## Instalação e Execução

1. **Configurar o Ambiente Python:**
   Crie uma máquina virtual (venv) e instale as dependências do projeto:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # No Windows (Git Bash)
   # source venv/bin/activate    # No Linux/Mac
   pip install -r requirements.txt
   ```

2. **Configurar variáveis de ambiente:**
   Crie o seu `.env` com base no `.env.example` inserindo sua API Key:
   ```bash
   cp .env.example .env
   ```

3. **Atalho (Script de Automação):**
   Para facilitar a execução diária, criamos um único script consolidado na pasta `shortcuts/`. Você pode rodá-lo no Git Bash ou WSL.

   - **Fluxo Completo (Reset, Ingestão e Chat):**
     Derruba o banco de dados para limpar contextos antigos, sobe o banco limpo, ingere o documento PDF atual e já abre o chat!
     ```bash
     bash shortcuts/reset_and_init.sh
     ```

*(Se preferir rodar cada etapa manualmente, você pode usar os comandos `docker-compose down -v && docker-compose up -d`, depois com a venv ativada rodar `python src/ingest.py` seguido de `python src/chat.py`)*

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

## Autoria

Desenvolvido como parte do MBA Engenharia de Software com IA - Full Cycle.

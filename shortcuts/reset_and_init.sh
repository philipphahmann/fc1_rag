#!/bin/bash
cd "$(dirname "$0")/.."

echo "=================================================="
echo "INICIANDO PIPELINE DE RAG"
echo "=================================================="
echo ""

echo "▶ ETAPA 1: RESETANDO O BANCO DE DADOS"
echo "--------------------------------------------------"
docker-compose down -v
docker-compose up -d
echo ""
echo "✅ Banco de dados resetado com sucesso!"
echo ""

echo "▶ ETAPA 2: INGESTÃO DO DOCUMENTO PDF"
echo "--------------------------------------------------"
./venv/Scripts/python src/ingest.py
echo ""

echo "▶ ETAPA 3: ABRINDO O CHAT"
echo "--------------------------------------------------"
./venv/Scripts/python src/chat.py
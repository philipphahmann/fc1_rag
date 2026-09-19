from search import search_prompt

def main():
    print("Iniciando chat com o banco de dados do PDF... (Digite 'sair' para encerrar)")
    print("-" * 50)
    while True:
        try:
            question = input("PERGUNTA: ")
            if question.strip().lower() in ['sair', 'exit', 'quit']:
                print("Encerrando o chat.")
                break
            
            if not question.strip():
                continue

            resposta = search_prompt(question)
            print(f"RESPOSTA: {resposta}\n")
            print("-" * 50)
        except KeyboardInterrupt:
            print("\nEncerrando o chat.")
            break

if __name__ == "__main__":
    main()
from search import search_prompt

def main():
    print("==================================================")
    print("Chat iniciado! (Digite 'sair' para encerrar)")
    print("==================================================")
    while True:
        try:
            question = input("\nPERGUNTA: ")
            if question.strip().lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Encerrando o chat. Até logo!\n")
                break
            
            if not question.strip():
                continue

            resposta = search_prompt(question)
            print(f"RESPOSTA: {resposta}\n")
            print("--------------------------------------------------")
        except KeyboardInterrupt:
            print("\n👋 Encerrando o chat. Até logo!\n")
            break

if __name__ == "__main__":
    main()
"""CLI for the locally hosted Ollama agent."""
from agent import Agent

def main():
    agent = Agent()
    print('Empório da Música 🎵 | Digite sair para encerrar.')
    while True:
        try:
            message = input('\nVocê: ').strip()
        except (KeyboardInterrupt, EOFError):
            break
        if message.lower() in ('sair', 'exit', 'quit'):
            break
        if not message:
            continue
        try:
            print('Assistente:', agent.reply(message))
        except Exception as exc:
            print('Falha ao acessar o Ollama local. Execute ollama pull qwen2.5:3b e inicie o Ollama.', type(exc).__name__)

if __name__ == '__main__':
    main()

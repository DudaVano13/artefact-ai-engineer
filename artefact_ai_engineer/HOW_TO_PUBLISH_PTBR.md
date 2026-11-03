# Como executar o projeto gratuitamente (sem API paga)

1. Instale o **Ollama** em https://ollama.com/download e abra o programa.
2. Abra o VS Code na pasta do projeto. Instale os pacotes com `python -m pip install -r requirements.txt`.
3. Em um terminal, execute `ollama pull qwen2.5:3b`. Ele vai baixar o modelo gratuito para seu computador. Esse download pode ocupar alguns GB.
4. Teste o modelo: `ollama run qwen2.5:3b` e digite `Olá`; depois digite `/bye`.
5. Encerre o Streamlit antigo (Ctrl+C no terminal em que ele está aberto) e execute `python -m streamlit run app.py`.
6. Se aparecer erro de conexão, confira se o Ollama está aberto. Se necessário, abra outro terminal e execute `ollama serve` (não execute duas instâncias do servidor).
7. Faça perguntas de catálogo, preço, política de devolução e pedidos (pedido exige e-mail cadastrado). Revise se o modelo realmente usa as funções; modelos pequenos podem errar.
8. Rode `python -m unittest discover -s tests -v`, salve de 3 a 5 **conversas reais** na pasta `examples/` e substitua os roteiros ilustrativos antes da entrega.
9. Atualize o README com resultados reais, limitações e como você usou ChatGPT. Publique no GitHub com commits correspondentes às etapas que você realmente realizou. Não altere o repositório depois do prazo.

**Observação:** o projeto usa a biblioteca Python `openai` como cliente HTTP para `http://localhost:11434/v1`. **Isso NÃO usa a API paga da OpenAI** e não pede chave: o servidor é o Ollama instalado em seu próprio computador.

# Empório da Música — AI Customer Support Agent

A Python prototype for Artefact's AI Engineer technical challenge. The project builds a friendly Portuguese-speaking text assistant for a **fictional** musical instrument store in Campo Grande, Brazil.

## Features

- Product search by name, category, budget, and availability.
- Read-only, source-grounded current CSV price and promotion checks.
- Order tracking with an order-number **and registered e-mail** verification gate.
- On-demand lookup of store rules, refunds, shipping, payment, business hours, and warranty from the supplied policy PDF.
- Out-of-scope handling and transparent escalation advice.
- CLI and optional Streamlit chat UI, with in-session conversation history.

## Requirements

- Python 3.10+
- A locally running **Ollama** installation and a downloaded tool-calling model (`qwen2.5:3b` by default). No paid API key or cloud token is required. Downloading a model uses internet and running it uses local RAM/CPU (or GPU).

## Setup

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Install [Ollama](https://ollama.com/download) and download the free model:

```powershell
ollama pull qwen2.5:3b
```

Ollama normally starts a local server automatically on Windows. If necessary, run `ollama serve` in another terminal. You can optionally change the model by setting `$env:OLLAMA_MODEL="qwen2.5:7b"` after downloading that model. `qwen2.5:3b` is smaller and easier to run on an ordinary laptop, but its tool-use reliability may be lower than 7b. No `OPENAI_API_KEY` is used.

Run the terminal chat:

```bash
python main.py
```

Or run the optional interface:

```bash
streamlit run app.py
```

Test source-data retrieval **without any paid API calls**:

```bash
python -m unittest discover -s tests -v
```

## Architecture

```text
Customer -> CLI / Streamlit -> local Ollama LLM (tool calling)
                                     |
                    +----------------+------------------+
                    |                |                  |
                catalog /       order_status        policy_lookup
                get_product      (identity gate)     (PDF page retrieval)
                    |                |                  |
              Products /         Orders +          PDF policies
              Categories /       Customers /       (pypdf)
              Promotions         Order items
```

**Agent strategy:** hybrid tool-calling architecture with deterministic routing for explicit budget/catalog searches and frequent store-policy questions (address, opening hours, online returns). This fallback was added after live tests revealed unreliable tool selection by the small local model. For other requests, the LLM interprets the intent and selects a function. Python executes queries deterministically; the model explains the returned results. This is simpler, auditable, and less error-prone for structured, frequently changing prices and order statuses than vector-searching CSV data. The policy PDF is retrieved through a lightweight page-level lexical search rather than embeddings because the policy manual is small (eight pages), and the challenge values simplicity. The model does **not** execute arbitrary SQL or user-supplied code.

**Model/provider:** locally hosted Ollama with `qwen2.5:3b` via its OpenAI-compatible local API. It avoids API fees and sending customer data to a remote model. The `OLLAMA_MODEL` environment variable allows changing models (for example, `qwen2.5:7b` for potentially stronger tool calling). The OpenAI Python SDK is used only as an HTTP client; it does not call OpenAI servers. Tool-calling compatibility and quality depend on the chosen local model and must be validated end-to-end.

**Prompting:** system instructions define the brand persona, enforce checking retrieved evidence instead of hallucinating factual data, and refuse to claim unsupported operations such as refunds or orders. The customer-facing answer follows the user's language. Policy lookups return PDF text and page numbers.

**Data handling:** immutable local CSV snapshots are loaded using Python's `csv.DictReader`. Product search normalizes diacritics and uses live-from-file filtering by status/stock; promotional prices are calculated with `Decimal`. No modifications are made to original records. The order tool requires exact order ID and customer e-mail matches and avoids returning customer contact details. This is a **prototype identity check**, not a production authentication system.

**Conversation history:** session-only memory; the Python process holds previous customer and tool messages in memory, and the Streamlit app keeps a session-specific agent. No persistent storage is implemented, reducing privacy risk and scope.

## Example prompts

1. `Quais violões disponíveis custam até R$ 1000?`
2. `Quanto custa o Takamine GD20?`
3. `Qual é o endereço e o horário de funcionamento?`
4. `Me arrependi da compra online. Como funciona a devolução?`
5. `Onde está meu pedido 8?` (the agent should ask for the registered e-mail before querying).
6. `Vocês vendem amplificadores?`

The `examples/` directory includes deterministic tool-output demonstrations and **clearly labeled expected conversation scenarios**. They are not represented as actual LLM transcripts. After testing with a real model, replace them with genuine transcripts for submission.

## Limitations and next steps

- **Not a live commerce integration**: inventory, orders and promotions come from the files supplied with the challenge, rather than a real-time POS, carrier or payment API. The agent must avoid implying freshness beyond this snapshot.
- **Identity verification is only a demo**: an order number plus known e-mail does not establish robust ownership. Production would use a verified OTP, authentication tokens and rate limiting, with encrypted secrets and audit trails.
- **No write actions**: placing an order, changing a delivery, authorizing a return and human handoff are out of scope.
- **Policy lookup is lexical**: sophisticated paraphrases may retrieve a suboptimal page. A production system could index the extracted PDF in a vector database and rerank evidence.
- **PDF policy ambiguities**: the payment summary says credit card up to 12 installments with a R$100 minimum, while the detailed rules allow smaller minimums in fewer installments. When ambiguous, the agent should cite detailed rules and recommend human confirmation. There are also different WhatsApp numbers in the PDF; avoid assuming one is authoritative without confirmation.
- **Local inference limitations**: running Ollama requires sufficient memory and may be slow without a GPU. Small models may fail to select tools correctly or respond accurately. Deterministic tool tests do not guarantee response quality. Add evaluation scenarios, adversarial prompt injection tests, tracing and response quality metrics.
- **Data retention**: in-memory history disappears when the session restarts. Production use requires explicit retention and LGPD governance.

## Tests and validation

Run `python -m unittest discover -s tests -v`. The tests cover stock-and-price filtering, one product lookup, current promotion calculations, authorization gate, authorized order retrieval, and PDF policy lookup. **Full end-to-end LLM tests need the local Ollama model to be running** and must be executed before claiming full conversational verification.

## Use of AI coding assistants

> **Update this section before submission to accurately reflect your own workflow.**
>
> Initial project scaffold, architecture explanation, code drafts, and test suggestions were created with OpenAI ChatGPT. The candidate is responsible for running the program, reviewing and understanding its implementation, checking outputs, adding actual conversation transcripts, and disclosing any further AI assistance used. Only document steps that actually happened.

## Submission

Submit the public GitHub repository link as requested in the challenge PDF, and verify the recruiter's separate Google Forms/PDF submission instructions. Make meaningful, sequential commits and stop editing the repository after the deadline. Do not upload API keys, `.env`, or sensitive production information.

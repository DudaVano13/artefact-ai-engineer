# Empório da Música — AI Customer Support Agent

A Python-based AI customer support prototype developed for Artefact's AI Engineer technical challenge.

The project implements a Portuguese-speaking virtual assistant for **Empório da Música**, a fictional musical instrument store located in Campo Grande, Brazil.

The main objective is to demonstrate how Large Language Models (LLMs) can be integrated with structured business data and internal policy documents to provide accurate, helpful, and context-aware customer support.

## 1. Project Overview

Empório da Música receives recurring customer questions about product availability, prices, promotions, store hours, orders, deliveries, payment methods, and return policies.

The proposed solution is a conversational AI assistant capable of understanding customer requests, retrieving relevant information, and generating responses based on the store's available data.

The solution prioritizes:

- Accurate responses grounded in provided information.
- Simple and maintainable architecture.
- Separation between business logic and language generation.
- Customer data protection.
- Transparent handling of limitations.
- Low-cost execution without paid AI APIs.

## 2. Main Features

The assistant supports the following capabilities:

**Product Catalog**

- Search products by name or category.
- Filter products by price range.
- Check available stock.
- Retrieve product information from CSV files.

**Orders**

- Look up an order using its identification number.
- Validate the registered customer email before returning order information.
- Retrieve order status, tracking information, and recorded delivery estimates.
- Avoid exposing customer order details when validation fails.

**Store Policies**

- Retrieve information about business hours and location.
- Answer questions about payment methods and installments.
- Explain shipping and delivery policies.
- Provide return and refund guidance.
- Retrieve warranty information from the policy document.

**Customer Support**

- Maintain a friendly, professional, and conversational tone.
- Respond to questions outside the store's business scope.
- Avoid inventing prices, stock quantities, or order details.
- Explain when an action requires human assistance.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Ollama | Local LLM execution |
| Qwen 2.5:3b | Language model |
| Streamlit | Web-based chat interface |
| Python CSV Library | Structured data processing |
| pypdf | PDF content extraction |
| OpenAI Python SDK | Communication with the Ollama-compatible local API |
| unittest | Automated testing |
| Git and GitHub | Version control and project delivery |

The OpenAI Python SDK is used exclusively as a client for the local Ollama-compatible API. The solution does not require a paid OpenAI API key.

## 4. Project Architecture

The solution uses a hybrid architecture combining LLM-based interpretation, tool calling, and deterministic Python functions.

```text
Customer
   |
   v
Streamlit / CLI Interface
   |
   v
AI Customer Support Agent
   |
   +--------------------------+
   |                          |
   v                          v
Intent Interpretation     Deterministic Routing
   |                          |
   +------------+-------------+
                |
                v
         Retrieval Tools
                |
      +---------+---------+
      |         |         |
      v         v         v
   Products   Orders   Store Policies
     CSV       CSV          PDF
      |         |           |
      +---------+-----------+
                |
                v
       Contextual Response
                |
                v
             Customer
```

### Architectural Decisions

A hybrid approach was selected because not every customer request requires complex LLM reasoning.

For example:

- Product availability and prices should be retrieved directly from structured records.
- Order information should be returned only after customer validation.
- Store policies should be retrieved from the supplied manual.
- The language model should help interpret requests and generate conversational responses.

This design reduces unnecessary model calls and makes critical operations more predictable.

During manual testing, the small local model occasionally failed to select the appropriate retrieval function. Deterministic routing was therefore introduced for selected catalog queries and frequently requested store policies.

This approach provides a practical balance between conversational flexibility and reliable information retrieval.

## 5. Language Model Selection

The selected model is **Qwen 2.5:3b**, executed locally using Ollama.

### Why Ollama?

Ollama was selected because it:

- Allows running language models locally.
- Does not require a paid API subscription.
- Provides an API compatible with the OpenAI Python SDK.
- Offers flexibility to test different models.
- Avoids sending the provided store data to an external model provider during inference.

### Why Qwen 2.5:3b?

The 3-billion-parameter model provides a practical starting point for local development.

It requires fewer computing resources than larger models and supports multilingual interactions.

However, smaller models may have limitations in reasoning consistency and tool selection.

For this reason, business-critical operations are supported by deterministic Python functions.

## 6. Data Sources

The project uses the fictional store data provided in the technical challenge.

The main files are:

- `products.csv`: Product catalog, prices, descriptions, and stock.
- `categories.csv`: Product categories.
- `customers.csv`: Customer records.
- `orders.csv`: Customer orders and delivery information.
- `order_items.csv`: Products associated with orders.
- `promotions.csv`: Promotional offers and discounts.
- `store_policies.pdf`: Internal store policies and customer service procedures.

### Data Processing

CSV files are loaded using Python's built-in CSV functionality.

The retrieval logic handles product searches, price filtering, stock availability, and order lookups.

Where applicable, promotional calculations use decimal arithmetic to avoid floating-point rounding issues.

The application does not modify the original source files.

**Important:** The CSV files represent a provided data snapshot. They are not connected to a live inventory, order management, or logistics system.

## 7. Policy Retrieval Strategy

The store's policy manual is a relatively small PDF document.

Instead of introducing a vector database, the prototype uses lightweight text extraction and page-level retrieval.

The retrieval process follows these steps:

1. Extract text from the PDF.
2. Identify relevant policy sections.
3. Retrieve information related to the customer's question.
4. Provide the relevant context for the response.
5. Reference the policy source when applicable.

This solution was selected to keep the project simple and easier to maintain.

For larger document collections, a Retrieval-Augmented Generation (RAG) architecture using embeddings, vector search, and reranking would be a possible improvement.

## 8. Installation and Configuration

### Requirements

- Python 3.10 or higher.
- Ollama installed locally.
- Qwen 2.5:3b downloaded.
- Python dependencies listed in `requirements.txt`.

### Step 1 — Clone the Repository

```bash
git clone https://github.com/DudaVano13/artefact-ai-engineer.git
cd artefact-ai-engineer/artefact_ai_engineer
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4 — Install and Configure Ollama

Download Ollama:

https://ollama.com/download

Then download the selected model:

```bash
ollama pull qwen2.5:3b
```

Ollama normally starts its local service automatically on Windows.

If necessary, start the service manually:

```bash
ollama serve
```

The project can optionally use a different compatible model through the `OLLAMA_MODEL` environment variable.

For example, in Windows PowerShell:

```powershell
$env:OLLAMA_MODEL="qwen2.5:3b"
```

No paid OpenAI API key is required.

### Step 5 — Run the Application

To start the Streamlit interface:

```bash
python -m streamlit run app.py
```

Open the local address displayed in the terminal, normally:

http://localhost:8501

Alternatively, run the command-line interface:

```bash
python main.py
```

## 9. Automated Testing

The project includes automated tests implemented with Python's `unittest` framework.

To execute the tests:

```bash
python -m unittest discover -s tests -v
```

The test suite covers scenarios such as:

- Product price and stock filtering.
- Specific product lookup.
- Promotional pricing.
- Store policy retrieval.
- Authorized order retrieval.
- Protection against unauthorized order disclosure.

These tests validate specific functions and business rules.

They do not replace complete end-to-end testing of the language model.

## 10. Manual Testing

The assistant was manually evaluated through the Streamlit interface using customer service scenarios.

The testing process included:

**Scenario 1 — Product Availability**

Customer question:

"Quais violões vocês têm disponíveis por até R$ 1.000?"

Objective: Verify whether the agent retrieves products based on category, budget, and inventory.

**Scenario 2 — Store Information**

Customer question:

"Qual é o endereço e horário de funcionamento da loja?"

Objective: Verify whether the assistant retrieves the correct store information.

**Scenario 3 — Returns and Refunds**

Customer question:

"Recebi um violão comprado online há 5 dias. Posso devolver?"

Objective: Verify whether the assistant applies the store's return policy correctly.

**Scenario 4 — Order Tracking**

Customer question:

"Quero consultar o pedido 8. Meu e-mail cadastrado é anacarol.ferreira@coldmail.com."

Objective: Verify order retrieval and customer email validation.

**Scenario 5 — Out-of-Scope Products**

Customer question:

"Vocês vendem palhetas, cabos para guitarra e amplificadores?"

Objective: Verify whether the assistant recognizes products outside the store's catalog and responds appropriately.

The `examples/` directory contains example scenarios. Expected examples should not be represented as actual LLM-generated transcripts. Any submitted conversation transcript must reflect an interaction actually executed with the agent.

## 11. Security and Privacy

The prototype implements basic measures to reduce unnecessary exposure of customer information.

For order-related requests, the retrieval function checks the order identification number and registered customer email before returning order data.

The agent does not need to disclose unrelated customer records.

The application operates with fictional data supplied for the challenge.

### Production Considerations

The current validation mechanism is suitable only for a demonstration.

In a production environment, stronger controls would be necessary, including:

- Verified customer authentication.
- One-time passwords or authenticated sessions.
- Rate limiting.
- Access logging.
- Secure secret management.
- Data minimization.
- LGPD-compliant data retention policies.

## 12. Known Limitations

**Local Model Reliability**

Qwen 2.5:3b may occasionally misunderstand requests or fail to select the appropriate tool. Deterministic routing reduces this issue for selected scenarios, but does not eliminate it.

**Static Data**

The agent uses CSV snapshots rather than live business systems. Stock quantities, promotions, order statuses, and delivery estimates may become outdated.

**Limited Customer Authentication**

Matching an order number and an email address is not equivalent to authenticating a customer.

**No Transactional Operations**

The assistant cannot complete purchases, issue refunds, change deliveries, or register return requests.

**Limited Policy Retrieval**

The lexical retrieval strategy is suitable for a small manual but may not perform as well with larger collections of documents.

**Session-Based History**

Conversation history is maintained during the application session and is not stored permanently.

**Local Resource Requirements**

Running an LLM locally requires sufficient CPU, RAM, and potentially GPU resources. Response times depend on the computer.

## 13. Future Improvements

Given additional development time, the following improvements would be prioritized:

1. Integrating inventory and order data with live APIs.
2. Implementing stronger customer authentication.
3. Adding automated end-to-end evaluation for LLM responses.
4. Introducing structured logging, observability, and performance metrics.
5. Improving retrieval through embeddings and semantic search.
6. Supporting multilingual customer service.
7. Implementing a human handoff mechanism.
8. Adding prompt-injection and adversarial testing.
9. Deploying the solution in a controlled environment.
10. Expanding automated regression tests for edge cases.

## 14. Use of AI Coding Assistants

I used **OpenAI ChatGPT** as a development assistant throughout this technical challenge.

ChatGPT supported the initial project structure, architecture decisions, Python code drafts, debugging, documentation, and automated test suggestions.

During development, I configured the Python environment, installed and tested the local Ollama model, executed automated tests, and manually evaluated customer support interactions.

The tests included product availability, store information, return policies, order tracking, and customer data protection.

During testing, I identified limitations in the small language model's tool selection. This led to adjustments in the architecture, including deterministic Python routing for selected queries.

The use of AI assistance helped accelerate implementation and troubleshooting while keeping the solution focused on simplicity, explainability, and practical business requirements.

I reviewed and tested the solution and take responsibility for the final technical decisions, limitations, and submitted project.

## 15. Conclusion

This project demonstrates a practical approach to building a customer service assistant with generative AI, structured business data, and internal documentation.

The solution combines local LLM inference with deterministic Python retrieval to improve reliability while keeping the architecture simple and cost-effective.

The project was designed as a functional prototype rather than a production-ready customer service platform.

The main technical focus is on grounded responses, transparent decision-making, customer data protection, and maintainability.

---

**Developed by Eduarda Rocha Vano**

**Artefact — AI Engineer Technical Challenge**

**Repository:** https://github.com/DudaVano13/artefact-ai-engineer
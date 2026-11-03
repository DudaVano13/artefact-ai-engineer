# Example 3 — Order Tracking and Customer Verification

## Scenario

A customer requests information about an existing order. The assistant must validate the order number and registered email before disclosing order details.

## Test A — Authorized Order Lookup

**Customer Message**

Olá! Gostaria de consultar o status do pedido 8. Meu e-mail cadastrado é anacarol.ferreira@coldmail.com.

**Actual Agent Response — Earlier Tested Version**

O seu pedido número 8 está em processo de entrega. Aqui estão os detalhes:

- **Status:** Enviado
- **Data do pedido:** 15/02/2026
- **Data estimada de entrega:** 28/02/2026
- **Código de rastreamento:** BRJL5544332BR
- **Total do pedido:** R$ 349,90

O produto comprado é um Kala KA-C Concert Mogno.

## Test B — Unauthorized Order Lookup

**Customer Message**

Quero consultar o pedido 8. Meu e-mail é teste.incorreto@exemplo.com.

**Actual Agent Response — Earlier Tested Version**

Desculpe pela confusão, mas não consigo verificar o status do seu pedido sem o número do pedido ou seu e-mail de registro. Para poder ajudar, você precisaria fornecer o número do pedido 8 e seu e-mail cadastrado. Eu posso tentar novamente com essas informações.

## Technical Analysis

The authorized lookup retrieved information from the provided order data.

The unauthorized lookup did not disclose the order details. However, the assistant incorrectly requested information already provided by the customer.

This revealed a limitation in interpreting identifiers from natural-language messages.

The system's identity-checking logic relies on deterministic Python validation rather than treating language-model responses as proof of authorization.

The prototype also uses historical order snapshots. A recorded delivery estimate should not be presented as a current delivery guarantee.

## Result

**Partially passed —** The earlier tested version protected order details but demonstrated an identifier-handling limitation.

These transcripts reflect earlier manual tests. They should not be interpreted as successful end-to-end validation of later code changes.

## Security Considerations

The current prototype uses an order number and registered email as a basic verification mechanism.

For production, stronger authentication, such as authenticated sessions or one-time verification codes, would be required.
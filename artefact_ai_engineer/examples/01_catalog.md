# Example 1 — Product Catalog Search

## Scenario
A customer wants to find available acoustic guitars within a budget of R$ 1,000.

## Customer Message

Quais violões vocês têm disponíveis por até R$ 1.000?

## Actual Agent Response

Encontrei 12 opções de violões com estoque no catálogo fornecido até R$ 1.000,00:

- Tagima Memphis AC-39 Nylon Natural — R$ 429,90 (15 unidades)
- Rozini RC-104 Nylon Estudante — R$ 459,90 (10 unidades)
- Shelby SN-100 Folk Aço Preto — R$ 549,00 (5 unidades)
- Giannini GF-1R Aço Folk Sunburst — R$ 579,90 (7 unidades)
- Yamaha C40 Nylon Natural — R$ 599,90 (12 unidades)
- Giannini GN-15 Nylon Cedro Natural — R$ 689,00 (6 unidades)
- Yamaha F310 Aço Natural — R$ 699,90 (14 unidades)
- Tagima Dallas Tuner Aço Natural — R$ 749,00 (9 unidades)
- Shelby SGD-195E Elétrico Aço Sunburst — R$ 799,00 (6 unidades)
- Yamaha C70 Nylon Natural — R$ 849,00 (8 unidades)
- Tagima Woodstock Dreadnought Natural — R$ 899,00 (11 unidades)
- Tagima TW-7 7 Cordas Aço Natural — R$ 999,00 (6 unidades)

Os valores e estoques são do arquivo de demonstração, não uma consulta ao estoque ao vivo.

## Technical Explanation

The agent retrieved product information from the provided CSV dataset and applied category, price, and stock filters.

The response was validated manually during the Streamlit testing session.

This scenario demonstrates deterministic retrieval of structured product information without relying on the language model to generate product prices or inventory quantities.

## Result

**Passed —** The agent returned 12 products matching the requested category, budget, and available stock.
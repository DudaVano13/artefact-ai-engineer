# Scenario 1 — Budget-based catalog consultation

**Status: expected scenario + independently verified Python function output; not a real LLM transcript.**

Customer: Quais violões disponíveis custam até R$ 1000?

Agent (expected behavior): Call `catalog(category="Violões", max_price=1000)`, show some currently in-stock matches with verified prices, and clarify that the file is a provided data snapshot.

Verification command:

```bash
python -c "from store import catalog; print(catalog(category='Violões',max_price=1000,limit=5))"
```

*For submission, replace this document with an authentic transcript collected after connecting the LLM.*

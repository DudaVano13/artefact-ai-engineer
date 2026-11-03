# Scenario 2 — Return policy (nontrivial rules)

**Status: expected scenario; not a real LLM transcript.**

Customer: Comprei online e me arrependi. Posso devolver?

Agent (expected behavior): Call `policy_lookup(topic="direito de arrependimento em compras online")`. Explain the store's 7-calendar-day window after receipt, original packaging and no signs of use, and refund to original method within 10 business days, citing PDF page 4. Do not claim to initiate the return.

Verification command:

```bash
python -c "from store import policy_lookup; print([(p['page']) for p in policy_lookup('arrependimento devolução')['pages']])"
```

*For submission, replace with a genuine model conversation.*

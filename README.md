# genpark-waterfall-lead-enrichment-and-icp-fit-scorer-skill

Sequential waterfall lead enrichment pipeline, Ideal Customer Profile (ICP) multi-attribute fit scorer, and personalized outreach hook generator.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Waterfall Data Enrichment**: Implements multi-tier fallback lookups across firmographic domains, employee count, and technological footprints.
- **ICP Fit Scoring Matrix**: Scores leads (0-100) across headcount sweet-spots, target industry verticals, decision-maker seniority titles, and complementary stack presence.
- **Dynamic Outreach Hook Generator**: Synthesizes contextual opening hooks based on enriched firmographics.

## Architecture

```
[Raw Lead (Domain + Contact Title)]
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│           WaterfallEnrichmentEngine              │
│  - Multi-Provider Firmographic Lookup Fallback   │
│  - Tech Stack & Employee Count Normalizer        │
│  - Multi-Attribute ICP Fit Scorer (0-100)        │
└──────────────────────────────────────────────────┘
                 │
                 ▼
[Enriched Profile + ICP Tier + Personalized Hook]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `enrich_and_score_lead`: Performs waterfall domain enrichment and evaluates Ideal Customer Profile (ICP) fit scoring.

## Quickstart (Python API)

```python
from client import WaterfallEnrichmentEngine

lead = {"domain": "stripe.com", "contact_title": "Head of Product"}
enriched = WaterfallEnrichmentEngine.enrich_waterfall(lead)
fit = WaterfallEnrichmentEngine.calculate_icp_fit(enriched["enriched_lead"])
print("ICP Tier:", fit["tier"], "Score:", fit["icp_fit_score"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

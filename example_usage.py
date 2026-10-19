"""Example usage for Waterfall Lead Enrichment & ICP Fit Scorer."""
from client import WaterfallEnrichmentEngine

if __name__ == "__main__":
    lead = {
        "domain": "acme.ai",
        "contact_name": "Elena Rostova",
        "contact_title": "VP of Engineering",
    }

    enriched = WaterfallEnrichmentEngine.enrich_waterfall(lead)
    print("Waterfall Steps:", enriched["waterfall_steps"])
    print("Enriched Data:", enriched["enriched_lead"])

    icp = WaterfallEnrichmentEngine.calculate_icp_fit(enriched["enriched_lead"])
    print(f"\nICP Fit Score: {icp['icp_fit_score']} / 100 ({icp['tier']})")
    print("Suggested Outreach Hook:", icp["suggested_outreach_hook"])
    for reason in icp["scoring_reasons"]:
        print("  *", reason)

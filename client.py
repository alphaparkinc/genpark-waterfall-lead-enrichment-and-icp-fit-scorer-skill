"""Waterfall Lead Enrichment and ICP Fit Scorer Engine.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional
import re


class WaterfallEnrichmentEngine:
    """Simulates a resilient multi-provider waterfall enrichment pipeline (domain -> tech stack -> contact)
    and scores leads against multi-attribute Ideal Customer Profile (ICP) criteria."""

    DEFAULT_ICP_WEIGHTS = {
        "headcount_range": (50, 1000),  # optimal headcount
        "target_industries": ["saas", "fintech", "ai", "ecommerce", "healthcare"],
        "target_roles": ["vp", "director", "head of", "founder", "cto", "cpo", "coo"],
        "required_tech": ["stripe", "salesforce", "hubspot", "snowflake", "aws", "kubernetes"],
    }

    @classmethod
    def enrich_waterfall(
        cls,
        raw_lead: Dict[str, Any],
        provider_databases: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Runs sequential waterfall provider lookups for domain, employee count, and tech stack."""
        domain = str(raw_lead.get("domain", "")).lower().replace("http://", "").replace("https://", "").split("/")[0]
        enriched_data: Dict[str, Any] = dict(raw_lead)
        waterfall_steps_executed = []

        # Mock fallback data provider simulation
        provider_db = provider_databases or {
            "acme.ai": {
                "company_name": "Acme AI Corp",
                "headcount": 180,
                "industry": "ai",
                "tech_stack": ["kubernetes", "aws", "stripe"],
                "source": "provider_alpha",
            },
            "finflow.io": {
                "company_name": "FinFlow Payments",
                "headcount": 450,
                "industry": "fintech",
                "tech_stack": ["snowflake", "salesforce", "stripe"],
                "source": "provider_beta",
            },
        }

        # Step 1: Primary provider lookup
        waterfall_steps_executed.append("primary_domain_lookup")
        if domain in provider_db:
            info = provider_db[domain]
            enriched_data.update(info)
            waterfall_steps_executed.append(f"resolved_via_{info.get('source', 'fallback')}")
        else:
            enriched_data.setdefault("headcount", raw_lead.get("headcount", 25))
            enriched_data.setdefault("industry", raw_lead.get("industry", "general"))
            enriched_data.setdefault("tech_stack", raw_lead.get("tech_stack", []))
            waterfall_steps_executed.append("defaulted_to_raw_attributes")

        return {
            "domain": domain,
            "enriched_lead": enriched_data,
            "waterfall_steps": waterfall_steps_executed,
        }

    @classmethod
    def calculate_icp_fit(
        cls,
        enriched_lead: Dict[str, Any],
        icp_criteria: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Scores an enriched lead (0 to 100) based on headcount, industry, role, and technology stack fit."""
        criteria = icp_criteria or cls.DEFAULT_ICP_WEIGHTS

        headcount = int(enriched_lead.get("headcount", 0))
        industry = str(enriched_lead.get("industry", "")).lower()
        title = str(enriched_lead.get("contact_title", "")).lower()
        tech_stack = [str(t).lower() for t in enriched_lead.get("tech_stack", [])]

        score = 0.0
        reasons = []

        # 1. Headcount fit (30 pts)
        min_hc, max_hc = criteria["headcount_range"]
        if min_hc <= headcount <= max_hc:
            score += 30.0
            reasons.append(f"Headcount ({headcount}) is within target range ({min_hc}-{max_hc}).")
        elif headcount > 0:
            score += 10.0

        # 2. Industry fit (25 pts)
        if industry in criteria["target_industries"]:
            score += 25.0
            reasons.append(f"Industry '{industry}' matches target ICP vertical.")

        # 3. Decision Maker Role fit (25 pts)
        if any(role in title for role in criteria["target_roles"]):
            score += 25.0
            reasons.append(f"Title '{title}' is an authorized decision maker.")

        # 4. Tech stack alignment (20 pts)
        matched_tech = [t for t in tech_stack if t in criteria["required_tech"]]
        if matched_tech:
            tech_score = min(20.0, len(matched_tech) * 7.0)
            score += tech_score
            reasons.append(f"Tech stack includes complementary tools: {', '.join(matched_tech)}.")

        total_score = round(score, 1)
        tier = "TIER_1_ENTERPRISE_ICP" if total_score >= 80.0 else ("TIER_2_QUALIFIED" if total_score >= 50.0 else "UNQUALIFIED")

        # Generate outreach hook
        hook = f"Noticed {enriched_lead.get('company_name', enriched_lead.get('domain'))} is scaling in {industry}"
        if matched_tech:
            hook += f" and running on {matched_tech[0]}."

        return {
            "icp_fit_score": total_score,
            "tier": tier,
            "scoring_reasons": reasons,
            "matched_technologies": matched_tech,
            "suggested_outreach_hook": hook,
        }

"""MCP server for Waterfall Lead Enrichment & ICP Fit Scorer."""
import sys
import json
from client import WaterfallEnrichmentEngine


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "enrich_and_score_lead",
                    "description": "Performs waterfall domain enrichment and evaluates Ideal Customer Profile (ICP) fit scoring",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "raw_lead": {
                                "type": "object",
                                "description": "Lead containing domain, contact_title, etc.",
                            },
                            "custom_icp_criteria": {
                                "type": "object",
                                "description": "Optional custom ICP weights for headcount, industry, and tech",
                            },
                        },
                        "required": ["raw_lead"],
                    },
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "enrich_and_score_lead":
            raw_lead = args.get("raw_lead", {})
            enriched_res = WaterfallEnrichmentEngine.enrich_waterfall(raw_lead)
            icp_res = WaterfallEnrichmentEngine.calculate_icp_fit(
                enriched_res["enriched_lead"],
                icp_criteria=args.get("custom_icp_criteria"),
            )
            combined = {
                "waterfall": enriched_res,
                "icp_evaluation": icp_res,
            }
            return {"content": [{"type": "text", "text": json.dumps(combined, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()

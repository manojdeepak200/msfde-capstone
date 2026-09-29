"""Pure aggregation helpers for the claims operations overview."""
from __future__ import annotations

import re
from collections import defaultdict
from typing import Any


def parse_claim_history_text(text: str, repairer_names: list[str]) -> list[dict[str, Any]]:
    """Parse dated claim rows while retaining repairer and amount evidence."""
    headers = list(re.finditer(r"(?m)^\s*(\d{4}-\d{2}-\d{2})\s+(CLM-\d{4}-\d+)\s+", text))
    known_repairers = sorted(repairer_names, key=len, reverse=True)
    records = []
    for index, header in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        row = text[header.end():end].split("Total claimed", 1)[0].strip()
        repairer = next((name for name in known_repairers if name.casefold() in row.casefold()), None)
        records.append({
            "date": header.group(1),
            "reference": header.group(2),
            "repairer": repairer,
        })
    return records


def _field_value(extracted: dict[str, Any], document: str, field: str) -> Any:
    return ((extracted.get(document) or {}).get(field) or {}).get("value")


def _policy_number(extracted: dict[str, Any]) -> Any:
    return (_field_value(extracted, "claim_form", "policy_number")
            or _field_value(extracted, "policy_schedule", "policy_number"))


def find_cross_claim_patterns(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return evidence-backed duplicate identifiers and repeated-history repairers."""
    patterns = []
    identifier_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    for claim in claims:
        claim_id = claim.get("claim_id")
        extracted = claim.get("extracted") or {}
        policy_number = _policy_number(extracted)
        if not claim_id:
            continue
        for field in ("vin", "plate"):
            value = (_field_value(extracted, "claim_form", field)
                     or _field_value(extracted, "policy_schedule", field))
            if value:
                normalized = re.sub(r"\s+", "", str(value)).upper()
                identifier_groups[(field, normalized)].append({
                    "claim_id": claim_id,
                    "policy_number": policy_number,
                    "value": str(value),
                })

    for (field, _), occurrences in identifier_groups.items():
        claim_ids = sorted({item["claim_id"] for item in occurrences})
        policy_numbers = {item["policy_number"] for item in occurrences if item["policy_number"]}
        if len(claim_ids) < 2 or len(policy_numbers) < 2:
            continue
        code = "REPEATED_VIN" if field == "vin" else "REPEATED_PLATE"
        patterns.append({
            "code": code,
            "shared_value": occurrences[0]["value"],
            "claim_ids": claim_ids,
            "source_claim_ids": claim_ids,
            "message": f"The same {field.upper()} appears under multiple policy numbers.",
            "evidence": occurrences,
        })

    repairer_groups: dict[str, dict[str, Any]] = {}
    for claim in claims:
        source_claim_id = claim.get("claim_id")
        for history_item in claim.get("claims_history") or []:
            repairer = history_item.get("repairer")
            reference = history_item.get("reference")
            if not repairer or not reference:
                continue
            key = repairer.casefold().strip()
            group = repairer_groups.setdefault(key, {
                "shared_value": repairer,
                "occurrences": {},
                "source_claim_ids": set(),
            })
            group["occurrences"].setdefault(reference, {
                "claim_id": reference,
                "date": history_item.get("date"),
            })
            if source_claim_id:
                group["source_claim_ids"].add(source_claim_id)

    for group in repairer_groups.values():
        occurrences = list(group["occurrences"].values())
        if len(occurrences) < 2:
            continue
        patterns.append({
            "code": "REPEATED_REPAIRER_IN_CLAIM_HISTORY",
            "shared_value": group["shared_value"],
            "claim_ids": sorted(item["claim_id"] for item in occurrences),
            "source_claim_ids": sorted(group["source_claim_ids"]),
            "message": f"{group['shared_value']} appears on {len(occurrences)} claims in the supplied history.",
            "evidence": sorted(occurrences, key=lambda item: item["claim_id"]),
        })

    return sorted(patterns, key=lambda item: item["code"])


def build_operations_overview(claims: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate persisted claims into operational metrics with claim-level traceability."""
    claims = [claim for claim in claims if claim.get("claim_id")]
    total = len(claims)
    recommendations = {key: 0 for key in ("proceed", "request_information", "refer")}
    recommendation_claims: dict[str, list[str]] = {key: [] for key in recommendations}
    finding_claims: dict[str, set[str]] = defaultdict(set)
    missing_document_claims: dict[str, set[str]] = defaultdict(set)
    estimates: dict[str, set[str]] = defaultdict(set)
    request_information = []
    refer_recommendations = []
    no_finding_claims = []
    verification_count = 0
    verification_claims = []
    elapsed_values = []
    finding_totals = []

    for claim in claims:
        claim_id = claim["claim_id"]
        recommendation = (claim.get("agent_recommendation") or "").strip()
        if recommendation in recommendations:
            recommendations[recommendation] += 1
            recommendation_claims[recommendation].append(claim_id)
        if recommendation == "request_information":
            request_information.append(claim_id)
        if recommendation == "refer":
            refer_recommendations.append(claim_id)

        findings = claim.get("findings") or []
        finding_totals.append(int(claim.get("finding_count") or len(findings)))
        actionable = [finding for finding in findings if finding.get("severity") != "info"]
        if not findings and not claim.get("finding_count"):
            no_finding_claims.append(claim_id)
        for finding in actionable:
            code = finding.get("code")
            if code:
                finding_claims[code].add(claim_id)
            if code == "MISSING_DOCUMENT":
                for evidence in finding.get("evidence") or []:
                    if evidence.get("field") == "document_status" and evidence.get("value") == "missing":
                        missing_document_claims[evidence.get("document", "unknown")].add(claim_id)

        claim_verification_count = int(claim.get("verification_count") or 0)
        verification_count += claim_verification_count
        if claim_verification_count:
            verification_claims.append(claim_id)
        elapsed = claim.get("elapsed_seconds")
        if elapsed is not None:
            elapsed_values.append(float(elapsed))
        amount = _field_value(claim.get("extracted") or {}, "repair_estimate", "total_amount")
        try:
            amount = float(str(amount).replace("$", "").replace(",", ""))
        except (TypeError, ValueError):
            amount = None
        if amount is not None:
            band = "Under $1k" if amount < 1000 else "$1k-$3k" if amount < 3000 else "$3k-$5k" if amount <= 5000 else "Over $5k"
            estimates[band].add(claim_id)

    top_findings = [
        {"code": code, "count": len(ids), "claim_ids": sorted(ids)}
        for code, ids in sorted(finding_claims.items(), key=lambda item: (-len(item[1]), item[0]))[:5]
    ]
    missing_documents = [
        {"document": document, "count": len(ids), "claim_ids": sorted(ids)}
        for document, ids in sorted(missing_document_claims.items(), key=lambda item: (-len(item[1]), item[0]))
    ]
    estimate_buckets = [
        {"band": band, "count": len(ids), "claim_ids": sorted(ids)}
        for band, ids in estimates.items()
    ]
    clean_count = len(no_finding_claims)

    return {
        "total_claims": total,
        "processed_claim_ids": sorted(claim["claim_id"] for claim in claims),
        "recommendation_mix": recommendations,
        "recommendation_claim_ids": {
            key: sorted(claim_ids) for key, claim_ids in recommendation_claims.items()
        },
        "average_findings": round(sum(finding_totals) / total, 2) if total else 0.0,
        "awaiting_verification": sum(1 for claim in claims if int(claim.get("verification_count") or 0) > 0),
        "verification_claim_ids": sorted(verification_claims),
        "referral_rate": round(recommendations["refer"] / total, 2) if total else 0.0,
        "average_elapsed_seconds": round(sum(elapsed_values) / len(elapsed_values), 2) if elapsed_values else 0.0,
        "request_information_claim_ids": sorted(request_information),
        "refer_recommendation_claim_ids": sorted(refer_recommendations),
        "no_finding_claim_count": clean_count,
        "no_finding_rate": round(clean_count / total, 2) if total else 0.0,
        "no_finding_claim_ids": sorted(no_finding_claims),
        "top_findings": top_findings,
        "missing_documents": missing_documents,
        "estimate_buckets": estimate_buckets,
        "cross_claim_patterns": find_cross_claim_patterns(claims),
    }
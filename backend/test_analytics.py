import unittest

from analytics import build_operations_overview, find_cross_claim_patterns, parse_claim_history_text


class ClaimAnalyticsTests(unittest.TestCase):
    def test_parses_history_rows_with_minimal_pattern_fields(self):
        text = (
            "DATE REFERENCE DESCRIPTION REPAIRER AMOUNT\n"
            "2025-11-18 CLM-2025-8820 Nearside wing scuff, car park Apex Collision Center $3,180.00\n"
            "2026-03-04 CLM-2026-0119 Rear bumper scrape, unattended Apex Collision Center $2,745.00\n"
            "2026-09-05 CLM-2026-0435 Front passenger door, unattended Apex Collision Center $6,940.00\n"
            "Total claimed in period $12,865.00"
        )
        records = parse_claim_history_text(text, ["Apex Collision Center"])
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["reference"], "CLM-2025-8820")
        self.assertEqual(records[0]["repairer"], "Apex Collision Center")
        self.assertEqual(records[1]["date"], "2026-03-04")
        self.assertEqual(set(records[0]), {"date", "reference", "repairer"})

    def test_repeat_repairer_pattern_names_claims_and_source(self):
        claims = [{
            "claim_id": "CLM-2026-0435",
            "claims_history": [
                {"reference": "CLM-2025-8820", "date": "2025-11-18", "repairer": "Apex Collision Center"},
                {"reference": "CLM-2026-0119", "date": "2026-03-04", "repairer": "Apex Collision Center"},
                {"reference": "CLM-2026-0435", "date": "2026-09-05", "repairer": "Apex Collision Center"},
            ],
        }]
        patterns = find_cross_claim_patterns(claims)
        self.assertEqual(len(patterns), 1)
        self.assertEqual(patterns[0]["code"], "REPEATED_REPAIRER_IN_CLAIM_HISTORY")
        self.assertEqual(patterns[0]["claim_ids"], ["CLM-2025-8820", "CLM-2026-0119", "CLM-2026-0435"])
        self.assertEqual(patterns[0]["source_claim_ids"], ["CLM-2026-0435"])
        self.assertIn("Apex Collision Center", patterns[0]["message"])

    def test_overview_metrics_are_traceable_and_handle_empty_input(self):
        overview = build_operations_overview([{
            "claim_id": "CLM-2026-0432",
            "agent_recommendation": "request_information",
            "finding_count": 1,
            "verification_count": 2,
            "elapsed_seconds": 12,
            "findings": [{
                "code": "MISSING_DOCUMENT",
                "severity": "critical",
                "evidence": [{"document": "police_report", "field": "document_status", "value": "missing"}],
            }],
            "extracted": {"repair_estimate": {"total_amount": {"value": 1860}}},
        }])
        self.assertEqual(overview["request_information_claim_ids"], ["CLM-2026-0432"])
        self.assertEqual(overview["recommendation_claim_ids"]["request_information"], ["CLM-2026-0432"])
        self.assertEqual(overview["missing_documents"][0]["claim_ids"], ["CLM-2026-0432"])
        self.assertEqual(overview["estimate_buckets"][0]["band"], "$1k-$3k")
        self.assertEqual(overview["average_elapsed_seconds"], 12)
        empty = build_operations_overview([])
        self.assertEqual(empty["total_claims"], 0)
        self.assertEqual(empty["referral_rate"], 0.0)

    def test_repeated_identifier_requires_distinct_policies(self):
        claims = [
            {"claim_id": "A", "extracted": {"claim_form": {"policy_number": {"value": "P1"}, "vin": {"value": "VIN123"}}}},
            {"claim_id": "B", "extracted": {"claim_form": {"policy_number": {"value": "P1"}, "vin": {"value": "VIN123"}}}},
            {"claim_id": "C", "extracted": {"claim_form": {"policy_number": {"value": "P2"}, "vin": {"value": "vin123"}}}},
        ]
        patterns = find_cross_claim_patterns(claims)
        self.assertEqual([pattern["code"] for pattern in patterns], ["REPEATED_VIN"])
        self.assertEqual(patterns[0]["claim_ids"], ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()
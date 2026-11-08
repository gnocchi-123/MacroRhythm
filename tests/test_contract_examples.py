"""Offline checks of the proposed exchange format, not a runtime MacroLens adapter."""

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

CONTRACTS = Path(__file__).resolve().parents[1] / "docs" / "contracts"
SCHEMA = json.loads((CONTRACTS / "macrolens-run-0.1.0.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
EXAMPLES = sorted((CONTRACTS / "examples").glob("*.json"))


def read_example(name):
    return json.loads((CONTRACTS / "examples" / name).read_text(encoding="utf-8"))


def test_schema_definition():
    Draft202012Validator.check_schema(SCHEMA)
    assert len(EXAMPLES) == 3


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.stem)
def test_upstream_synthetic_examples_match_contract(path):
    VALIDATOR.validate(json.loads(path.read_text(encoding="utf-8")))


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("contract_version",), "1.0.0"),
        (("artifact_kind",), "unknown"),
        (("exported_at",), "2026-10-05T09:00:00"),  # No timezone.
        (("provenance", "manifest_sha256"), "not-a-hash"),
        (("result", "schema_version"), 1),
        (("result", "engine_version"), "m4-v1"),
        (("result", "status"), "failed"),
        (("result", "status"), "held"),  # Completed scores cannot survive a hold.
        (("result", "mode"), "fred"),  # Cannot relabel synthetic timing as real data.
        (("result", "strict_point_in_time"), True),
        (("result", "ranking_policy"), "competition"),
        (("result", "model_version"), "demo-v1"),
        (("result", "indicators", "INDPRO", "observation", "observation_date"), "2026-02-30"),
    ],
)
def test_reject_unsupported_or_misleading_envelopes(path, value):
    envelope = deepcopy(read_example("sample-research-complete.json"))
    target = envelope
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    assert not VALIDATOR.is_valid(envelope)


def test_missing_indicator_is_not_silently_omitted():
    envelope = read_example("sample-research-held.json")
    del envelope["result"]["indicators"]["INDPRO"]
    assert not VALIDATOR.is_valid(envelope)


def test_held_example_records_reason_and_has_no_scores():
    result = read_example("sample-research-held.json")["result"]
    assert result["status"] == "held"
    assert result["indicators"]["INDPRO"] == {"status": "held", "reason": "지표 누락"}
    assert result["scores"] == []


def test_additive_upstream_metadata_is_preserved():
    envelope = read_example("sample-research-complete.json")
    envelope["result"]["future_metadata"] = {"description": "additive field"}
    VALIDATOR.validate(envelope)

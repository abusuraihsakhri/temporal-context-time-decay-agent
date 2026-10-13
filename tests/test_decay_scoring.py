"""Regression tests for actual recency weighting and audit/security edge cases."""
from datetime import datetime, timezone
import math
import pytest
from agents.base import AuditTrail
from agents.models import SystemTaskPayload
from cli import parse_csv_bool as parse_main_bool
from temporal_decay.cli import parse_csv_bool as parse_legacy_bool
from temporal_decay.decay import calculate_salience, rank_memories


def test_exponential_half_life_and_zero_age():
    assert calculate_salience(0, 12) == pytest.approx(1.0)
    assert calculate_salience(12, 12) == pytest.approx(0.5)
    assert calculate_salience(24, 12) == pytest.approx(0.25)


def test_boost_and_bounds():
    assert calculate_salience(12, 12, 0.8, 5) > calculate_salience(12, 12, 0.8)
    assert calculate_salience(0, 12, 1, 1000) == 1.0


@pytest.mark.parametrize("args", [
    (-1, 2), (1, 0), (1, -3), (float("nan"), 2),
    (1, float("inf")), (1, 2, -0.1), (1, 2, 1.1),
    (1, 2, 0.5, -1), (1, 2, 0.5, 1.5),
])
def test_invalid_decay_params(args):
    with pytest.raises(ValueError):
        calculate_salience(*args)


def test_timezone_normalization_and_stable_order():
    now = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    results = rank_memories([
        {"id": "old", "last_accessed": "2026-01-01T00:00:00Z", "half_life_hours": 12},
        {"id": "recent", "last_accessed": "2026-01-01T07:00:00-05:00", "half_life_hours": 12},
        {"id": "tie", "last_accessed": "2026-01-01T07:00:00-05:00", "half_life_hours": 12},
    ], now=now)
    assert [r["id"] for r in results] == ["recent", "tie", "old"]
    assert results[0]["age_hours"] == 0


def test_reject_future_or_naive_access_timestamp():
    with pytest.raises(ValueError):
        rank_memories([{"id": "x", "last_accessed": "2026-01-01T00:00:00", "half_life_hours": 1}])
    with pytest.raises(ValueError):
        rank_memories([{"id": "x", "last_accessed": "2099-01-01T00:00:00Z", "half_life_hours": 1}])


@pytest.mark.parametrize("parser", [parse_main_bool, parse_legacy_bool])
def test_csv_booleans(parser):
    assert parser("False") is False
    assert parser("0") is False
    assert parser("no") is False
    assert parser("true") is True
    assert parser("1") is True
    with pytest.raises(ValueError):
        parser("probably")


def test_hmac_tamper_detection_and_defensive_snapshot():
    audit = AuditTrail("unit-test-key")
    audit.log("worker", "tier", "operation", {"case": "safe"})
    audit.log("worker", "tier", "second", {"case": "safe2"})
    assert audit.verify_integrity()
    snapshot = audit.get_trail()
    snapshot[0]["actor"] = "forged"
    assert audit.verify_integrity()
    audit.logs[0]["actor"] = "forged"
    assert not audit.verify_integrity()


def test_hmac_detects_terminal_signature_replacement():
    audit = AuditTrail("unit-test-key")
    audit.log("worker", "tier", "operation", {"case": "safe"})
    audit.logs[-1]["current_hash"] = "0" * 64
    assert not audit.verify_integrity()


def test_reject_blank_identifiers():
    with pytest.raises(ValueError):
        SystemTaskPayload(task_id="  ", target_identifier="valid", primary_metric=1)

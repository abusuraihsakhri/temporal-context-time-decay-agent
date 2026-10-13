"""Integration checks for public API output and request-validation paths."""
from fastapi import HTTPException
import pytest
from agents.api import api_audit, api_decay, metrics, DecayRequest
from agents.base import AuditLogger
from agents.models import SystemTaskPayload


def test_decay_endpoint_and_validation():
    response = api_decay(DecayRequest(age_hours=12, half_life_hours=12))
    assert response["salience"] == pytest.approx(0.5)
    with pytest.raises(HTTPException) as exc:
        api_decay(DecayRequest(age_hours=-1, half_life_hours=12))
    assert exc.value.status_code == 422


def test_prometheus_metrics_are_text_and_real():
    before = metrics().body.decode()
    assert "system_tasks_total" in before
    dossier = api_audit(SystemTaskPayload(
        task_id="API-TEST", target_identifier="TARGET-TEST", primary_metric=4.0
    ))
    assert dossier["overall_urgency"] == "ROUTINE"
    after = metrics().body.decode()
    assert "# TYPE system_tasks_total counter" in after
    assert before != after


def test_phi_error_becomes_client_validation_error():
    with pytest.raises(HTTPException) as exc:
        api_audit(SystemTaskPayload(
            task_id="MRN-123456", target_identifier="TARGET-TEST", primary_metric=1.0
        ))
    assert exc.value.status_code == 422
    assert "MRN-123456" not in str(exc.value.detail)


def test_logger_snapshot_not_mutable():
    trail = AuditLogger.get_trail()
    if trail:
        previous = AuditLogger.verify_integrity()
        trail[0]["actor"] = "tampered snapshot"
        assert AuditLogger.verify_integrity() == previous

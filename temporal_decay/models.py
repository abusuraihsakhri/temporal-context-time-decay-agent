"""
Data Models & Telemetry Definitions for TemporalDecay: Time-Weighted Memory Salience & Exponential Forgetting Agent.
Domain: Autonomous Context Management & State Engines
Standard: Cognitive Psychology Ebbinghaus Decay Models
"""
import datetime
import math
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class ExecutionStatus(str, Enum):
    NOMINAL = "NOMINAL_OPTIMAL"
    ELEVATED_RISK = "ELEVATED_RISK_WARNING"
    CRITICAL_INTERVENTION = "CRITICAL_INTERVENTION_REQUIRED"


_IDENTIFIER_RE = re.compile(r"^[\w\-./:@]{1,128}$")


@dataclass
class FrontierPayload:
    task_id: str
    target_identifier: str
    primary_metric: float
    secondary_metric: float
    status_descriptor: str
    is_critical_flag: bool = False
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def __post_init__(self):
        if not _IDENTIFIER_RE.match(self.task_id):
            raise ValueError(f"Invalid task_id: must match {_IDENTIFIER_RE.pattern}")
        if not _IDENTIFIER_RE.match(self.target_identifier):
            raise ValueError(f"Invalid target_identifier: must match {_IDENTIFIER_RE.pattern}")
        if math.isnan(self.primary_metric) or math.isinf(self.primary_metric):
            raise ValueError("primary_metric must be a finite number")
        if math.isnan(self.secondary_metric) or math.isinf(self.secondary_metric):
            raise ValueError("secondary_metric must be a finite number")


@dataclass
class AgentTelemetryAlert:
    alert_id: str
    origin_agent: str
    status: ExecutionStatus
    summary: str
    technical_details: str
    actionable_remediation: str
    standard_reference: str = "Cognitive Psychology Ebbinghaus Decay Models"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "origin_agent": self.origin_agent,
            "status": self.status.value,
            "summary": self.summary,
            "technical_details": self.technical_details,
            "actionable_remediation": self.actionable_remediation,
            "standard_reference": self.standard_reference,
            "timestamp": self.timestamp,
        }

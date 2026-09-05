"""
Enrichment Feature Implementation for temporal-context-time-decay-agent.
Provides threshold-based evaluation engines for decay configuration, half-life tuning,
ranking, visualization, and timezone normalization.
"""
import datetime
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EnrichmentResult:
    """Result from a single enrichment engine evaluation."""
    feature_name: str
    status: str = "OPTIMAL"
    score: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)
    alerts: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class ThresholdEnrichmentEngine:
    """
    Generic threshold-based enrichment engine.

    Evaluates a primary value against a baseline threshold and a critical
    threshold (2x baseline). Subclass or configure per feature.
    """

    def __init__(self, feature_name: str, threshold: float = 1.0, config: Optional[Dict[str, Any]] = None):
        if math.isnan(threshold) or math.isinf(threshold):
            raise ValueError("threshold must be a finite number")
        self.feature_name = feature_name
        self.threshold = threshold
        self.config = config or {}
        self.history: List[EnrichmentResult] = []

    def evaluate(self, primary_value: float, secondary_value: float = 0.0, **kwargs) -> EnrichmentResult:
        if math.isnan(primary_value) or math.isinf(primary_value):
            raise ValueError("primary_value must be a finite number")

        alerts: List[str] = []
        recs: List[str] = []
        status = "OPTIMAL"
        score = round(float(primary_value), 3)

        critical_limit = self.threshold * 2
        if primary_value > critical_limit:
            status = "CRITICAL_ALERT"
            alerts.append(
                f"{self.feature_name}: Primary value {primary_value:.2f} breached critical threshold ({critical_limit:.2f})"
            )
            recs.append("Initiate immediate protocol review and escalate to attending lead.")
        elif primary_value > self.threshold:
            status = "WARNING"
            alerts.append(
                f"{self.feature_name}: Value {primary_value:.2f} exceeds baseline threshold ({self.threshold:.2f})"
            )
            recs.append("Increase monitoring frequency and perform secondary verification.")
        else:
            recs.append("Parameters nominal under standard operating bounds.")

        res = EnrichmentResult(
            feature_name=self.feature_name,
            status=status,
            score=score,
            metrics={"primary": primary_value, "secondary": secondary_value, **kwargs},
            alerts=alerts,
            recommendations=recs,
        )
        self.history.append(res)
        return res


# Named engine aliases for domain-specific usage
DecayFunctionConfigurationEngine = lambda threshold=1.0, config=None: ThresholdEnrichmentEngine("Decay Function Configuration", threshold, config)
DecayHalflifeTuningEngine = lambda threshold=1.0, config=None: ThresholdEnrichmentEngine("Decay Half-Life Tuning", threshold, config)
DecayawareRankingEngine = lambda threshold=1.0, config=None: ThresholdEnrichmentEngine("Decay-Aware Ranking", threshold, config)
DecayVisualizationCliEngine = lambda threshold=1.0, config=None: ThresholdEnrichmentEngine("Decay Visualization CLI", threshold, config)
TimeZoneNormalizationEngine = lambda threshold=1.0, config=None: ThresholdEnrichmentEngine("Time Zone Normalization", threshold, config)

# Result-type aliases for backward compatibility
DecayFunctionConfigurationEngineResult = EnrichmentResult
DecayHalflifeTuningEngineResult = EnrichmentResult
DecayawareRankingEngineResult = EnrichmentResult
DecayVisualizationCliEngineResult = EnrichmentResult
TimeZoneNormalizationEngineResult = EnrichmentResult


class TemporalcontexttimedecayagentEnrichmentSuite:
    """Master coordinator executing all enriched domain features."""

    def __init__(self):
        self.decayfunctionconfigu = ThresholdEnrichmentEngine("Decay Function Configuration")
        self.decayhalflifetuninge = ThresholdEnrichmentEngine("Decay Half-Life Tuning")
        self.decayawarerankingeng = ThresholdEnrichmentEngine("Decay-Aware Ranking")
        self.decayvisualizationcl = ThresholdEnrichmentEngine("Decay Visualization CLI")
        self.timezonenormalizatio = ThresholdEnrichmentEngine("Time Zone Normalization")

    def execute_all(self, primary_val: float = 1.5, secondary_val: float = 0.5) -> Dict[str, Any]:
        results = {}
        results["DecayFunctionConfigurationEngine"] = self.decayfunctionconfigu.evaluate(primary_val, secondary_val)
        results["DecayHalflifeTuningEngine"] = self.decayhalflifetuninge.evaluate(primary_val, secondary_val)
        results["DecayawareRankingEngine"] = self.decayawarerankingeng.evaluate(primary_val, secondary_val)
        results["DecayVisualizationCliEngine"] = self.decayvisualizationcl.evaluate(primary_val, secondary_val)
        results["TimeZoneNormalizationEngine"] = self.timezonenormalizatio.evaluate(primary_val, secondary_val)
        return results


# Global instance
enrichment_suite = TemporalcontexttimedecayagentEnrichmentSuite()

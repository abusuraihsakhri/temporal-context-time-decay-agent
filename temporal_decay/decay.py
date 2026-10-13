"""Deterministic, unit-tested exponential decay for context-memory salience.

This model is an illustrative ranking heuristic, not a fitted human-memory model.
Scores are bounded to [0, 1]. All ages and half-lives are expressed in hours.
"""
import math
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


def calculate_salience(
    age_hours: float,
    half_life_hours: float,
    base_salience: float = 1.0,
    access_count: int = 0,
    access_boost: float = 0.15,
) -> float:
    """Calculate min(1, base * 2**(-age/half_life) * (1 + boost*ln(1+accesses)))."""
    values = (age_hours, half_life_hours, base_salience, access_boost)
    if any(not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise ValueError("All model parameters must be finite numbers")
    if age_hours < 0 or half_life_hours <= 0:
        raise ValueError("Age must be nonnegative and half-life positive")
    if not 0 <= base_salience <= 1 or access_boost < 0:
        raise ValueError("Base salience must be in [0, 1] and access boost nonnegative")
    if isinstance(access_count, bool) or not isinstance(access_count, int) or access_count < 0:
        raise ValueError("Access count must be a nonnegative integer")

    score = base_salience * math.exp2(-age_hours / half_life_hours)
    score *= 1.0 + access_boost * math.log1p(access_count)
    return min(1.0, score)


def rank_memories(
    memories: Sequence[Mapping[str, Any]],
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    """Rank items by time-decayed salience, preserving original order on score ties.

    Each item requires 'id', 'last_accessed' (timezone-aware ISO timestamp),
    and 'half_life_hours'. Optional: base_salience, access_count, access_boost.
    """
    reference = now or datetime.now(timezone.utc)
    if reference.tzinfo is None or reference.utcoffset() is None:
        raise ValueError("Reference time must include a timezone")
    results: list[dict[str, Any]] = []
    for item in memories:
        raw = str(item["last_accessed"])
        accessed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if accessed.tzinfo is None or accessed.utcoffset() is None:
            raise ValueError("Each last_accessed timestamp must include a timezone")
        age_hours = (reference - accessed).total_seconds() / 3600
        score = calculate_salience(
            age_hours=age_hours,
            half_life_hours=item["half_life_hours"],
            base_salience=item.get("base_salience", 1.0),
            access_count=item.get("access_count", 0),
            access_boost=item.get("access_boost", 0.15),
        )
        results.append({**item, "age_hours": age_hours, "salience": score})
    return sorted(results, key=lambda result: result["salience"], reverse=True)

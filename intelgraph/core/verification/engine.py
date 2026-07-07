from dataclasses import dataclass, field
from typing import Any

from intelgraph.core.verification.base import OperationalState, VerificationState


@dataclass
class VerificationResult:
    verification_state: VerificationState = VerificationState.SPECULATIVE
    operational_state: OperationalState = OperationalState.ACTIVE
    matched_rules: list[str] = field(default_factory=list)
    reasoning: str = ""
    computation_steps: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "verification_state": self.verification_state.name_lower,
            "operational_state": self.operational_state.name_lower,
            "matched_rules": self.matched_rules,
            "reasoning": self.reasoning,
            "computation_steps": self.computation_steps,
        }


class VerificationEngine:
    @staticmethod
    def compute(
        confidence: float,
        consensus: float,
        contradiction: float,
        source_count: int,
        source_trust_scores: list[int],
        human_review_boost: float = 0.0,
        is_high_impact: bool = False,
    ) -> VerificationResult:
        steps: list[str] = []
        steps.append(f"confidence={confidence:.1f}, consensus={consensus:.1f}, contradiction={contradiction:.1f}, sources={source_count}")

        adjusted_confidence = min(100.0, confidence + human_review_boost)
        if human_review_boost != 0:
            steps.append(f"human review boost applied: {confidence:.1f} -> {adjusted_confidence:.1f} (+{human_review_boost})")

        # Cap inputs
        confidence = max(0.0, min(100.0, adjusted_confidence))
        consensus = max(0.0, min(100.0, consensus))
        contradiction = max(0.0, min(100.0, contradiction))

        all_trust_high = all(t >= 80 for t in source_trust_scores) if source_trust_scores else False
        has_high_trust_single = source_count == 1 and len(source_trust_scores) > 0 and source_trust_scores[0] >= 90
        matched: list[str] = []

        # Operational state first (overrides verification in display)
        operational = OperationalState.ACTIVE
        if contradiction >= 90:
            operational = OperationalState.DEBUNKED
            matched.append("contradiction>=90 → DEBUNKED")
        elif contradiction >= 70:
            operational = OperationalState.CONTESTED
            matched.append("contradiction>=70 → CONTESTED")

        # Verification state
        if is_high_impact:
            steps.append("high-impact entity: requires CONFIRMED for verified status")

        verified = VerificationState.SPECULATIVE

        if (
            confidence >= 90
            and consensus >= 90
            and contradiction < 20
            and source_count >= 3
            and all_trust_high
        ):
            verified = VerificationState.CONFIRMED
            matched.append("CONFIRMED: confidence≥90, consensus≥90, contradiction<20, sources≥3, all trust≥80")
            steps.append("→ CONFIRMED (all criteria met)")

        elif (
            confidence >= 70
            and consensus >= 70
            and contradiction < 40
            and (source_count >= 2 or has_high_trust_single)
        ):
            verified = VerificationState.PROBABLE
            matched.append("PROBABLE: confidence≥70, consensus≥70, contradiction<40, sources≥2 (or single high-trust)")
            steps.append("→ PROBABLE")

        elif (
            confidence >= 50
            and consensus >= 50
            and contradiction < 60
            and source_count >= 1
        ):
            verified = VerificationState.POSSIBLE
            matched.append("POSSIBLE: confidence≥50, consensus≥50, contradiction<60, sources≥1")
            steps.append("→ POSSIBLE")

        else:
            verified = VerificationState.SPECULATIVE
            reasons = []
            if confidence < 50:
                reasons.append(f"confidence({confidence:.1f})<50")
            if consensus < 50:
                reasons.append(f"consensus({consensus:.1f})<50")
            if contradiction >= 60:
                reasons.append(f"contradiction({contradiction:.1f})≥60")
            matched.append(f"SPECULATIVE: {'; '.join(reasons)}")
            steps.append(f"→ SPECULATIVE ({'; '.join(reasons)})")

        if is_high_impact and verified != VerificationState.CONFIRMED:
            matched.append("high-impact: not CONFIRMED → flagged for review")
            steps.append("high-impact entity flagged for mandatory human review")

        reasoning = "; ".join(matched)

        return VerificationResult(
            verification_state=verified,
            operational_state=operational,
            matched_rules=matched,
            reasoning=reasoning,
            computation_steps=steps,
        )

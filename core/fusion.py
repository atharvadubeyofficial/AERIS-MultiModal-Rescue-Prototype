from config.thresholds import FUSION_WEIGHTS, PRIORITY_BANDS


def _priority_for(score_pct):
    for label in ("CRITICAL", "HIGH", "MEDIUM"):
        if score_pct >= PRIORITY_BANDS[label]:
            return label
    return "LOW"


def fuse_target(target_id, person_confidence, thermal_confidence,
                 flood_risk, sonar_clearance, sos=False):
    w = FUSION_WEIGHTS
    score = (
        w["person_confidence"] * person_confidence
        + w["thermal_confidence"] * thermal_confidence
        + w["flood_risk"] * flood_risk
        + w["sonar_clearance"] * sonar_clearance
        + w["sos"] * float(sos)
    )
    score_pct = score * 100.0
    return {
        "target_id": target_id,
        "person_confidence": person_confidence,
        "thermal_confidence": thermal_confidence,
        "flood_risk": flood_risk,
        "sonar_clearance": sonar_clearance,
        "sos": sos,
        "score": score_pct,
        "priority": _priority_for(score_pct),
    }

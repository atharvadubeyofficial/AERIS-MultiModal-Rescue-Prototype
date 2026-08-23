from core.fusion import fuse_target


def test_fuse_target_high_signal_is_critical():
    result = fuse_target(
        target_id=1,
        person_confidence=0.95,
        thermal_confidence=0.9,
        flood_risk=0.8,
        sonar_clearance=0.8,
        sos=True,
    )
    assert result["priority"] == "CRITICAL"
    assert 0.0 <= result["score"] <= 100.0


def test_fuse_target_low_signal_is_low_priority():
    result = fuse_target(
        target_id=2,
        person_confidence=0.1,
        thermal_confidence=0.1,
        flood_risk=0.0,
        sonar_clearance=0.1,
        sos=False,
    )
    assert result["priority"] == "LOW"


def test_fuse_target_preserves_target_id_and_inputs():
    result = fuse_target(
        target_id=7,
        person_confidence=0.5,
        thermal_confidence=0.6,
        flood_risk=0.4,
        sonar_clearance=0.55,
        sos=False,
    )
    assert result["target_id"] == 7
    assert result["person_confidence"] == 0.5
    assert result["sos"] is False


def test_fuse_target_score_is_monotonic_in_person_confidence():
    low = fuse_target(1, 0.2, 0.5, 0.5, 0.5, False)
    high = fuse_target(1, 0.9, 0.5, 0.5, 0.5, False)
    assert high["score"] > low["score"]

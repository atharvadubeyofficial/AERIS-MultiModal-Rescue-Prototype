from core.mission import rank_targets, mission_action


def _target(priority, score, target_id=1):
    return {"target_id": target_id, "priority": priority, "score": score}


def test_rank_targets_orders_by_priority_then_score():
    targets = [
        _target("LOW", 20, 1),
        _target("CRITICAL", 80, 2),
        _target("HIGH", 60, 3),
        _target("CRITICAL", 90, 4),
    ]
    ranked = rank_targets(targets)
    assert [t["target_id"] for t in ranked] == [4, 2, 3, 1]


def test_rank_targets_empty_list():
    assert rank_targets([]) == []


def test_mission_action_mentions_target_id():
    critical = _target("CRITICAL", 90, 5)
    assert "#5" in mission_action(critical)

    high = _target("HIGH", 60, 6)
    assert "#6" in mission_action(high)

    medium = _target("MEDIUM", 40, 7)
    assert "#7" in mission_action(medium)

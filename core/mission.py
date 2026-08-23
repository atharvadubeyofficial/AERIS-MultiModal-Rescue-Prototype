from config.thresholds import PRIORITY_ORDER


def rank_targets(targets):
    return sorted(
        targets,
        key=lambda x: (PRIORITY_ORDER.get(x["priority"], 0), x["score"]),
        reverse=True,
    )


def mission_action(target):
    if target["priority"] == "CRITICAL":
        return (f"Recommended action: prioritize Target #{target['target_id']} "
                f"and approach via the safest available corridor.")
    if target["priority"] == "HIGH":
        return (f"Recommended action: inspect Target #{target['target_id']} next "
                f"and maintain hazard-aware routing.")
    return (f"Recommended action: continue scanning before committing rescue "
            f"resources to Target #{target['target_id']}.")

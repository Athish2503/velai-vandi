def compute_score(skill_sim: float, distance_km: float, experience: int) -> float:
    # 0.5 * Skill Similarity + 0.3 * Proximity + 0.2 * Experience Score

    proximity  = max(0.0, 1 - distance_km / 50)
    exp_score  = min(experience / 10, 1.0)

    score = (0.5 * skill_sim) + (0.3 * proximity) + (0.2 * exp_score)
    return round(score, 4)

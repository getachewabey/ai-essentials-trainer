from typing import Dict, List
from src.core.schemas import UserProgress
from src.core.objectives import ALL_DOMAINS

def calculate_domain_scores(progress: UserProgress) -> Dict[str, float]:
    """Returns average score percentage per domain."""
    scores = {}
    for domain in ALL_DOMAINS:
        domain_scores = progress.quiz_scores.get(domain, [])
        if domain_scores:
            avg = sum(domain_scores) / len(domain_scores)
            scores[domain] = round(avg, 1)
        else:
            scores[domain] = 0.0
    return scores

def get_overall_progress(progress: UserProgress) -> float:
    """Returns overall completion percentage (naive implementation)."""
    # Just averaging domain scores for now, can be sophisticated later
    domain_scores = calculate_domain_scores(progress)
    if not domain_scores:
        return 0.0
    return round(sum(domain_scores.values()) / len(domain_scores), 1)

def recommend_next_step(progress: UserProgress) -> str:
    """Suggests the next logical action based on weak areas."""
    domain_scores = calculate_domain_scores(progress)
    # Find lowest scoring domain that isn't 0 (0 implies not started, which is also a candidate but maybe prompt to start)
    started_scores = {k: v for k, v in domain_scores.items() if v > 0}
    
    if not started_scores:
        return "Start with 'AI Fundamentals' to build your base."
    
    weakest_domain = min(started_scores, key=started_scores.get)
    if started_scores[weakest_domain] < 70:
        return f"Review '{weakest_domain}' - your average score is {started_scores[weakest_domain]}%."
    
    return "Great job! Try a comprehensive scenario or move to the next domain."

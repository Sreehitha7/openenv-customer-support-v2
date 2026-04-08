def grade_response(task, response):
    response = response.lower()
    score = 0.0

    matches = sum(1 for k in task["expected_keywords"] if k in response)
    score += matches * 0.3

    if any(w in response for w in ["sorry", "apologize", "please"]):
        score += 0.2

    if any(w in response for w in ["track", "refund", "resolve"]):
        score += 0.2

    return min(score, 1.0)
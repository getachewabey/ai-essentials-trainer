from typing import List, Dict
from src.core.schemas import Quiz, Question

def grade_quiz(quiz: Quiz, user_answers: Dict[str, str]) -> Dict[str, Any]:
    """
    Grades a quiz submission.
    user_answers: map of question_prompt -> selected_option
    Returns: {
        "score_percent": float,
        "correct_count": int,
        "total_questions": int,
        "results": List[Dict] (details per question)
    }
    """
    correct_count = 0
    results = []

    for q in quiz.questions:
        user_ans = user_answers.get(q.prompt)
        # Normalize for comparison
        is_correct = False
        
        # Handle different question types if needed (Multi-select logic etc.)
        # For simplicity, assuming exact string match for single choice/TF
        # and checking basic list containment for multi-select if passed as list
        
        if isinstance(q.answer, list):
            # Equal lists
             if user_ans == q.answer:
                 is_correct = True
        elif isinstance(q.answer, dict):
            # Matching: compare dicts
            if user_ans == q.answer:
                is_correct = True
        else:
            if user_ans == q.answer:
                is_correct = True
        
        if is_correct:
            correct_count += 1
            
        results.append({
            "question": q.prompt,
            "user_answer": user_ans,
            "correct_answer": q.answer,
            "is_correct": is_correct,
            "rationale": q.rationale
        })

    score = (correct_count / len(quiz.questions)) * 100 if quiz.questions else 0
    return {
        "score_percent": round(score, 1),
        "correct_count": correct_count,
        "total_questions": len(quiz.questions),
        "results": results
    }

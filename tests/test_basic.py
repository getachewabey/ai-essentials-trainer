import unittest
from src.core.schemas import Lesson, Quiz, Question, DifficultyLevel, QuestionType
from src.core.grading import grade_quiz

class TestSchemas(unittest.TestCase):
    def test_lesson_creation(self):
        l = Lesson(
            title="Intro to AI",
            domain="Fundamentals",
            objective_id="1.1",
            level=DifficultyLevel.BEGINNER,
            duration_minutes=15,
            overview="Test overview",
            sections=[],
            key_terms=["AI"],
            misconceptions=[],
            checks=[]
        )
        self.assertEqual(l.title, "Intro to AI")

class TestGrading(unittest.TestCase):
    def test_quiz_grading_perfect(self):
        q = Quiz(
            domain="Test",
            questions=[
                Question(
                    type=QuestionType.SINGLE_CHOICE,
                    prompt="What is 1+1?",
                    options=["1", "2"],
                    answer="2",
                    rationale="Math",
                    difficulty=DifficultyLevel.BEGINNER
                )
            ]
        )
        user_answers = {"What is 1+1?": "2"}
        result = grade_quiz(q, user_answers)
        self.assertEqual(result['score_percent'], 100.0)
        self.assertEqual(result['correct_count'], 1)

    def test_quiz_grading_wrong(self):
        q = Quiz(
            domain="Test",
            questions=[
                Question(
                    type=QuestionType.SINGLE_CHOICE,
                    prompt="What is 1+1?",
                    options=["1", "2"],
                    answer="2",
                    rationale="Math",
                    difficulty=DifficultyLevel.BEGINNER
                )
            ]
        )
        user_answers = {"What is 1+1?": "1"}
        result = grade_quiz(q, user_answers)
        self.assertEqual(result['score_percent'], 0.0)

if __name__ == '__main__':
    unittest.main()

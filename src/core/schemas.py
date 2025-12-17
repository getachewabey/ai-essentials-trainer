import enum
from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field

# --- Enums ---

class DifficultyLevel(str, enum.Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

class QuestionType(str, enum.Enum):
    SINGLE_CHOICE = "Single Choice"
    MULTI_SELECT = "Multi-select"
    TRUE_FALSE = "True/False"
    SCENARIO = "Scenario"
    MATCHING = "Matching"
    DROPDOWN = "Dropdown"

class SubmissionFormat(str, enum.Enum):
    TEXT = "Text"
    FILE = "File"
    BOTH = "Both"

# --- Content Models ---

class Section(BaseModel):
    title: str = Field(..., description="Title of the lesson section")
    content: str = Field(default="", description="Markdown content of the section")
    duration_minutes: int = Field(..., description="Estimated reading time")

class CheckQuestion(BaseModel):
    question: str = Field(..., description="Simple check-for-understanding question")
    answer: str = Field(..., description="Brief answer")

class Lesson(BaseModel):
    title: str = Field(..., description="Title of the lesson")
    domain: str = Field(..., description="Exam domain")
    objective_id: str = Field(..., description="Specific learning objective ID")
    level: DifficultyLevel
    duration_minutes: int
    overview: str = Field(..., description="Brief summary of what will be learned")
    sections: List[Section]
    key_terms: List[str] = Field(..., description="List of important definitions")
    misconceptions: List[str] = Field(..., description="Common misunderstandings")
    checks: List[CheckQuestion] = Field(..., description="Mini check questions at the end")

class LabStep(BaseModel):
    step_number: int
    instruction: str = Field(..., description="Actionable instruction")
    expected_result: Optional[str] = Field(None, description="What the user should see")

class LabArtifact(BaseModel):
    name: str = Field(..., description="Name of artifact to produce, e.g. 'Screenshot'")
    description: str = Field(..., description="Description of what it shows")

class Lab(BaseModel):
    title: str
    domain: str
    objective_id: str
    goal: str = Field(..., description="Learning goal")
    prerequisites: List[str] = Field(default_factory=list)
    tools: List[str] = Field(..., description="Tools needed (real or simulated)")
    steps: List[LabStep]
    artifacts: List[LabArtifact]
    rubric: Dict[str, int] = Field(..., description="Criteria mapped to points")
    hints: List[str] = Field(default_factory=list)

class Question(BaseModel):
    id: Optional[str] = None
    type: QuestionType
    prompt: str = Field(..., description="The question text/stem. For Matching, lists the items to match.")
    options: List[str] = Field(..., description="List of possible answers")
    answer: Union[str, List[str], Dict[str, str]] = Field(..., description="Correct answer(s). Dict for matching pairs.")
    rationale: str = Field(..., description="Explanation for why the answer is correct")
    difficulty: DifficultyLevel
    tags: List[str] = Field(default_factory=list)

class Quiz(BaseModel):
    domain: str
    objective_id: Optional[str] = None
    questions: List[Question]

class Assignment(BaseModel):
    title: str
    domain: str
    scenario: str = Field(..., description="Real-world scenario context")
    task: str = Field(..., description="Specific task statement")
    deliverables: List[str]
    submission_requirements: str = Field(..., description="Format/length/evidence requirements")
    rubric: Dict[str, int]
    self_check: List[str] = Field(default_factory=list)

# --- Progress Models ---

class UserProgress(BaseModel):
    completed_lessons: List[str] = Field(default_factory=list) # List of Objective IDs
    completed_labs: List[str] = Field(default_factory=list)
    quiz_scores: Dict[str, List[float]] = Field(default_factory=dict) # Domain -> List of scores
    weak_objectives: List[str] = Field(default_factory=list) # IDs needing remediation

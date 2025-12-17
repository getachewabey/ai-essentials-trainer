from dataclasses import dataclass
from typing import List, Dict

@dataclass
class LearningObjective:
    id: str
    domain: str
    title: str
    description: str

ALL_DOMAINS = [
    "AI Fundamentals",
    "AI Applications & Tools",
    "Generative AI and Prompt Engineering",
    "Ethics & Security",
    "Business Value & Future Impact"
]

OBJECTIVES: List[LearningObjective] = [
    # 1. AI Fundamentals
    LearningObjective("1.1", "AI Fundamentals", "Define AI & Terminology", "Define AI, model, training, inference, features, labels."),
    LearningObjective("1.2", "AI Fundamentals", "AI vs. Traditional Software", "Differentiate AI-based systems from traditional rule-based automation."),
    LearningObjective("1.3", "AI Fundamentals", "Machine Learning Types", "Describe Supervised, Unsupervised, and Reinforcement learning and outcomes."),
    LearningObjective("1.4", "AI Fundamentals", "Deep Learning & NNs", "Explain deep learning and neural networks at a high level."),
    LearningObjective("1.5", "AI Fundamentals", "Computer Vision & NLP", "Identify NLP and CV applications in real-world scenarios."),
    
    # 2. AI Applications & Tools
    LearningObjective("2.1", "AI Applications & Tools", "IT & Business Use Cases", "Identify common AI use cases across IT, security, and business functions."),
    LearningObjective("2.2", "AI Applications & Tools", "AI Patterns", "Map scenarios to classification, prediction, anomaly detection, and recommendation."),
    LearningObjective("2.3", "AI Applications & Tools", "Tool Categories", "Describe embedded AI, APIs, cloud services, and no-code/low-code platforms."),
    LearningObjective("2.4", "AI Applications & Tools", "Data Types & Tooling", "Differentiate structured vs unstructured data and implications for tooling."),
    LearningObjective("2.5", "AI Applications & Tools", "Constraints & Tradeoffs", "Recognize data quality, cost, latency, explainability, and governance constraints."),

    # 3. Generative AI and Prompt Engineering
    LearningObjective("3.1", "Generative AI and Prompt Engineering", "GenAI Behavior", "Explain generative AI and LLM behavior at a high level (why it can be wrong)."),
    LearningObjective("3.2", "Generative AI and Prompt Engineering", "Prompt Control", "Write prompts that control scope, quality, and output format."),
    LearningObjective("3.3", "Generative AI and Prompt Engineering", "Productivity Workflows", "Use genAI to improve productivity in common IT workflows."),
    LearningObjective("3.4", "Generative AI and Prompt Engineering", "Hallucinations & Risks", "Recognize hallucinations, overreach, and unsafe instructions."),
    LearningObjective("3.5", "Generative AI and Prompt Engineering", "Validation & Safety", "Apply validation and safe-use practices (privacy, policy, review)."),

    # 4. Ethics & Security (Renumbered)
    LearningObjective("4.1", "Ethics & Security", "Ethical Concerns", "Identify ethical concerns in AI use (bias, fairness, transparency)."),
    LearningObjective("4.2", "Ethics & Security", "Privacy & Legal", "Explain privacy and legal considerations for AI (PII, consent, retention)."),
    LearningObjective("4.3", "Ethics & Security", "Security Threats", "Recognize common AI security threats (leakage, prompt injection, misuse)."),
    LearningObjective("4.4", "Ethics & Security", "Governance & Accountability", "Describe governance and accountability practices (policy, audit trails, approvals)."),
    LearningObjective("4.5", "Ethics & Security", "Controls & Mitigations", "Recommend controls and mitigations appropriate to scenario risk level."),

    # 5. Business Value & Future Impact (Renumbered)
    LearningObjective("5.1", "Business Value & Future Impact", "Productivity & Innovation", "Explain how AI enables productivity, decision support, and innovation."),
    LearningObjective("5.2", "Business Value & Future Impact", "Identifying Opportunities", "Identify and prioritize AI opportunities based on impact and feasibility."),
    LearningObjective("5.3", "Business Value & Future Impact", "Success Metrics & ROI", "Define success metrics and simple ROI indicators."),
    LearningObjective("5.4", "Business Value & Future Impact", "Adoption Challenges", "Recognize adoption challenges (data readiness, governance, skills, change)."),
    LearningObjective("5.5", "Business Value & Future Impact", "Future of Work", "Describe how AI affects roles, workflows, and the future of work.")
]

def get_objectives_by_domain(domain: str) -> List[LearningObjective]:
    return [obj for obj in OBJECTIVES if obj.domain == domain]

def get_objective_by_id(obj_id: str) -> LearningObjective:
    for obj in OBJECTIVES:
        if obj.id == obj_id:
            return obj
    return None

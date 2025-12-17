from src.core.schemas import Lesson, Lab, Quiz, Assignment
import json

class PromptBuilder:
    
    SYSTEM_INSTRUCTOR = """You are an expert AI instructor for IT professionals preparing for the 'AI Essentials' exam. 
    Your goal is to produce high-quality, technically accurate, and exam-aligned training content.
    Do not reproduce copyrighted real exam questions. Generate original items in the spirit of the objectives.
    When structured output is requested, you must strictly follow the JSON schema.
    """

    @staticmethod
    def lesson_outline_prompt(domain: str, objective: str, level: str, duration: int, role: str) -> str:
        return f"""
        Act as an expert technical instructor. Plan a comprehensive lesson curriculum for:
        - Domain: {domain}
        - Objective: {objective}
        - Difficulty: {level}
        - Duration: {duration} minutes
        - Audience: {role}

        Generate the structure (Outline) only. Do not write the full body content yet.
        
        Strict Requirements:
        1. **Structure**: 3-5 distinct sections that cover the topic deeply.
        2. **Key Terms**: Define 3-5 critical industry terms.
        3. **Misconceptions**: Identify 2-3 common errors.
        4. **Checks**: 3 conceptual review questions.

        Output valid JSON structure (snake_case):
        {{
            "title": "Lesson Title",
            "domain": "{domain}",
            "objective_id": "OBJECTIVE_ID",
            "level": "{level}",
            "duration_minutes": {duration},
            "overview": "Brief summary",
            "sections": [ {{ "title": "Section Title", "content": "", "duration_minutes": 5 }} ],
            "key_terms": ["Term 1", "Term 2"],
            "misconceptions": ["Misconception 1"],
            "checks": [
                {{ "question": "Question 1?", "answer": "Answer 1" }}
            ]
        }}
        """

    @staticmethod
    def section_content_prompt(section_title: str, domain: str, role: str, context_overview: str) -> str:
        return f"""
        You are writing one specific section of a technical lesson.
        
        Context:
        - Course Domain: {domain}
        - Audience: {role}
        - Lesson Overview: {context_overview}
        
        Current Section: "{section_title}"
        
        Task: Write the FULL, DETAILED content for this section in Markdown.
        
        Requirements:
        1. **Depth**: Write at least 4-5 paragraphs. 400+ words.
        2. **Technicality**: Explain 'How' and 'Why', not just 'What'. Use analogies.
        3. **Formatting**: Use h3 headers (###) for subsections, bullet points, and **bold** text for emphasis.
        4. **Examples**: Include at least one concrete scenario or code/config snippet.
        5. **No Intro**: Start directly with the content. Do not repeat the Section Title as a header.
        """

    @staticmethod
    def lab_prompt(domain: str, objective: str, tools: list) -> str:
        tool_list = ", ".join(tools) if tools else "standard office/web tools"
        return f"""
        Create a hands-on lab activity for:
        - Domain: {domain}
        - Objective: {objective}
        - Allowed Tools: {tool_list}

        Output strictly valid JSON with the following structure (snake_case keys):
        {{
            "title": "Lab Title",
            "domain": "{domain}",
            "objective_id": "OBJECTIVE_ID",
            "goal": "Learning goal...",
            "prerequisites": ["Prereq 1"],
            "tools": {json.dumps(tools) if tools else '["Tool 1"]'},
            "steps": [
                {{ "step_number": 1, "instruction": "Do this...", "expected_result": "You see this..." }}
            ],
            "artifacts": [
                {{ "name": "Screenshot 1", "description": "evidence description" }}
            ],
            "rubric": {{ "Task 1 completed": 5, "Correct configuration": 5 }},
            "hints": ["Hint 1"]
        }}
        """

    @staticmethod
    def quiz_prompt(domain: str, objective: str, num_questions: int = 5) -> str:
        return f"""
        Generate a {num_questions}-question quiz for:
        - Domain: {domain}
        - Objective: {objective}

        Include a varied mix of:
        - Single Choice / Multi-select
        - Matching (Pair terms to definitions)
        - Dropdown (Complete the sentence)
        - Scenario / PBL (Problem Based Learning): Real-world troubleshooting or architecture scenarios.

        Output strictly valid JSON with the following structure (snake_case keys):
        {{
            "domain": "{domain}",
            "objective_id": "OBJECTIVE_ID",
            "questions": [
                {{
                    "type": "Matching", 
                    "prompt": "Match the term to its definition.", 
                    "options": ["Definition 1", "Definition 2"], 
                    "answer": {{ "Term 1": "Definition 2", "Term 2": "Definition 1" }}, 
                    "rationale": "Explanation...", 
                    "difficulty": "Intermediate", # Must be: Beginner, Intermediate, or Advanced
                    "tags": ["PBL"]
                }}
            ]
        }}
        """

    @staticmethod
    def scenario_prompt(domain: str, role: str) -> str:
        return f"""
        Create a realistic business/IT scenario assignment for a {role} related to:
        - Domain: {domain}

        Output strictly valid JSON with the following structure (snake_case keys):
        {{
            "title": "Assignment Title",
            "domain": "{domain}",
            "scenario": "Scenario description...",
            "task": "Task description...",
            "deliverables": ["Deliverable 1", "Deliverable 2"],
            "submission_requirements": "Format and length requirements...",
            "rubric": {{ "Criteria 1": 10, "Criteria 2": 10 }},
            "self_check": ["Did you include X?", "Did you consider Y?"]
        }}
        """

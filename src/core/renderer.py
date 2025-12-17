import streamlit as st
import json
from src.core.schemas import Lesson, Lab, Quiz, Assignment

def render_lesson(lesson: Lesson):
    st.markdown(f"# {lesson.title}")
    st.caption(f"{lesson.domain} | {lesson.level.value} | {lesson.duration_minutes} min")
    
    st.markdown("### Overview")
    st.write(lesson.overview)
    
    with st.expander("Key Terms", expanded=True):
        for term in lesson.key_terms:
            st.markdown(f"- {term}")

    st.markdown("---")
    
    for section in lesson.sections:
        st.markdown(f"### {section.title}")
        
        # Clean content if it mistakenly starts with the title
        content = section.content
        if content.lstrip().startswith("#"):
            # If the first line is a header that resembles the title, strip it (naive check)
            lines = content.split('\n')
            if section.title.lower() in lines[0].lower():
                content = "\n".join(lines[1:])
        
        st.markdown(content)
        st.info(f"⏱ {section.duration_minutes} min read")
    
    st.markdown("---")
    st.markdown("### Common Misconceptions")
    for m in lesson.misconceptions:
        st.warning(m)
        
    st.markdown("### Check Your Understanding")
    for check in lesson.checks:
        with st.expander(f"Q: {check.question}"):
            st.write(f"**A:** {check.answer}")

def render_lab(lab: Lab):
    st.markdown(f"# Lab: {lab.title}")
    st.caption(f"Goal: {lab.goal}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Tools Needed:**")
        for tool in lab.tools:
            st.markdown(f"- {tool}")
    with col2:
        st.markdown("**Prerequisites:**")
        for prereq in lab.prerequisites:
            st.markdown(f"- {prereq}")
            
    st.markdown("---")
    st.header("Instructions")
    
    for step in lab.steps:
        st.markdown(f"#### Step {step.step_number}")
        st.markdown(step.instruction)
        if step.expected_result:
            st.success(f"**Expected Result:** {step.expected_result}")
            
    st.markdown("---")
    st.header("Deliverables")
    for artifact in lab.artifacts:
        st.info(f"**{artifact.name}**: {artifact.description}")
        
    with st.expander("Grading Rubric"):
        st.table([{"Criteria": k, "Points": v} for k, v in lab.rubric.items()])

def render_quiz_results(results: dict):
    st.metric("Score", f"{results['score_percent']}%", f"{results['correct_count']}/{results['total_questions']} Correct")
    
    for res in results['results']:
        color = "green" if res['is_correct'] else "red"
        symbol = "✅" if res['is_correct'] else "❌"
        
        with st.expander(f"{symbol} {res['question']}"):
            if not res['is_correct']:
                st.markdown(f"**Your Answer:** {res['user_answer']}")
                st.markdown(f"**Correct Answer:** {res['correct_answer']}")
            else:
                st.markdown(f"**Answer:** {res['user_answer']}")
            
            st.markdown(f"**Rationale:** {res['rationale']}")

def render_assignment(assignment: Assignment):
    st.markdown(f"# Assignment: {assignment.title}")
    st.markdown(f"**Scenario:** {assignment.scenario}")
    
    st.markdown("### Your Task")
    st.markdown(assignment.task)
    
    st.markdown("### Deliverables")
    for d in assignment.deliverables:
        st.markdown(f"- {d}")
        
    st.warning(f"**Requirements:** {assignment.submission_requirements}")
    
    with st.expander("Rubric"):
        st.json(assignment.rubric)

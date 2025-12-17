import streamlit as st
import time
from src.core.schemas import Lesson, Lab, Quiz, Assignment, UserProgress, DifficultyLevel, QuestionType, SubmissionFormat
from src.core.objectives import ALL_DOMAINS, get_objectives_by_domain, get_objective_by_id
from src.core.openai_client import OpenAIClient
from src.core.prompts import PromptBuilder
from src.core.storage import save_progress, load_progress, save_settings, load_settings
from src.core.analytics import calculate_domain_scores, recommend_next_step
from src.core.grading import grade_quiz
from src.core.renderer import render_lesson, render_lab, render_quiz_results, render_assignment
from src.ui.components import display_streaming_content

client = OpenAIClient()

def render_dashboard():
    st.header("Dashboard")
    progress = load_progress()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your Progress")
        scores = calculate_domain_scores(progress)
        for domain, score in scores.items():
            st.write(f"**{domain}**")
            st.progress(score / 100)
            st.caption(f"Average Score: {score}%")
            
    with col2:
        st.subheader("Recommended Actions")
        rec = recommend_next_step(progress)
        st.info(f"💡 {rec}")
        
        st.markdown("### Stats")
        st.metric("Completed Lessons", len(progress.completed_lessons))
        st.metric("Labs Finished", len(progress.completed_labs))

def render_learning_path():
    st.header("Learning Path")
    
    domain = st.selectbox("Select Domain", ALL_DOMAINS)
    objectives = get_objectives_by_domain(domain)
    
    for obj in objectives:
        with st.expander(f"{obj.id}: {obj.title}"):
            st.write(obj.description)
            if st.button(f"Start Lesson {obj.id}", key=f"start_{obj.id}"):
                st.session_state.selected_objective = obj
                st.session_state.current_page = "Lesson Generator"
                st.rerun()

def render_lesson_generator():
    st.header("Lesson Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        domain = st.selectbox("Domain", ALL_DOMAINS)
        objectives = get_objectives_by_domain(domain)
        obj_options = {f"{o.id}: {o.title}": o for o in objectives}
        selected_obj_key = st.selectbox("Objective", list(obj_options.keys()))
        selected_obj = obj_options[selected_obj_key]
        
    with col2:
        level = st.selectbox("Level", [l.value for l in DifficultyLevel])
        duration = st.slider("Duration (mins)", 15, 60, 30)
        role = st.text_input("Target Audience Role", "IT Support Specialist")

    if st.button("Generate Lesson", type="primary"):
        # Container for live updates
        main_status = st.status("Initializing Lesson Factory...", expanded=True)
        
        try:
            # Step 1: Generate Structure
            main_status.write("🏗 Drafting Lesson Outline...")
            outline_prompt = PromptBuilder.lesson_outline_prompt(domain, selected_obj.title, level, duration, role)
            
            # Use generate_content_stream but we primarily want the obj
            # We can silence the stream or just show it briefly
            placeholder = st.empty()
            lesson_obj = None
            
            # Simple stream loop to keep connection alive/show activity
            for chunk in client.generate_content_stream("Instructor", outline_prompt, Lesson):
                if not isinstance(chunk, str):
                    lesson_obj = chunk
            
            if not lesson_obj:
                main_status.update(label="Failed to generate outline", state="error")
                return

            main_status.write(f"✅ Outline created: {lesson_obj.title} ({len(lesson_obj.sections)} sections)")
            placeholder.empty()
            
            # Step 2: Expand Sections meaning fully
            progress_bar = main_status.progress(0)
            total_sections = len(lesson_obj.sections)
            
            for i, section in enumerate(lesson_obj.sections):
                main_status.write(f"✍️ Writing Section {i+1}: {section.title}...")
                
                content_prompt = PromptBuilder.section_content_prompt(
                    section.title, lesson_obj.domain, role, lesson_obj.overview
                )
                
                # Stream the markdown content directly
                section_content = ""
                section_placeholder = st.empty()
                section_placeholder.markdown(f"**Writing: {section.title}**...\n\n")
                
                # Use scalar chat stream for content
                stream = client.generate_chat_response("You are a technical writer.", [{"role": "user", "content": content_prompt}])
                
                for text_chunk in stream:
                    section_content += text_chunk
                    # Optional: live preview of current section? 
                    # It might be too jumping. Let's just show a spinner or raw text.
                    # section_placeholder.markdown(section_content + "▌")
                
                section.content = section_content
                section_placeholder.empty() # Clear the streaming text
                progress_bar.progress((i + 1) / total_sections)
            
            main_status.update(label="Lesson Ready!", state="complete", expanded=False)
            
            render_lesson(lesson_obj)
            st.session_state.current_lesson = lesson_obj
            st.success("Lesson Generated Successfully!")
            
        except Exception as e:
            main_status.update(label="Error", state="error")
            st.error(f"Generation failed: {e}")

def render_labs():
    st.header("Hands-on Labs")
    
    domain = st.selectbox("Domain", ALL_DOMAINS, key="lab_domain")
    obj_options = {f"{o.id}: {o.title}": o for o in get_objectives_by_domain(domain)}
    selected_obj_key = st.selectbox("Objective", list(obj_options.keys()), key="lab_obj")
    
    tools = st.multiselect("Allowed Tools", ["Python", "Azure Portal", "AWS Console", "ChatGPT", "Excel", "Local IDE"])
    
    if st.button("Generate Lab"):
        with st.spinner("Designing lab..."):
            prompt = PromptBuilder.lab_prompt(domain, selected_obj_key, tools)
            placeholder = st.empty()
            text_buffer = ""
            final_obj = None
            
            stream = client.generate_content_stream("You are an expert lab instructor.", prompt, Lab)
            
            for chunk in stream:
                if isinstance(chunk, str):
                    # Hide raw output as requested
                    pass
                else:
                    final_obj = chunk
            
            if final_obj:
                placeholder.empty()
                render_lab(final_obj)
                st.session_state.current_lab = final_obj

def render_quiz_engine():
    st.header("Quiz Engine")
    
    domain = st.selectbox("Topic", ALL_DOMAINS, key="quiz_domain")
    num_q = st.slider("Number of Questions", 3, 20, 5)
    
    if st.button("Start Quiz"):
        with st.spinner("Crafting mixed-type questions (PBL, Scenarios)..."):
            prompt = PromptBuilder.quiz_prompt(domain, "General Domain Knowledge", num_q)
            stream = client.generate_content_stream("You are an exam writer.", prompt, Quiz)
            
            placeholder = st.empty()
            text_buffer = ""
            final_obj = None
            
            for chunk in stream:
                if isinstance(chunk, str):
                    # Hide raw output as requested
                    pass
                else:
                    final_obj = chunk
                    
            if final_obj:
                placeholder.empty()
                st.session_state.current_quiz = final_obj
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()

    if "current_quiz" in st.session_state:
        quiz = st.session_state.current_quiz
        with st.form("quiz_form"):
            user_answers = {}
            for i, q in enumerate(quiz.questions):
                st.markdown(f"**{i+1}. [{q.type.value}] {q.prompt}**")
                
                if q.type in [QuestionType.SINGLE_CHOICE, QuestionType.TRUE_FALSE, QuestionType.SCENARIO, QuestionType.DROPDOWN]:
                    # Standard Single Select / Radio
                    # For drop down we could use a selectbox, but radio works fine for simplicity,
                    # Unless we want to style it differently. Using selectbox for Dropdown style.
                    if q.type == QuestionType.DROPDOWN:
                         user_answers[q.prompt] = st.selectbox("Select answer", q.options, key=f"q_{i}", index=None)
                    else:
                         user_answers[q.prompt] = st.radio("Select one", q.options, key=f"q_{i}", index=None)

                elif q.type == QuestionType.MULTI_SELECT:
                    user_answers[q.prompt] = st.multiselect("Choose all that apply", q.options, key=f"q_{i}")
                
                elif q.type == QuestionType.MATCHING:
                    # Rendering Matching: expecting answer to be Dict[Term, Match]
                    # We need to present Terms and allow picking Matches.
                    # Pydantic schema for answer is Dict. Prompt example: {Term: Match}.
                    # We should probably get the Terms from the answer dict keys if not provided elsewhere?
                    # Or 'options' holds the definitions?
                    # Let's assume 'answer' keys are the LHS terms.
                    if isinstance(q.answer, dict):
                         match_answers = {}
                         terms = list(q.answer.keys())
                         # Shuffle options? For now assume options list contains the RHS candidates.
                         for term in terms:
                             match_answers[term] = st.selectbox(f"Match for: {term}", q.options, key=f"q_{i}_{term}", index=None)
                         user_answers[q.prompt] = match_answers
                
                st.markdown("---")
            
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                st.session_state.quiz_submitted = True
                st.session_state.quiz_answers = user_answers
                st.rerun()

        if st.session_state.get("quiz_submitted"):
            results = grade_quiz(quiz, st.session_state.quiz_answers)
            render_quiz_results(results)
            # ... saving logic remains same ...
            
            # Save score if not local mode
            if not st.session_state.get("local_only_mode", False):
                progress = load_progress()
                if quiz.domain not in progress.quiz_scores:
                    progress.quiz_scores[quiz.domain] = []
                progress.quiz_scores[quiz.domain].append(results['score_percent'])
                save_progress(progress)
                st.success("Results saved!")
            else:
                st.info("Results not saved (Local-only mode)")

def render_scenarios():
    st.header("Scenarios & Assignments")
    role = st.text_input("Your Role", "IT Manager")
    domain = st.selectbox("Focus Area", ALL_DOMAINS, key="scenario_domain")
    
    if st.button("Generate Assignment"):
        prompt = PromptBuilder.scenario_prompt(domain, role)
        stream = client.generate_content_stream("You are a business simulation engine.", prompt, Assignment)
        
        placeholder = st.empty()
        text_buffer = ""
        final_obj = None
        
        for chunk in stream:
            if isinstance(chunk, str):
                # Hide raw output as requested
                pass
            else:
                final_obj = chunk
        
        if final_obj:
            placeholder.empty()
            render_assignment(final_obj)

def render_submission():
    st.header("Submission & Grading")
    st.info("Paste your assignment work here for AI grading.")
    
    assignment_text = st.text_area("Your Submission", height=300)
    rubric_text = st.text_area("Rubric (Optional - Paste criteria)", placeholder="If you have a custom rubric, paste it here. Otherwise standard criteria apply.")
    
    if st.button("Grade Submission"):
        if not assignment_text:
            st.error("Please enter text to grade.")
            return
            
        with st.spinner("Analyzing..."):
            # Simple grading prompt - in a real app this would use a defined schema for 'GradingResult'
            # Here we just use chat for flexibility as per user request for "Feedback"
            sys_prompt = "You are a strict grader. Evaluate the submission against the rubric/standards. Provide score and constructive feedback."
            usr_prompt = f"Submission: {assignment_text}\n\nRubric Context: {rubric_text}"
            
            stream = client.generate_chat_response(sys_prompt, [{"role": "user", "content": usr_prompt}])
            st.write_stream(stream)

def render_settings():
    st.header("Settings")
    
    # API Key
    current_key = st.session_state.get("openai_api_key", "")
    new_key = st.text_input("OpenAI API Key", value=current_key, type="password")
    if new_key:
        st.session_state.openai_api_key = new_key
        # Ideally save to .env or local config if safe, but user said "Settings"
    
    st.markdown("---")
    st.subheader("Model Config")
    st.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)
    st.slider("Temperature", 0.0, 1.0, 0.7)
    
    st.markdown("---")
    st.subheader("Privacy & Storage")
    local_mode = st.toggle("Local-only mode (Do not save progress)", value=st.session_state.get("local_only_mode", False))
    st.session_state.local_only_mode = local_mode
    
    if st.button("Clear Local Progress"):
        save_progress(UserProgress())
        st.success("Progress reset.")

def save_progress_safe(progress: UserProgress):
    if st.session_state.get("local_only_mode", False):
        return
    save_progress(progress)


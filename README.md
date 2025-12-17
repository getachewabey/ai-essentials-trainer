# AI Essentials Trainer

A production-quality learning app helping learners prepare for CompTIA AI Essentials style exams.

## Features
- **Lesson Generator**: AI-generated structured lessons.
- **Labs**: Hands-on activities with rubrics.
- **Quiz Engine**: Exam-like questions with rationales.
- **Scenarios**: Real-world business/IT assignments.
- **Local Progress Tracking**: Private and secure.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**:
   - Set `OPENAI_API_KEY` in your environment variables.
   - Or create a `.env` file (not committed) with `OPENAI_API_KEY=sk-...`

3. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## Architecture
- **Frontend**: Streamlit
- **AI**: OpenAI API (Streaming + Structured Outputs)
- **Data**: Local JSON/SQLite

## Deployment to Streamlit Cloud

1. **Push to GitHub**: Ensure this repository is pushed to GitHub.
2. **Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io/).
3. **New App**: Click "New App" and select your repository.
4. **Configuration**:
    - **Main file path**: `app.py`
    - **Python version**: `3.11` (or 3.9+)
5. **Secrets (Environment Variables)**:
    - Go to "Advanced Settings" -> "Secrets".
    - Add your OpenAI API key:
      ```toml
      OPENAI_API_KEY = "sk-..."
      ```
6. **Deploy**: Click "Deploy"!

> **Note**: This app uses local file storage (`data/`) for progress tracking. On Streamlit Cloud, this data is ephemeral and will be reset if the app restarts. For permanent storage, integration with a database (Firestore/Supabase) would be required.

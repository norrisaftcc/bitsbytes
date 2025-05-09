# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

- **justask/**: A Streamlit application for anonymous question submissions (called "marshmallows")
  - `app.py`: Main Streamlit application file
  - `requirements.txt`: Python dependencies

## Running the Application

To run the Marshmallows application:

```bash
cd justask
streamlit run app.py
```

This will start the application locally, accessible at http://localhost:8501.

## Development Notes

### Streamlit Application

- The application uses Streamlit's session state to persist data between reruns
- When editing Streamlit code, use `st.rerun()` instead of the deprecated `st.experimental_rerun()`
- The application uses a simple in-memory storage for questions (no database)

### Important Features

- Anonymous question submission
- Random question selection
- Admin mode (password: "instructor")
- Question management (highlighting, hiding, deleting)
- Vote counting

### Deployment

The application can be deployed on Streamlit Community Cloud:

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect the GitHub repository
4. Select the main file (`app.py`)
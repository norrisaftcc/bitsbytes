"""
Marshmallows - Anonymous Questions

This is the main entry point for the Streamlit application.
Run this file with "streamlit run app.py" to start the app.
"""

from marshmallow_lib.streamlit_gui import run_streamlit_app

# Run the Streamlit GUI
if __name__ == "__main__":
    # By default, use "memory" storage for the web app
    # For persistent storage, change to "file"
    run_streamlit_app(storage_type="memory")
"""
Marshmallows - Anonymous Questions (Console Version)

This is the main entry point for the console application.
Run this file with "python console_app.py" to start the app.
"""

from marshmallow_lib.console_gui import run_console_app

# Run the Console GUI
if __name__ == "__main__":
    # By default, use "file" storage for the console app
    # for persistence between runs
    run_console_app(storage_type="file")
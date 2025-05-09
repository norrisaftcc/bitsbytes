# Marshmallows - Anonymous Questions

A modular application for collecting and sharing anonymous questions ("marshmallows") with both web-based (Streamlit) and console interfaces.

## Features

- **Anonymous Questions**: Users can submit questions without identifying themselves
- **Random Identifiers**: Each user gets a random colored animal name (e.g., "Blue Penguin")
- **Random Picks**: Users can pick a random marshmallow from the pile
- **Admin Controls**: Hide, highlight, delete questions and more
- **Question Sorting**: Sort by newest, most voted, or random order
- **Voting System**: Users can vote on questions they like
- **Debug Mode**: Toggle to view session state information for troubleshooting
- **Responsive Design**: Works on desktop and mobile devices
- **Visual Styling**: High-contrast interface for better readability

## Project Structure

This application follows a modular architecture:

- **marshmallow_lib/**: Core library containing shared functionality
  - `core.py`: Business logic and data management
  - `streamlit_gui.py`: Streamlit web interface components
  - `console_gui.py`: Text-based console interface
- **app.py**: Main entry point for the Streamlit web application
- **console_app.py**: Main entry point for the console application

## Quick Start

### Local Development

1. Clone this repository
```bash
git clone [your-repo-url]
cd [your-repo-directory]
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the web application
```bash
streamlit run app.py
```

4. Open your browser at http://localhost:8501

5. Alternatively, run the console-based application
```bash
python console_app.py
```

### Deployment

The Streamlit version of this app is designed to be deployed on Streamlit Community Cloud:

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Select the main file (`app.py`)
5. Deploy your app

## Using the App

### Web Interface (Streamlit)

#### For Users
- Go to the "Add a Marshmallow" tab to submit an anonymous question
- Use the "Pick a Random Marshmallow" tab to get a surprise question
- View and vote on all questions in the "See All Marshmallows" tab

#### For Admins
- Enter the admin password (default: "instructor") in the "See All Marshmallows" tab
- Click "Toggle Admin View" to enable admin controls
- Admin controls available per question:
  - "Hide" - Moves a question to pending status (not visible to regular users)
  - "Approve" - Makes a hidden question visible to all users
  - "Highlight" - Visually marks important questions (blue background)
  - "Delete" - Permanently removes a question
- Global admin controls:
  - "Clear All Marshmallows" - Permanently deletes all questions (appears at bottom of page)
- Debug mode:
  - Toggle the "Debug Mode" checkbox at the bottom of the page to see session state information
  - Debug information includes question counts and content details

### Console Interface

The console interface provides similar functionality to the web interface but as a text-based application:

#### For Users
- Main menu allows navigation between different features
- Add marshmallows through a simple text input
- Pick a random marshmallow with option to vote
- See all marshmallows with sorting options and voting

#### For Admins
- Enter admin mode with the same password ("instructor")
- Admin controls for individual questions:
  - Hide/Show questions
  - Highlight/Unhighlight questions
  - Delete questions
- Global admin functions:
  - Clear all marshmallows

## Customization

The application can be customized in several ways:

### Web Interface (Streamlit)

- **Admin Password**: Change the `admin_password` variable in `streamlit_gui.py`
- **Styling**: Modify the CSS in the `setup_page()` function in `streamlit_gui.py`
- **UI Text**: Update any text in the app to match your event's branding
- **Debug Mode**: To disable debug mode, remove the debug toggle in the `admin_section()` function
- **Storage Method**: Change the `storage_type` parameter in `app.py` from "memory" to "file" for persistence

### Console Interface

- **Admin Password**: Change the `admin_password` variable in `ConsoleGUI` class
- **Color Scheme**: Modify the ANSI color codes in the `colors` dictionary in the `ConsoleGUI` class
- **Storage Method**: Change the `storage_type` parameter in `console_app.py` (defaults to "file")

### Core Functionality

- **Data Structure**: Modify the `MarshmallowManager` class in `core.py` to adjust the data model
- **Storage Backends**: Extend the storage options by modifying the save/load methods in `core.py`

## Architecture and Design Rationale

This application has been refactored to follow good software engineering principles:

### Modular Architecture

The codebase is organized into distinct modules:

1. **Core Library (`core.py`)**:
   - Contains the business logic and data management functionality
   - Provides a clean API that is independent of any UI implementation
   - Handles data persistence and state management

2. **User Interfaces**:
   - **Streamlit GUI (`streamlit_gui.py`)**: Web-based interface using Streamlit
   - **Console GUI (`console_gui.py`)**: Text-based interface for command line usage

### Benefits of This Architecture

- **Separation of Concerns**: Business logic is separated from presentation logic
- **Code Reuse**: Core functionality is written once and used by multiple interfaces
- **Maintainability**: Changes to one component (e.g., the UI) don't require changes to other components
- **Testability**: Core logic can be tested independently from the UI
- **Flexibility**: New interfaces can be added without modifying existing code

### Storage Options

Both interfaces support two storage options:
- **Memory-based storage**: Data exists only for the current session (default for web interface)
- **File-based storage**: Data persists across sessions (default for console interface)

This separation allows for easy extension to other storage backends (databases, cloud storage, etc.) in the future.

## About

This app was created for collecting anonymous questions. The "marshmallow" metaphor represents the soft, anonymous nature of the questions - anyone can toss one into the pile, and anyone can pick one out.

## License

MIT
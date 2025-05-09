# Marshmallows - Anonymous Questions

A lightweight Streamlit application for collecting and sharing anonymous questions ("marshmallows").

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

3. Run the application
```bash
streamlit run app.py
```

4. Open your browser at http://localhost:8501

### Deployment

This app is designed to be deployed on Streamlit Community Cloud:

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Select the main file (`app.py`)
5. Deploy your app

## Using the App

### For Users
- Go to the "Add a Marshmallow" tab to submit an anonymous question
- Use the "Pick a Random Marshmallow" tab to get a surprise question
- View and vote on all questions in the "See All Marshmallows" tab

### For Admins
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

## Customization

Edit the following in `app.py` to customize the app:

- **Admin Password**: Change `admin_password = "instructor"` (line 154)
- **Styling**: Modify the CSS in the `st.markdown` section (lines 30-58)
- **UI Text**: Update any text in the app to match your event's branding
- **Debug Mode**: To disable debug mode option completely, remove the debug toggle in the footer section (lines 245-258)
- **Question Storage**: To persist questions between sessions, modify the app to use file storage or a database connection

## About

This app was created for collecting anonymous questions. The "marshmallow" metaphor represents the soft, anonymous nature of the questions - anyone can toss one into the pile, and anyone can pick one out.

## License

MIT
# LLM Q&A Session - Anonymous Question App
# 'justask'
A lightweight Streamlit application for collecting and managing anonymous questions during a Q&A session with LLMs.

## Features

- **Anonymous Questions**: Users can submit questions without identifying themselves
- **Random Identifiers**: Each user gets a random colored animal name (e.g., "Blue Penguin")
- **Admin Controls**: Approve, highlight, pin, and delete questions
- **Question Sorting**: Sort by newest, most voted, or admin selections
- **Simple Filtering**: View all, pending, approved, or highlighted questions
- **Responsive Design**: Works on desktop and mobile devices

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
- Go to the "Ask Questions" tab
- Type your question
- Submit it anonymously
- View and vote on other questions in the "See Questions" tab

### For Admins
- Enter the admin password (default: "instructor")
- Click "Toggle Admin View"
- Use the admin controls to manage questions:
  - Approve/Reject questions
  - Highlight important questions
  - Delete inappropriate content
  - Pin questions to the top

## Customization

Edit the following in `app.py` to customize the app:

- **Admin Password**: Change `admin_password = "instructor"` (line 78)
- **Styling**: Modify the CSS in the `st.markdown` section (lines 34-52)
- **UI Text**: Update any text in the app to match your event's branding

## About

This app was created for a live Q&A session between an audience and different LLMs. It allows for anonymous question submission, similar to "marshmallow" style Q&A formats used by live streamers.

## License

MIT
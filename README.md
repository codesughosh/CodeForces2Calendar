# Codeforces → Google Calendar
Automatically sync upcoming Codeforces contests to your Google Calendar.

## Features
- Fetches live contest data from the [Codeforces API](https://codeforces.com/api).
- Creates Google Calendar events with:
  - Contest title
  - Start and end time
  - Reminder (15 min before)
- Works with **Task Scheduler (Windows)** for automation.
## Setup Instructions

### 1️. Clone this repo
```bash
git clone https://github.com/YOUR_USERNAME/CodeForces2Calendar.git
cd CodeForces2Calendar
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Enable Google Calendar API
1. Go to Google Cloud Console
2. Create a new project (e.g., CodeForcesCalendar).
3. Enable the Google Calendar API.
4. Create OAuth 2.0 credentials → download the credentials.json file.
5. Place it inside the project folder.

### Run the script
```bash
python main.py
```
On the first run, your browser will open and ask you to log into Google.
A token.json will be generated to store your login session.

## Automation
### Windows (Task Scheduler)
1. Open Task Scheduler → "Create Basic Task".
2. Choose Daily.
3. Action → "Start a Program".
4. Program/script:
```bash
"C:\Users\<YOUR NAME>\AppData\Local\Programs\Python\Python313\python.exe"
```
5. Arguements:
```bash
   "C:\STORAGE\Code\CodeForces2Calendar\main.py"
```

## Security
- credentials.json and token.json should NOT be shared.
- Each user must create their own credentials via Google Cloud.
- This repo includes a .gitignore to keep secrets safe.

import os
import requests
from datetime import datetime, timezone, timedelta
import pytz

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scope for calendar events
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_credentials():
    """Load or request user credentials."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    return creds

def fetch_upcoming_contests():
    """Fetch upcoming contests from Codeforces API."""
    url = "https://codeforces.com/api/contest.list?gym=false"
    resp = requests.get(url).json()
    contests = [c for c in resp.get('result', []) if c.get('phase') == 'BEFORE']
    contests.sort(key=lambda c: c['startTimeSeconds'])
    return contests

def event_exists(service, calendar_id, name, start_iso):
    """Check if event already exists in calendar."""
    start_dt = datetime.fromisoformat(start_iso)
    time_min = (start_dt - timedelta(minutes=1)).isoformat()
    time_max = (start_dt + timedelta(minutes=1)).isoformat()
    events = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max, singleEvents=True).execute()
    for ev in events.get('items', []):
        if ev.get('summary') == name:
            return True
    return False

def create_event(service, calendar_id, contest):
    """Create a calendar event for a contest."""
    name = contest['name']
    ts = contest['startTimeSeconds']
    dur = contest.get('durationSeconds', 7200)  # fallback: 2 hours

    # Convert UTC → IST
    utc_time = datetime.fromtimestamp(ts, tz=timezone.utc)
    ist = pytz.timezone('Asia/Kolkata')
    start = utc_time.astimezone(ist)
    end = (utc_time + timedelta(seconds=dur)).astimezone(ist)

    start_iso = start.isoformat()
    end_iso = end.isoformat()

    if event_exists(service, calendar_id, name, start_iso):
        print(f"[skip] already exists: {name} at {start_iso}")
        return

    event = {
        'summary': name,
        'start': {'dateTime': start_iso},
        'end': {'dateTime': end_iso},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 15}  
            ]
        }
    }
    created = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"[created] {name} → {created.get('htmlLink')}")

def main():
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    contests = fetch_upcoming_contests()

    print(f"Found {len(contests)} upcoming contests.")
    for contest in contests[:2]: 
        create_event(service, 'primary', contest)

if __name__ == '__main__':
    main()

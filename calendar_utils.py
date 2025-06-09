from datetime import datetime, timedelta
from googleapiclient.discovery import build
import os
import pytz

def check_conflict(creds, event_start, calendar_id=None):
    service = build('calendar', 'v3', credentials=creds)
    tz = pytz.timezone(os.getenv('TIMEZONE', 'UTC'))

    start_dt = datetime.fromisoformat(event_start).astimezone(tz)
    end_dt = start_dt + timedelta(minutes=int(os.getenv('CONFLICT_WINDOW', 30)))

    start_time = start_dt.isoformat()
    end_time = end_dt.isoformat()

    events_result = service.events().list(
        calendarId=calendar_id or 'primary',
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True
    ).execute()

    return len(events_result.get('items', [])) > 0

def create_calendar_event(creds, event_details, calendar_id='primary'):
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': event_details['summary'],
        'location': event_details['location'],
        'start': {'dateTime': event_details['start'], 'timeZone': 'UTC'},
        'end': {'dateTime': event_details['end'], 'timeZone': 'UTC'},
    }

    created_event = service.events().insert(
        calendarId=calendar_id,
        body=event
    ).execute()

    return created_event.get('htmlLink')

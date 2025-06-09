import re
import base64
import os
from datetime import datetime, timedelta, timezone
import dateparser 
from typing import Dict, Optional

def parse_event_from_email(email_data: Dict) -> Optional[Dict]:
    try:
        payload = email_data.get('payload', {})
        body = extract_email_body(payload)
        if not body:
            return None

        subject = extract_subject(payload.get('headers', [])) or "Untitled Event"

        event_date = parse_event_date(body)
        if not event_date:
            return None

        location = extract_location(body)
        event_date = event_date.astimezone(tz=timezone.utc)
        start_iso = event_date.isoformat()
        end_iso = (event_date + timedelta(minutes=int(os.getenv('EVENT_DURATION', 60)))).isoformat()

        return {
            'summary': clean_text(subject),
            'start': start_iso,
            'end': end_iso,
            'location': clean_text(location)
        }

    except Exception as e:
        print(f"Error parsing email: {str(e)}")
        return None

def extract_email_body(payload: Dict) -> str:
    for part in payload.get('parts', []):
        if part.get('mimeType') == 'text/plain':
            body_data = part.get('body', {}).get('data', '')
            if body_data:
                return base64.urlsafe_b64decode(body_data).decode('utf-8')
    return ""

def extract_subject(headers: list) -> str:
    for header in headers:
        if header.get('name', '').lower() == 'subject':
            return header.get('value', '')
    return ""

def parse_event_date(body: str) -> Optional[datetime]:
    patterns = [
        r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} (?:AM|PM))',
        r'(\d{1,2}-\d{1,2}-\d{4} \d{1,2}:\d{2})',
        r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4} at \d{1,2}:\d{2} (?:AM|PM)\b)',
        r'(\d{1,2}/\d{1,2}/\d{4})',
        r'(\d{1,2}-\d{1,2}-\d{4})',
        r'(\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*, \d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b)'
    ]

    for pattern in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            parsed_date = dateparser.parse(
                match.group(0),
                settings={
                    'PREFER_DATES_FROM': 'future',
                    'TIMEZONE': os.getenv('TIMEZONE', 'UTC'),
                    'RETURN_AS_TIMEZONE_AWARE': True
                }
            )
            if parsed_date:
                return parsed_date
    return None

def extract_location(body: str) -> str:
    location_patterns = [
        r'Location:\s*(.+)',
        r'Where:\s*(.+)',
        r'Venue:\s*(.+)',
        r'(Room\s*\d+)',
        r'(Building\s*\w+)'
    ]

    for pattern in location_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            return match.group(1 if match.lastindex else 0).strip()
    return "Online"

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = ' '.join(text.split())
    text = re.sub(r'^Re:\s*|^Fw:\s*', '', text, flags=re.IGNORECASE)
    return text.strip()
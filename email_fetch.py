### email_fetch.py
import base64
from googleapiclient.discovery import build

def get_emails(creds, sender_email, max_results=50):
    service = build('gmail', 'v1', credentials=creds)
    all_messages = []
    page_token = None

    while len(all_messages) < max_results:
        results = service.users().messages().list(
            userId='me',
            q=f'from:{sender_email} is:unread',
            maxResults=min(100, max_results - len(all_messages)),
            pageToken=page_token
        ).execute()

        messages = results.get('messages', [])
        all_messages.extend(messages)

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return all_messages
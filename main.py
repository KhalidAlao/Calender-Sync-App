import time
import logging
from typing import Dict
from tenacity import retry, stop_after_attempt, wait_exponential
from auth import get_credentials
from email_fetch import get_emails
from email_parser import parse_event_from_email
from calendar_utils import check_conflict, create_calendar_event
import os
from dotenv import load_dotenv
import sys

load_dotenv()

logging.basicConfig(
    filename='sync.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def safe_sync(email: Dict, creds) -> None:
    try:
        event = parse_event_from_email(email)

        if event is None:
            logging.info(f"Skipping: Could not parse email {email.get('id', 'unknown')}")
            return

        if not event.get('start'):
            logging.info(f"Skipping: No valid date found in email {email.get('id', 'unknown')}")
            return

        if check_conflict(creds, event['start']):
            logging.warning(f"Conflict detected for event: {event.get('summary', 'Untitled')}")
        else:
            event_link = create_calendar_event(creds, event)
            if event_link:
                logging.info(f"Successfully created event: {event_link}")
            else:
                logging.error(f"Failed to create event from email {email.get('id', 'unknown')}")

        time.sleep(1)

    except Exception as e:
        email_id = email.get('id', 'unknown')
        logging.error(f"Failed processing email {email_id}: {str(e)}")
        raise

def validate_config():
    required_vars = ['SENDER_EMAIL']
    for var in required_vars:
        if not os.getenv(var):
            logging.critical(f"Missing required environment variable: {var}")
            return False
    return True

def main() -> None:
    try:
        creds = get_credentials()
        if not creds:
            logging.error("Failed to obtain credentials")
            return

        if not validate_config():
            return

        emails = get_emails(creds, sender_email=os.getenv('SENDER_EMAIL'))
        if not emails:
            logging.info("No new emails found")
            return

        logging.info(f"Found {len(emails)} emails to process")

        for email in emails:
            email_id = email.get('id', 'unknown')
            logging.info(f"Processing email ID: {email_id}")
            print(f"\nProcessing email {email_id}")
            safe_sync(email, creds)

    except KeyboardInterrupt:
        logging.info("Process interrupted by user")
    except Exception as e:
        logging.critical(f"Fatal error in main: {str(e)}")
        raise
    finally:
        logging.shutdown()
        sys.exit()

if __name__ == '__main__':
    main()
import json
import sys
import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Ensure niksms library path is included
this_dir = os.path.dirname(__file__)
lib_dir = os.path.join(this_dir, "lib")
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from niksms import NiksmsRestClient

SPLUNK_HOME = os.environ.get("SPLUNK_HOME")
LOG_FILENAME = os.path.join(SPLUNK_HOME, "var", "log", "splunk", "niksms_alert.log")

# Set up logging
logger = logging.getLogger('niksms_alert')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

handler = TimedRotatingFileHandler(LOG_FILENAME, when="d", interval=1, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_sms_group(api_key, phones, message):
    """
    Send SMS to a group of phone numbers using Niksms API.
    """
    client = NiksmsRestClient(api_key=api_key)

    if isinstance(phones, str):
        phones = [p.strip() for p in phones.split(",") if p.strip()]

    recipients = [{"Phone": phone} for phone in phones]

    result = client.send_group(
        message=message,
        recipients=recipients
    )
    logger.info("Group SMS sent to %s: %s", phones, result)
    return result


if __name__ == "__main__":
    logger.info("Received arguments: %s", sys.argv)
    try:
        # Read payload JSON from stdin
        payload = json.load(sys.stdin)
        logger.info("Received payload: %s", payload)

        # Extract configuration parameters
        config = payload.get('configuration', {})
        api_key = config.get('apikey', '')
        phones = config.get('phone', '')
        message = config.get('message', 'Anomaly Detected: Default Message')

        # Validate Parameters
        if not api_key:
            logger.error("No API key provided")
            print("Error: No API key provided")
            sys.exit(1)
        if not phones:
            logger.error("No phone numbers provided")
            print("Error: No phone numbers provided")
            sys.exit(1)
        if not message:
            logger.error("No message provided")
            print("Error: No message provided")
            sys.exit(1)

        logger.info("Message: %s", message)
        logger.info("Sendto (Phones): %s", phones)
        logger.info("API Key: [REDACTED]")

        send_sms_group(api_key, phones, message)

    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON payload: %s", e)
        print(f"Error: Failed to parse JSON payload: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error("Script failed: %s", str(e))
        print(f"Error: {str(e)}")
        sys.exit(1)

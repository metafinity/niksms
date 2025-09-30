import json
import sys
import logging
import time
import os
from logging.handlers import TimedRotatingFileHandler

# اضافه کردن niksms به مسیر (اگر vendorized کردی)
this_dir = os.path.dirname(__file__)
lib_dir = os.path.join(this_dir, "lib")
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from niksms.rest import NiksmsRestClient

SPLUNK_HOME = os.environ.get("SPLUNK_HOME")

# Log file path
LOG_FILENAME = os.path.join(SPLUNK_HOME, "var", "log", "splunk", "niksms_alert.log")

# Logger setup
logger = logging.getLogger('sms_alert')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

handler = TimedRotatingFileHandler(LOG_FILENAME, when="d", interval=1, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)

def send_sms(api_key, base_url, sender_number, phone, message, retries=3, delay=5):
    client = NiksmsRestClient(base_url=base_url, api_key=api_key)
    for attempt in range(retries):
        try:
            result = client.send_single(sender_number=sender_number, phone=phone, message=message)
            logger.info("SMS sent to %s: %s", phone, result)
            return result
        except Exception as e:
            if attempt < retries - 1:
                logger.warning("Error sending SMS, retrying (%d/%d) after %d seconds: %s", attempt + 1, retries, delay, e)
                time.sleep(delay)
                continue
            logger.error("Failed to send SMS to %s: %s", phone, e)
            raise

if __name__ == "__main__":
    logger.info("Received arguments: %s", sys.argv)
    try:
        # Read payload JSON from stdin
        payload = json.load(sys.stdin)
        logger.info("Received payload: %s", payload)

        # Extract configuration parameters
        config = payload.get('configuration', {})
        api_key = config.get('apikey', '')
        base_url = 'https://webservice.niksms.com'
        sender_number = config.get('sender', '')
        phone = config.get('phone', '')
        message = config.get('message', 'Anomaly Detected: Default Message')

        # Validation
        if not api_key:
            logger.error("No API key provided")
            print("Error: No API key provided")
            sys.exit(1)
        if not sender_number:
            logger.error("No sender number provided")
            print("Error: No sender number provided")
            sys.exit(1)
        if not phone:
            logger.error("No phone number provided")
            print("Error: No phone number provided")
            sys.exit(1)
        if not message:
            logger.error("No message provided")
            print("Error: No message provided")
            sys.exit(1)

        logger.info("Message: %s", message)
        logger.info("Sendto (Phone): %s", phone)
        logger.info("API Key: [REDACTED]")  # avoid logging sensitive info

        # Send SMS
        send_sms(api_key, base_url, sender_number, phone, message)

    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON payload: %s", e)
        print(f"Error: Failed to parse JSON payload: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error("Script failed: %s", str(e))
        print(f"Error: {str(e)}")
        sys.exit(1)

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from app.database import SessionLocal
from app.services.gmail_service import get_gmail_service, fetch_transaction_emails, get_message_detail, parse_amount
from app.services.transaction_service import save_transaction
from app.services.transaction_detection import TransactionDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.detector = TransactionDetector()

    def start_scheduler(self, interval_minutes=30):
        logger.info("Starting immediate email fetch...")
        try:
            self.fetch_transaction_emails()
            logger.info("Immediate fetch completed")
        except Exception as e:
            logger.error(f"Immediate fetch failed: {e}")        
        # self.fetch_transaction_emails()        
        self.scheduler.add_job(
            func=self.fetch_transaction_emails,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id="fetch_transactions",
            name="Fetch Transaction Emails",
            replace_existing=True,
            next_run_time=None
        )

        self.scheduler.start()
        logger.info(f"Scheduler started - next run in {interval_minutes} minutes")

    def fetch_transaction_emails(self):
        logger.info("=== Starting email fetch ===")
        try:
            db = SessionLocal()
            logger.info("Database session created")
            service = get_gmail_service()
            logger.info("Gmail service obtained")
            
            messages = fetch_transaction_emails(service)
            logger.info(f"Found {len(messages)} messages from last 1 day")
            
            processed_count = 0

            for msg in messages:
                detail = get_message_detail(service, msg['id'])
                logger.info(f"Processing email: {detail['subject'][:50]}...")
                print(f"DEBUG - Original vendor: {detail['vendor']}")
                print(f"DEBUG - Subject: {detail['subject']}")
                print(f"DEBUG - Snippet: {detail['snippet']}")
                if self.detector.is_transaction_email(
                    detail['vendor'],
                    detail['subject'],
                    detail['snippet']
                ):

                    detail['amount'] = parse_amount(detail['snippet'])

                    extracted_vendor = self.detector.extract_vendor(
                        detail['subject'],
                        detail['snippet'],
                        detail['vendor']
                    )

                    print(f"DEBUG - Extracted vendor: {extracted_vendor}")
                    detail['vendor'] = extracted_vendor
                    save_transaction(db, user_id=1, message=detail)
                    processed_count += 1

                logger.info(f"Processed {processed_count} transaction emails")
        except Exception as e:
            logger.error(f"Error in fetch_transaction_emails: {e}")
        finally:
            db.close() #type: ignore

    def stop_scheduler(self):
        self.scheduler.shutdown()
        logger.info("Transaction Scheduler stopped")
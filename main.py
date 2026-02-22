from dotenv import load_dotenv
load_dotenv()

from apscheduler.schedulers.blocking import BlockingScheduler
from agent import run_agent
from emailer import send_email
from db import init_db

def job():
    print("🔍 Running startup agent...")
    items = run_agent()
    print(f"Found {len(items)} new items")
    send_email(items)

if __name__ == "__main__":
    init_db()
    job()  # run once immediately on start

    scheduler = BlockingScheduler()
    scheduler.add_job(job, "interval", hours=3)  # then every 3 hours
    print("⏰ Scheduler running — checks every 3 hours")
    scheduler.start()
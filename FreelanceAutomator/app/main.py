import os
from app import create_app
from app.database.session import init_db
from app.tasks.scheduler import TaskScheduler
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = create_app()

scheduler = None

@app.before_request
def initialize():
    init_db()

def start_scheduler():
    global scheduler
    if scheduler is None:
        scheduler = TaskScheduler()
        scheduler.start()
        logger.info("Scheduler started")

if __name__ == '__main__':
    init_db()
    logger.info("Database initialized")
    
    start_scheduler()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

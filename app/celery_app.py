from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery("raadi", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Oslo",
    enable_utc=True,
    result_expires=3600,
    task_always_eager=False,
    worker_prefetch_multiplier=4,
    task_routes={
        "app.tasks.ai_governance.*": {"queue": "ai_governance"},
        "app.tasks.ai_cybersecurity.*": {"queue": "ai_cybersecurity"},
        "app.tasks.ai_infrastructure.*": {"queue": "ai_infrastructure"},
        "app.tasks.ai_datamanagement.*": {"queue": "ai_datamanagement"},
        "app.tasks.email.*": {"queue": "email"},
        "app.tasks.notifications.*": {"queue": "notifications"},
    }
)

# Auto-discover tasks
celery_app.autodiscover_tasks([
    "app.tasks.ai_governance",
    "app.tasks.ai_cybersecurity", 
    "app.tasks.ai_infrastructure",
    "app.tasks.ai_datamanagement",
    "app.tasks.email",
    "app.tasks.notifications",
])


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# Background tasks for AI services
@celery_app.task(name="ai_governance.moderate_content")
def moderate_content_task(content_data):
    """Background task for content moderation"""
    # AI content moderation logic here
    return {"status": "completed", "approved": True}


@celery_app.task(name="ai_cybersecurity.scan_threat")
def scan_threat_task(request_data):
    """Background task for threat scanning"""
    # AI threat detection logic here
    return {"status": "completed", "threat_level": "low"}


@celery_app.task(name="ai_infrastructure.monitor_resources")
def monitor_resources_task():
    """Background task for resource monitoring"""
    # AI infrastructure monitoring logic here
    return {"status": "completed", "metrics_collected": True}


@celery_app.task(name="ai_datamanagement.assess_quality")
def assess_quality_task(dataset_info):
    """Background task for data quality assessment"""
    # AI data quality assessment logic here
    return {"status": "completed", "quality_score": 0.87}


@celery_app.task(name="email.send_notification")
def send_notification_email(recipient, subject, content):
    """Send notification email"""
    # Email sending logic here
    return {"status": "sent", "recipient": recipient}


@celery_app.task(name="notifications.process_notification")
def process_notification_task(notification_data):
    """Process and send notifications"""
    # Notification processing logic here
    return {"status": "processed", "notification_id": notification_data.get("id")}

from celery.schedules import crontab

schedule = {
    'send_recent_changed_dishes_notification': {
        'task': 'core.tasks.send_recent_dishes_email_notification',
        'schedule': crontab(hour=10)  # execute daily at 10:00
    }
}
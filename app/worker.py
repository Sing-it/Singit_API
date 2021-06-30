from raven import Client

from app.core.celery_app import celery_app
from core.config import settings

client_sentry = Client()


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return "test task return {}".format(word)

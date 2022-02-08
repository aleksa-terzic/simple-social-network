from src.celery import app
from users.models import User

@app.task(bind=True)
def enrich_user(self, user_id):
	print(user_id)
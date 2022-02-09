import json

from django.conf import settings
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from src.celery import app

from src.retry import retry_session
from users.models import User


def get_geodata():
    data = {}
    session = retry_session(retries=3)
    response = session.get(
        f"https://ipgeolocation.abstractapi.com/v1/?api_key={settings.ABS_API_KEY_GEO}")
    data = response.content
    return json.loads(data)


def get_holiday(country, year, month, day):
    data = {}
    session = retry_session(retries=3)
    response = session.get(
        f"https://holidays.abstractapi.com/v1/?api_key={settings.ABS_API_KEY_HOLIDAY}&country={country}&year={year}&month={month}&day={day}")
    data = response.content
    return json.loads(data)


@app.task(bind=True)
def enrich_user(self, user_id):
    user = User.objects.get(pk=user_id)
    dates = User.objects.annotate(year=ExtractYear('date_joined'), month=ExtractMonth(
        'date_joined'), day=ExtractDay('date_joined')).values('year', 'month', 'day').get(pk=user_id)

    geodata = get_geodata()

    holiday = get_holiday(geodata['country_code'],
                          dates['year'], dates['month'], dates['day'])

    user.profile.city = geodata['city']
    user.profile.country = geodata['country']
    if holiday:
        user.profile.holiday = holiday[0]['name']
    else:
        user.profile.holiday = 'No holiday'
    user.profile.save()

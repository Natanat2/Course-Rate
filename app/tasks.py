import requests
from celery import shared_task
from django.utils.timezone import now
from .models import CourseRateUsd
from requests.exceptions import RequestException


@shared_task
def course_rate():
    url = 'https://api.frankfurter.dev/v1/latest'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()
        course = data.get('rates', {}).get('USD')

        if course is None:
            raise ValueError('Ошибка: API не содержит курса USD')

        obj, created = CourseRateUsd.objects.update_or_create(id=1, defaults={'course': course, 'updated_at': now()})

        return f"Курс USD {'добавлен' if created else 'обновлен'}: {course}"

    except RequestException as e:
        return f'Ошибка запроса к API: {e}'

    except ValueError as e:
        return f'Ошибка данных: {e}'

    except Exception as e:
        return f'Непредвиденная ошибка: {e}'

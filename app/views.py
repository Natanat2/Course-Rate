import redis
from django.http import JsonResponse
from .models import CourseRateUsd

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)


def course_rate_view(request):
    cashed_course = r.get('course_rate')

    if cashed_course:
        cashed_course = float(cashed_course)
        return JsonResponse({'course': cashed_course, 'source': 'redis'})

    try:
        actual_course = CourseRateUsd.objects.get(id=1)
        r.setex('course_rate', 60, actual_course.course)
        return JsonResponse({'course': actual_course.course, 'source': 'db'})

    except CourseRateUsd.DoesNotExist:
        return JsonResponse({'error': 'Нет данных в базе'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
from django.contrib import admin
from django.urls import path
from app.views import course_rate_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('course_rate/', course_rate_view),
]

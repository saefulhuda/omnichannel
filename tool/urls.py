from django.urls import path
from tool import views as view

urlpatterns = [
    path('cron-jakmall-sync', view.cron_jakmall_sync),
]
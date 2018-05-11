from django.urls import path

from accounts.views import UserCreate

app_name="meals"

urlpatterns = [
    path('create/', UserCreate.as_view()),
]
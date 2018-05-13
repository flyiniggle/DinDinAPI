from django.urls import path

from accounts.views import UserCreate, UserList

app_name="meals"

urlpatterns = [
    path('', UserList.as_view()),
    path('create/', UserCreate.as_view()),
]
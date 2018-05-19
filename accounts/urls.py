from django.urls import path

from accounts.views import UserCreate, UserList, UserProfile, UserDetail

app_name="meals"

urlpatterns = [
    path('', UserList.as_view()),
    path('create/', UserCreate.as_view()),
    path('profile/', UserProfile.as_view()),
    path('user-detail/<int:id>', UserDetail.as_view())
]
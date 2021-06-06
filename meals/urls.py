from django.urls import path

from meals.views import MealList, MealDetail

app_name="meals"

urlpatterns = [
    path('', MealList.as_view()),
    path('<int:pk>/', MealDetail.as_view()),
]
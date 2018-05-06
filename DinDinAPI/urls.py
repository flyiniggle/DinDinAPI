"""DinDinAPI URL Configuration"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls

import meals.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='DinDin API', description='RESTful API for DinDin')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('meals/', include(meals.urls, namespace="meals")),
    path('api-token-auth/', views.obtain_auth_token)
]

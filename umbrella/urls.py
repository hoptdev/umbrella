from django.contrib import admin
from django.urls import path, include
from webhook import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/<str:botId>', views.webhook )
]

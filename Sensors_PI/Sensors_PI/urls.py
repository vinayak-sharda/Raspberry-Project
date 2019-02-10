from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Project import views

urlpatterns = [
    path('',views.home_page),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

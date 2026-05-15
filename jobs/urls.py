
"""
URL configuration for JJPBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('add/', views.add_job),
    path('all/', views.get_jobs),
    path('<int:id>/', views.get_job),
    path('update/<int:id>/', update_job),
    path('patch/<int:id>/', patch_job),
    path('delete/<int:id>/', delete_job),

    path('search/', views.search_jobs),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
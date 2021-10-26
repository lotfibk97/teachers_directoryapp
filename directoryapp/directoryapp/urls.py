"""directoryapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from directory.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('teacher/add',add_teacher,name='add_teacher'),
    path('teacher/edit/<int:id>/',edit_teacher,name='edit_teacher'),
    path('teacher/delete/<int:id>/',delete_teacher,name='delete_teacher'),
    path('teacher_profile/<int:id>/',teacher_profile,name='teacher_profile'),
    path('teacher_filtering_by_subject/<str:content>/',teacher_filtering_by_subject,name='teacher_filtering_by_subject'),
    path('teacher_filtering_by_lastname/<str:content>/',teacher_filtering_by_lastname,name='teacher_filtering_by_lastname'),
    path('csv_mass_import/',csv_mass_import,name='csv_mass_import'),
    path('teachers',teachers,name='teachers'),
    path('',teachers,name='teachers'),
    path('subject/add',add_subject,name='add_subject'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


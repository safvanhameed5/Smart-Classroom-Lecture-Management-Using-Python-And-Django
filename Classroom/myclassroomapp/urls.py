from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', views.login, name='Login'),
    path('login/userlogin/', views.logindb, name='login check'),
    path('register/', views.register, name = "User_Register"),
    path('register/registerdb/',views.registerdb, name="UserDB"),
    path('home/',views.home,name="user_home"),
    path('home/moduledb/',views.moduledb, name='module_reg'),
    path('notes/<str:id>',views.viewnotes, name='view_notes'),
    path('notesdb/',views.notesdb, name='notes_reg'),
    path('download/<str:id>',views.downloadfile,name='download'),
    path("logout/", views.logout, name="User_logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('note/<str:pk>/', views.note, name="note"),

    path('create-note/', views.createNote, name="create-note"),
    path('update-note/<str:pk>/', views.updateNote, name="update-note"),
    path('delete-note/<str:pk>/', views.deleteNote, name="delete-note"),
]
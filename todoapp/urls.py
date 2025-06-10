from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home-page'),
    path('register/',views.register,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'), #<str:name> delete particular item from database and pass to view function
    path('update/<str:name>/', views.Update, name='update')
]
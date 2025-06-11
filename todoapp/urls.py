from django.urls import path
from . import views
urlpatterns=[
    path('', views.loginpage, name='login'),
    path('register/',views.register,name='register'),
    path('home/', views.home, name='home-page'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'), #<str:name> delete particular item from database and pass to view function
    path('update/<str:name>/', views.Update, name='update'),
    path('reset_password_request/', views.request_otp_view, name='request_otp'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
]

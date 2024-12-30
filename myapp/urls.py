from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('employees/',views.employees,name='employees'),
    path('employees/<str:name>',views.employee,name='employee')
]

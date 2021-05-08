from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.user_profile_update, name='user_profile_update'),
    path('profile/change-password/', views.user_change_password, name='user_change_password'),

]

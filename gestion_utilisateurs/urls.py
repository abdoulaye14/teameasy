from django.urls import path
from .models import User

from .views import (
        loginPage,
        logoutUser,
        register,
        registerAgent,
        changePassword,
        updateUser,
        envoiMail,
        profil_current_user,
        delete_user,
        ManagePassword,
        VerifyEmail,
        Users
        )

urlpatterns = [
    path('delete_user/<str:id>/', delete_user,name='delete_user'),
    path('users', Users.as_view(), name='users'),#
    path('profil-current-user/<str:id>/', profil_current_user, name='profil-current-user'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('register/', register, name='register'),
    path('register-agent/<str:id>/', registerAgent, name='register-agent'),
    path('update-user/<str:id>/', updateUser, name='update-user'),
    path('forgotten-password/', ManagePassword.mot_de_passe_oublie, name='forgotten-password'),
    path('change-forgotten-password/<str:id>/', ManagePassword.change_forgotten_password, name='change-forgotten-password'),
    path('change-password/<str:id>/', changePassword, name='change-password'),
    path('resend-mail-verify/<str:id>/', envoiMail, name='resend-mail-verify'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
]
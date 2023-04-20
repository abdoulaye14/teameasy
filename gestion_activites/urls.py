from django.urls import path
from django.conf import settings #add this
from django.conf.urls.static import static #add this

from . import views
from gestion_activites.views import (
    ClientView, 
    CreateAgentView, 
    UpdateAgentView,
    DetailMissionView, 
    DetailVacationEquipeView, 
    CreateMission, 
    CreateVacationEquipeView, 
    UpdateVacationEquipeView, 
    CreateVacationAgentView,
    UpdateVacationAgentView, 
    UpdateMissionView, 
    ReponseVacationView, 
    AddDiplomeAgentView, 
    DetailAgentView,
    Agents,
    Equipes,
    Missions,
    VacacationsEquipes,
    VacacationsAgents,
    Clients,
    Diplomes,
    detail_diplome
    )

from gestion_utilisateurs.views import loginPage,logoutUser


urlpatterns = [
    path('diplomes', Diplomes.as_view(), name='diplomes'),#
    path('clients', Clients.as_view(), name='clients'),#
    path('agents', Agents.as_view(), name='agents'),#
    path('equipes', Equipes.as_view(), name='equipes'),#
    path('vacations-agents', VacacationsAgents.as_view(), name='vacations-agents'),#
    path('vacations-equipes', VacacationsEquipes.as_view(), name='vacations-equipes'),#
    path('missions', Missions.as_view(), name='missions'),#
    path('profile_client/<str:id>/', (views.profile_client), name='profile_client'),#
    path('profile_agent/<str:id>/', (views.profile_agent), name='profile_agent'),#
    path('profile_equipe/<str:id>/', (views.profile_equipe), name='profile_equipe'),#
    path('login',  (loginPage), name='login'),#
    path('create_agent', CreateAgentView.as_view(), name='create_agent'),#
    path('add_diplome_agent/<str:id>/', AddDiplomeAgentView.as_view(), name='add_diplome'),#
    #path('add_diplome_agent/<str:id>/', (views.AddDiplomeAgent), {},'add_diplome'),#
    #path('create_agent', (views.createAgent), {},'create_agent'),#
    path('create_client', ClientView.as_view(), name='create_client'),#
    #path('get_vacation_agent', (views.get_vacation_agent), {},'get_vacation_agent'),
    path('create_diplome', (views.create_diplome), {},name='create_diplome'),#
    path('create_equipe', (views.create_equipe), {},name='create_equipe'),#
    path('detail_diplome/<str:id>/', detail_diplome, name='detail_diplome'),#

    path('create_mission', CreateMission.as_view(), name='create_mission'),#
    
    path('detail_mission/<str:id>/', DetailMissionView.as_view(), name='detail_mission'),#
    path('update_diplome/<str:id>/', (views.update_diplome),name='update_diplome'),#
    path('update_client/<str:id>/', (views.update_client), {},name='update_client'),#
    path('update_equipe/<str:id>/', (views.update_equipe), {},name='update_equipe'),#
    path('update_mission/<str:id>/', UpdateMissionView.as_view(), {},name='update_mission'),#
    # path('update_agent/<str:id>/', (views.update_agent), {},'update_agent'),#
    path('update_agent/<str:id>/', UpdateAgentView.as_view(), name='update_agent'),#
    
    path('delete_agent/<str:id>/', (views.delete_agent), {},name='delete_agent'),
    path('delete_client/<str:id>/', (views.delete_client), {},name='delete_client'),
    path('delete_diplome/<str:id>/', (views.delete_diplome), {},name='delete_diplome'),
    path('delete_equipe/<str:id>/', (views.delete_equipe), {},name='delete_equipe'),
    path('delete_mission/<str:id>/', (views.delete_mission), {},name='delete_mission'),
    path('delete_vacation_equipe/<str:id>/', (views.delete_vacation_equipe), {},name='delete_vacation_equipe'),
    path('delete_vacation_agent/<str:id>/', (views.delete_vacation_agent), {},name='delete_vacation_agent'),

    path('detail_vacation_equipe/<str:id>/', DetailVacationEquipeView.as_view(), name='detail_vacation_equipe'),#
    path('detail_vacation_agent/<str:id>/', DetailAgentView.as_view(), name='detail_vacation_agent'),#

    path('create_vacation_equipe', CreateVacationEquipeView.as_view(), name='create_vacation_equipe'),#
    path('update_vacation_equipe/<str:id>/', UpdateVacationEquipeView.as_view(), name='update_vacation_equipe'),#
    path('create_vacation_agent', CreateVacationAgentView.as_view(), name='create_vacation_agent'),#
    path('update_vacation_agent/<str:id>/', UpdateVacationAgentView.as_view(), name='update_vacation_agent'),#

    path('emails/reponse_vacation/<str:id>/', ReponseVacationView.as_view(), name='reponse_vacation'),#

    path('dashboard',(views.dashboard),name='dashboard')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
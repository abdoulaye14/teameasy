import django_filters

from .models import *

class SimpleAgentFilter(django_filters.FilterSet):
    class Meta:
        model = Agent
        fields = ['nom','code_postal','disponibilite',]

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = ['nom','code_postal']


class AgentFilter(django_filters.FilterSet):
    class Meta:
        model = Vacation_agent
        fields = ['client','date_debut','date_fin']

class EquipeFilter(django_filters.FilterSet):
    class Meta:
        model = Equipe
        fields = ['responsable_equipe','nom_equipe']

class MissionFilter(django_filters.FilterSet):
    class Meta:
        model = Mission
        fields = ['equipe','client']

class Vacation_AgentFilter(django_filters.FilterSet):
    class Meta:
        model = Vacation_agent
        fields = ['etat_mission','date_debut','date_fin']

class Vacation_EquipeFilter(django_filters.FilterSet):
    class Meta:
        model = Details_mission
        fields = ['mission','client','equipe','date_debut','date_fin']
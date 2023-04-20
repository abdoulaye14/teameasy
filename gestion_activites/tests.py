from django.test import TestCase, Client
from django.urls import reverse
from gestion_activites.models import Agent
from gestion_utilisateurs.models import *

class TestViews(TestCase):
    def test_list_agents(self):
        client = Client()
        response = client.get(reverse('agents'))
        self.assertEquals(response.status_code, 302)
        # self.assertTemplateUsed(response, 'gestion_activites/agents.html')

    # def test_list_agents(self):
    #     client = Client()
    #     response = client.get('gestion_utilisateurs/register.html')
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'gestion_utilisateurs/register.html')

    def test_home(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEquals(response.status_code, 302)
    
    def test_create_agent(self):
        client = Client()
        response = client.get(reverse('create_agent'))
        self.assertEquals(response.status_code, 302)
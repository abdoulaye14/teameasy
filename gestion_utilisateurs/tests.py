# from django.test import TestCase
# from django.urls import reverse
# from gestion_activites.models import *
# from gestion_utilisateurs.models import *
# from .forms import *
# # Create your tests here.
# class AuthorModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         Agent.objects.create(nom='Big', prenom='Bob')

#     def test_first_name_label(self):
#         agent = Agent.objects.get(id=1)
#         field_label = agent._meta.get_field('nom').verbose_name
#         self.assertEqual(field_label, 'nom')

#     def test_date_of_death_label(self):
#         agent = Agent.objects.get(id=1)
#         field_label = agent._meta.get_field('modified_at').verbose_name
#         self.assertEqual(field_label, 'modified at')

#     def test_first_name_max_length(self):
#         author = Agent.objects.get(id=1)
#         max_length = author._meta.get_field('nom').max_length
#         self.assertEqual(max_length, 50)

#     def test_object_name_is_last_name_comma_first_name(self):
#         agent = Agent.objects.get(id=1)
#         expected_object_name = f'{agent.prenom} {agent.nom}'
#         self.assertEqual(str(agent), expected_object_name)

# class AgentListViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 13 authors for pagination tests
#         number_of_authors = 13
#         societe = Societe.objects.create(
#             nom="Test"
#         )
#         User.objects.create(
#                 username=f'Dominique ',
#                 email=f'Surname@gmail.com',
#                 password=f'oktest',
#                 societe= societe
#         )
#         for author_id in range(number_of_authors):
#             Agent.objects.create(
#                 nom=f'Dominique {author_id}',
#                 mail=f'Surname{author_id}@gmail.com',
#                 prenom=f'oktest {author_id}',
#                 societe= societe
#             )
    
#     def test_view_url_exists_at_desired_location(self):
#         response = self.client.get('gestion_activites/agents')
#         self.assertEqual(response.status_code, 200)
    
#     def test_view_url_register(self):
#         societe = Societe.objects.get(id=1)
#         agent = Agent.objects.get(societe=societe, id=1)
#         role = 'role'
#         statut = 'statut'
#         permis = True
#         username = agent.prenom+' '+agent.nom
#         email = agent.mail
#         password = 'random_password(9)'

#         user = User.objects.get(id=1)
#         if permis and agent and email and password and societe:
#             print("2")
#             message = None
#             if role == 'responsable':
#                 print("CREATE RESPONSABLE USER")
#                 message = 'Responsable'
#                 user = User.objects.create_user(username, email, password, societe)
#                 user.responsable = True
#                 user.save()
            
#             elif role == 'staff':
#                 print("CREATE STAFF USER")
#                 message = 'Admin'
#                 user = User.objects.create_staffuser(username, email, password, societe)
                
#             else :
#                 print("CREATE SIMPLE USER")
#                 message = 'Utilisateur'
#                 user = User.objects.create_user(username, email, password, societe)
                
#             if statut == 'on':
#                 user.active = True
#                 user.save()
#             print(user)
#             agent.user = user
#             agent.save()
#     def test_view_url_updateUser(self):
#         societe = Societe.objects.get(id=1)
#         agent = Agent.objects.get(societe=societe, id=1)
#         role = 'role'
#         statut = 'statut'
#         permis = True
#         username = agent.prenom+' '+agent.nom
#         email = agent.mail
#         password = 'random_password(9)'
#         user = User.objects.get(id=1)
#         if role is not None or role != "":
#             if role == 'responsable':
#                 print("Update RESPONSABLE USER")
#                 user.responsable = True
                
            
#             elif role == 'staff':
#                 print("Update STAFF USER")
#                 user.staff = True
#             elif role == 'default':
#                 print("Update Default USER")
#                 user.staff = False
#                 user.responsable = False
#             if statut == 'on':
#                 user.active = True
#             if statut is None:
#                 print(statut)
#                 user.active = False
#             user.save()

#     def test_view_url_changepassword(self):
#         societe = Societe.objects.get(id=1)
#         agent = Agent.objects.get(societe=societe, id=1)
#         role = 'role'
#         statut = 'statut'
#         permis = True
#         username = agent.prenom+' '+agent.nom
#         email = agent.mail
#         password = 'random_password(9)'
#         password_2 = "random_password(9)"
#         user = User.objects.get(id=1)
#         user_verif = user
#         if user_verif is not None and user_verif == user:
#             if password is not None and password != password_2:
#                 print("Erreur")
#             else:
#                 print("Pas d'erreur")
#             user.set_password(password)
#             user.save()

# class MissionListViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 13 authors for pagination tests
#         number_of_authors = 13
#         societe = Societe.objects.create(
#             nom="Test"
#         )
#         User.objects.create(
#                 username=f'Dominique ',
#                 email=f'Surname@gmail.com',
#                 password=f'oktest',
#                 societe= societe
#         )
#         for author_id in range(number_of_authors):
#             Agent.objects.create(
#                 nom=f'Dominique {author_id}',
#                 mail=f'Surname{author_id}@gmail.com',
#                 prenom=f'oktest {author_id}',
#                 societe= societe
#             )
    
#     def test_view_url_exists_at_desired_location(self):
#         response = self.client.get('gestion_activites/agents')
#         self.assertEqual(response.status_code, 200)
    
#     def test_view_url_register(self):
#         societe = Societe.objects.get(id=1)
#         agent = Agent.objects.get(societe=societe, id=1)
#         role = 'role'
#         statut = 'statut'
#         permis = True
#         username = agent.prenom+' '+agent.nom
#         email = agent.mail
#         password = 'random_password(9)'

#         user = User.objects.get(id=1)
#         if permis and agent and email and password and societe:
#             print("2")
#             message = None
#             if role == 'responsable':
#                 print("CREATE RESPONSABLE USER")
#                 message = 'Responsable'
#                 user = User.objects.create_user(username, email, password, societe)
#                 user.responsable = True
#                 user.save()
            
#             elif role == 'staff':
#                 print("CREATE STAFF USER")
#                 message = 'Admin'
#                 user = User.objects.create_staffuser(username, email, password, societe)
                
#             else :
#                 print("CREATE SIMPLE USER")
#                 message = 'Utilisateur'
#                 user = User.objects.create_user(username, email, password, societe)
                
#             if statut == 'on':
#                 user.active = True
#                 user.save()
#             print(user)
#             agent.user = user
#             agent.save()
#     def test_view_url_updateUser(self):
#         societe = Societe.objects.get(id=1)
#         agent = Agent.objects.get(societe=societe, id=1)
#         role = 'role'
#         statut = 'statut'
#         permis = True
#         username = agent.prenom+' '+agent.nom
#         email = agent.mail
#         password = 'random_password(9)'
#         user = User.objects.get(id=1)
#         if role is not None or role != "":
#             if role == 'responsable':
#                 print("Update RESPONSABLE USER")
#                 user.responsable = True
                
            
#             elif role == 'staff':
#                 print("Update STAFF USER")
#                 user.staff = True
#             elif role == 'default':
#                 print("Update Default USER")
#                 user.staff = False
#                 user.responsable = False
#             if statut == 'on':
#                 user.active = True
#             if statut is None:
#                 print(statut)
#                 user.active = False
#             user.save()

#     def test_view_url_changepassword(self):
#         societe = Societe.objects.get(id=1)
#         agent = Agent.objects.get(societe=societe, id=1)
#         role = 'role'
#         statut = 'statut'
#         permis = True
#         username = agent.prenom+' '+agent.nom
#         email = agent.mail
#         password = 'random_password(9)'
#         password_2 = "random_password(9)"
#         user = User.objects.get(id=1)
#         user_verif = user
#         if user_verif is not None and user_verif == user:
#             if password is not None and password != password_2:
#                 print("Erreur")
#             else:
#                 print("Pas d'erreur")
#             user.set_password(password)
#             user.save()


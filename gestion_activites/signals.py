from django.dispatch import receiver
from datetime import date
from django.template.loader import render_to_string
from django.core.mail import send_mail
from gestion_utilisateurs.utils import Util
from django.db.models.signals import (
    pre_save,
    post_save
)
from .models import (
    Details_diplome,
    Vacation_agent,
    Details_mission,
    Mission
)


@receiver(pre_save, sender=Details_diplome)
def detail_mission_save(sender,instance,*args, **kwargs):
    today = date.today()
    if instance.date_expiration > instance.date_delivrance and instance.date_expiration > today:
        instance.validite = True

# @receiver(post_save, sender=Vacation_agent)
# def vacation_agent_save(sender,instance,created,*args,**kwargs):
#     print("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111 "+str(instance.id))
#     if created:
#         send_mail_vacation(instance)
#     elif instance.etat_mission == 'RF':
#         send_mail_statut_vacation(instance)
#     elif instance.etat_mission == 'AC':
#         send_mail_statut_vacation(instance)
        

# def create_new_vacation_agent(mission=None, agent=None, client=None, date_debut=None, date_fin=None, heure_debut=None, heure_fin=None):
    
#     new_vacation = Vacation_agent.objects.create(
#         mission = mission.id,
#         agent = agent.id,
#         client = client.id,
#         date_debut = date_debut,
#         date_fin = date_fin,
#         heure_debut = heure_debut,
#         heure_fin = heure_fin
#     )
#     new_vacation.save()

def send_mail_vacation(vacation):
    mission = None
    if vacation.mission !=None:
        mission = vacation.mission.mission

    html = render_to_string('gestion_activites/emails/confirmation_vacation.html',{
        'vacation':vacation,
        'mission':mission
        }
    )

    send_mail(
    'test envoie message',
    'Here is the message.',
    '',
    [vacation.agent.mail],
    fail_silently=False,
    html_message=html
    )

def send_mail_statut_vacation(vacation):
    html = render_to_string('gestion_activites/emails/statut_vacation.html',{
        'vacation':vacation
        }
    )

    send_mail(
    'test envoie message',
    'Here is the message.',
    '',
    [vacation.agent.mail],
    fail_silently=False,
    html_message=html
    )
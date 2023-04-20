import threading
from django.core.mail import EmailMessage
from gestion_activites.models import Vacation_agent

class ThreadVacationAgent(threading.Thread):
    def __init__(self,request, mission=None, agent=None, client=None, date_debut=None, date_fin=None, heure_debut=None, heure_fin=None, etat_mission='EA', comment=None, new=True, vacation=None):
        self.societe = request.user.societe
        self.mission = mission
        self.agent = agent
        self.client = client
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.etat_mission = etat_mission
        self.new = new
        self.vacation = vacation
        self.comment = comment
        threading.Thread.__init__(self)

    def run(self):
        if self.new :
            print("Nouvelle VACATION ")
            new_vacation = Vacation_agent.objects.create(
                societe = self.societe,
                mission = self.mission,
                agent = self.agent,
                client = self.client,
                date_debut = self.date_debut,
                date_fin = self.date_fin,
                heure_debut = self.heure_debut,
                heure_fin = self.heure_fin,
                etat_mission = self.etat_mission,
                comment = self.comment
            )
            new_vacation.save()
        else :
            print("Modification VACATION ")
            self.vacation.mission = self.mission
            self.vacation.agent = self.agent
            self.vacation.client = self.client
            self.vacation.date_debut = self.date_debut
            self.vacation.date_fin = self.date_fin
            self.vacation.heure_debut = self.heure_debut
            self.vacation.heure_fin = self.heure_fin
            self.vacation.etat_mission = self.etat_mission
            self.vacation.comment = self.comment
            self.vacation.save()

        #send_mail_vacation(new_vacation,self.mission.mission)

class ThreadVacationEquipe(threading.Thread):
    def __init__(self,societe, mission=None, equipe=None, client=None, date_debut=None, date_fin=None, heure_debut=None, heure_fin=None):
        self.societe = societe
        self.mission = mission
        self.equipe = equipe
        self.client = client
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        threading.Thread.__init__(self)

    def run(self):
        print("VACATION "+str(self.mission))
        for agent in self.equipe.agents.all():
            print("ThreadVacationEquipe")
            new_vacation = Vacation_agent.objects.create(
                societe = self.societe,
                mission = self.mission,
                agent = agent,
                client = self.client,
                date_debut = self.date_debut,
                date_fin = self.date_fin,
                heure_debut = self.heure_debut,
                heure_fin = self.heure_fin
            )
            new_vacation.save()
        #send_mail_vacation(new_vacation,self.mission.mission)

class ThreadUpdateVacationEquipe(threading.Thread):
    def __init__(self,detail_mission, request, delete=False):
        self.vacations = Vacation_agent.objects.filter(mission_id=detail_mission.id)
        self.detail_mission = detail_mission
        self.societe = request.user.societe
        self.delete = delete
        threading.Thread.__init__(self)

    def run(self):
        print("VACATION update detail")
        if self.delete == False:
            for vacation in self.vacations:
                vacation.client = self.detail_mission.client
                print("DEDANS")
                vacation.date_debut = self.detail_mission.date_debut
                vacation.date_fin = self.detail_mission.date_fin
                vacation.heure_debut = self.detail_mission.heure_debut
                vacation.heure_fin = self.detail_mission.heure_fin
                vacation.mission = self.detail_mission
                vacation.save()
        else:
            self.vacations.delete()
            print("Vacations agents supprimées")
            equipe = self.detail_mission.equipe
            for agent in equipe.agents.all():
                print("Vacation recreate")
                new_vacation = Vacation_agent.objects.create(
                    societe = self.societe,
                    mission = self.detail_mission,
                    agent = agent,
                    client = self.detail_mission.client,
                    date_debut = self.detail_mission.date_debut,
                    date_fin = self.detail_mission.date_fin,
                    heure_debut = self.detail_mission.heure_debut,
                    heure_fin = self.detail_mission.heure_fin
                )
                new_vacation.save()
        #send_mail_vacation(new_vacation,self.mission.mission)

class ThreadMail(threading.Thread):
    def __init__(self,subject,body,from_email,email,reply_to):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.email = email
        self.reply_to = reply_to
        threading.Thread.__init__(self)

    def run(self):
        email=EmailMessage(subject=self.subject, body=self.body, from_email=self.from_email,to=[self.email], reply_to=[self.reply_to])
        email.send()
from datetime import date, datetime, time, timedelta
from msilib.schema import ListView
from re import template
from time import sleep
import threading
import re
from django.contrib import messages
from django.core.mail import send_mail
from django.forms import formset_factory, inlineformset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template, render_to_string
from django.urls import resolve
from django.views import View
from django.views.generic import ListView, UpdateView
from gestion_utilisateurs.utils import Util
from .filters import *
from .forms import *
from gestion_utilisateurs.threads import *
import pandas as pd
from plotly.offline import plot
import plotly.express as px

from django.contrib.auth.decorators import login_required
#from .parametres_twilio import *

from random import randint
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.contrib.auth.mixins import LoginRequiredMixin
extend_de_base = 'gestion_activites/base.html'

global now, today, horaire
now = datetime.now()
today = date.today()
horaire= time(now.hour,now.minute)

class Diplomes(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'gestion_activites/diplomes.html'
    def get(self, request):
        user = request.user
        if user.staff:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                user = request.user
                societe = user.societe

                try:
                    if user.staff:
                        diplomes = Diplome.objects.filter(societe=societe)
                        data = json.loads(serialize('json', diplomes))
                    else:
                        data = {}
                except:
                    data = {}
                    print("Except")
                extend = extend_de_base
                return JsonResponse({'content-data': data}, safe=False)
            return render(request, 'gestion_activites/diplomes.html', {'user': user})
        else:
            extend = extend_de_base
            return render(request, 'gestion_utilisateurs/permissions.html', locals())

class Clients(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'gestion_activites/clients.html'
   
    def get(self, request):
        user = request.user
        if user.staff:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                user = request.user
                societe = user.societe

                try:
                    if user.staff:
                        clients = Client.objects.filter(societe=societe)
                        data = json.loads(serialize('json', clients))
                    else:
                        data = {}
                except:
                    data = {}
                    print("Except")
                extend = extend_de_base
                return JsonResponse({'content-data': data}, safe=False)
            return render(request, 'gestion_activites/clients.html', {'user': user})
        else:
            extend = extend_de_base
            return render(request, 'gestion_utilisateurs/permissions.html', locals())

class Agents(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'gestion_activites/agents.html'
    
    def get(self, request):
        user = request.user
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            societe = request.user.societe
            user = request.user
            try:
                if user.staff:
                    agents = Agent.objects.filter(societe=societe)
                elif user.responsable:
                    agent = Agent.objects.get(user_id=user.id)
                    equipes = Equipe.objects.filter(responsable_equipe_id=agent)
                    agents = Agent.objects.none()
                    for equipe in equipes.all():
                        agents |= equipe.agents.all() 
                else:
                    agents = Agent.objects.get(user_id=user.id) 
                data= json.loads(serialize('json', agents))
            except :
                agents = None  
                data= {}
            extend = extend_de_base
            return JsonResponse({'content-data': data}, safe=False)
        return render(request, 'gestion_activites/agents.html', {'user':user})

class Equipes(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'gestion_activites/equipes.html'

    def get(self, request):
        user = request.user
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            
            user = request.user
            societe = user.societe
            try:
                if user.staff:
                    equipes = Equipe.objects.filter(societe=societe)
                    responsables = {}
                    for equipe in equipes:
                        responsable = {}
                        responsable["id_responsable"] = equipe.responsable_equipe.id
                        responsable["nom"] = equipe.responsable_equipe.nom
                        responsable["prenom"] = equipe.responsable_equipe.prenom
                        responsable["ville"] = equipe.responsable_equipe.ville
                        responsable["code_postal"] = equipe.responsable_equipe.code_postal
                        responsable["telephone"] = equipe.responsable_equipe.telephone
                        responsable["photo"] = str(equipe.responsable_equipe.photo)
                        responsables[str(equipe.id)] = responsable
                    responsables_equipes = json.dumps(responsables)
                    responsables = json.loads(responsables_equipes)
                    data= json.loads(serialize('json', equipes))
                elif user.responsable:
                    agent = Agent.objects.get(user_id=user.id)
                    equipes = Equipe.objects.filter(societe=societe, responsable_equipe_id=agent.id)
                    responsables = {}
                    for equipe in equipes:
                        responsable = {}
                        responsable["id_responsable"] = equipe.responsable_equipe.id
                        responsable["nom"] = equipe.responsable_equipe.nom
                        responsable["prenom"] = equipe.responsable_equipe.prenom
                        responsable["ville"] = equipe.responsable_equipe.ville
                        responsable["code_postal"] = equipe.responsable_equipe.code_postal
                        responsable["telephone"] = equipe.responsable_equipe.telephone
                        responsable["photo"] = str(equipe.responsable_equipe.photo)
                        responsables[str(equipe.id)] = responsable
                    responsables_equipes = json.dumps(responsables)
                    responsables = json.loads(responsables_equipes)
                    data= json.loads(serialize('json', equipes))
                else :
                    data = {}
                    responsables = {}
            except :
                responsables = {}  
                data= {}
            extend = extend_de_base
            return JsonResponse({'content-data': data, 'responsables': responsables}, safe=False)
        return render(request, 'gestion_activites/equipes.html', {'user':user})

class VacacationsAgents(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'gestion_activites/vacations-agents.html'

    def get(self, request):
        user = request.user
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            #data = randint(1,10)
            user = request.user
            societe = user.societe
            
            # myFilterVacation_agent = Vacation_AgentFilter(request.GET, queryset=vacations)
            # vacations = myFilterVacation_agent.qs
            
            try :
                if user.staff:
                    vacations = Vacation_agent.objects.filter(societe=societe)
                    clients = {}
                    agents = {}
                    for vacation in vacations:
                        # responsables[str(equipe.id)] = equipe.responsable_equipe.__dict__
                        client = {}
                        agent = {}
                        if vacation.client:
                            client["nom"] = vacation.client.nom
                        else:
                            client["nom"] = None
                        if vacation.agent:
                            agent["nom"] = vacation.agent.nom
                            agent["photo"] = str(vacation.agent.photo)
                            agent["prenom"] = vacation.agent.prenom
                        else:
                            agent["nom"] = None
                            agent["photo"] = None
                            agent["prenom"] = None
                        clients[str(vacation.id)] = client
                        agents[str(vacation.id)] = agent
                    clients_vacations = json.dumps(clients)
                    clients = json.loads(clients_vacations)
                    agents_vacations = json.dumps(agents)
                    agents = json.loads(agents_vacations)
                    data= json.loads(serialize('json', vacations))
                elif user.responsable:
                    print("1")
                    agent = Agent.objects.get(user_id=user.id)
                    print("2", agent)
                    clients = {}
                    agents = {}
                    equipes = Equipe.objects.filter(responsable_equipe_id=agent)
                    vacations = Details_mission.objects.none()
                    vacations_agents = Vacation_agent.objects.filter(agent_id=agent)
                    for equipe in equipes.all():
                        print('4',equipe)
                        vacations |=Details_mission.objects.filter(societe=societe, equipe_id=equipe.id)
                    for vacation in vacations.all():
                        vacations_agents |= Vacation_agent.objects.filter(societe=societe, mission_id=vacation)
                    print("1", vacations_agents)
                    for vacation in vacations_agents:
                        # responsables[str(equipe.id)] = equipe.responsable_equipe.__dict__
                        client = {}
                        agent = {}
                        if vacation.client:
                            client["nom"] = vacation.client.nom
                        else:
                            client["nom"] = None
                        if vacation.agent:
                            agent["nom"] = vacation.agent.nom
                            agent["photo"] = str(vacation.agent.photo)
                            agent["prenom"] = vacation.agent.prenom
                        else:
                            agent["nom"] = None
                            agent["photo"] = None
                            agent["prenom"] = None
                
                        clients[str(vacation.id)] = client
                        agents[str(vacation.id)] = agent
                    print('2')
                    agents_vacations = json.dumps(agents)
                    agents = json.loads(agents_vacations)
                    data= json.loads(serialize('json', vacations_agents))
                else:
                    agent = Agent.objects.get(user_id=user.id)
                    vacations = Vacation_agent.objects.filter(societe=societe, agent_id=agent.id)
                    clients = {}
                    agents = {}
                    for vacation in vacations:
                        # responsables[str(equipe.id)] = equipe.responsable_equipe.__dict__
                        client = {}
                        agent = {}
                        if vacation.client:
                            client["nom"] = vacation.client.nom
                        else:
                            client["nom"] = None
                        if vacation.agent:
                            agent["nom"] = vacation.agent.nom
                            agent["photo"] = str(vacation.agent.photo)
                            agent["prenom"] = vacation.agent.prenom
                        else:
                            agent["nom"] = None
                            agent["photo"] = None
                            agent["prenom"] = None
                        clients[str(vacation.id)] = client
                        agents[str(vacation.id)] = agent
                    clients_vacations = json.dumps(clients)
                    clients = json.loads(clients_vacations)
                    agents_vacations = json.dumps(agents)
                    agents = json.loads(agents_vacations)
                    data= json.loads(serialize('json', vacations))
            except:
                data = {}
                clients = {}
                agents = {}
            extend = extend_de_base
            return JsonResponse({'content-data': data, 'clients': clients, 'agents':agents}, safe=False)
        return render(request, 'gestion_activites/vacations-agents.html', {'user':user})

class VacacationsEquipes(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'gestion_activites/vacations-equipes.html'

    def get(self, request):
        user = request.user
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            user = request.user
            societe = user.societe
            try :
                if user.staff:
                    vacations = Details_mission.objects.filter(societe=societe)
                    clients = {}
                    equipes = {}
                    for vacation in vacations:
                        # responsables[str(equipe.id)] = equipe.responsable_equipe.__dict__
                        client = {}
                        equipe = {}
                        if vacation.client:
                            client["nom"] = vacation.client.nom
                        else:
                            client["nom"] = None
                        if vacation.equipe:
                            equipe["nom"] = vacation.equipe.nom_equipe
                        else:
                            equipe["nom"] = None
                        clients[str(vacation.id)] = client
                        equipes[str(vacation.id)] = equipe
                    clients_vacations = json.dumps(clients)
                    clients = json.loads(clients_vacations)
                    equipes_vacations = json.dumps(equipes)
                    equipes = json.loads(equipes_vacations)
                    data= json.loads(serialize('json', vacations))
                elif user.responsable:
                    print("1")
                    agent = Agent.objects.get(user_id=user.id)
                    print("2", agent)
                    clients_dict = {}
                    equipes_dict = {}
                    equipes = Equipe.objects.filter(responsable_equipe_id=agent)

                    # vacations = Details_mission.objects.filter(societe=societe, equipe_id=2)
                    vacations = Details_mission.objects.none()
                    for equipe in equipes.all():
                        print('4',equipe)
                        vacations |=Details_mission.objects.filter(societe=societe, equipe_id=equipe.id)

                    print("5", vacations)
                    for vacation in vacations:
                        # responsables[str(equipe.id)] = equipe.responsable_equipe.__dict__
                        print('6', vacation)
                        client = {}
                        equipe = {}
                        if vacation.client:
                            client["nom"] = vacation.client.nom
                        else:
                            client["nom"] = None
                        if vacation.equipe:
                            equipe["nom"] = vacation.equipe.nom_equipe
                        else:
                            equipe["nom"] = None
                        clients_dict[str(vacation.id)] = client
                        equipes_dict[str(vacation.id)] = equipe
                    clients_vacations = json.dumps(clients_dict)
                    clients = json.loads(clients_vacations)
                    equipes_vacations = json.dumps(equipes_dict)
                    equipes = json.loads(equipes_vacations)
                    print('11')
                    data= json.loads(serialize('json', vacations))
                    print('12')
                else:
                    data = {}
                    clients = {}
                    equipes = {}
            except:
                print("EXCEPT")
                data= {}
                clients = {}
                equipes = {}
            extend = extend_de_base
            return JsonResponse({'content-data': data, 'clients': clients, 'equipes':equipes}, safe=False)
        return render(request, 'gestion_activites/vacations-equipes.html', {'user':user})

class Missions(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'gestion_activites/missions.html'

    def get(self, request):
        user = request.user
        if user.staff:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                user = request.user
                societe = user.societe
                try :
                    if user.staff:
                        missions = Mission.objects.filter(societe=societe)
                        clients = {}
                        for mission in missions:
                            client = {}
                            if mission.client:
                                client["nom"] = mission.client.nom
                            else:
                                client["nom"] = None
                            clients[str(mission.id)] = client
                        clients_missions = json.dumps(clients)
                        clients = json.loads(clients_missions)
                        data= json.loads(serialize('json', missions))
                    else:
                        data = {}
                        clients = {}
                except:
                    data = {}
                    clients = {}
                extend = extend_de_base
                return JsonResponse({'content-data': data, 'clients': clients}, safe=False)
            return render(request, 'gestion_activites/missions.html', {'user':user})
        else:
            extend = extend_de_base
            return render(request, 'gestion_utilisateurs/permissions.html', locals())
        

@login_required(login_url='login/')
def dashboard(request):
    user = request.user
    if user.staff:
        societe = user.societe
        now = datetime.now()
        today = date.today()
        horaire= time(now.hour,now.minute)
        a_venir,en_cours,termine = statut_mission(societe)
        clients = Client.objects.filter(societe_id=societe)[:10]
        vacations = Vacation_agent.objects.filter(societe_id=societe,mission_id=None).order_by('-date_debut')[:10]
        vacations_all = Vacation_agent.objects.filter(societe_id=societe)
        a_venirVac,en_coursVac,termineVac = statut_vacations(vacations_all)
        missions = Mission.objects.filter(societe_id=societe).order_by('-date_debut')[:10]
        #details_mission = [n if Details_mission.objects.filter(constitution_equipe=0, mission_id=id).count() 
        stat_equipe = stat(missions)
        print(stat_equipe)
        extend = extend_de_base
        return render(request, 'gestion_activites/dashboard.html', locals())#{'extend': extend}) 
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())#{'extend': extend}) 

def stat(missions):
    n =[]
    for mission in missions :
        n.append(Details_mission.objects.filter(constitution_equipe=1, mission_id=mission.id).count())
    return n

############# Class Create View #########################################

class CreateAgentView(View):
    form_class = AgentForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.staff:
            form = self.form_class()
            current_url = resolve(request.path_info).url_name
            template = 'gestion_activites/create_agent.html'
            extend = extend_de_base
            return render(request, template, locals())
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.staff:
            form = AgentForm(request.POST,request.FILES)
            print(form.is_valid())
            if form.is_valid():
                form.save(request)
                messages.success(request, 'Un nouvel agent a été ajouté')
                return redirect(reverse('agents'))
            messages.error(request, 'Agent non enregistré, saisie erronée, Soucis technique')
            current_url = resolve(request.path_info).url_name
            template = 'gestion_activites/create_agent.html'
            extend = extend_de_base
            return render(request, template, locals())
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

@login_required(login_url='gestion_activites/login/')
def update_diplome(request,id):
    if request.user.staff:
        try:
            societe = request.user.societe
            diplome = Diplome.objects.get(id=id)
            current_url = resolve(request.path_info).url_name
            if request.method == 'POST':
                form = DiplomeForm(request.POST, instance = diplome)
                if form.is_valid():
                    form.save(request)
                    messages.success(request, 'Modifications enregistrées')
                    return redirect("diplomes")
            form = DiplomeForm(instance=diplome)
            current_url = resolve(request.path_info).url_name
            extend = extend_de_base
            template = 'gestion_activites/create_diplome.html'
            return render(request, template, locals())
        except Diplome.DoesNotExist:
            messages.error(request, 'action non autorisé, veuillez créer un nouveau diplôme')
        except Exception as e:
            messages.error(request, 'diplome non enregistré, saisie erronée '+str(e))
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals()) 
        


class UpdateAgentView(View):
    form_class = AgentForm

    def get(self, request, id):
        user = request.user
        agent = Agent.objects.get(id=id)
        if user.staff or agent.user == user.id:
            form = self.form_class(instance=agent)
            current_url = resolve(request.path_info).url_name
            extend = extend_de_base
            template = 'gestion_activites/create_agent.html'
            return render(request, template, locals())

        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())
    
    def post(self, request, id):
        user = request.user
        agent = Agent.objects.get(id=id)
        if user.staff or agent.user == user.id:
            form = self.form_class(request.POST,request.FILES,instance = agent)

            if form.is_valid():
                #photo = request.FILES["photo"]
                form.save(request)
                messages.success(request, 'Modifications enregistrées')
                return redirect(reverse('profile_agent',args=[agent.id]))
            messages.error(request, 'Agent non enregistré, saisie erronée')
            current_url = resolve(request.path_info).url_name
            extend = extend_de_base
            template = 'gestion_activites/create_agent.html'
            return render(request, template, locals())
        
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())
    
class DetailAgentView(View):
    def get(self, request, id):
        user = request.user
        societe = user.societe
        vacation = Vacation_agent.objects.get(id=id)
        current_agent = None
        try:
            current_agent = Agent.objects.get(user_id=user)
            responsable = vacation.mission.equipe.responsable_equipe
        except:
            responsable = None

        if user.staff or responsable == current_agent or vacation.agent == current_agent:
            vacations_all = Vacation_agent.objects.filter(societe=societe,agent_id=vacation.agent)
            try:
                equipe = vacation.mission.equipe.responsable_equipe
            except:
                equipe = None
            duree_restante = Util.duree_restante(vacation)
            jours_restants = duree_restante[0]
            heures_restantes = duree_restante[1]*jours_restants
            minutes_restantes = duree_restante[2]

            duree_ecoulee = Util.duree_reelle_ecoulee(vacation)
            jours_ecoules = duree_ecoulee[0]
            heures_ecoulees = duree_ecoulee[1]*jours_ecoules
            minutes_ecoulees = duree_ecoulee[2]
            
            duree_totale = Util.duree_totale(vacation)
            jours_totaux = duree_totale[0]
            heures_totales = duree_totale[1]*jours_totaux
            minutes_totales = duree_totale[2]

            template = 'gestion_activites/detail_vacation_agent.html'
            extend = extend_de_base
            return render(request, template, locals())
        template_name = 'gestion_utilisateurs/permissions.html'
        return render(request, template_name)

    def post(self, request, id):
        # try:
        societe = request.user.societe
        comment = request.POST.get('comment')
        vacation = Vacation_agent.objects.get(id=id)
        if comment != vacation.comment :
            vacation.comment = comment
            vacation.save()
        
        return redirect("detail_vacation_agent", id)


class ReponseVacationView(View):
    form_class = ReponseVacationForm

    def get(self, request, id):
        form = self.form_class
        vacation = Vacation_agent.objects.get(id=id)
        if vacation.client:
            client = vacation.client
        else:
            client = None

        current_url = resolve(request.path_info).url_name
        extend = extend_de_base
        template =  'gestion_activites/emails/reponse_vacation.html'
        return render(request, template, locals())
    
    def post(self, request, id):
        vacation = Vacation_agent.objects.get(id=id)
        form = self.form_class(request.POST)

        if form.is_valid():
            vacation.etat_mission = form.cleaned_data['etat_mission']
            vacation.save()
            try:
                if vacation.mission == None:
                    detail_mission = None
                else :
                    detail_mission = vacation.mission
                accepte,en_attente,refus = update_etat_detail_mission(detail_mission)
                Util.send_mail_statut_vacation(request,vacation.agent,detail_mission.nom,accepte,refus,en_attente)
                if refus != 0 or en_attente == 0 :
                    accepte,en_attente,refus = update_etat_detail_mission(detail_mission)
                    
                    # send_mail_statut_vacation(vacation)
                    # Util.send_mail_statut_vacation(request,vacation.agent,detail_mission.nom,accepte,refus,en_attente)
            except Exception as e:
                print("Exception Validation en cours !"+str(e))
            return redirect(reverse('missions'))

        current_url = resolve(request.path_info).url_name
        extend = extend_de_base 
        template = 'gestion_activites/emails/reponse_vacation.html' #get_template('emails/reponse_vacation.html')
        return render(request, template, {'form': form, 'extend': extend, 'current_url': current_url})


class AddDiplomeAgentView(View):
    try:
        DiplomeformSet = inlineformset_factory(Agent, Details_diplome, form=DiplomeDetailForm, exclude=('validite',), extra = Diplome.objects.all().count(), max_num = Diplome.objects.all().count())
    except:
        print("Table diplome vide")
        
    def get(self, request, id):
        agent = Agent.objects.get(id=id)
        DiplomeformSet = inlineformset_factory(Agent, Details_diplome, form=DiplomeDetailForm, exclude=('validite',), extra = Diplome.objects.all().count(), max_num = Diplome.objects.all().count())
        formset = DiplomeformSet(instance=agent)
        template = 'gestion_activites/add_diplome_agent.html'
        extend = extend_de_base
        return render(request, template, locals())

    def post(self, request, id):
        agent = Agent.objects.get(id=id)
        DiplomeformSet = inlineformset_factory(Agent, Details_diplome, form=DiplomeDetailForm, exclude=('validite',), extra = Diplome.objects.all().count(), max_num = Diplome.objects.all().count())
        form = DiplomeformSet(request.POST, instance=agent)

        if form.is_valid():
            form.save(request)
            return redirect(reverse('agents'))
        template = 'gestion_activites/add_diplome_agent.html'
        extend = extend_de_base
        return render(request, template, locals())

def AddDiplomeAgent(request, id):
    DiplomeformSet = inlineformset_factory(Agent, Details_diplome, form=DiplomeDetailForm, exclude=('validite',), extra = Diplome.objects.all().count(), max_num = Diplome.objects.all().count())
    agent = Agent.objects.get(id=id)
    formset = DiplomeformSet(instance=agent)
    #print(formset)
    if request.method == 'POST':
        form = DiplomeformSet(request.POST, instance=agent)
        
        print(form)
        if form.is_valid():
            form.save(request)
            return redirect(reverse('agents'))
    template = 'gestion_activites/add_diplome_agent.html'
    extend = extend_de_base
    return render(request, template, locals())

def delete_diplome(request, id):
    if request.user.staff:
        try:
            obj = Diplome.objects.get(id=id)
            url_path = "profile_agent"
            if request.method == 'POST':
                print("---------------------- Post DELETE --------------------------")
                obj.delete()
                messages.success(request, 'Diplome supprimé: '+str(obj))
                return redirect(reverse('diplomes'))
                
            else :
                form = DiplomeForm(instance=obj)
        except Exception as e :
            messages.warning(request, f'Ce diplome ne peut être supprimée: Error {e}')
            print(str(e))
        template = 'gestion_activites/delete.html'
        extend = extend_de_base
        return render(request,template,locals())
    else:
        extend = extend_de_base
        template_name = 'gestion_utilisateurs/permissions.html'
        return render(request, template_name)

def delete_agent(request, id):
    if request.user.staff:
        try:
            obj = Agent.objects.get(id=id)
            url_path = "profile_agent"
            if request.method == 'POST':
                print("---------------------- Post DELETE --------------------------")
                obj.delete()
                messages.success(request, 'Agent supprimé: '+str(obj))
                return redirect(reverse('agents'))
                
            else :
                form = AgentForm(instance=obj)
        except Exception as e :
            messages.warning(request, f'Cet agent ne peut être supprimée: Error {e}')
            print(str(e))
        template = 'gestion_activites/delete.html'
        extend = extend_de_base
        return render(request,template,locals())
    else:
        extend = extend_de_base
        template_name = 'gestion_utilisateurs/permissions.html'
        return render(request, template_name)


def create_equipe(request):
    current_url = resolve(request.path_info).url_name
    user = request.user
    societe = user.societe
    if user.staff:
        if request.method == 'POST':

            agents = request.POST.get('native-select-agents')
            agents = re.sub("[\"\']",'',agents)
            agents = agents.replace('[','')
            agents = agents.replace(']','').split(",")
            print(agents)
            
            # form = EquipeForm(request.POST)
            nom_equipe = request.POST.get('nom_equipe')
            responsable_equipe = request.POST.get('native-select-responsable')

            if nom_equipe and responsable_equipe and agents :
                
                new_equipe = Equipe.objects.create(
                    nom_equipe = nom_equipe,
                    responsable_equipe = Agent.objects.get(id=int(responsable_equipe)),
                    societe = societe
                )
                new_equipe.agents.add(responsable_equipe)
                #update_membership_photo(new_equipe,responsable_equipe,responsable_equipe.photo)
                for x in agents:
                    if int(x) == responsable_equipe :
                        pass
                    else :
                        new_equipe.agents.add(Agent.objects.get(id=int(x)))
                    #update_membership_photo(new_equipe,Agent.objects.get(id=x),Agent.objects.get(id=x).photo)
                new_equipe.save()   
                
                return redirect(reverse('equipes'))

        template = 'gestion_activites/create_equipe.html'
        agents = Agent.objects.filter(societe=request.user.societe)
        extend = extend_de_base
        return render(request, template, locals())
    
    extend = extend_de_base
    return render(request, 'gestion_utilisateurs/permissions.html', locals())

def update_equipe(request, id):
    if request.user.staff:
        try:
            equipe = Equipe.objects.get(id=id)
            societe = request.user.societe
            current_url = resolve(request.path_info).url_name
            if request.method == 'POST':
                #form = EquipeForm(request.POST, instance = equipe)
                agents = request.POST.get('native-select-agents')
                agents = re.sub("[\"\']",'',agents)
                agents = agents.replace('[','')
                agents = agents.replace(']','').split(",")
                print(agents)
                
                # form = EquipeForm(request.POST)
                nom_equipe = request.POST.get('nom_equipe')
                responsable_equipe = request.POST.get('native-select-responsable')
                if nom_equipe and responsable_equipe and nom_equipe:
                    equipe.delete()

                    new_equipe = Equipe.objects.create(
                        nom_equipe = nom_equipe,
                        responsable_equipe = Agent.objects.get(id=int(responsable_equipe)),
                        societe = societe
                    )
                    new_equipe.agents.add(responsable_equipe)
                    #update_membership_photo(new_equipe,responsable_equipe,responsable_equipe.photo)
                    for x in agents:
                        if int(x) == responsable_equipe :
                            pass
                        else :
                            new_equipe.agents.add(Agent.objects.get(id=int(x)))
                        #update_membership_photo(new_equipe,Agent.objects.get(id=x),Agent.objects.get(id=x).photo)
                    new_equipe.save()
                    messages.success(request, 'Données équipes mises à jour')
                    return redirect(reverse('equipes'))
            nom_equipe = equipe.nom_equipe
            responsable_equipe = equipe.responsable_equipe
            agents_selected = Membership.objects.filter(equipe_id=equipe.id).values_list('agent_id', flat=True)
            agents = Agent.objects.filter(societe=request.user.societe)
            template = 'gestion_activites/create_equipe.html'
            extend = extend_de_base
            return render(request,template,locals())
        except Equipe.DoesNotExist as e:
            messages.error(request, 'Saisie non enregistrée, Cette équipe n\'existe plus')
        except Exception as e:
            messages.error(request, 'Erreur inattendue '+str(e))
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

def delete_equipe(request, id):
    if request.user.staff:
        try:
            obj = Equipe.objects.get(id=id)
            url_path = "profile_equipe"
            if request.method == 'POST':
                print("---------------------- Post DELETE --------------------------")
                obj.delete()
                messages.success(request, 'Equipe supprimée '+str(obj))
                return redirect(reverse('equipes'))
                
            else :
                form = EquipeForm(instance=obj)
        except Exception as e :
            messages.warning(request, f'Cette équipe ne peut être supprimée: Error {e}')
            print(str(e))

        template = 'gestion_activites/delete.html'
        extend = extend_de_base
        return render(request,template,locals())
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())


class ClientView(View):
    form_class = ClientForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.staff:
            form = self.form_class()
            template = 'gestion_activites/create_client.html'
            extend = extend_de_base
            current_url = resolve(request.path_info).url_name
            return render(request, template, locals())
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.staff:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save(request)
                messages.success(request, 'Client créé avec succès')
            return  redirect(reverse('clients'))
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

def delete_client(request, id):
    if request.user.staff:
        try :
            obj = Client.objects.get(id=id)
            url_path = "profile_client"
            if request.method == 'POST':
                print("---------------------- Post DELETE --------------------------")
                obj.delete()
                messages.success(request, 'Client supprimé '+str(obj))
                return redirect(reverse('clients'))
                
            else :
                form = ClientForm(instance=obj)
        except Exception as e :
            messages.warning(request, f'Ce client ne peut être supprimé: Error {e}')
            return redirect(reverse('clients'))
        template = 'gestion_activites/delete.html'
        extend = extend_de_base
        return render(request,template,locals())
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

        
def create_new_vacation_agent(mission=None, agent=None, client=None, date_debut=None, date_fin=None, heure_debut=None, heure_fin=None):
    
    new_vacation = Vacation_agent.objects.create(
        mission = mission,
        agent = agent,
        client = client,
        date_debut = date_debut,
        date_fin = date_fin,
        heure_debut = heure_debut,
        heure_fin = heure_fin
    )
    new_vacation.save()
    #send_mail_vacation(new_vacation,mission.mission)


def create_new_vacation_equipe(societe,mission, equipe, client, date_debut, date_fin, heure_debut, heure_fin):
    try:
        vacations = Details_mission.objects.filter(mission_id=mission)
        for vacation in vacations:
            print("Detail mission")
            equipe = vacation.equipe
            ThreadVacationEquipe(societe, mission, equipe, client, date_debut, date_fin, heure_debut, heure_fin).start()
    except Exception as  e :
        print("---------------- Erreur de saisie -------------- id mission "+str(mission)+ " " + str(e))


def update_etat_detail_mission(detail_mission):
    mission = detail_mission.mission
    
    
    date_debut = detail_mission.date_debut
    heure_debut = detail_mission.heure_debut

    refus = 0
    en_attente = 0
    accepte = 0
    if detail_mission.client:
        client = detail_mission.client
    else:
        client = None
    if detail_mission.equipe:
        equipe = detail_mission.equipe
        for agent in equipe.agents.all():
            try :
                etat_vacation = Vacation_agent.objects.get(agent_id=agent.id,client_id=client.id,date_debut=date_debut,heure_debut=heure_debut,mission_id=detail_mission.id).etat_mission
                print(Vacation_agent.objects.get(agent_id=agent.id,client_id=client.id,date_debut=date_debut,heure_debut=heure_debut))
                if etat_vacation == "RF":
                    refus += 1 
                    print("refus")
                elif etat_vacation == "EA":
                    en_attente += 1
                    print("en_attente")
                elif etat_vacation == "AC":
                    accepte += 1
                    print("accepte")
            except Exception as e:
                print("except update_etat_detail "+str(e))
                # accepte = 0
                # en_attente = 0
                # refus = 0
    else:
        equipe = None

    if refus == 0 and en_attente == 0 and accepte != 0:
        detail_mission.constitution_equipe = True
        detail_mission.save()

    return accepte,en_attente,refus
    
def update_etat_mission(mission):

    try:
        detail_missions = Details_mission.objects.filter(mission_id=mission)
    except:
        print("-------------- Erreur DetailMission non trouvé ---------------")
    accepte = 0
    en_attente = 0
    refus=0
    for detail_mission in detail_missions :
        accepte_current = 0
        en_attente_current = 0
        refus_current = 0
        accepte_current,en_attente_current,refus_current=update_etat_detail_mission(detail_mission)
        accepte += accepte_current
        en_attente += en_attente_current
        refus += refus_current
    
    return accepte,en_attente,refus


def statut_detail_mission(mission,today, horaire):

    termine = 0
    en_cours = 0
    a_venir = 0

    if mission.date_debut > today:
        a_venir += 1
    elif mission.date_fin >= mission.date_debut and mission.date_fin >= today and today >= mission.date_debut:
        if today == mission.date_fin and horaire >= mission.heure_fin:
            termine += 1
        elif today == mission.date_debut and mission.heure_debut >= horaire:
            a_venir +=1
        else:
            en_cours += 1
    elif today >= mission.date_fin:
        termine += 1
    
    return a_venir,en_cours,termine



def statut_mission(societe):
    
    try:
        missions = Mission.objects.filter(societe_id=societe)
    except:
        a_venir = 0
        en_cours = 0
        termine = 0
    a_venir = 0
    en_cours = 0
    termine = 0

    for mission in missions:
        avenir_current = 0
        en_cours_current = 0
        termine_current = 0
        avenir_current,en_cours_current,termine_current = statut_detail_mission(mission, today, horaire)
        a_venir += avenir_current
        en_cours += en_cours_current
        termine += termine_current
    
    return a_venir,en_cours,termine

def statut_vacations(vacations):

    a_venir = 0
    en_cours = 0
    termine = 0
    a_venir = 0
    en_cours = 0
    termine = 0

    for mission in vacations:
        avenir_current = 0
        en_cours_current = 0
        termine_current = 0
        avenir_current,en_cours_current,termine_current = statut_detail_mission(mission, today, horaire)
        a_venir += avenir_current
        en_cours += en_cours_current
        termine += termine_current
    
    return a_venir,en_cours,termine

class CreateMission(View):
    form_class = MissionForm

    def get(self, request):
        user = request.user
        if user.staff:
            societe = user.societe
            equipes = Equipe.objects.filter(societe=societe )
            clients = Client.objects.filter(societe=societe)
            form = self.form_class()
            current_url = resolve(request.path_info).url_name
            template = 'gestion_activites/create_mission.html'
            extend = extend_de_base
            return render(request, template, locals())
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

    def post(self, request):
        user = request.user
        if user.staff:
            form = self.form_class(request.POST)

            equipes = request.POST.get('native-select-equipes')
            equipes = re.sub("[\"\']",'',equipes)
            equipes = equipes.replace('[','')
            equipes = equipes.replace(']','').split(",")

            client = request.POST.get('native-select-client')

            if form.is_valid():

                date_debut = form.cleaned_data['date_debut']
                date_fin = form.cleaned_data['date_fin']
                heure_debut = form.cleaned_data['heure_debut']
                heure_fin = form.cleaned_data['heure_fin']
                criteres = form.cleaned_data['criteres']
                nature_mission = form.cleaned_data['nature_mission']
                nom = form.cleaned_data['nom']
                site = form.cleaned_data['site']
                societe = request.user.societe
                client = Client.objects.get(id =int(client))
                
                new_mission = Mission.objects.create(
                    societe = societe,
                    client = client,
                    date_debut = date_debut,
                    date_fin = date_fin,
                    heure_debut = heure_debut,
                    heure_fin = heure_fin,
                    criteres = criteres,
                    nature_mission = nature_mission,
                    nom = nom,
                    site = site
                )

                new_mission.save() 
                for x in equipes: 
                    try:
                        equipe = Equipe.objects.get(id=int(x))
                        new_mission.equipe.add(equipe)
                        vacation = Details_mission.objects.get(mission_id=new_mission, equipe_id=x)
                        vacation.nom = nom
                        vacation.societe = societe
                        vacation.client = client
                        vacation.date_debut = date_debut
                        vacation.date_fin = date_fin 
                        vacation.heure_debut = heure_debut
                        vacation.heure_fin = heure_fin
                        # create_new_vacation_equipe(societe,new_mission.id, Equipe.objects.get(id=x), client, date_debut, date_fin, heure_debut, heure_fin)
                        ThreadVacationEquipe(societe, vacation, equipe, client, date_debut, date_fin, heure_debut, heure_fin).start()
                        vacation.save()
                    except:
                        print("PROBLEME LECTURE ThreadVacationEquipe")

                return redirect(reverse('missions'))
        
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

class UpdateMissionView(View):
    form_class = MissionForm
    def get(self, request, id):
        user = request.user
        if user.staff:
            try:
                societe = user.societe
                vacation = Mission.objects.get(id=id)
                equipes = Equipe.objects.filter(societe=societe)
                clients = Client.objects.filter(societe=societe)
                if vacation.client:
                    client_selected = Client.objects.get(id=vacation.client_id)
                else:
                    client_selected = None
                if equipes_selected:
                    equipes_selected = Details_mission.objects.filter(societe=societe,mission_id=vacation.id).values_list('equipe_id', flat=True)
                else:
                    equipes_selected = None
                form = self.form_class(instance=vacation)
                current_url = resolve(request.path_info).url_name
                template = 'gestion_activites/create_mission.html'
                extend = extend_de_base
                return render(request, template, locals())
            except Mission.DoesNotExist as e:
                messages.error(request, 'Saisie non enregistrée, la mission séléctionnée n\'existe plus')
            except Equipe.DoesNotExist:
                messages.error(request, 'Saisie non enregistrée, l\'équipe sélectionnée n\'existe plus')
            except Client.DoesNotExist:
                messages.error(request, 'Saisie non enregistrée, le client sélectionnée n\'existe plus')
            except Exception as e:
                messages.error(request, 'Saisie non enregistrée, erreur inattendue '+str(e))
        else:
            extend = extend_de_base
            return render(request, 'gestion_utilisateurs/permissions.html', locals())

    def post(self, request, id):
        if request.user.staff:
            try:
                mission = Mission.objects.get(id=id)
                equipes = request.POST.get('native-select-equipes')
                equipes = re.sub("[\"\']",'',equipes)
                equipes = equipes.replace('[','')
                equipes = equipes.replace(']','').split(",")
                print(equipes)

                client = request.POST.get('native-select-client')
                form = self.form_class(request.POST, instance = mission)
                if form.is_valid():
                    
                    date_debut = form.cleaned_data['date_debut']
                    date_fin = form.cleaned_data['date_fin']
                    heure_debut = form.cleaned_data['heure_debut']
                    heure_fin = form.cleaned_data['heure_fin']
                    criteres = form.cleaned_data['criteres']
                    nature_mission = form.cleaned_data['nature_mission']
                    nom = form.cleaned_data['nom']
                    site = form.cleaned_data['site']
                    if client:
                        client = Client.objects.get(id =int(client))
                    else:
                        client = None
                    societe = request.user.societe

                    #new_mission = Mission.objects.create(
                    new_mission = Mission.objects.create(
                        societe = societe,
                        client = client,
                        date_debut = date_debut,
                        date_fin = date_fin,
                        heure_debut = heure_debut,
                        heure_fin = heure_fin,
                        criteres = criteres,
                        nature_mission = nature_mission,
                        nom = nom,
                        site = site
                    )
                    new_mission.save()
                    try:
                        for x in equipes:
                            equipe = Equipe.objects.get(id=int(x))
                            new_mission.equipe.add(equipe)
                            vacation = Details_mission.objects.get(mission_id=new_mission, equipe_id=int(x))
                            vacation.nom = nom
                            vacation.societe = societe
                            vacation.client = client
                            vacation.date_debut = date_debut
                            vacation.date_fin = date_fin 
                            vacation.heure_debut = heure_debut
                            vacation.heure_fin = heure_fin
                            vacation.mission = new_mission
                        
                            # create_new_vacation_equipe(societe,new_mission.id, Equipe.objects.get(id=x), client, date_debut, date_fin, heure_debut, heure_fin)
                            
                            print("equipe changed")
                            ThreadUpdateVacationEquipe(vacation, request, True).start()
                            print("equipe is changing")
                            vacation.save()
                        mission.delete()
                        return redirect(reverse('missions'))
                    except Equipe.DoesNotExist as e:
                        messages.error(request, 'Saisie non enregistrée, l\'équipe séléctionnée n\'existe plus')
                    except Exception as e:
                        print("PROBLEME LECTURE ThreadVacationEquipe "+str(e))
            except Mission.DoesNotExist as e:
                messages.error(request, 'Saisie non enregistrée, la mission séléctionnée n\'existe plus')
            except Client.DoesNotExist as e:
                messages.error(request, 'Saisie non enregistrée, le client séléctionné n\'existe plus')
            except Exception as e:
                messages.error(request, 'Saisie non enregistrée, Veuillez réessayer '+str(e))

            current_url = resolve(request.path_info).url_name
            template = 'gestion_activites/create_mission.html'
            extend = extend_de_base
            return render(request, template, locals())
        else:
            extend = extend_de_base
            return render(request, 'gestion_utilisateurs/permissions.html', locals())


class CreateVacationEquipeView(View):
    form_class = VacationEquipeForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.staff:
            societe = user.societe
            clients = Client.objects.filter(societe=societe)
            equipes = Equipe.objects.filter(societe=societe)
            missions = Mission.objects.filter(societe=societe)
            form = self.form_class()
            current_url = resolve(request.path_info).url_name
            template = 'gestion_activites/create_vacation_equipe.html'
            extend = extend_de_base
            return render(request, template, locals())
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.staff:
            try:
                form = self.form_class(request.POST)
                client = request.POST.get('native-select-client')
                equipe = request.POST.get('native-select-equipe')
                mission = request.POST.get('native-select-mission')
                if form.is_valid():
                    #form.save(request)
                    nom = form.cleaned_data.get('nom')
                    comment = form.cleaned_data.get('comment')
                    incident = form.cleaned_data.get('incident')
                    date_debut = form.cleaned_data.get('date_debut')
                    date_fin = form.cleaned_data.get('date_fin')
                    print("DATE FIN "+str(date_fin))
                    heure_debut = form.cleaned_data.get('heure_debut')
                    heure_fin = form.cleaned_data.get('heure_fin')
                    societe = request.user.societe
                    if equipe:
                        equipe = Equipe.objects.get(id=(equipe))
                    else:
                        equipe = None
                    if client:
                        client = Client.objects.get(id=int(client))
                    else:
                        client = None

                    vacation = Details_mission.objects.create(
                        societe = societe,
                        nom = nom,
                        client = client,
                        date_debut = date_debut,
                        date_fin = date_fin,
                        heure_debut = heure_debut,
                        heure_fin = heure_fin,
                        equipe = equipe,
                        incident = incident,
                        comment = comment
                        #mission = mission
                    )
                    if mission != None :
                        vacation.mission = Mission.objects.get(id=int(mission))
                    vacation.save()

                    ThreadVacationEquipe(societe,vacation, equipe, client, date_debut, date_fin, heure_debut, heure_fin).start()
                    return redirect('vacations-equipes')     
            except Exception as e:
                messages.error(request, 'Saisie non enregistrée, veuillez réessayer '+str(e)) 
            current_url = resolve(request.path_info).url_name
            template = 'gestion_activites/create_vacation_equipe.html'
            extend = extend_de_base
            return render(request, template, {'form': form, 'extend': extend, 'current_url': current_url})
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

class UpdateVacationEquipeView(View):
    form_class = VacationEquipeForm

    def get(self, request, id):
        if request.user.staff or request.user.responsable:
            societe = request.user.societe
            vacation = Details_mission.objects.get(id=id)
            clients = Client.objects.filter(societe=societe)
            equipes = Equipe.objects.filter(societe=societe)
            missions = Mission.objects.filter(societe=societe)
            if vacation.client:
                client_selected = Client.objects.get(id=vacation.client_id)
            else:
                client_selected = None
            if vacation.equipe:
                equipe_selected = Equipe.objects.get(societe=societe,id=vacation.equipe_id)
            else:
                equipe_selected = None
            if vacation.mission:
                mission_selected = Mission.objects.get(id=vacation.mission_id)
            else:
                mission_selected = None
            form = self.form_class(instance=vacation)
            current_url = resolve(request.path_info).url_name
            extend = extend_de_base
            template = 'gestion_activites/create_vacation_equipe.html'
            return render(request, template, locals())
        else:
            extend = extend_de_base
            return render(request, 'gestion_utilisateurs/permissions.html', locals())
    
    def post(self, request, id):
        user = request.user
        if user.staff or user.responsable:
            vacation = Details_mission.objects.get(id=id)
            nom_vac = vacation.nom
            form = self.form_class(request.POST, instance = vacation)
            if request.user.staff:
                client = request.POST.get('native-select-client')
                equipe = request.POST.get('native-select-equipe')
                mission = request.POST.get('native-select-mission')
            else :
                if vacation.client:
                    client = vacation.client_id
                else:
                    client = None
                if vacation.equipe:
                    equipe = vacation.equipe_id
                else:
                    equipe = None
                if vacation.mission:
                    mission = vacation.mission_id
                else:
                    mission = None

            if form.is_valid():
                #form.save(request)
                if request.user.staff:
                    nom = form.cleaned_data.get('nom')
                else:
                    vacation.nom = nom_vac
                print("nom vacation")
                print(nom_vac)
                date_debut = form.cleaned_data.get('date_debut')
                date_fin = form.cleaned_data.get('date_fin')
                print("DATE FIN "+str(date_fin))
                heure_debut = form.cleaned_data.get('heure_debut')
                heure_fin = form.cleaned_data.get('heure_fin')
                societe = request.user.societe
                if equipe:
                    equipe = Equipe.objects.get(id=(equipe))
                if client:
                    client = Client.objects.get(id=int(client))
                detail_mission = vacation
                if mission:
                    mission = Mission.objects.get(id=int(mission))

                vacation.date_debut = date_debut
                vacation.date_fin = date_fin
                vacation.heure_debut = heure_debut
                vacation.heure_fin = heure_fin
                vacation.client = client
                vacation.mission = mission
                print("Equipe id "+str(vacation.equipe_id))
                if vacation.equipe_id != equipe.id:
                    print("equipe changed")
                    ThreadUpdateVacationEquipe(detail_mission, request, True).start()
                else:
                    print("equipe didn't change")
                    ThreadUpdateVacationEquipe(detail_mission, request, False).start()
                
                vacation.save()

                # update_detail_mission(detail_mission)
                
                return redirect(reverse('vacations-equipes'))

            current_url = resolve(request.path_info).url_name
            extend = extend_de_base
            template = 'gestion_activites/create_vacation_equipe.html'
            return render(request, template, locals())
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

class CreateVacationAgentView(View):
    form_class = VacationAgentForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.staff:
            form = self.form_class()
            societe = request.user.societe
            agents = Agent.objects.filter(societe=societe)
            clients = Client.objects.filter(societe=societe)
            missions = Details_mission.objects.filter(societe=societe)
            current_url = resolve(request.path_info).url_name
            template = 'gestion_activites/create_vacation_agent.html'
            extend = extend_de_base
            return render(request, template, locals())
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.staff:
            form = self.form_class(request.POST)
            client = request.POST.get('native-select-client')
            agent = request.POST.get('native-select-agent')
            mission = request.POST.get('native-select-mission')
            societe = request.user.societe
            if form.is_valid():
                #form.save()
                try :
                    mission = Details_diplome.objects.get(societe=societe, id=int(mission))
                    agent = Agent.objects.get(id=int(agent))
                    client = Client.objects.get(id=int(client))
                except :
                    messages.error(request, "Erreur de saisie, veuillez réessayer")
                    current_url = resolve(request.path_info).url_name
                    template = 'gestion_activites/create_vacation_agent.html'
                    extend = extend_de_base
                    return render(request, template, {'form': form, 'extend': extend, 'current_url': current_url})

                comment = form.cleaned_data['comment']
                date_debut = form.cleaned_data['date_debut']
                date_fin = form.cleaned_data['date_fin']
                heure_debut = form.cleaned_data['heure_debut']
                heure_fin = form.cleaned_data['heure_fin']
                etat_mission = form.cleaned_data['etat_mission']
                
                ThreadVacationAgent(request,mission, agent, client, date_debut, date_fin, heure_debut, heure_fin, etat_mission, comment).start()
                return redirect(reverse('vacations-agents'))
            
            current_url = resolve(request.path_info).url_name
            template = 'gestion_activites/create_vacation_agent.html'
            extend = extend_de_base
            return render(request, template, {'form': form, 'extend': extend, 'current_url': current_url})
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

class UpdateVacationAgentView(View):
    form_class = VacationAgentForm

    def get(self, request, id):
        user = request.user
        vacation = Vacation_agent.objects.get(id=id)
        try:
            agent = Agent.objects.get(user_id=user)
            responsable = vacation.mission.equipe.responsable_equipe
        except:
            responsable = None
        if user.staff or responsable == agent:
            societe = user.societe
            agents = Agent.objects.filter(societe=societe)
            clients = Client.objects.filter(societe=societe)
            missions = Details_mission.objects.filter(societe=societe)
            if vacation.client:
                client_selected = vacation.client
            else:
                client_selected = None
            if vacation.agent:
                agent_selected = Agent.objects.get(id=vacation.agent_id)
            else:
                agent_selected = None
            if vacation.mission:
                mission_selected = vacation.mission
            else:
                mission_selected = None
            
            form = self.form_class(instance=vacation)
            current_url = resolve(request.path_info).url_name
            extend = extend_de_base
            template = 'gestion_activites/create_vacation_agent.html'
            return render(request, template, locals())
        else: 
            extend = extend_de_base
            return render(request, 'gestion_utilisateurs/permissions.html')

    def post(self, request, id):
        user = request.user 
        vacation = Vacation_agent.objects.get(id=id)
        try:
            current_agent = Agent.objects.get(user_id=user)
            responsable = vacation.mission.equipe.responsable_equipe
        except:
            responsable = None
        if user.staff or responsable == current_agent:
            if user.staff:
                client = request.POST.get('native-select-client')
                agent = request.POST.get('native-select-agent')
                mission = request.POST.get('native-select-mission')
            else:
                if vacation.client:
                    client = vacation.client.id
                else:
                    client = None
                if vacation.agent:
                    agent = vacation.agent.id
                else:
                    agent = None
                if vacation.mission is not None:
                    mission = vacation.mission.id
                else:
                    mission = None
            form = self.form_class(request.POST, instance = vacation)

            if form.is_valid():
                #form.save(request)
                try :
                    if mission == 'cliquer ici...':
                        mission = None
                    else :
                        mission = Details_mission.objects.get(id=int(mission))
                except Details_mission.DoesNotExist as e:
                    messages.error(request, "Cette vacation n'existe pas!")
                    print("try None "+str(e))
                comment = form.cleaned_data['comment']
                if agent:
                    agent = Agent.objects.get(id=int(agent))
                if client:
                    client = Client.objects.get(id=int(client))
                date_debut = form.cleaned_data['date_debut']
                date_fin = form.cleaned_data['date_fin']
                heure_debut = form.cleaned_data['heure_debut']
                heure_fin = form.cleaned_data['heure_fin']
                etat_mission = form.cleaned_data['etat_mission']
                ThreadVacationAgent(request,mission, agent, client, date_debut, date_fin, heure_debut, heure_fin, etat_mission, comment, False, vacation).start()
                return redirect(reverse('vacations-agents'))

            current_url = resolve(request.path_info).url_name
            extend = extend_de_base
            template = 'gestion_activites/create_vacation_agent.html'
            return render(request, template, {'form': form, 'extend': extend, 'current_url': current_url})
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html')


class DetailMissionView(View):
    form_class = MissionForm
    
    def get(self, request, id):
        
        mission = Mission.objects.get(id=id)
        detail_missions = Details_mission.objects.filter(mission_id=mission.id)
        accepte = 0
        en_attente = 0
        refus = 0
        duree_tot = ()
        duree_ecoulee = ()
        duree_restante = ()
        jours_tot = 0
        jours_ecoul = 0
        jours_rest = 0
        heures_tot = 0
        heures_ecoul = 0
        heures_rest = 0
        minutes_tot = 0
        minutes_ecoul = 0
        minutes_rest = 0
        for vacation in detail_missions.all():
        #accepte,en_attente,refus = update_etat_mission(mission)
            if vacation.constitution_equipe :
                accepte += 1
            else :
                refus += 1
            vacations = Vacation_agent.objects.filter(mission_id=vacation.id)
            for vac in vacations:
                duree_tot = Util.duree_totale(vac)
                duree_ecoulee = Util.duree_reelle_ecoulee(vac)
                duree_restante = Util.duree_restante(vac)
                # jours_tot += duree_tot[0]*24
                heures_tot += duree_tot[0]*duree_tot[1]
                minutes_tot += duree_tot[2]
                # jours_ecoul += duree_ecoulee[0]*24
                heures_ecoul += duree_ecoulee[0]*duree_ecoulee[1]
                minutes_ecoul += duree_ecoulee[2]
                # jours_rest += duree_restante[0]*24
                heures_rest += duree_restante[0]*duree_restante[1]
                minutes_rest += duree_restante[2]   
        
        if minutes_ecoul >= 60:
            minutes_ecoul -= 60
            heures_ecoul += 1

        if minutes_tot >= 60:
            minutes_tot -= 60
            heures_tot += 1
        
        if minutes_rest >= 60:
            minutes_rest -= 60
            heures_rest += 1
        now = datetime.now()
        today = date.today()
        horaire = time(now.hour,now.minute)
        

        nb_equipes = Details_mission.objects.filter(mission_id=mission).count()

        template = 'gestion_activites/detail_mission.html'
        missions = Details_mission.objects.filter(mission=id).order_by('-date_debut')
        extend = extend_de_base
        return render(request, template, locals())#{'form': form, 'extend': extend, 'missions' : missions, "mission": mission})

        
def delete_mission(request, id):
    if request.user.staff:
        try:
            obj = Mission.objects.get(id=id)
            url_path = "detail_mission"
            if request.method == 'POST':
                print("---------------------- Post DELETE --------------------------")
                obj.delete()
                messages.success(request, 'Mission supprimée: '+str(obj))
                return redirect(reverse('missions'))
            else :
                form = MissionForm(instance=obj)
        except Exception as e :
            messages.warning(request, f'Cette mission ne peut être supprimée: Error {e}')
            print(str(e))
            
        template = 'gestion_activites/delete.html'
        extend = extend_de_base
        return render(request,template,locals())
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

class DetailVacationEquipeView(View):
    form_class = MissionForm
    
    def get(self, request, id):
        societe = request.user.societe
        try:
            mission = Details_mission.objects.get(id=id)
        except:
            mission = None

        accepte,en_attente,refus = update_etat_detail_mission(mission)
        now = datetime.now()
        today = date.today()
        horaire = time(now.hour,now.minute)
        print (now)
        form = self.form_class(instance=mission)

        try:
            vacations = Vacation_agent.objects.filter(mission_id=mission)
        except:
            vacations = None
        duree_tot = ()
        duree_ecoulee = ()
        duree_restante = ()
 
        heures_tot = 0
        heures_ecoul = 0
        heures_rest = 0
        minutes_tot = 0
        minutes_ecoul = 0
        minutes_rest = 0
        if vacations is not None:
            for vac in vacations:
                duree_tot = Util.duree_totale(vac)
                duree_ecoulee = Util.duree_reelle_ecoulee(vac)
                duree_restante = Util.duree_restante(vac)
                # jours_tot += duree_tot[0]*24
                heures_tot += duree_tot[0]*duree_tot[1]
                minutes_tot += duree_tot[2]
                # jours_ecoul += duree_ecoulee[0]*24
                heures_ecoul += duree_ecoulee[0]*duree_ecoulee[1]
                minutes_ecoul += duree_ecoulee[2]
                # jours_rest += duree_restante[0]*24
                heures_rest += duree_restante[0]*duree_restante[1]
                minutes_rest += duree_restante[2]
            if minutes_ecoul >= 60:
                minutes_ecoul -= 60
                heures_ecoul += 1

            if minutes_tot >= 60:
                minutes_tot -= 60
                heures_tot += 1
            
            if minutes_rest >= 60:
                minutes_rest -= 60
                heures_rest += 1
        # print(duree_ecoulee)
        nb_equipes = vacations.count()
        template = 'gestion_activites/detail_vacation_equipe.html'
        # missions = Vacation_agent.objects.filter(mission_id=mission)
        print (vacations)
        extend = extend_de_base
        return render(request, template, locals())
    
    def post(self, request, id):
        # try:
        societe = request.user.societe
        comment = request.POST.get('comment')
        mission = Details_mission.objects.get(id=id)
        if comment != mission.comment :
            print(comment)
            mission.comment = comment
            mission.save()
        
        return redirect("detail_vacation_equipe", id)
        # except Exception as e:
        #     print(e)

class DetailVacationAgentView(View):
    form_class = MissionForm
    
    def get(self, request, id):
        user = request.user
        societe = user.societe
        try:
            mission = Vacation_agent.objects.get(id=id)
        except:
            mission = None

        now = datetime.now()
        today = date.today()
        horaire = time(now.hour,now.minute)
        print (now)
        form = self.form_class(instance=mission)
        
        #nb_equipes = Vacation_agent.objects.filter(mission_id=mission).count()
        #print(f"Nombre equipe : {nb_equipes}")
        template = 'gestion_activites/detail_vacation_equipe.html'
        missions = Vacation_agent.objects.filter(agent_id=mission.agent, client_id=mission.client)
        extend = extend_de_base
        return render(request, template, locals())


def create_diplome(request):
    user = request.user
    if user.staff:
        try:
            current_url = resolve(request.path_info).url_name
            if request.method == 'POST':
                form = DiplomeForm(request.POST)
                if form.is_valid():
                    form.save(request)
                    return redirect('diplomes')

            form = DiplomeForm()
            template = 'gestion_activites/create_diplome.html'
            extend = extend_de_base
            return render(request, template, locals())
        except Exception as e:
            return HttpResponse({'error : \n'+str(e)})
    extend = extend_de_base
    return render(request, 'gestion_utilisateurs/permissions.html', locals())

def detail_diplome(request, id):
    if request.user.staff:
        try:
            societe = request.user.societe
            diplome = Diplome.objects.get(id=id, societe_id=societe)

            template = 'gestion_activites/profile_diplome.html'
            extend = extend_de_base
            return render(request, template, locals())
        except Exception as e:
            return HttpResponse({'error : \n'+str(e)})
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

def delete_vacation_equipe(request, id):
    if request.user.staff:
        try:
            obj = Details_mission.objects.get(id=id)
            url_path = "detail_vacation_equipe"
            if request.method == 'POST':
                print("---------------------- Post DELETE --------------------------")
                obj.delete()
                messages.success(request, 'Vacation supprimée: '+str(obj))
                return redirect(reverse('vacations-equipes'))
                
            else :
                form = VacationEquipeForm(instance=obj)
        except Exception as e :
            messages.warning(request, f'Cette vacation ne peut être supprimée: Error {e}')
            print(str(e))
        template = 'gestion_activites/delete.html'
        extend = extend_de_base
        return render(request,template,locals())
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

def delete_vacation_agent(request, id):
    if request.user.staff:
        try:
            obj = Vacation_agent.objects.get(id=id)
            url_path = "detail_vacation_agent"
            if request.method == 'POST':
                print("---------------------- Post DELETE --------------------------")
                obj.delete()
                messages.success(request, 'Vacation supprimée: '+str(obj))
                return redirect(reverse('vacations-agents'))
                #messages.success(request, 'You have successfully delete the agent')
            else :
                form = VacationAgentForm(instance=obj)
        except Exception as e :
            messages.warning(request, f'Cette vacation ne peut être supprimée: Error {e}')
            print(str(e))
            
        template = 'gestion_activites/delete.html'
        extend = extend_de_base
        return render(request,template,locals())
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())


def update_membership_photo(equipe,agent,photo):
    Membership.objects.filter(equipe_id=equipe, agent_id=agent).update(photo=photo)


def update_client(request, id):
    if request.user.staff:
        try:
            current_url = resolve(request.path_info).url_name
            client = Client.objects.get(id=id)
            form = ClientForm(instance=client)
    
            if request.method == 'POST':
                form = ClientForm(request.POST, instance=client)

                print(str(form.is_valid()))
                if form.is_valid():
                    form.save(request)
                    messages.success(request, 'Données client mises à jour')
                    return redirect(reverse('profile_client',args=id))
            template = 'gestion_activites/create_client.html'
            extend = extend_de_base
            return render(request,template,locals()) 
        except Client.DoesNotExist as e:
            messages.error(request, 'ce client n\'existe plus')
        except Exception as e:
            messages.error(request, 'Erreur inattendue '+str(e))
    else:
        extend = extend_de_base
        return render(request, 'gestion_utilisateurs/permissions.html', locals())

@login_required(login_url='gestion_activites/login/')
def profile_client(request, id):
    societe = request.user.societe
    try:
        client = Client.objects.get(societe=societe, id=id)
    except Client.DoesNotExist as e:
        client = None
        messages.error(request, 'Client introuvable')

    extend = extend_de_base
    return render(request, 'gestion_activites/profile_client.html', locals())#{'extend': extend}) 


@login_required(login_url='gestion_activites/login/')
def profile_agent(request, id):
    societe = request.user.societe
    user = request.user
    decalage = 1
    diplomes =[]
    try:
        agent = Agent.objects.get(societe=societe, id=id)
        diplomes_details = Details_diplome.objects.filter(agent_id=agent.id)
        for diplome in diplomes_details:
            diplo = Diplome.objects.get(id=diplome.diplome_id)
            diplomes.append(diplo)
        if agent.user :
            user_agent = agent.user
        else :
            user_agent = None
        permis = perm(user, user_agent)
        now = datetime.now()
        now_year = now.year
        now_month = now.month
        res = now_month-decalage
        if res <= 0:
            now_year = now_year-1
            now_month = 12+res
            now_ = date(now_year, now_month,1)
        else:
            now_month = res
            now_ = date(now_year,res,1)
        # elif now_month == 1:
        #     now_ = date(now_year-1,11,1)
        # else:
        #     now_ = date(now_year,now_month-2,1)
        # now_ = date(now_year,now_month,1)
        time1 = time(0,0)
        now_ = datetime.combine(now_,time1)

        # now_ = datetime.date(now_year,now_month)
        vacation_duree = Vacation_agent.objects.filter(agent_id=id,
                                                        date_fin__gte=now_
                                                        )
        duree=timedelta(days=0) 
        duree_dec1=timedelta(days=0)
        for vac in vacation_duree:
            duree += Util.duree_ecoulee_dans_le_mois(vac)
            print("2")
            duree_dec1 += Util.duree_ecoulee_mois_passe(vac,decalage)

        
        # print("Vac DUREE en cours "+str(duree))
        # print("Vac DUREE DECALAGE en cours "+str(duree_dec1))
        ## La durée des vacations du mois en cours
        days = duree.days
        minutes, seconds = divmod(duree.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        hours = days*24 + hours
        ## La durée des vacations du mois m-décalage
        days1 = duree_dec1.days
        minutes1, seconds1 = divmod(duree_dec1.seconds, 60)
        hours1, minutes1 = divmod(minutes1, 60)
        hours1 = days1*24 + hours1
        
    except Agent.DoesNotExist as e:
        messages.error(request, 'Vous n\'avez pas les permissions requises'+ str(e))
        agent = None
        diplomes = None
        return redirect(reverse('agents'))
    
    try:
        vacations_all = Vacation_agent.objects.filter(agent_id=agent.id)
        last_vac = vacations_all.order_by('-created_at')[0]
        data = [
            {
                'Agent': x.agent,
                'Client': x.client.nom,
                'Date de début': x.date_debut,
                'Date de fin': x.date_fin,
                'Heure de début': x.heure_debut,
                'Heure de fin': x.heure_fin   
            } if x.client 
            else {
                'Agent': x.agent,
                'Client': "Inconnu",
                'Date de début': x.date_debut,
                'Date de fin': x.date_fin,
                'Heure de début': x.heure_debut,
                'Heure de fin': x.heure_fin   
            }
            for x in vacations_all 
        ]  
        df = pd.DataFrame(data)
        fig = px.timeline(
            df, x_start="Date de début", x_end="Date de fin", y="Client", color="Client"
        ) 
        fig.update_yaxes(autorange="reversed")
        gantt_plot = plot(fig, output_type="div")
    except Exception as e:
        print(e)
        messages.error(request, '0 vacation')

    extend = extend_de_base
    return render(request, 'gestion_activites/profile_agent.html', locals())#{'extend': extend}) 

@login_required(login_url='gestion_activites/login/')
def profile_equipe(request, id):
    societe = request.user.societe
    agents =[]
    try:
        equipe = Equipe.objects.get(societe=societe, id=id)
        list_agents = Membership.objects.filter(equipe_id=id)
        last_vacation = Details_mission.objects.filter(societe_id=societe,equipe_id=id).order_by('-created_at')
        if last_vacation :
            last_vac = Details_mission.objects.filter(societe_id=societe,equipe_id=id).order_by('-created_at')[0]

        for agent in list_agents.all():
            ag = Agent.objects.get(id=agent.agent_id)
            agents.append(ag)
    except Exception as e:
        print(e)
        agent = None

    extend = extend_de_base
    return render(request, 'gestion_activites/profile_equipe.html', locals())#{'extend': extend}) 

def perm(user1, user2):
    if user1 is None:
        return False
    if user1.staff or user2.staff:
        return True
    return False
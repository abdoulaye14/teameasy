import datetime
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.views.generic import CreateView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import LoginForm, RegisterForm

from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from gestion_activites.models import Agent
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
import string, random, secrets
from gestion_activites.models import Agent, Equipe
import logging
from django.http import JsonResponse
from django.core.serializers import serialize
import json
# Get an instance of a logger
logger = logging.getLogger(__name__)

SUPERUSER_LIFETIME = datetime.timedelta(days=1)
# Create your views here.
extend_de_base = 'gestion_activites/base.html'

class Users(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'gestion_utilisateurs/users.html'
    
    def get(self, request):
        user = request.user
        if request.user.staff:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                societe = request.user.societe
                user = request.user
                try:
                    users = User.objects.filter(societe=societe)
                    data= json.loads(serialize('json', users))
                except :
                    users = None  
                    data= {}
                    messages.warning(request, 'Liste vide')
                extend = extend_de_base
                return JsonResponse({'content-data': data}, safe=False)
            return render(request, 'gestion_utilisateurs/users.html')
        else:
            extend = extend_de_base
            return render(request, 'gestion_utilisateurs/permissions.html', locals())

def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_2 = request.POST.get('password_2')
            role = request.POST.get('role')
            statut = request.POST.get('statut')
            societe = request.user.societe
            
            permis = request.user.is_staff

            if permis and email and password and password_2 and societe:
                print("2")
                message = None
                if password is not None and password != password_2:
                    return ValueError("Vos mot de passe ne correspondent pas")
                print("3")
                if role == 'responsable':
                    message = 'Responsable'
                    user = User.objects.create_user(username, email, password, societe)
                    user.responsable = True
                    user.save()

                    print("CREATE RESPONSABLE USER")
                
                elif role == 'staff':
                    message = 'Admin'
                    user = User.objects.create_staffuser(username, email, password, societe)

                    print("CREATE ADMIN USER")
                else :
                    message = 'Utilisateur'
                    user = User.objects.create_user(username, email, password, societe)
                    print("CREATE SIMPLE USER")
                if statut == 'on':
                    user.active = True
                    user.save()
                    
                Util.send_verify_email(request, user, password)
                messages.success(request, f'Un compte {message} a été créé')
                logger.info('Société : '+str(societe)+' Compte '+message+' créé par '+str(request.user)+' pour '+str(email))
                return redirect('home')
            elif not permis:
                messages.warning(request, 'Vous n\'avez pas les autorisations requises pour exécuter cette action')
                logger.warning('Société : '+str(request.user.societe)+' Echec Autorisations insuffisantes : update user: '+str(user)+ ' initiée par '+str(request.user))
            else:
                messages.error(request, 'Erreur dans votre saisie veuillez réessayer!')
        except IntegrityError as exp:
            messages.error(request, 'error : Cet utilisateur existe déjà\n')
            logger.warning('Société : '+str(societe)+' Echec Compte '+message+' tentative de création de compte par '+str(request.user)+' pour l\'agent '+str(email)+' Erreur: Compte existe déjà '+str(exp))
            return redirect('register')
        except Exception as e:
            messages.error(request, 'Veuillez vous rapprocher de l\'administrateur pour corriger ce soucis technique!')
            logger.warning('Société : '+str(societe)+' Echec Compte '+message+' tentative de création de compte par '+str(request.user)+' pour l\'agent '+str(email)+' Erreur: '+str(exp))
            return redirect('register')
    extend = extend_de_base
    template_name = 'gestion_utilisateurs/register.html'
    return render(request, template_name, locals())

def registerAgent(request,id):
    form = RegisterForm()
    user = request.user

    if request.method == 'POST':
        try:
            societe = request.user.societe
            agent = Agent.objects.get(societe=societe, id=id)
            role = request.POST.get('role')
            statut = request.POST.get('statut')
            permis = request.user.is_staff
            username = agent.prenom+' '+agent.nom
            email = agent.mail
            password = random_password(9)

            try : 
                user = User.objects.get(email=email)
                messages.error(request, 'Un utilisateur existe déjà pour cette adresse email!')
                return redirect('profile_agent', id)
            except:
                if permis and agent and email and password and societe:
                    print("2")
                    message = None
                    if role == 'responsable':
                        print("CREATE RESPONSABLE USER")
                        message = 'Responsable'
                        user = User.objects.create_user(username, email, password, societe)
                        user.responsable = True
                        user.save()
                    
                    elif role == 'staff':
                        print("CREATE STAFF USER")
                        message = 'Admin'
                        user = User.objects.create_staffuser(username, email, password, societe)
                        
                    else :
                        print("CREATE SIMPLE USER")
                        message = 'Utilisateur'
                        user = User.objects.create_user(username, email, password, societe)
                        
                    if statut == 'on':
                        user.active = True
                        user.save()
                    print(user)
                    agent.user = user
                    agent.save()

                    Util.send_verify_email(request, user, password)
                    messages.success(request, f'Un compte {message} a été créé')
                    logger.info('Société : '+str(societe)+' Compte '+message+' créé par '+str(request.user)+' pour l\'agent '+str(email))
                    return redirect('profile_agent', id)
                elif not permis:
                    messages.warning(request, 'Vous n\'avez pas les autorisations requises pour exécuter cette action')
                    logger.warning('Société : '+str(request.user.societe)+' Echec Autorisations insuffisantes : update user: '+str(user)+ ' initiée par '+str(request.user))
                else:
                    messages.error(request, 'Erreur dans votre saisie veuillez réessayer!')
        except IntegrityError as exp:
            messages.error(request, 'error : Cet utilisateur existe déjà\n')
            logger.warning('Société : '+str(societe)+' Echec Compte '+message+' tentative de création de compte par '+str(request.user)+' pour l\'agent '+str(email)+' Erreur: Agent introuvable '+str(exp))
            return redirect('add-account')
        except Exception as e:
            messages.error(request, 'Veuillez vous rapprocher de l\'administrateur pour corriger ce soucis technique!')
            logger.error('Société : '+str(societe)+' Echec Compte '+message+' tentative de création de compte par '+str(request.user)+' pour l\'agent '+str(email)+' Erreur: '+str(exp))
            return redirect('add-account')
    extend = extend_de_base
    template_name = 'gestion_utilisateurs/add-account.html'
    return render(request, template_name, locals())

def updateUser(request, id):
    
    try:
        user = User.objects.get(id=id)
        current_user = request.user
        #permis = perm(current_user, user)
    except Exception as e:
        messages.error(request, 'Utilisateur introuvable')
        return redirect('profile_agent', id)
    # if request.user.staff or user == current_user:
    
    if request.method == 'POST':
        try:
            role = request.POST.get('role')
            statut = request.POST.get('statut')
            email = request.POST.get('email')
            username = request.POST.get('username')
            print(statut)
            # if permis:
            if role is not None or role != "":
                if role == 'responsable':
                    print("Update RESPONSABLE USER")
                    user.responsable = True
                
                elif role == 'staff':
                    print("Update STAFF USER")
                    user.staff = True
                elif role == 'default':
                    print("Update Default USER")
                    user.staff = False
                    user.responsable = False
                if statut == 'on':
                    if user.active is not True:
                        user.active = True
                if statut is None:
                    print(statut)
                    user.active = False
            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            user.save()
            messages.success(request, 'Les modifications ont été enregistrées avec succès')
            logger.info('Société : '+str(current_user.societe)+' Compte '+str(user)+ ' modifié par '+str(current_user))
            return redirect(reverse('profil-current-user',args=[user.id]))
            # else:
                # messages.warning(request, 'Vous n\'avez pas les autorisations requises pour effectuer cette action!')
        except User.DoesNotExist as e:
            messages.error(request, 'Utilisateur introuvable')
            logger.warning('Société : '+str(current_user.societe)+' Echec user introuvable : update user: '+str(user)+ ' initiée par '+str(current_user)+' Erreur '+str(e))
        except Exception as e :
            messages.error(request, 'Erreur inattendue veuillez vous rapprocher de l\'administrateur')
            logger.info('Société : '+str(current_user.societe)+' Echec Compte '+str(user)+ ' tentative de modification par '+str(current_user))
            extend = extend_de_base
            # template_name = 'gestion_utilisateurs/update-user.html'
            template_name = 'gestion_utilisateurs/update-user.html'
            return render(request, template_name, locals())
            
    extend = extend_de_base
    template_name = 'gestion_utilisateurs/update-user.html'
    return render(request, template_name, locals())
    # else:
    #     logger.warning('Société : '+str(current_user.societe)+' Echec Autorisations insuffisantes : update user: '+str(user)+ ' initiée par '+str(current_user))
    #     extend = extend_de_base
    #     return render(request, 'gestion_utilisateurs/permissions.html', locals())#{'extend': extend}) 

def changePassword(request, id):
    try:
        user = User.objects.get(id=id)
        current_user = request.user
        permis = perm(current_user, user)
    except Exception as e:
        messages.error(request, 'Utilisateur introuvable')
        return redirect('home')
    if request.method == 'POST':
        try:
            oldpassword = request.POST.get('oldpassword')
            password = request.POST.get('password')
            password_2 = request.POST.get('password_2')
            if permis:
                user_verif = authenticate(request, email=user.email, password=oldpassword)
                if user_verif is not None and user_verif == user:
                    if password is not None and password != password_2:
                        messages.info(request, "Vos mot de passe ne correspondent pas")
                        extend = extend_de_base
                        template_name = 'gestion_utilisateurs/change-password.html'
                        return render(request, template_name, locals())
                    
                    user.set_password(password)
                    user.save()
                    
                    Util.send_change_password_email(request, user)
                    messages.success(request, 'Mot de passe changé avec succés'+str(user))
                    logger.info('Société : '+str(current_user.societe)+' Mot de passe Compte '+str(user)+ ' modifié par '+str(current_user))
                    return redirect('logout')
                else:
                    messages.error(request,'Mot de passe invalides, veuillez réessayer')
                    extend = extend_de_base
                    template_name = 'gestion_utilisateurs/change-password.html'
                    return render(request, template_name, locals())
            else:
                messages.warning(request, 'Vous n\'avez pas les autorisations requises pour effectuer cette action!')
                logger.warning('Société : '+str(current_user.societe)+' Echec Autorisations insuffisantes : update user: '+str(user)+ ' initiée par '+str(current_user))
        except User.DoesNotExist as e:
            messages.error(request, 'Utilisateur introuvable')
            logger.warning('Société : '+str(current_user.societe)+' Echec action update_user user introuvable: '+str(user)+ ' initiée par '+str(current_user)+' Erreur '+str(e))
        except Exception as e:
            messages.error(request, 'Erreur inattendue veuillez vous rapprocher de l\'administrateur')
            logger.error('Société : '+str(current_user.societe)+' Echec action : changePassworde user: '+str(user)+ ' initiée par '+str(current_user)+' Erreur '+str(e))
            extend = extend_de_base
            template_name = 'gestion_utilisateurs/change-password.html'
            return render(request, template_name, locals())

    extend = extend_de_base
    template_name = 'gestion_utilisateurs/change-password.html'
    return render(request, template_name, locals())

class ManagePassword:
    def mot_de_passe_oublie(request):
        if request.method == 'POST':
            try:
                email = request.POST.get('email')
                user = User.objects.get(email=email)
                Util.send_mail_mot_de_passe_oublie(request,user)
                messages.success(request, 'Veuillez vérifier votre compte de messagerie afin de finaliser la procédure '+str(user))
                logger.info('Société : '+str(user.societe)+' Initialisation mot de passe inititié par '+str(user))
                return redirect('login')
            except User.DoesNotExist as exp:
                logger.warning('Société : '+str(user.societe)+' Echec mot de passe oublié: user introuvable; par '+str(user)+ ' Erreur :'+str(e))
                return HttpResponse({'error : Cet utilisateur n\'existe pas\n'})
            except Exception as e:
                logger.error('Société : '+str(user.societe)+' Echec mot de passe oublié: user introuvable; par '+str(user)+ ' Erreur :'+str(e))
                return HttpResponse({f'error ok mot de oub: {e}\n'})

        extend = extend_de_base
        template_name = 'gestion_utilisateurs/forgotten-password.html'
        return render(request, template_name, locals())
    
    def change_forgotten_password(request,id):
        if request.method == 'POST':
            try:
                password = request.POST.get('password')
                password_2 = request.POST.get('password_2')
                user = User.objects.get(id=id)
                if user is not None:
                    if password is not None and password != password_2:
                        messages.info(request, "Vos mot de passe ne correspondent pas")
                        extend = extend_de_base
                        template_name = 'gestion_utilisateurs/change-forgotten-password.html'
                        return render(request, template_name, locals())
                    user.set_password(password)
                    user.save()
                    
                    Util.send_change_password_email(request, user)
                    messages.success(request, 'Mot de passe changé avec succés'+str(user))
                    logger.info('Société : '+str(user.societe)+' Initialisation mot de passe terminée par '+str(user))
                    return redirect('login')
            except User.DoesNotExist as exp:
                logger.warning('Société : '+str(user.societe)+' Echec Initialisation mot de passe : user introuvable; par '+str(user)+ ' Erreur :'+str(exp))
                return HttpResponse({'error : Cet utilisateur n\'existe plus\n'})
            except Exception as e:
                logger.error('Société : '+str(user.societe)+' Echec Initialisation mot de passe : user introuvable; par '+str(user)+ ' Erreur :'+str(e))
                return HttpResponse({f'error change : {e}\n'})

        extend = extend_de_base
        template_name = 'gestion_utilisateurs/change-forgotten-password.html'
        return render(request, template_name, locals())

def perm(user1, user2):
    if user1.staff or user2.staff or user1 == user2:
        return True
    return False

def envoiMail(request, id):
    try:
        user = User.objects.get(id=id)
        Util.resend_verify_email(request, user)
        agent = Agent.objects.get(user_id=id)
        logger.info('Société : '+str(user.societe)+' Mail envoyé par '+str(request.user)+ ' à : '+str(user))
        return redirect('profile_agent', agent.id)
    except User.DoesNotExist as exp:
        logger.warning('Société : '+str(user.societe)+' Echec user introuvable; par '+str(user)+ ' Erreur : '+str(exp))
        return HttpResponse({'error : Cet utilisateur n\'existe plus\n'})   

def random_password(length):
    password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(length)))
    return password
   
class VerifyEmail(CreateView):
    def get(self, request):
        try:
            token = request.GET.get('token')
            payload=jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.active = True
                user.save()
                SUPERUSER_LIFETIME = datetime.timedelta(seconds=1)
                token = RefreshToken.for_user(user).access_token
                token.set_exp(lifetime=SUPERUSER_LIFETIME)
            messages.success(request,'Compte activé avec succés')
            logger.info('Société : '+str(user.societe)+' Compte vérifié et activé: '+str(user))
            return redirect('login')
        except jwt.ExpiredSignatureError as identifier:
            logger.warning('Société : '+str(user.societe)+' Echec token expiré ; par '+str(user)+ ' Erreur')
            return HttpResponse({'error : Vous avez dépassé le délai accordé pour la validation de votre compte \n'+str(identifier)})
            #return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            logger.warning('Société : '+str(user.societe)+' Echec token invalide ; par '+str(user)+ ' Erreur')
            return HttpResponse({'error : Token invalide\n'+str(identifier)})
        except User.DoesNotExist as exp:
            logger.warning('Société : '+str(user.societe)+' user introuvable; par '+str(user)+ ' Erreur : '+str(exp))
            return HttpResponse({'error : Cet utilisateur n\'existe plus\n'})


def loginPage(request):
    form = LoginForm()
    #print(request.user.societe)
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is None:
                messages.error(request,'Identifiants invalides, veuillez réessayer')
                return redirect('login')
            if user.active == False:
                messages.warning(request,'Compte disactivé, veuillez vous rapprocher d\'un administrateur')
                return redirect('login')
            if not user.is_verified and not user.admin:
                messages.info(request,'Email pas encore vérifié')
                return redirect('login')
            if user is not None:
                messages.success(request, 'Connexion réussie')
                login(request, user)
                logger.info('Société : '+str(user.societe)+' Connexion réussie au compte de '+str(user))
                if user.staff:
                    return redirect('home')
                else:
                    return redirect('profil-current-user', user.id)
            else:
                messages.error(request,'Adresse email ou mot de passe incorrrect')
        except Exception as e:
            messages.error(request,'Soucis technique, veuillez vous rapprocher de l\'administrateur')
            logger.error('Société : '+str(user.societe)+' Echec Connexion compte: '+str(user))
            template_name = 'gestion_utilisateurs/login.html'
            extend = extend_de_base
            return render(request, template_name, locals())
    template_name = 'gestion_utilisateurs/login.html'
    extend = extend_de_base
    return render(request, template_name, locals())

def delete_user(request, id):
    if request.user.staff:
        try:
            obj = User.objects.get(id=id)
            url_path = "profil-current-user"
            if request.method == 'POST':
                print("---------------------- Post DELETE --------------------------")
                obj.delete()
                messages.success(request, 'Utilisateur supprimé: '+str(obj))
                return redirect(reverse('users'))
                
        except Exception as e :
            messages.warning(request, f'Cet uilisateur ne peut être supprimée: Error {e}')
            print(str(e))
        template = 'gestion_activites/delete.html'
        extend = extend_de_base
        return render(request,template,locals())
    else:
        extend = extend_de_base
        template_name = 'gestion_utilisateurs/permissions.html'
        return render(request, template_name)
def profil_current_user(request, id):
    # user = request.user
    current_user = request.user
    societe = current_user.societe
    
    user = User.objects.get(id=id, societe_id=societe)
    try:
        agent = Agent.objects.get(user_id=user.id)
        equipes = Equipe.objects.filter(societe_id=societe, responsable_equipe_id=agent.id)
    except Exception as e:
        agent = None
        logger.error('Société : '+str(user.societe)+' Echec action: '+str(user)+' Erreur: '+str(e))

    template_name = 'gestion_utilisateurs/profil-current-user.html'
    extend = extend_de_base
    return render(request, template_name, locals())

def logoutUser(request):
    user = request.user
    if user.id is None:
        logger.info('Déconnexion réussie au compte de '+str(user))
    else:
        societe = user.societe
        logger.info('Société : '+str(societe)+' Déconnexion réussie au compte de '+str(user))
    logout(request)
    return redirect('login')
    # user = request.user
    # if user:
    #     societe = user.societe
    #     logger.info('Société : ' Déconnexion réussie au compte de '+str(user))
    # logout(request)
    # logger.info('Société : '+str(societe)+' Déconnexion réussie au compte de '+str(user))
    # return redirect('login')

def error_404(request, exception):
    return render(request, 'gestion_utilisateurs/error/404.html')
import calendar
import datetime
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
import jwt 
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .threads import ThreadMail
from twilio.rest import Client

class Util:
    
    @staticmethod
    def send_verify_email(request, user, password):
        SUPERUSER_LIFETIME = datetime.timedelta(days=1)
        token = RefreshToken.for_user(user).access_token
        token.set_exp(lifetime=SUPERUSER_LIFETIME)
        current_site = get_current_site(request)
        relativeLink = reverse('email-verify')
        absurl = 'http://'+str(current_site)+str(relativeLink)+"?token="+str(token)
        email_body = 'Bonjour '+user.username+'\nVotre mot de passe est : '+password+'\nVous avez 24h pour finaliser cette action. Passer ce délai, veuillez contacter l\'administrateur de votre société\nutilisez ce lien pour vérifier votre email \n'+ absurl
        from_email = request.user.email
        reply_to = request.user.email
        email_subject = 'Vérification email'
        ThreadMail(email_subject,email_body,from_email,user.email,reply_to).start()
    
    @staticmethod
    def resend_verify_email(request, user):
        SUPERUSER_LIFETIME = datetime.timedelta(days=1)
        token = RefreshToken.for_user(user).access_token
        token.set_exp(lifetime=SUPERUSER_LIFETIME)
        print(token)
        current_site = get_current_site(request)
        relativeLink = reverse('email-verify')
        absurl = 'http://'+str(current_site)+str(relativeLink)+"?token="+str(token)
        email_body = 'Bonjour '+user.username+'\nPour votre mot de passe, reliser le premier mail de vérification envoyé \nVous avez 24h pour finaliser cette action. Passer ce délai, veuillez contacter l\'administrateur de votre société\nVeuillez utiliser ce lien pour confirmer votre adresse e-mail \n'+ absurl
        from_email = request.user.email
        reply_to = request.user.email
        email_subject = 'Vérification e-mail'
        ThreadMail(email_subject,email_body,from_email,user.email,reply_to).start()
    

    @staticmethod
    def send_change_password_email(request, user):
        email_body = 'Bonjour '+user.username+'\nVotre mot de passe a été mis à jour avec succés'
        if (request.user.is_authenticated):
            from_email = request.user.email
            reply_to = request.user.email
        else : 
            from_email = None
            reply_to = None
        email_subject = 'Suivi mise à jour de votre mot de passe'
        ThreadMail(email_subject,email_body,from_email,user.email,reply_to).start()

    @staticmethod
    def send_mail_statut_vacation(request, agent, mission, accepte, refus, en_attente):
        email_body = 'Bonjour '+agent.prenom+'\nEtat des lieux de la mission '+mission+' :\n - Nombre d\'agents ayant acceptés : '+str(accepte)+'\n - Nombre d\'agents ayant refusés : '+str(refus)+'\n - Nombre d\'agents n\'ayant pas encore répondu : '+str(en_attente)
        from_email = request.user.email
        reply_to = request.user.email
        email_subject = 'Statut vacation'
        ThreadMail(email_subject,email_body,from_email,agent.mail,reply_to).start()
    
    @staticmethod
    def send_mail_bug(request, exception):
        email_body = "Erreur rencontrée : \n" + str(exception)
        from_email = request.user.email
        reply_to = request.user.email
        email_subject = 'Nouveau bug'
        ThreadMail(email_subject,email_body,from_email,reply_to).start()
    
    @staticmethod
    def send_mail_mot_de_passe_oublie(request, user):
        SUPERUSER_LIFETIME = datetime.timedelta(days=1)
        token = RefreshToken.for_user(user).access_token
        token.set_exp(lifetime=SUPERUSER_LIFETIME)
        current_site = get_current_site(request)
        relativeLink = reverse('change-forgotten-password', args=[user.id])
        absurl = 'http://'+str(current_site)+str(relativeLink)+"?token="+str(token)
        email_body = 'Bonjour '+user.username+'\nVeuillez suivre ce lien pour mettre à jour votre mot de passe\n'+ absurl
        from_email = None
        reply_to = None
        email_subject = 'Mise à jour de votre mot de passe'
        ThreadMail(email_subject,email_body,from_email,user.email,reply_to).start()
    
    @staticmethod
    def duree_reelle_ecoulee(vacation):
        if vacation is None:
            return 0
        date_debut = vacation.date_debut
        date_fin = vacation.date_fin
        heure_debut = vacation.heure_debut
        heure_fin = vacation.heure_fin
        now = datetime.datetime.now()
        date_1 = datetime.datetime.combine(date_debut,heure_debut)
        date_2 = datetime.datetime.combine(date_fin,heure_fin)
        if now < date_1:
            return (0,0,0)
        elif now > date_2:
            duree_days = date_fin - date_debut
        else :
            duree_days = now - date_1
        
        duree_hours = datetime.datetime.combine(datetime.date.today(), heure_fin) - datetime.datetime.combine(datetime.date.today(), heure_debut)
        
        minutes, seconds = divmod(duree_hours.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        data=(duree_days.days+1, hours, minutes)
        return data

    @staticmethod
    def duree_totale(vacation):
        if vacation is None:
            return (0,0,0)
        date_debut = vacation.date_debut
        date_fin = vacation.date_fin
        heure_debut = vacation.heure_debut
        heure_fin = vacation.heure_fin
        date_1 = datetime.datetime.combine(date_debut,heure_debut)
        date_2 = datetime.datetime.combine(date_fin,heure_fin)
        if date_2 < date_1:
            return (0,0,0)

        duree_days = date_fin - date_debut
        
        duree_hours = datetime.datetime.combine(datetime.date.today(), heure_fin) - datetime.datetime.combine(datetime.date.today(), heure_debut)

        minutes, seconds = divmod(duree_hours.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        data=(duree_days.days+1, hours, minutes)
        return data

    @staticmethod
    def duree_restante(vacation):
        if vacation is None:
            return (0,0,0)
        date_debut = vacation.date_debut
        date_fin = vacation.date_fin
        heure_debut = vacation.heure_debut
        heure_fin = vacation.heure_fin
        now = datetime.datetime.now()
        date_1 = datetime.datetime.combine(date_debut,heure_debut)
        date_2 = datetime.datetime.combine(date_fin,heure_fin)
        if now < date_2 and now > date_1:
            duree_days = date_2 - now
        elif now > date_2:
            return (0,0,0)
        else :
            duree_days = date_fin - date_debut
        duree_hours = datetime.datetime.combine(datetime.date.today(), heure_fin) - datetime.datetime.combine(datetime.date.today(), heure_debut)

        minutes, seconds = divmod(duree_hours.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        data=(duree_days.days+1, hours, minutes)
        return data

    @staticmethod
    def duree_ecoulee_dans_le_mois(vacation):
        if vacation is None:
            return (0,0,0)
        date_debut = vacation.date_debut
        date_fin = vacation.date_fin
        heure_debut = vacation.heure_debut
        heure_fin = vacation.heure_fin
        now = datetime.datetime.now()
        now_month = now.month
        now_year = now.year
        now_ = datetime.date(now_year,now_month,1)
        time = datetime.time(0,0)
        now_ = datetime.datetime.combine(now_,time)
        date_1 = datetime.datetime.combine(date_debut,heure_debut)
        date_2 = datetime.datetime.combine(date_fin,heure_fin)
        if date_1 > now or date_2 < now_:
            duree = datetime.timedelta(days=0)
        else :
            if now_ > date_2 or now < date_1:
                duree_days = datetime.timedelta(days=0)
            elif now > date_2 and date_1 < now_:
                duree_days = date_2 - now_
            elif now > date_2 and date_1 > now_:
                duree_days = date_fin - date_debut
            elif now < date_2 and date_1 < now_:
                duree_days = now - now_
            elif now < date_2 and date_1 > now_:
                duree_days = now - date_1
            else :
                duree_days = datetime.timedelta(days=0)

            duree_hours = datetime.datetime.combine(datetime.date.today(), heure_fin) - datetime.datetime.combine(datetime.date.today(), heure_debut)
            minutes, seconds = divmod(duree_hours.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            all_ = duree_days.days+1
            hours = hours*all_

            duree = datetime.timedelta(days=0,hours=hours,minutes=minutes)

        # print("DATA PRINT "+str(duree))
        return duree
    
    @staticmethod
    def duree_ecoulee_mois_passe(vacation,decalage):
        if vacation is None:
            return 0

        date_debut = vacation.date_debut
        date_fin = vacation.date_fin
        heure_debut = vacation.heure_debut
        heure_fin = vacation.heure_fin
        now = datetime.datetime.now()
        now_month = now.month
        now_year = now.year
        res = now_month-decalage
        if res <= 0:
            now_year = now_year-1
            now_month = 12+res
            now_ = datetime.date(now_year, now_month,1)
        else:
            now_month = res
            now_ = datetime.date(now_year,res,1)
        dernierjour = calendar.monthrange(now_year, now_month)[1]

        now = datetime.date(now_year,now_month,dernierjour)
        time = datetime.time(0,0)
        time_final = datetime.time(23,59)
        now_ = datetime.datetime.combine(now_,time)
        now = datetime.datetime.combine(now,time_final)

        date_1 = datetime.datetime.combine(date_debut,heure_debut)
        date_2 = datetime.datetime.combine(date_fin,heure_fin)
        if date_1 > now or date_2 < now_:
            duree = datetime.timedelta(days=0)
        else :
            if now_ > date_2 or now < date_1:
                duree = datetime.timedelta(days=0)
            elif now > date_2 and date_1 < now_:
                duree = date_2 - now_
            elif now > date_2 and date_1 > now_:
                duree = date_fin - date_debut
            elif now < date_2 and date_1 < now_:
                duree = now - now_
            elif now < date_2 and date_1 > now_:
                duree = now - date_1
            else :
                duree = datetime.timedelta(days=0)
            duree_hours = datetime.datetime.combine(datetime.date.today(), heure_fin) - datetime.datetime.combine(datetime.date.today(), heure_debut)
            minutes, seconds = divmod(duree_hours.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            #data=(duree.days+1, duree_hours, minutes)
            all_ = duree.days+1
            hours = hours*all_
            duree = datetime.timedelta(days=0,hours=hours,minutes=minutes)

        return duree

def envoi_sms():

    account_sid = 'ACc8dcf517098ce8c8d496c0450f9aa81b'
    auth_token = 'f20236301d8c8460ad5f61746c111df1'
    twilio_num = '+19566668022'
    my_num = '+33651457421'

    client = Client(account_sid, auth_token)

    msg = "on y est"
    message = client.messages.create(
        to = my_num,
        from_ = twilio_num,
        body=msg
    )
    
    
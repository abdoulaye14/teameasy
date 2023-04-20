from django.db import models
from enum import Enum
from django.utils import timezone
from django.urls import reverse
from gestion_utilisateurs.models import (
    Societe,
    User
)

# Create your models here.


class Diplome(models.Model) :
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE, null=True)
    nom_diplome = models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_diplome
    

class Agent(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    identifiant = models.CharField(max_length=50,null=True)
    nom = models.CharField(max_length=50,null=True)
    prenom = models.CharField(max_length=50,null=True)
    adresse = models.CharField(max_length=50,null=True)
    code_postal = models.CharField(max_length=5,null=True)
    ville = models.CharField(max_length=50,null=True)
    telephone = models.CharField(max_length=13,null=True)
    mail = models.EmailField(max_length=50,unique=True,null=True)
    photo = models.ImageField(upload_to='images/',null=True)
    disponibilite = models.BooleanField(default=False,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def get_absolute_url(self):
    #     return reverse("gestion_activites:create_agent",kwargs={"id": self.id})

    def __str__(self):
        return self.prenom + " " + self.nom


class Details_diplome(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    diplome = models.ForeignKey(Diplome, on_delete=models.CASCADE)
    date_delivrance = models.DateField()
    date_expiration = models.DateField()
    validite = models.BooleanField(default=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Client(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE,null=True)
    nom = models.CharField(max_length=50,null=True)
    telephone = models.CharField(max_length=15,null=True)
    rue1 = models.CharField(max_length=50,null=True)
    rue2 = models.CharField(max_length=50,null=True)
    code_postal = models.CharField(max_length=5,null=True)
    ville = models.CharField(max_length=50,null=True)
    boite_postale = models.CharField(max_length=50,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nom)


class Status(models.TextChoices):
    ACCEPTEE = "AC", "Acceptée"
    REFUSEE = "RF", "Refusée"
    EN_ATTENTE = "EA", "En Attente"

class Equipe(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE,null=True)
    nom_equipe = models.CharField(max_length=50,unique = True,null=True)
    responsable_equipe = models.ForeignKey(Agent,related_name="%(app_label)s_%(class)s_related", on_delete=models.CASCADE,null=True)
    agents = models.ManyToManyField(Agent, through="Membership")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # qualif_pro = 
    # photos = models.ImageField(upload_to='photos', verbose_name='My Photo')
    # vacation_agent = 

    def __str__(self):
        return self.nom_equipe + str(self.id)

    
class Membership(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)
    validite_diplome = models.BooleanField(default=False,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Mission(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE,null=True)
    nom = models.CharField(max_length=50,null=True)
    equipe = models.ManyToManyField(Equipe, through="Details_mission")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,null=True)

    site = models.CharField(max_length=50,null=True)
    nature_mission = models.CharField(max_length=250,null=True)
    criteres = models.CharField(max_length=250,null=True)

    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True)
    heure_debut = models.TimeField(null=True)
    heure_fin = models.TimeField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nom)


class Details_mission(models.Model):
    nom = models.CharField(max_length=50,null=True)
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE,null=True)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE,null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,null=True)
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL,null=True)
    constitution_equipe = models.BooleanField(default=False,null=True)
    comment = models.CharField(max_length=250,null=True)
    incident = models.IntegerField(default=0, null=True)
    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True)
    heure_debut = models.TimeField(null=True)
    heure_fin = models.TimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nom)

# class Verification(models.Model):
#     agents = models.ManyToManyField(Agent, through="Membership")
#     nom = models.CharField(max_length=50,null=True)

class Vacation_agent(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE,null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL,null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,null=True)
    mission = models.ForeignKey(Details_mission, on_delete=models.CASCADE,null=True)
    # Enumération acceptée, refusée, en attente
    etat_mission = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.EN_ATTENTE,
    )
    comment = models.CharField(max_length=250,null=True)
    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True)
    heure_debut = models.TimeField(null=True)
    heure_fin = models.TimeField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.agent)

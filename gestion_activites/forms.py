
from .models import *
from django import forms
from django.forms import ModelForm,Form
from django.utils import timezone

class AgentForm(forms.ModelForm):
    identifiant = forms.CharField(required=False, label="Identifiant", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Entrer votre identifiant"}))
    nom = forms.CharField(required=False, label="Nom", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter votre nom"}))
    prenom = forms.CharField(required=False, label="Prénom", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter votre prenom"}))
    adresse = forms.CharField(required=False, label="Adresse", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter votre adresse"}))
    code_postal = forms.CharField(required=False, label="Code Postal", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter votre code postal"}))
    ville = forms.CharField(required=False, label="Ville", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter votre ville"}))
    telephone = forms.CharField(required=False, label="Téléphone", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter votre numéro de téléphone"}))
    
    mail = forms.EmailField(required=False, label="Adresse Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter votre adresse email"}))
    photo = forms.ImageField(required=False, label="Photo")
    #diplomes = forms.ModelMultipleChoiceField(queryset=Diplome.objects.all(), widget=forms.CheckboxSelectMultiple)
    disponibilite = forms.BooleanField(required=False, label="disponibilite")
    societe = forms.ModelChoiceField(required=False,queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))
    user = forms.ModelChoiceField(required=False,queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Agent
        fields = ['identifiant', 'nom', 'prenom', 'adresse', 'code_postal', 'ville', 'telephone', 'mail', 'photo']

    def clean_email(self):
        '''
        Verify both societe match.
        '''
        mail = self.cleaned_data.get('mail')
        qs = Agent.objects.filter(mail=mail)
        if qs.exists():
            raise forms.ValidationError("Cet email existe déjà")
        return mail
    
    def clean_agent(self, societe):
        cleaned_data = super().clean()
        identifiant = cleaned_data.get("identifiant")

        if societe is None:
            raise forms.ValidationError("Vous ne pouvez pas ajouter d'utilisateurs")

        # qs = Agent.objects.filter(identifiant=identifiant, societe= societe)
        # if qs.exists():
        #     raise forms.ValidationError("Cet identifiant existe déjà")
        
        return cleaned_data
    
    def save(self, request, commit=True):
        # Save the provided password in hashed format
        agent = super(AgentForm, self).save(commit=False)
        # photo = request.POST["photo"]
        # print("photo")
        # print(photo)
        agent.societe = request.user.societe
        # agent.photo = photo
        #self.clean_email()
        #self.clean_agent(agent.societe)
        # user.active = False # send confirmation email
        if commit:
            agent.save()
        return agent

class DiplomeDetailForm(forms.ModelForm):
    diplome = forms.ModelChoiceField(required=False, queryset=Diplome.objects.all(), widget=forms.Select(attrs={'class':'form-control form-control-sm form-control-inline'}))
    date_delivrance = forms.DateField(required=False, label="Date de délivrance", widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class':'form-control form-control-sm form-control-inline'}))
    date_expiration = forms.DateField(required=False, label="Date d'expiration", widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class':'form-control form-control-sm form-control-inline'}))

    class Meta:
        model = Details_diplome
        fields = '__all__'

    # def clean_myfield(self):
    #     diplome = self.cleaned_data['diplome']
    #     date_delivrance = self.cleaned_data['date_delivrance']
    #     date_expiration = self.cleaned_data['date_expiration']
    #     if diplome == None or date_expiration <= date_delivrance :
    #         raise forms.ValidationError("I hates it!")
    #     return [diplome,date_delivrance,date_expiration]

class ClientForm(forms.ModelForm):
    nom = forms.CharField(required=False, label="Nom du client", widget=forms.TextInput(attrs={'class':'form-control'}))
    rue1 = forms.CharField(required=False, label="Rue 1", widget=forms.TextInput(attrs={'class':'form-control'}))
    rue2 = forms.CharField(required=False, label="Rue 2", widget=forms.TextInput(attrs={'class':'form-control'}))
    telephone = forms.CharField(required=False, label="Telephone", widget=forms.TextInput(attrs={'class':'form-control'}))
    code_postal = forms.CharField(required=False, label="Code Postal", widget=forms.TextInput(attrs={'class':'form-control'}))
    ville = forms.CharField(required=False, label="Ville", widget=forms.TextInput(attrs={'class':'form-control'}))
    site = forms.CharField(required=False, label="Site", widget=forms.TextInput(attrs={'class':'form-control'}))

    boite_postale = forms.CharField(required=False, label="Boîte postale", widget=forms.TextInput(attrs={'class':'form-control'}))
    
    societe = forms.ModelChoiceField(required=False,queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Client
        fields = '__all__'

    def clean_client(self, societe):
        '''
        Verify name is available.
        '''
        nom = self.cleaned_data.get('nom')
        if societe is None:
            raise forms.ValidationError("Vous ne pouvez pas ajouter de clients")

        # qs = Client.objects.filter(nom=nom, societe=societe)
        # if qs.exists():
        #     raise forms.ValidationError("Cette socièté existe déjà")
        
        return super().clean()

    def save(self, request, commit=True):
        # Save the provided password in hashed format
        client = super(ClientForm, self).save(commit=False)
        
        client.societe = request.user.societe
        self.clean_client(client.societe)
        # user.active = False # send confirmation email
        if commit:
            client.save()
        return client

class VacationAgentForm(forms.ModelForm):
    # agent = forms.ModelChoiceField(queryset=Agent.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    # mission = forms.ModelChoiceField(required=False, queryset=Details_mission.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    # client = forms.ModelChoiceField(required=False, queryset=Client.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    etat_mission = forms.ChoiceField(required=True, label="Etat constitution",choices=Status.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(required=False, label="Commentaires", widget=forms.Textarea(attrs={'class':'form-control', 'style':'max-height: 150px'}))
    date_debut = forms.DateField(label="Date de début mission", initial=timezone.datetime.now().strftime('%Y-%m-%d'), widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control','type':'date'}))
    date_fin = forms.DateField(label="Date de fin de la mission ", initial=timezone.datetime.now().strftime('%Y-%m-%d'), widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control','type':'date'}))
    heure_debut = forms.TimeField(label="Commence à", widget=forms.TimeInput(format='%H:%M',attrs={'class': 'form-control','type':'time'}))
    heure_fin = forms.TimeField(label="Finit à", widget=forms.TimeInput(format='%H:%M',attrs={'class': 'form-control','type':'time'}))

    societe = forms.ModelChoiceField(required=False,queryset=None)

    class Meta:
        model = Vacation_agent
        fields = ['date_debut', 'date_fin', 'heure_debut', 'heure_fin', 'etat_mission', 'comment']
    
    def clean_vacation_agent(self, societe):
        '''
        Verify name is available.
        '''
        date_debut = self.cleaned_data.get('date_debut')
        date_fin = self.cleaned_data.get('date_fin')
        heure_debut = self.cleaned_data.get('heure_debut')
        heure_fin = self.cleaned_data.get('heure_fin')
        
        if date_debut > date_fin:
            raise forms.ValidationError("Veuillez vérifier la saisie des dates")
        if date_debut == date_fin and heure_debut > heure_fin:
            raise forms.ValidationError("Veuillez vérifier la saisie des dates")

        if societe is None:
            raise forms.ValidationError("Vous ne pouvez pas ajouter de vacations")
        
        return super().clean()

    def save(self, request, commit=True):
        # Save the provided password in hashed format
        vacation = super(VacationAgentForm, self).save(commit=False)
        
        vacation.societe = request.user.societe
        self.clean_vacation_agent(vacation.societe)
        # user.active = False # send confirmation email
        if commit:
            vacation.save()
        return vacation

class UpdateVacationAgentForm(forms.Form):
    nom = forms.CharField(required=False, label="Nom", widget=forms.TextInput(attrs={'class':'form-control'}))
    prenom = forms.CharField(required=False, label="Prénom", widget=forms.TextInput(attrs={'class':'form-control'}))
    etat_mission = forms.ChoiceField(required=False, label="Etat Vacation",choices=Status.choices,widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(required=False, label="Commentaires", widget=forms.Textarea(attrs={'class':'form-control', 'style':'max-height: 150px'}))

class DiplomeForm(forms.ModelForm):
    nom_diplome = forms.CharField(required=True, label="Diplome", widget=forms.TextInput(attrs={'class':'form-control'}))

    societe = forms.ModelChoiceField(required=False,queryset=None)

    class Meta:
        model = Diplome
        fields = ['nom_diplome']

    def clean_diplome(self, societe):
        '''
        Verify both passwords match.
        '''

        cleaned_data = super().clean()
        nom_diplome = cleaned_data.get("nom_diplome")
        if nom_diplome is None:
            raise forms.ValidationError("Vous ne pouvez pas ajouter d'utilisateur")
        qs = Diplome.objects.filter(nom_diplome=nom_diplome, societe=societe)
        if qs.exists():
            raise forms.ValidationError("Ce diplôme existe déjà")
        if societe is None:
            raise forms.ValidationError("Vous ne pouvez pas ajouter de diplôme")
        return societe
    
    def save(self, request, commit=True):
        # Save the provided password in hashed format
        diplome = super(DiplomeForm, self).save(commit=False)
        
        diplome.societe = request.user.societe
        # user.active = False # send confirmation email
        if commit:
            diplome.save()
        return diplome

class VacationEquipeForm(forms.ModelForm):
    nom = forms.CharField(required=False, label="Nom de la mission",widget=forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder': 'exemple: Théâtre de Rouen'}))
    # equipe = forms.ModelChoiceField(queryset=Equipe.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    # mission = forms.ModelChoiceField(required=False, queryset=Mission.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    # client = forms.ModelChoiceField(required=False, queryset=Client.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    constitution_equipe = forms.BooleanField(required=False)
    #etat_equipe = forms.ChoiceField(required=False, label="Etat constitution EQUIPE",choices=Status_equipe.choices, initial = Status.EN_ATTENTE,widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(required=False, label="Commentaires", widget=forms.Textarea(attrs={'class':'form-control', 'style':'max-height: 150px'}))
    incident = forms.IntegerField(required=False, label="Commentaires", initial=0, widget=forms.NumberInput(attrs={'class':'form-control', 'style':'max-height: 30px'}))
    date_debut = forms.DateField(label="Date de début mission", initial=timezone.datetime.now().strftime('%Y-%m-%d'), widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control','type':'date'}))
    date_fin = forms.DateField(label="Date de fin de la mission ", initial=timezone.datetime.now().strftime('%Y-%m-%d'), widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control','type':'date'}))
    heure_debut = forms.TimeField(label="Commence à", widget=forms.TimeInput(format='%H:%M',attrs={'class': 'form-control','type':'time'}))
    heure_fin = forms.TimeField(label="Finit à", widget=forms.TimeInput(format='%H:%M',attrs={'class': 'form-control','type':'time'}))

    societe = forms.ModelChoiceField(required=False,queryset=None)
    
    class Meta:
        model = Details_mission
        fields = ['nom', 'date_debut', 'date_fin', 'heure_debut', 'heure_fin', 'comment', 'incident']
    
    # def clean_vacation_equipe(self, societe):
    #     '''
    #     Verify name is available.
    #     '''
    #     date_debut = self.cleaned_data.get('date_debut')
    #     date_fin = self.cleaned_data.get('date_fin')
    #     heure_debut = self.cleaned_data.get('heure_debut')
    #     heure_fin = self.cleaned_data.get('heure_fin')
        
    #     if date_debut > date_fin:
    #         raise forms.ValidationError("Veuillez vérifier la saisie des dates")
    #     if date_debut == date_fin and heure_debut > heure_fin:
    #         raise forms.ValidationError("Veuillez vérifier la saisie des dates")

    #     if societe is None:
    #         raise forms.ValidationError("Vous ne pouvez pas ajouter de vacations")
        
    #     return super().clean()

    def save(self, request, commit=True):
        # Save the provided password in hashed format
        vacation = super(VacationEquipeForm, self).save(commit=False)
        
        vacation.societe = request.user.societe
        # self.clean_vacation_equipe(vacation.societe)
        # user.active = False # send confirmation email
        if commit:
            vacation.save()
        return vacation

class EquipeForm(forms.ModelForm):
    nom_equipe = forms.CharField(required=False, label="Equipe", initial="Equipe ",widget=forms.TextInput(attrs={'class':'form-control'}))
    #responsable_equipe = forms.ModelChoiceField(queryset=Agent.objects.all())
    #agents = forms.ModelMultipleChoiceField(queryset=Agent.objects.all(), widget=forms.CheckboxSelectMultiple)

    societe = forms.ModelChoiceField(required=False,queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Equipe
        fields = ['nom_equipe']

    # def clean_equipe(self, societe):
    #     '''
    #     Verify name is available.
    #     '''
    #     cleaned_data = super().clean()
    #     responsable_equipe = cleaned_data.get("responsable_equipe")
        
    #     if responsable_equipe is None:
    #         raise forms.ValidationError("Veuillez vérifier la saisie des dates")

    #     if societe is None:
    #         raise forms.ValidationError("Vous ne pouvez pas ajouter de vacations")
        
    #     return super().clean()

    # def save(self, request, commit=True):
    #     # Save the provided password in hashed format
    #     equipe = super(EquipeForm, self).save(commit=False)
        
    #     equipe.societe = request.user.societe
    #     #self.clean_equipe(equipe.societe)
    #     # user.active = False # send confirmation email
    #     if commit:
    #         equipe.save()
    #     return equipe


class MissionForm(forms.ModelForm):
    nom = forms.CharField(label="Mission",widget=forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':'Exemple: Parc des bruyéres'}))
    # equipe = forms.ModelMultipleChoiceField(queryset=Equipe.objects.all(), widget=forms.CheckboxSelectMultiple)
    nature_mission = forms.CharField(required=False, label="Description", widget=forms.Textarea(attrs={'class':'form-control', 'style':'max-height: 150px'}))
    criteres = forms.CharField(required=False, label="Critéres", widget=forms.Textarea(attrs={'class':'form-control', 'style':'max-height: 150px'}))

    date_debut = forms.DateField(label="Date de début mission", initial=timezone.datetime.now().strftime('%Y-%m-%d'), widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control','type':'date'}))
    date_fin = forms.DateField(label="Date de fin de la mission ", initial=timezone.datetime.now().strftime('%Y-%m-%d'), widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control','type':'date'}))
    heure_debut = forms.TimeField(label="Commence à", widget=forms.TimeInput(format='%H:%M',attrs={'class': 'form-control','type':'time'}))
    heure_fin = forms.TimeField(label="Finit à", widget=forms.TimeInput(format='%H:%M',attrs={'class': 'form-control','type':'time'}))
    site = forms.CharField(required=False, label="Site", widget=forms.TextInput(attrs={'class':'form-control'}))
    # client = forms.ModelChoiceField(required=False, queryset=Client.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    
    societe = forms.ModelChoiceField(required=False,queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Mission
        fields = ['nom', 'nature_mission', 'criteres', 'date_debut', 'date_fin', 'heure_debut', 'heure_fin', 'site']

    def clean_mission(self, societe):
        '''
        Verify date is available.
        '''
        date_debut = self.cleaned_data.get('date_debut')
        date_fin = self.cleaned_data.get('date_fin')
        heure_debut = self.cleaned_data.get('heure_debut')
        heure_fin = self.cleaned_data.get('heure_fin')
        
        if date_debut > date_fin:
            raise forms.ValidationError("Veuillez vérifier la saisie des dates")
        if date_debut == date_fin and heure_debut > heure_fin:
            raise forms.ValidationError("Veuillez vérifier la saisie des dates")

        if societe is None:
            raise forms.ValidationError("Vous ne pouvez pas ajouter de vacations")
        
        return super().clean()

    # def save(self, request, commit=True):
    #     # Save the provided password in hashed format
    #     mission = super(MissionForm, self).save(commit=False)
        
    #     # mission.societe = request.user.societe
    #     self.clean_mission(request.user.societe)
    #     # user.active = False # send confirmation email
    #     if commit:
    #         mission.save()
    #     return mission


class ReponseVacationForm(forms.Form):
    etat_mission = forms.ChoiceField(required=True, label="Veillez cliquer sur le menu déroulant pour choisir votre réponse", choices=Status.choices, initial = Status.EN_ATTENTE, widget=forms.Select(attrs={'class': 'form-control'}))
    commentaire = forms.CharField(required=False, label="Commentaire", widget=forms.Textarea(attrs={'class':'form-control'}))

# class FilterForm(forms.Form):
#     code_postal = forms.CharField(required=False, label="Code postal", widget=forms.TextInput(attrs={'class':'form-control'}))
#     diplomes = forms.ModelMultipleChoiceField(queryset=Diplome_agent.objects.all(), widget=forms.CheckboxSelectMultiple)
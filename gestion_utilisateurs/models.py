from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin
)

class Societe(models.Model):
    nom = models.CharField(max_length=507)
    #administrateur = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15,blank=True)
    rue1 = models.CharField(max_length=50,blank=True)
    rue2 = models.CharField(max_length=50,blank=True)
    code_postal = models.CharField(max_length=5,blank=True)
    ville = models.CharField(max_length=50,blank=True)
    pays = models.CharField(max_length=50,blank=True,default='FRANCE')
    boite_postale = models.CharField(max_length=50,blank=True)
    # active = models.BooleanField(default=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nom)

class UserManager(BaseUserManager):

    def create_user(self, username, email, password, societe):
        # if not societe and:
        #     raise ValueError("Un utilisateur doit avoir une societe")
        if email is None:
            raise TypeError("Un utilisateur doit avoir un adresse email")
        if password is None:
            raise TypeError("Un utilisateur doit avoir un mot de passe")

        user_obj = self.model(
            username = username,
            email = self.normalize_email(email)
        )
        user_obj.societe = societe
        user_obj.staff = False
        user_obj.admin = False
        user_obj.active = False
        user_obj.set_password(password)
        user_obj.save(using=self.db)
        return user_obj

    def create_staffuser(self, username, email, password, societe):
        user = self.create_user(
            username,
            email,
            password,
            societe
        )
        user.staff = True
        user.admin = False
        user.active = False
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password, societe=None):
        user = self.create_user(
            username,
            email,
            password,
            societe
        )
        user.staff = True
        user.admin = True
        user.active = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=255,blank=True)
    email = models.EmailField(
        verbose_name='adresse email',
        max_length=255,
        unique=True,
    )
    is_verified = models.BooleanField(default=False) # can login
    active = models.BooleanField(default=False) # can login
    responsable = models.BooleanField(default=False) # can view his vacations
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.staff

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.admin

    @property
    def is_active(self):
        "Is the user a responsible?"
        return self.active

    @property
    def is_responsable(self):
        "Is the user a responsible?"
        return self.responsable

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

class Fonctionnalites(models.Model) :
    nom = models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

class Detailsfonctionnalites(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE,null=True)
    fonction = models.ForeignKey(Fonctionnalites, on_delete=models.CASCADE)
    valide = models.BooleanField(default=False)
    date_delivrance = models.DateField()
    date_expiration = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
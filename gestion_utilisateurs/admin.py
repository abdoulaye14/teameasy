from django.contrib import admin
from django.contrib.auth import get_user_model
from gestion_utilisateurs.models import Societe
from gestion_activites.models import (
    Mission,
    Agent,
    Client,
    Equipe,
    Diplome,
    Vacation_agent,
    Details_mission,
    Details_diplome
)
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
# Register your models here.

User = get_user_model()
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['username','email','societe','active','staff','admin']
    list_filter = ['societe','active','staff','admin']
    fieldsets = (
        (None, {'fields': ('societe', 'username', 'email', 'password')}),
        #('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('societe', 'email', 'password', 'password_2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(Societe)
admin.site.register(Mission)
admin.site.register(Client)
admin.site.register(Equipe)
admin.site.register(Agent)
admin.site.register(Diplome)
admin.site.register(Details_diplome)
admin.site.register(Details_mission)
admin.site.register(Vacation_agent)
admin.site.register(User, UserAdmin)
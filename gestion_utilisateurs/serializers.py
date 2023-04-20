from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, societe, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        socitete = societe
        if not username.isalnum():
            raise serializers.ValidationError('Votre nom d\'utilisateur ne doit contenir que des les lettres alphanumériques')
        if not societe:
            raise serializers.ValidationError('Vous n\'êtes pas habilité à ajouter un utilisateur, veuillez contacter votre administrateur')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
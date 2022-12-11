from django import forms
from .models import ActivityParticepationList
from .models import Activity
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class JoinActivityForm(forms.ModelForm):
    class Meta:
        model = ActivityParticepationList
        fields = (
            'userID',
            'activityID'
        )

class CreateActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            '__all__'
        )

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username", 
            "first_name", 
            "last_name", 
            "password1", 
            "password2", 
            "userBio", 
            "profileImage"
        ]

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username", 
            "first_name", 
            "last_name",
            "userBio",
            "profileImage"
        ]

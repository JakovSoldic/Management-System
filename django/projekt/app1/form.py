from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role, Subject

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label='Role')
    status = forms.ChoiceField(choices=User.STATUS_CHOICES, label='Status')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'status']

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        status = cleaned_data.get('status')

        if role and status:
            if role.role in ['admin', 'professor'] and status != 'none':
                self.add_error('status', "Status must be 'None' for admin or professor roles.")
            elif role.role == 'student' and status not in ['izvanredni', 'redovni']:
                self.add_error('status', "Status must be 'izvanredni' or 'redovni' for student role.")

        return cleaned_data

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'program', 'points', 'sem_red', 'sem_izv', 'izborni', 'carrier']

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','status']

class ProfessorUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class EnrollmentForm(forms.Form):
    subject_id = forms.IntegerField(widget=forms.HiddenInput())
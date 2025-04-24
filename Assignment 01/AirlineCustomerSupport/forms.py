from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SupportRequest, Message

class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        if commit:
            user.save()
        return user

class SupportRequestForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['issue_type', 'subject', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your issue here...'}),
        }
        labels = {
            'issue_type': 'Issue Type',
            'subject': 'Subject',
            'description': 'Description',
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your message here...'}),
        }
        labels = {
            'content': 'Message',
        }

class ManualUserCreateForm(UserCreationForm):
    ROLE_CHOICES = [
        ('support', 'Support Agent'),
        ('admin', 'System Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    staff_id = forms.CharField(max_length=6, help_text='6-digit Staff ID')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'staff_id']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.staff_id = self.cleaned_data['staff_id']
        if commit:
            user.save()
        return user

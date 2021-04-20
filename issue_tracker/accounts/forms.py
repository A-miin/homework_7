from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import Profile

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        fields=['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if first_name=='' and last_name=='':
            raise forms.ValidationError('Должно быть заполнено хотя бы одно из полей имени или фамилии!')

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя', 'last_name' : 'Фамилия', 'email':'Почта'}

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude=['user']


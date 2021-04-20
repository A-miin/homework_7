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

class PasswordUpdateForm(forms.ModelForm):
    password = forms.CharField(label="New password", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm password", strip=False, widget=forms.PasswordInput)
    old_password = forms.CharField(label="Old password", strip=False, widget=forms.PasswordInput)
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password_confirm and password and (password!=password_confirm):
            raise forms.ValidationError('Password confirm error!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Old password error')
        return old_password

    def save(self, commit = True):
        user = self.instance
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']



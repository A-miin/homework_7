from django.contrib.auth.forms import UserCreationForm
from django import forms


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

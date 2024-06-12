from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import DateField, CharField, Textarea, NumberInput
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'registration/login.html'


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    date_of_birth = DateField(widget=NumberInput(attrs={'type': 'date'}))
    biography = CharField(label='Tell us your story with movies.', widget=Textarea)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)  # creates instance of User
        date_of_birth = self.cleaned_data['date_of_birth']  # take information about Profile
        biography = self.cleaned_data['biography']
        profile = Profile(user=user, date_of_birth=date_of_birth, biography=biography)  # creates instance of Profile
        if commit:
            profile.save()
        return user


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')


# TODO: ProfileListView - seznam všech profilů
# TODO: ProfileDetailView - informace z konkrétního profilu
# ProfileCreateView - nemusíme řešit - profil se vytváří při signup
# TODO: ProfileUpdateView
# TODO: ProfileDeleteView


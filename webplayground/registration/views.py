from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
# from django.views.generic.base import TemplateView
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    #succes_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    def get_success_url(self):
        return reverse_lazy('login') +'?register'
    
    
    def get_form(self,form_class=None):
        form = super(SignUpView,self).get_form()
        #modificamos en el acto
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Introduzca Nombre Usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Introduzca email Usuario'})
        form.fields['password1'].widget = forms.PasswordInput (attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput (attrs={'class':'form-control mb-2', 'placeholder':'Repite la contraseña'})
        
        return form
    
@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):  # en lugar de TemplateView
    form_class=ProfileForm
    success_url= reverse_lazy('profile')
    # fields = ['avatar','bio', 'link']
    template_name = "registration/profile_form.html"

    def get_object(self):
        # recuperamos al usuario a editar
        profile, created= Profile.objects.get_or_create(user=self.request.user)
        return profile


@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):  # en lugar de TemplateView
    form_class=EmailForm
    success_url= reverse_lazy('profile')
    template_name = "registration/profile_email_form.html"

    def get_object(self):
        # recuperamos al usuario a editar
        # profile, created= Profile.objects.get_or_create(user=self.request.user)
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super(EmailUpdate,self).get_form()
        #modificamos en el acto
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'email'})
        return form
    

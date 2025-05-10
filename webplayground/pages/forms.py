from django import forms
from .models import Page


class PageForm(forms.ModelForm):
    class Meta:
        model = Page  # Aquí se debe especificar el modelo
        fields = ['title', 'content', 'order']  # Los campos del formulario
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Introduzca Título'}),
            'content': forms.Textarea (attrs={'class':'form-control','placeholder':'Introduzca contenido'}),
            'order':forms.NumberInput(attrs={'class':'form-control'}),
        }
        labels = {
            'title': '', 'content': '', 'order':'',
        }
        
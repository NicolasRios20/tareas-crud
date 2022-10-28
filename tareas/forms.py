from django.forms import ModelForm
from .models import tarea

class TareaForm(ModelForm):
    class Meta:
        model = tarea
        fields = ['titulo', 'descripcion', 'importante']
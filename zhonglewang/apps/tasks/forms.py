from django import forms
from .models import Tasks

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('avatar','title','content','tags','category','reward','mode')
from django import forms
from .models import Articles

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('title','body')
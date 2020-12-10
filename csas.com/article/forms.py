from django import forms
from django.contrib.auth import get_user_model
from .models import Article, Tag, Tagmap

User = get_user_model()

class ArticleSearchFrom(forms.Form):
    key_word = forms.CharField(
        label='key word', requeired=False,
        widget=forms.TextInput(attrs={'class': 'input'})
    )
    tag = forms.ModelChoiceField(
        label='tag', required=False,
        queryset=Tag.objects.all(),
    )

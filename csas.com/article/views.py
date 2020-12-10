from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.db.models import Q
from .models import Article, Tag, Tagmap

class ArticleList(generic.ListView):
    model = Article
    ordering = '-updated'

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            object_list = Article.objects.filter(
                Q(title__icontains=q_word) | Q(text__icontains=q_word)
            )
        else:
            object_list = Article.objects.all()
        return object_list

class ArticleDetail(generic.DetailView):
    model = Article

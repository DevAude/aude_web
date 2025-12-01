"""
Configuration des URLs pour le blog
Conventions :
- Namespace 'blog' pour éviter conflits
- Slugs SEO-friendly
- Nommage cohérent des routes
"""

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Liste des articles (page principale)
    path('', views.ArticleListView.as_view(), name='article_list'),

    # Détail d'un article
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),

    # Articles par catégorie
    path('categorie/<slug:slug>/', views.CategorieDetailView.as_view(), name='categorie_detail'),

    # Articles par tag
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
]

"""
EXEMPLES D'URLS GÉNÉRÉES :
- /blog/                                    → Liste tous les articles
- /blog/?categorie=innovation               → Filtre par catégorie
- /blog/?tag=ia                             → Filtre par tag
- /blog/?q=btp                              → Recherche
- /blog/article/intelligence-revolutionne-btp/  → Détail article
- /blog/categorie/innovation/               → Tous les articles "Innovation"
- /blog/tag/ia/                             → Tous les articles avec tag "IA"
"""

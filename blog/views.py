from django.shortcuts import render

# Create your views here.
def blog(request):
    return render(request, 'article_list.html')
"""
Vues pour le blog Aude
Conventions Django :
- Utilisation de Class-Based Views pour réutilisabilité
- Optimisation avec select_related/prefetch_related
- Pagination intégrée
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.utils import timezone

from .models import Article, Categorie, Tag


class ArticleListView(ListView):
    """
    Vue liste des articles de blog avec pagination et filtres
    """
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 9  # 3 colonnes x 3 lignes

    def get_queryset(self):
        """
        Requête optimisée avec tous les filtres possibles
        """
        queryset = Article.objects.filter(
            statut='publie',
            date_publication__lte=timezone.now()
        ).select_related(
            'categorie',
            'auteur',
            'auteur__user'
        ).prefetch_related(
            'tags'
        )

        # Filtre par catégorie (ex: ?categorie=innovation)
        categorie_slug = self.request.GET.get('categorie')
        if categorie_slug:
            queryset = queryset.filter(categorie__slug=categorie_slug)

        # Filtre par tag (ex: ?tag=ia)
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # Recherche textuelle (ex: ?q=btp)
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(titre__icontains=search_query) |
                Q(resume__icontains=search_query) |
                Q(contenu__icontains=search_query)
            )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        """
        Ajouter des données contextuelles pour les filtres
        """
        context = super().get_context_data(**kwargs)

        # Toutes les catégories avec compteur d'articles
        context['categories'] = Categorie.objects.annotate(
            nb_articles=Count('articles', filter=Q(articles__statut='publie'))
        ).filter(nb_articles__gt=0)

        # Tous les tags populaires
        context['tags_populaires'] = Tag.objects.annotate(
            nb_articles=Count('articles', filter=Q(articles__statut='publie'))
        ).filter(nb_articles__gt=0).order_by('-nb_articles')[:10]

        # Article en vedette (si aucun filtre actif)
        if not any([self.request.GET.get('categorie'),
                   self.request.GET.get('tag'),
                   self.request.GET.get('q')]):
            context['article_vedette'] = Article.objects.filter(
                statut='publie',
                en_vedette=True
            ).select_related('categorie', 'auteur').first()

        # Paramètres de recherche actifs
        context['categorie_active'] = self.request.GET.get('categorie')
        context['tag_actif'] = self.request.GET.get('tag')
        context['recherche'] = self.request.GET.get('q')

        return context


class ArticleDetailView(DetailView):
    """
    Vue détail d'un article avec incrément des vues
    """
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """
        Requête optimisée pour le détail
        """
        return Article.objects.filter(
            statut='publie',
            date_publication__lte=timezone.now()
        ).select_related(
            'categorie',
            'auteur',
            'auteur__user'
        ).prefetch_related(
            'tags'
        )

    def get_object(self, queryset=None):
        """
        Récupération de l'article avec incrément des vues
        """
        obj = super().get_object(queryset)

        # Incrémenter les vues (uniquement si pas en mode preview)
        if not self.request.GET.get('preview'):
            obj.incrementer_vues()

        return obj

    def get_context_data(self, **kwargs):
        """
        Données supplémentaires pour la page détail
        """
        context = super().get_context_data(**kwargs)

        # Articles similaires/liés
        context['articles_lies'] = self.object.get_articles_lies(limit=3)

        # Article précédent
        context['article_precedent'] = Article.objects.filter(
            statut='publie',
            date_publication__lt=self.object.date_publication
        ).order_by('-date_publication').first()

        # Article suivant
        context['article_suivant'] = Article.objects.filter(
            statut='publie',
            date_publication__gt=self.object.date_publication
        ).order_by('date_publication').first()

        return context


class CategorieDetailView(ListView):
    """
    Vue pour afficher tous les articles d'une catégorie
    """
    model = Article
    template_name = 'categorie_detail.html'
    context_object_name = 'articles'
    paginate_by = 9

    def get_queryset(self):
        """Articles de la catégorie sélectionnée"""
        self.categorie = get_object_or_404(
            Categorie,
            slug=self.kwargs['slug']
        )

        return Article.objects.filter(
            statut='publie',
            categorie=self.categorie,
            date_publication__lte=timezone.now()
        ).select_related(
            'categorie',
            'auteur'
        ).prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorie'] = self.categorie
        return context


class TagDetailView(ListView):
    """
    Vue pour afficher tous les articles d'un tag
    """
    model = Article
    template_name = 'tag_detail.html'
    context_object_name = 'articles'
    paginate_by = 9

    def get_queryset(self):
        """Articles avec le tag sélectionné"""
        self.tag = get_object_or_404(
            Tag,
            slug=self.kwargs['slug']
        )

        return Article.objects.filter(
            statut='publie',
            tags=self.tag,
            date_publication__lte=timezone.now()
        ).select_related(
            'categorie',
            'auteur'
        ).prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


# Vue fonction alternative (plus simple pour la liste)
def article_list_fonction(request):
    """
    Alternative en vue fonction (plus flexible pour customisation)
    """
    articles = Article.objects.filter(
        statut='publie',
        date_publication__lte=timezone.now()
    ).select_related('categorie', 'auteur').prefetch_related('tags')

    # Filtres
    categorie_slug = request.GET.get('categorie')
    if categorie_slug:
        articles = articles.filter(categorie__slug=categorie_slug)

    context = {
        'articles': articles,
        'categories': Categorie.objects.all(),
    }

    return render(request, 'article_list.html', context)

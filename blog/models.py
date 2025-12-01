"""
Modèles de données pour le blog Aude
Conventions Django :
- Noms de classes en PascalCase
- Noms de champs en snake_case
- related_name explicites pour éviter les conflits
- Auteur auto-attribué à l'utilisateur connecté
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class Categorie(models.Model):
    """
    Catégories principales du blog (IA, Innovation, ROI, Étude de cas, etc.)
    """
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la catégorie"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Généré automatiquement depuis le nom"
    )
    description = models.TextField(
        blank=True,
        help_text="Description courte de la catégorie"
    )
    icone = models.CharField(
        max_length=50,
        blank=True,
        help_text="Classe Bootstrap Icons (ex: bi-lightbulb)"
    )
    ordre = models.IntegerField(
        default=0,
        help_text="Ordre d'affichage (plus petit = premier)"
    )

    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        """Génération automatique du slug si absent"""
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL canonique de la catégorie"""
        return reverse('blog:categorie_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    """
    Étiquettes multiples pour classifier les articles
    """
    nom = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom du tag"
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        blank=True
    )
    couleur = models.CharField(
        max_length=7,
        default="#6366f1",
        help_text="Code hexadécimal (ex: #6366f1)"
    )

    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Auteur(models.Model):
    """
    Profil auteur étendu (au-delà du User Django)
    Créé automatiquement lors de la première création d'article
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil_auteur'
    )
    bio = models.TextField(
        blank=True,
        help_text="Biographie courte de l'auteur"
    )
    photo = models.ImageField(
        upload_to='auteurs/',
        blank=True,
        null=True,
        help_text="Photo de profil"
    )
    poste = models.CharField(
        max_length=100,
        blank=True,
        help_text="Poste/titre (ex: Expert BTP Digital)"
    )
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_nombre_articles(self):
        """Nombre d'articles publiés"""
        return self.articles.filter(statut='publie').count()


class Article(models.Model):
    """
    Article de blog principal
    L'auteur est automatiquement défini à partir de l'utilisateur connecté
    """

    # Choix de statut
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('archive', 'Archivé'),
    ]

    # Champs principaux
    titre = models.CharField(
        max_length=200,
        verbose_name="Titre de l'article"
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        help_text="URL de l'article (généré automatiquement)"
    )
    resume = models.TextField(
        max_length=300,
        help_text="Résumé court pour les cartes (max 300 caractères)"
    )
    contenu = models.TextField(
        help_text="Contenu complet de l'article (Markdown supporté)"
    )

    # Médias
    image_couverture = models.ImageField(
        upload_to='blog/covers/%Y/%m/',
        help_text="Image principale (recommandé: 1200x630px)"
    )
    image_alt = models.CharField(
        max_length=200,
        blank=True,
        help_text="Texte alternatif pour l'accessibilité"
    )

    # Métadonnées
    temps_lecture = models.IntegerField(
        default=5,
        help_text="Temps de lecture estimé (en minutes)"
    )
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='brouillon'
    )
    vues = models.IntegerField(
        default=0,
        editable=False,
        help_text="Nombre de vues"
    )

    # Relations
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name='articles',
        help_text="Catégorie principale"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True,
        help_text="Tags multiples"
    )
    auteur = models.ForeignKey(
        Auteur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        editable=False,  # ⭐ Auto-attribué dans l'admin
        help_text="Auteur (défini automatiquement)"
    )

    # Dates
    date_publication = models.DateTimeField(
        default=timezone.now,
        help_text="Date de publication visible"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    # SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Description pour les moteurs de recherche (160 caractères max)"
    )

    # Options avancées
    en_vedette = models.BooleanField(
        default=False,
        help_text="Mettre en avant sur la page d'accueil"
    )
    autoriser_commentaires = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication']
        indexes = [
            models.Index(fields=['-date_publication']),
            models.Index(fields=['slug']),
            models.Index(fields=['statut']),
        ]

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        """Génération automatique du slug et de la meta_description"""
        if not self.slug:
            self.slug = slugify(self.titre)

        if not self.meta_description:
            self.meta_description = self.resume[:160]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL canonique de l'article"""
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

    def incrementer_vues(self):
        """Incrémenter le compteur de vues de manière atomique"""
        self.vues = models.F('vues') + 1
        self.save(update_fields=['vues'])
        self.refresh_from_db()

    def get_articles_lies(self, limit=3):
        """Articles similaires (même catégorie ou tags communs)"""
        return Article.objects.filter(
            statut='publie'
        ).filter(
            models.Q(categorie=self.categorie) | models.Q(tags__in=self.tags.all())
        ).exclude(
            id=self.id
        ).distinct()[:limit]

    @property
    def est_publie(self):
        """Vérifie si l'article est publié et visible"""
        return (
            self.statut == 'publie' and
            self.date_publication <= timezone.now()
        )

"""
Configuration de l'interface d'administration Django pour le blog
Conventions :
- list_display pour affichage optimal
- list_filter et search_fields pour faciliter recherche
- prepopulated_fields pour slugs automatiques
- Auto-attribution de l'auteur à l'utilisateur connecté
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Article, Categorie, Tag, Auteur


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    """
    Administration des catégories
    """
    list_display = ['nom', 'slug', 'nb_articles', 'ordre', 'date_creation']
    list_editable = ['ordre']
    search_fields = ['nom', 'description']
    prepopulated_fields = {'slug': ('nom',)}
    readonly_fields = ['date_creation', 'date_modification']

    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'slug', 'description')
        }),
        ('Apparence', {
            'fields': ('icone', 'ordre')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )

    def nb_articles(self, obj):
        """Affiche le nombre d'articles dans la catégorie"""
        count = obj.articles.filter(statut='publie').count()
        url = reverse('admin:blog_article_changelist') + f'?categorie__id__exact={obj.id}'
        return format_html('<a href="{}">{} articles</a>', url, count)
    nb_articles.short_description = 'Articles publiés'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Administration des tags
    """
    list_display = ['nom', 'couleur_preview', 'slug', 'nb_articles', 'date_creation']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}
    readonly_fields = ['date_creation']

    def couleur_preview(self, obj):
        """Affiche un aperçu de la couleur"""
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; '
            'background-color: {}; border-radius: 4px; border: 1px solid #ddd;"></span>',
            obj.couleur
        )
    couleur_preview.short_description = 'Couleur'

    def nb_articles(self, obj):
        """Nombre d'articles avec ce tag"""
        count = obj.articles.filter(statut='publie').count()
        return f"{count} article{'s' if count > 1 else ''}"
    nb_articles.short_description = 'Utilisations'


@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    """
    Administration des auteurs
    """
    list_display = ['user', 'poste', 'photo_preview', 'nb_articles_publie', 'date_creation']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'poste']
    readonly_fields = ['date_creation', 'photo_preview_large']

    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Profil public', {
            'fields': ('poste', 'bio', 'photo', 'photo_preview_large')
        }),
        ('Réseaux sociaux', {
            'fields': ('linkedin', 'twitter'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )

    def photo_preview(self, obj):
        """Miniature de la photo dans la liste"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; '
                'border-radius: 50%; object-fit: cover;" />',
                obj.photo.url
            )
        return '-'
    photo_preview.short_description = 'Photo'

    def photo_preview_large(self, obj):
        """Grande prévisualisation dans le formulaire"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 200px; border-radius: 12px;" />',
                obj.photo.url
            )
        return 'Aucune photo'
    photo_preview_large.short_description = 'Aperçu de la photo'

    def nb_articles_publie(self, obj):
        """Nombre d'articles publiés par l'auteur"""
        return obj.get_nombre_articles()
    nb_articles_publie.short_description = 'Articles publiés'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Administration des articles avec auto-attribution de l'auteur
    """
    list_display = [
        'titre',
        'statut_badge',
        'categorie',
        'auteur',
        'date_publication',
        'vues',
        'en_vedette',
        'actions_rapides'
    ]
    list_filter = [
        'statut',
        'categorie',
        'en_vedette',
        'date_publication',
        'auteur'
    ]
    search_fields = ['titre', 'resume', 'contenu']
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'
    readonly_fields = [
        'vues',
        'date_creation',
        'date_modification',
        'image_preview',
        'auteur_display'
    ]

    filter_horizontal = ['tags']

    fieldsets = (
        ('Contenu principal', {
            'fields': ('titre', 'slug', 'resume', 'contenu')
        }),
        ('Classification', {
            'fields': ('categorie', 'tags')
        }),
        ('Auteur', {
            'fields': ('auteur_display',),
            'description': 'L\'auteur est automatiquement défini à partir de votre compte utilisateur.'
        }),
        ('Image de couverture', {
            'fields': ('image_couverture', 'image_alt', 'image_preview')
        }),
        ('Publication', {
            'fields': ('statut', 'date_publication', 'temps_lecture')
        }),
        ('Options avancées', {
            'fields': ('en_vedette', 'autoriser_commentaires', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('vues', 'date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )

    actions = ['publier_articles', 'mettre_en_brouillon', 'archiver_articles']

    def auteur_display(self, obj):
        """Afficher l'auteur de manière readonly avec style"""
        if obj.auteur:
            return format_html(
                '<div style="padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
                'border-radius: 12px; color: white; display: inline-block;">'
                '<i class="bi bi-person-circle"></i> <strong>{}</strong><br>'
                '<small style="opacity: 0.9;">{}</small>'
                '</div>',
                obj.auteur,
                obj.auteur.poste or 'Auteur'
            )
        return format_html(
            '<div style="padding: 12px; background: #fff3cd; border-radius: 12px; '
            'color: #856404; border: 2px dashed #ffc107;">'
            '<i class="bi bi-info-circle"></i> <strong>Auto-attribution</strong><br>'
            '<small>L\'auteur sera défini automatiquement lors de la sauvegarde</small>'
            '</div>'
        )
    auteur_display.short_description = 'Auteur de l\'article'

    def save_model(self, request, obj, form, change):
        """
        Attribuer automatiquement l'auteur lors de la création
        """
        if not change:  # Seulement lors de la création
            try:
                # Récupérer ou créer le profil auteur de l'utilisateur connecté
                auteur, created = Auteur.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'poste': 'Contributeur Blog',
                        'bio': f'Auteur chez Aude - {request.user.get_full_name() or request.user.username}'
                    }
                )
                obj.auteur = auteur

                if created:
                    self.message_user(
                        request,
                        format_html(
                            '✅ Profil auteur créé automatiquement pour <strong>{}</strong>',
                            request.user.get_full_name() or request.user.username
                        ),
                        level='SUCCESS'
                    )
                else:
                    self.message_user(
                        request,
                        format_html(
                            'ℹ️ Article attribué à <strong>{}</strong>',
                            auteur
                        ),
                        level='INFO'
                    )

            except Exception as e:
                self.message_user(
                    request,
                    f'❌ Erreur lors de l\'attribution de l\'auteur : {str(e)}',
                    level='ERROR'
                )

        super().save_model(request, obj, form, change)

    def statut_badge(self, obj):
        """Badge coloré pour le statut"""
        colors = {
            'publie': '#10b981',
            'brouillon': '#f59e0b',
            'archive': '#6b7280'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 12px; font-weight: 600;">{}</span>',
            colors.get(obj.statut, '#6b7280'),
            obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'

    def image_preview(self, obj):
        """Prévisualisation de l'image de couverture"""
        if obj.image_couverture:
            return format_html(
                '<img src="{}" style="max-width: 400px; border-radius: 12px;" />',
                obj.image_couverture.url
            )
        return 'Aucune image'
    image_preview.short_description = 'Aperçu de l\'image'

    def actions_rapides(self, obj):
        """Boutons d'action rapides"""
        view_url = obj.get_absolute_url()
        return format_html(
            '<a class="button" href="{}" target="_blank" '
            'style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
            'color: white; padding: 6px 16px; border-radius: 50px; text-decoration: none; '
            'font-weight: 600;">Voir l\'article</a>',
            view_url
        )
    actions_rapides.short_description = 'Actions'

    # Actions personnalisées
    @admin.action(description='✅ Publier les articles sélectionnés')
    def publier_articles(self, request, queryset):
        updated = queryset.update(statut='publie')
        self.message_user(request, f'✅ {updated} article(s) publié(s) avec succès.')

    @admin.action(description='📝 Mettre en brouillon')
    def mettre_en_brouillon(self, request, queryset):
        updated = queryset.update(statut='brouillon')
        self.message_user(request, f'📝 {updated} article(s) mis en brouillon.')

    @admin.action(description='📦 Archiver les articles')
    def archiver_articles(self, request, queryset):
        updated = queryset.update(statut='archive')
        self.message_user(request, f'📦 {updated} article(s) archivé(s).')

    class Media:
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',)
        }


# Configuration du site admin
admin.site.site_header = "📰 Administration Blog Aude"
admin.site.site_title = "Blog Aude Admin"
admin.site.index_title = "Gestion du contenu"

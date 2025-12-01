from django.db import models

class HeroSection(models.Model):
    badge = models.CharField(
        max_length=255,
        default="LOGICIEL INTELLIGENT NOUVELLE GÉNÉRATION",
    )

    title_part1 = models.CharField(
        max_length=255,
        default="Révolutionnez",
        help_text="Texte en couleur (classe .text-gradient)"
    )

    title_part2 = models.CharField(
        max_length=255,
        default="votre gestion BTP & Architecture",
    )

    description = models.TextField(
        default=(
            "Aude combine algorithmes avancés et expertise métier pour vous offrir "
            "la solution la plus innovante du marché. Simplifiez vos projets, "
            "optimisez vos coûts et transformez votre façon de travailler dès aujourd'hui."
        )
    )

    primary_button_text = models.CharField(
        max_length=255,
        default="Démarrer mon essai gratuit"
    )
    primary_button_url = models.URLField(
        default="https://app.aude.ci"
    )

    secondary_button_text = models.CharField(
        max_length=255,
        default="Découvrir Aude"
    )
    secondary_button_modal_target = models.CharField(
        max_length=255,
        default="#videoModal",
        help_text="ID du modal Bootstrap"
    )

    image = models.ImageField(
        upload_to="hero/",
        default="hero/default.png",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Section Hero"
        verbose_name_plural = "Section Hero"

    def __str__(self):
        return "Section Hero"


class StatItem(models.Model):
    number = models.CharField(
        max_length=50,
        default="0"        # Exemple : 15, 30, 24/7, 0€
    )
    label = models.CharField(
        max_length=255,
        default="Nouvelle statistique"
    )
    animation_delay = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0
    )
    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ("order",)
        verbose_name = "Statistique"
        verbose_name_plural = "Statistiques"

    def __str__(self):
        return f"{self.number} — {self.label}"

class AdvantageItem(models.Model):
    icon = models.CharField(
        max_length=100,
        default="bi bi-lightning-charge-fill"   # Classe Bootstrap Icons
    )
    icon_color = models.CharField(
        max_length=20,
        default="#fbbf24"    # Couleur hex
    )
    title = models.CharField(
        max_length=255,
        default="Nouvel avantage"
    )
    description = models.TextField(
        default="Description de l’avantage."
    )
    footer_text = models.CharField(
        max_length=255,
        default=""
    )
    animation_delay = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0
    )
    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ("order",)
        verbose_name = "Avantage"
        verbose_name_plural = "Avantages"

    def __str__(self):
        return self.title


class CallToAction(models.Model):
    title = models.CharField(
        max_length=255,
        default="Prêt à Révolutionner Votre Gestion BTP ?"
    )

    subtitle = models.TextField(
        blank=True,
        null=True,
        default="Rejoignez plus de 2500 professionnels qui ont déjà transformé leur business avec Aude. Démarrez votre essai gratuit dès maintenant !"
    )

    primary_button_text = models.CharField(
        max_length=100,
        default="Commencer gratuitement"
    )
    primary_button_url = models.URLField(
        default="https://app.aude.ci"
    )

    secondary_button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Demander une démo"
    )
    secondary_button_url = models.URLField(
        blank=True,
        null=True,
        default="https://aude.ci/contact"
    )

    badge_1 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="30 jours gratuits"
    )
    badge_2 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Sans engagement"
    )
    badge_3 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Support inclus"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class AboutHero(models.Model):
    title = models.CharField(
        max_length=255,
        default="Au Cœur d'Aude : Notre Mission et Nos Valeurs"
    )

    subtitle = models.TextField(
        default="Animés par la passion de l'innovation et une compréhension profonde des défis du BTP..."
    )

    story_title = models.CharField(
        max_length=255,
        default="Notre Histoire : Née des Défis du Terrain"
    )
    story_text = models.TextField(
        default="Aude est le fruit d'une ambition : transformer radicalement la manière..."
    )

    vision_title = models.CharField(
        max_length=255,
        default="Notre Vision : L'Humain Augmenté par la Technologie"
    )
    vision_text = models.TextField(
        default="Nous croyons fermement que la technologie doit servir l'humain..."
    )

    button_text = models.CharField(
        max_length=100,
        default="Discutons de vos projets"
    )
    button_url = models.URLField(
        default="https://aude.ci/contact"
    )

    image = models.ImageField(
        upload_to="about/",
        default="about/apropos1.png"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class AboutPillar(models.Model):
    icon = models.CharField(
        max_length=100,
        default="bi-lightbulb-fill"
    )
    title = models.CharField(
        max_length=255,
        default="Innovation Continue"
    )
    text = models.TextField(
        default="Anticiper vos besoins futurs avec des technologies de pointe."
    )
    accent_color = models.CharField(
        max_length=50,
        default="var(--accent-secondary)"
    )
    animation_delay = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.3
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return self.title


class AboutStat(models.Model):
    number = models.CharField(
        max_length=50,
        default="2500"
    )
    label = models.CharField(
        max_length=255,
        default="Professionnels utilisateurs"
    )
    animation_delay = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return f"{self.number} — {self.label}"


class AboutCTA(models.Model):
    title = models.CharField(
        max_length=255,
        default="Prêt à Rejoindre l'Aventure Aude ?"
    )

    subtitle = models.TextField(
        default="Découvrez comment Aude peut transformer votre façon de travailler..."
    )

    primary_button_text = models.CharField(
        max_length=100,
        default="Commencer gratuitement"
    )
    primary_button_url = models.URLField(
        default="https://app.aude.ci"
    )

    secondary_button_text = models.CharField(
        max_length=100,
        default="Nous contacter"
    )
    secondary_button_url = models.URLField(
        default="https://aude.ci/contact"
    )

    badge_1 = models.CharField(
        max_length=100,
        default="30 jours gratuits"
    )
    badge_2 = models.CharField(
        max_length=100,
        default="Sans engagement"
    )
    badge_3 = models.CharField(
        max_length=100,
        default="Support dédié"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# -------------------------
# solution model
# -------------------------

# -------------------------
# SECTION 1 – Pour qui ?
# -------------------------

class SolutionAudienceCategory(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=100, help_text="Bootstrap Icon ex: bi bi-buildings")
    description = models.TextField()

    badge_1 = models.CharField(max_length=100, blank=True, null=True)
    badge_2 = models.CharField(max_length=100, blank=True, null=True)
    badge_3 = models.CharField(max_length=100, blank=True, null=True)

    bullet_1 = models.CharField(max_length=255, blank=True, null=True)
    bullet_2 = models.CharField(max_length=255, blank=True, null=True)
    bullet_3 = models.CharField(max_length=255, blank=True, null=True)
    bullet_4 = models.CharField(max_length=255, blank=True, null=True)

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title


# -------------------------
# SECTION 2 – Fonctionnalités BTP
# -------------------------

class SolutionFeatureBTP(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=100)
    description = models.TextField()

    badge_1 = models.CharField(max_length=100, blank=True, null=True)
    badge_2 = models.CharField(max_length=100, blank=True, null=True)
    badge_3 = models.CharField(max_length=100, blank=True, null=True)

    bullet_1 = models.CharField(max_length=255, blank=True, null=True)
    bullet_2 = models.CharField(max_length=255, blank=True, null=True)
    bullet_3 = models.CharField(max_length=255, blank=True, null=True)
    bullet_4 = models.CharField(max_length=255, blank=True, null=True)

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title


# -------------------------
# SECTION 3 – Fonctionnalités Architecture
# -------------------------

class SolutionFeatureArchitecture(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=100)
    description = models.TextField()

    badge_1 = models.CharField(max_length=100, blank=True, null=True)
    badge_2 = models.CharField(max_length=100, blank=True, null=True)
    badge_3 = models.CharField(max_length=100, blank=True, null=True)

    bullet_1 = models.CharField(max_length=255, blank=True, null=True)
    bullet_2 = models.CharField(max_length=255, blank=True, null=True)
    bullet_3 = models.CharField(max_length=255, blank=True, null=True)
    bullet_4 = models.CharField(max_length=255, blank=True, null=True)

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title


# -------------------------
# SECTION 4 – CTA Final
# -------------------------

class SolutionCTA(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500)

    primary_text = models.CharField(max_length=100)
    primary_url = models.URLField()

    secondary_text = models.CharField(max_length=100)
    secondary_url = models.URLField()

    highlight_1 = models.CharField(max_length=150, blank=True, null=True)
    highlight_2 = models.CharField(max_length=150, blank=True, null=True)
    highlight_3 = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.title


#

class PricingPlan(models.Model):
    """
    Modèle représentant les formules d'abonnement Aude
    """
    PLAN_CHOICES = [
        ('essentiel', 'Essentiel'),
        ('privilege', 'Privilège'),
        ('elite', 'Elite'),
        ('prestige', 'Prestige'),
    ]

    PERIOD_CHOICES = [
        ('monthly', 'Mensuel'),
        ('quarterly', 'Trimestriel'),
        ('biannual', 'Semestriel'),
        ('annual', 'Annuel'),
    ]

    # Identification du plan
    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        verbose_name="Type de formule"
    )
    period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        verbose_name="Période de facturation"
    )

    # Informations tarifaires
    price_eur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix en EUR",
        help_text="Prix par utilisateur"
    )
    price_cfa = models.IntegerField(
        verbose_name="Prix en F CFA",
        help_text="Prix par utilisateur"
    )

    # Informations d'affichage
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Plan mis en avant"
    )
    featured_badge = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Badge du plan vedette",
        help_text="Ex: ⭐ Le plus populaire"
    )

    # URLs d'action
    action_url = models.URLField(
        verbose_name="URL d'action",
        default="https://app.aude.ci"
    )
    action_text = models.CharField(
        max_length=50,
        verbose_name="Texte du bouton",
        default="Choisir"
    )

    # Métadonnées
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    display_order = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Formule tarifaire"
        verbose_name_plural = "Formules tarifaires"
        ordering = ['display_order', 'period']
        unique_together = ['plan_type', 'period']

    def __str__(self):
        return f"{self.get_plan_type_display()} - {self.get_period_display()}"

    def get_discount_percentage(self):
        """Retourne le pourcentage de réduction selon la période"""
        discounts = {
            'quarterly': 3.5,
            'biannual': 4,
            'annual': 5
        }
        return discounts.get(self.period, 0)


class PricingFeature(models.Model):
    """
    Modèle représentant les fonctionnalités incluses dans chaque formule
    """
    pricing_plan = models.ForeignKey(
        PricingPlan,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name="Formule tarifaire"
    )

    feature_text = models.CharField(
        max_length=200,
        verbose_name="Fonctionnalité"
    )

    is_bold = models.BooleanField(
        default=False,
        verbose_name="Texte en gras",
        help_text="Ex: 'Tout l'Essentiel +'"
    )

    display_order = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )

    class Meta:
        verbose_name = "Fonctionnalité tarifaire"
        verbose_name_plural = "Fonctionnalités tarifaires"
        ordering = ['pricing_plan', 'display_order']

    def __str__(self):
        return f"{self.pricing_plan.plan_type} - {self.feature_text}"


class FAQ(models.Model):
    """
    Modèle pour les questions fréquentes
    """
    question = models.CharField(
        max_length=300,
        verbose_name="Question"
    )

    answer = models.TextField(
        verbose_name="Réponse"
    )

    icon_class = models.CharField(
        max_length=50,
        default="bi bi-plus-circle",
        verbose_name="Classe d'icône Bootstrap"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    display_order = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Question fréquente"
        verbose_name_plural = "Questions fréquentes"
        ordering = ['display_order']

    def __str__(self):
        return self.question


class CTASection(models.Model):
    """
    Modèle pour la section Call-to-Action
    """
    PAGE_CHOICES = [
        ('pricing', 'Page Tarifs'),
        ('home', 'Page Accueil'),
        ('features', 'Page Fonctionnalités'),
    ]

    page = models.CharField(
        max_length=20,
        choices=PAGE_CHOICES,
        unique=True,
        verbose_name="Page"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Titre"
    )

    subtitle = models.TextField(
        verbose_name="Sous-titre"
    )

    # Bouton principal
    primary_text = models.CharField(
        max_length=50,
        verbose_name="Texte bouton principal"
    )
    primary_url = models.URLField(
        verbose_name="URL bouton principal"
    )
    primary_icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icône bouton principal",
        help_text="Classe Bootstrap Icon"
    )

    # Bouton secondaire
    secondary_text = models.CharField(
        max_length=50,
        verbose_name="Texte bouton secondaire"
    )
    secondary_url = models.CharField(
        max_length=200,
        verbose_name="URL bouton secondaire"
    )
    secondary_icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icône bouton secondaire"
    )

    # Points de réassurance
    highlight_1 = models.CharField(
        max_length=50,
        verbose_name="Point de réassurance 1"
    )
    highlight_1_icon = models.CharField(
        max_length=50,
        default="bi bi-shield-lock",
        verbose_name="Icône point 1"
    )

    highlight_2 = models.CharField(
        max_length=50,
        verbose_name="Point de réassurance 2"
    )
    highlight_2_icon = models.CharField(
        max_length=50,
        default="bi bi-credit-card-2-front-fill",
        verbose_name="Icône point 2"
    )

    highlight_3 = models.CharField(
        max_length=50,
        verbose_name="Point de réassurance 3"
    )
    highlight_3_icon = models.CharField(
        max_length=50,
        default="bi bi-headset",
        verbose_name="Icône point 3"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    class Meta:
        verbose_name = "Section CTA"
        verbose_name_plural = "Sections CTA"

    def __str__(self):
        return f"CTA - {self.get_page_display()}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du client")
    position = models.CharField(max_length=100, verbose_name="Poste / Fonction")
    company = models.CharField(max_length=100, verbose_name="Société")
    photo = models.ImageField(upload_to="testimonials/", null=True, blank=True, verbose_name="Photo")
    testimonial = models.TextField(verbose_name="Témoignage")
    tags = models.CharField(max_length=200, blank=True, help_text="Séparez les mots-clés par des virgules")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.company}"

    def get_tags_list(self):
        """Retourne les tags sous forme de liste."""
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

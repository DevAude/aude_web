from django.contrib import admin
from .models import HeroSection
from .models import StatItem
from .models import AdvantageItem
from .models import CallToAction
from .models import AboutHero, AboutPillar, AboutStat, AboutCTA
from .models import Testimonial



from .models import (
    SolutionAudienceCategory, SolutionFeatureBTP, SolutionFeatureArchitecture, SolutionCTA
)
from .models import PricingPlan, PricingFeature, FAQ, CTASection, Testimonial




@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company', 'created_at')
    search_fields = ('name', 'company', 'position', 'testimonial')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
    (None, {
    'fields': ('name', 'position', 'company', 'photo', 'testimonial', 'tags')
    }),
    ('Dates', {
    'fields': ('created_at', 'updated_at')
    }),
)
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "badge", "title_part1", "title_part2")
    list_display_links = ("id", "badge")
    ordering = ("id",)

    fieldsets = (
        ("Badge", {
            "fields": ("badge",)
        }),

        ("Titre", {
            "fields": ("title_part1", "title_part2")
        }),

        ("Description", {
            "fields": ("description",)
        }),

        ("Bouton principal", {
            "fields": ("primary_button_text", "primary_button_url")
        }),

        ("Bouton secondaire", {
            "fields": ("secondary_button_text", "secondary_button_modal_target")
        }),

        ("Image", {
            "fields": ("image",)
        }),
    )

    search_fields = ("badge", "title_part1", "title_part2")


@admin.register(StatItem)
class StatItemAdmin(admin.ModelAdmin):
    list_display = ("number", "label", "animation_delay", "order")
    list_editable = ("order",)
    search_fields = ("number", "label")
    list_filter = ("animation_delay",)

@admin.register(AdvantageItem)
class AdvantageItemAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "animation_delay")
    list_editable = ("order", "animation_delay")
    search_fields = ("title", "description", "footer_text")


@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")

@admin.register(AboutHero)
class AboutHeroAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    list_editable = ("is_active",)


@admin.register(AboutPillar)
class AboutPillarAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    search_fields = ("title",)


@admin.register(AboutStat)
class AboutStatAdmin(admin.ModelAdmin):
    list_display = ("number", "label", "order")
    list_editable = ("order",)
    search_fields = ("label", "number")


@admin.register(AboutCTA)
class AboutCTAAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    list_editable = ("is_active",)


@admin.register(SolutionAudienceCategory)
class SolutionAudienceCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "position")
    list_editable = ("position",)


@admin.register(SolutionFeatureBTP)
class SolutionFeatureBTPAdmin(admin.ModelAdmin):
    list_display = ("title", "position")
    list_editable = ("position",)


@admin.register(SolutionFeatureArchitecture)
class SolutionFeatureArchitectureAdmin(admin.ModelAdmin):
    list_display = ("title", "position")
    list_editable = ("position",)


@admin.register(SolutionCTA)
class SolutionCTAAdmin(admin.ModelAdmin):
    list_display = ("title",)


class PricingFeatureInline(admin.TabularInline):
    model = PricingFeature
    extra = 1
    fields = ('feature_text', 'is_bold', 'display_order')


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'period', 'price_eur', 'price_cfa', 'is_featured', 'is_active')
    list_filter = ('plan_type', 'period', 'is_featured', 'is_active')
    search_fields = ('plan_type',)
    inlines = [PricingFeatureInline]

    fieldsets = (
        ('Identification', {
            'fields': ('plan_type', 'period', 'display_order')
        }),
        ('Tarification', {
            'fields': ('price_eur', 'price_cfa')
        }),
        ('Mise en avant', {
            'fields': ('is_featured', 'featured_badge')
        }),
        ('Action', {
            'fields': ('action_url', 'action_text')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    list_editable = ('display_order',)


@admin.register(CTASection)
class CTASectionAdmin(admin.ModelAdmin):
    list_display = ('page', 'title', 'is_active')
    list_filter = ('page', 'is_active')

    fieldsets = (
        ('Configuration', {
            'fields': ('page', 'is_active')
        }),
        ('Contenu principal', {
            'fields': ('title', 'subtitle')
        }),
        ('Bouton principal', {
            'fields': ('primary_text', 'primary_url', 'primary_icon')
        }),
        ('Bouton secondaire', {
            'fields': ('secondary_text', 'secondary_url', 'secondary_icon')
        }),
        ('Points de réassurance', {
            'fields': (
                'highlight_1', 'highlight_1_icon',
                'highlight_2', 'highlight_2_icon',
                'highlight_3', 'highlight_3_icon'
            )
        }),
    )

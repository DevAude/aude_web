
# Create your views here.
from django.shortcuts import render
from .models import HeroSection
from .models import StatItem
from .models import AdvantageItem
from .models import CallToAction
from .models import AboutHero, AboutPillar, AboutStat, AboutCTA
from .models import SolutionAudienceCategory, SolutionFeatureBTP, SolutionFeatureArchitecture, SolutionCTA
from .models import PricingPlan, PricingFeature, FAQ, CTASection




def home(request):
    hero_section = HeroSection.objects.first()
    stats = StatItem.objects.all()
    ctas = CallToAction.objects.filter(is_active=True)

    advantages = AdvantageItem.objects.all()

    return render(request, "home.html", {"hero_section": hero_section, "stats": stats, "advantages": advantages,"ctas": ctas})


def a_propos(request):
    context = {
        "hero": AboutHero.objects.filter(is_active=True).first(),
        "pillars": AboutPillar.objects.all(),
        "stats": AboutStat.objects.all(),
        "cta": AboutCTA.objects.filter(is_active=True).first(),
    }
    return render(request, "a-propos.html", context)

def solutions(request):
    audiences = SolutionAudienceCategory.objects.all()
    btp_features = SolutionFeatureBTP.objects.all()
    archi_features = SolutionFeatureArchitecture.objects.all()
    cta = SolutionCTA.objects.first()
    return render(request, 'solutions.html', {'audiences': audiences, 'btp_features': btp_features, 'archi_features': archi_features, 'cta': cta})

def pricing_page(request):
    """
    Vue pour afficher la page des tarifs avec tous les plans, FAQ et CTA
    """

    # Récupérer tous les plans actifs avec leurs fonctionnalités
    # prefetch_related pour optimiser les requêtes (évite le N+1)
    plans = PricingPlan.objects.filter(
        is_active=True
    ).prefetch_related('features').order_by('period', 'display_order')

    # Récupérer les FAQ actives
    faqs = FAQ.objects.filter(
        is_active=True
    ).order_by('display_order')

    # Récupérer le CTA pour la page tarifs
    cta = CTASection.objects.filter(
        page='pricing',
        is_active=True
    ).first()

    # Préparer les choix de périodes avec les pourcentages de réduction
    period_choices = [
        ('monthly', 'Mensuel', 0),
        ('quarterly', 'Trimestriel', 3.5),
        ('biannual', 'Semestriel', 4),
        ('annual', 'Annuel', 5),
    ]

    context = {
        'plans': plans,
        'faqs': faqs,
        'cta': cta,
        'period_choices': period_choices,
    }

    return render(request, 'pricing/pricing_page.html', context)


# Vue alternative avec filtre par période (optionnel)
def tarifs(request):
    """
    Vue pour afficher la page des tarifs avec tous les plans
    """

    # Récupérer TOUS les plans actifs (pas de filtre par période)
    plans = PricingPlan.objects.filter(
        is_active=True
    ).prefetch_related('features').order_by('period', 'display_order')

    # Récupérer les FAQ actives
    faqs = FAQ.objects.filter(is_active=True).order_by('display_order')

    # Récupérer le CTA pour la page tarifs
    cta = CTASection.objects.filter(page='pricing', is_active=True).first()

    # Préparer les choix de périodes avec les pourcentages de réduction
    period_choices = [
        ('monthly', 'Mensuel', 0),
        ('quarterly', 'Trimestriel', 3.5),
        ('biannual', 'Semestriel', 4),
        ('annual', 'Annuel', 5),
    ]

    context = {
        'plans': plans,  # TOUS les plans (16 au total)
        'faqs': faqs,
        'cta': cta,
        'period_choices': period_choices,
    }

    return render(request, 'tarifs.html', context)

def contact(request):
    return render(request, 'contact.html')

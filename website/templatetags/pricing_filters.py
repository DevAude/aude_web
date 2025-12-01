"""
Filtres de template personnalisés pour la page tarifs

Fichier: your_app/templatetags/pricing_filters.py

IMPORTANT: Ce fichier doit être dans un dossier 'templatetags'
dans votre application Django.

Structure :
your_app/
    templatetags/
        __init__.py  (fichier vide)
        pricing_filters.py  (ce fichier)
"""

from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """
    Multiplie une valeur par un argument
    Usage dans le template: {{ forloop.counter0|multiply:0.1 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def format_price(value):
    """
    Formate un prix avec des espaces pour les milliers
    Usage: {{ plan.price_cfa|format_price }}
    Exemple: 5000 -> "5 000"
    """
    try:
        return "{:,.0f}".format(float(value)).replace(',', ' ')
    except (ValueError, TypeError):
        return value


@register.filter
def lower_first(value):
    """
    Met le premier caractère en minuscule
    Usage: {{ plan.get_period_display|lower_first }}
    """
    if not value:
        return value
    return value[0].lower() + value[1:]


@register.filter
def get_period_icon(period):
    """
    Retourne l'icône Bootstrap appropriée pour une période
    Usage: {{ period|get_period_icon }}
    """
    icons = {
        'monthly': 'bi-calendar-month',
        'quarterly': 'bi-calendar3',
        'biannual': 'bi-calendar2-date',
        'annual': 'bi-calendar-year',
    }
    return icons.get(period, 'bi-calendar')


@register.filter
def discount_badge(period):
    """
    Retourne le badge de réduction pour une période
    Usage: {% if period|discount_badge %}...{% endif %}
    """
    discounts = {
        'quarterly': '-3,5%',
        'biannual': '-4%',
        'annual': '-5%',
    }
    return discounts.get(period, '')


@register.simple_tag
def animation_delay(index):
    """
    Calcule le délai d'animation
    Usage: {% animation_delay forloop.counter0 %}
    """
    return f"{index * 0.1}s"

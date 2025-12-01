"""
Django Management Command pour le seeding des données Aude

Usage:
    python manage.py seed_pricing
    python manage.py seed_pricing --clear  (efface et recrée toutes les données)
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal


class Command(BaseCommand):
    help = 'Remplit la base de données avec les données tarifaires Aude'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Efface toutes les données existantes avant le seeding',
        )

    def handle(self, *args, **options):
        from website.models import PricingPlan, PricingFeature, FAQ, CTASection

        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS('🚀 DÉMARRAGE DU SEEDING DES DONNÉES AUDE'))
        self.stdout.write("="*60 + "\n")

        # Effacement si demandé
        if options['clear']:
            self.stdout.write(self.style.WARNING('⚠️  Effacement des données existantes...'))
            PricingFeature.objects.all().delete()
            PricingPlan.objects.all().delete()
            FAQ.objects.all().delete()
            CTASection.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Données effacées\n'))

        try:
            with transaction.atomic():
                # Seed pricing plans
                self._seed_pricing_plans(PricingPlan)

                # Seed features
                self._seed_pricing_features(PricingPlan, PricingFeature)

                # Seed FAQ
                self._seed_faq(FAQ)

                # Seed CTA
                self._seed_cta_section(CTASection)

            self.stdout.write("\n" + "="*60)
            self.stdout.write(self.style.SUCCESS('✅ SEEDING TERMINÉ AVEC SUCCÈS!'))
            self.stdout.write("="*60 + "\n")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ ERREUR: {str(e)}\n'))
            raise

    def _seed_pricing_plans(self, PricingPlan):
        """Remplit la table PricingPlan"""
        self.stdout.write('🔄 Seeding PricingPlan...')

        pricing_data = [
            # MENSUEL
            {'plan_type': 'essentiel', 'period': 'monthly', 'price_eur': Decimal('7.62'), 'price_cfa': 5000, 'is_featured': False, 'featured_badge': '', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Essentiel', 'display_order': 1},
            {'plan_type': 'privilege', 'period': 'monthly', 'price_eur': Decimal('9.15'), 'price_cfa': 6000, 'is_featured': False, 'featured_badge': '', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Privilège', 'display_order': 2},
            {'plan_type': 'elite', 'period': 'monthly', 'price_eur': Decimal('10.67'), 'price_cfa': 7000, 'is_featured': True, 'featured_badge': '⭐ Le plus populaire', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Elite', 'display_order': 3},
            {'plan_type': 'prestige', 'period': 'monthly', 'price_eur': Decimal('0.00'), 'price_cfa': 0, 'is_featured': False, 'featured_badge': '', 'action_url': '/contact', 'action_text': 'Demander un devis', 'display_order': 4},

            # TRIMESTRIEL
            {'plan_type': 'essentiel', 'period': 'quarterly', 'price_eur': Decimal('22.11'), 'price_cfa': 14500, 'is_featured': False, 'featured_badge': '', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Essentiel', 'display_order': 1},
            {'plan_type': 'privilege', 'period': 'quarterly', 'price_eur': Decimal('26.37'), 'price_cfa': 17300, 'is_featured': False, 'featured_badge': '', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Privilège', 'display_order': 2},
            {'plan_type': 'elite', 'period': 'quarterly', 'price_eur': Decimal('30.49'), 'price_cfa': 22000, 'is_featured': True, 'featured_badge': '⭐ Le plus populaire', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Elite', 'display_order': 3},
            {'plan_type': 'prestige', 'period': 'quarterly', 'price_eur': Decimal('0.00'), 'price_cfa': 0, 'is_featured': False, 'featured_badge': '', 'action_url': '/contact', 'action_text': 'Demander un devis', 'display_order': 4},

            # SEMESTRIEL
            {'plan_type': 'essentiel', 'period': 'biannual', 'price_eur': Decimal('44.21'), 'price_cfa': 29000, 'is_featured': False, 'featured_badge': '', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Essentiel', 'display_order': 1},
            {'plan_type': 'privilege', 'period': 'biannual', 'price_eur': Decimal('52.75'), 'price_cfa': 34600, 'is_featured': False, 'featured_badge': '', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Privilège', 'display_order': 2},
            {'plan_type': 'elite', 'period': 'biannual', 'price_eur': Decimal('60.98'), 'price_cfa': 40000, 'is_featured': True, 'featured_badge': '⭐ Le plus populaire', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Elite', 'display_order': 3},
            {'plan_type': 'prestige', 'period': 'biannual', 'price_eur': Decimal('0.00'), 'price_cfa': 0, 'is_featured': False, 'featured_badge': '', 'action_url': '/contact', 'action_text': 'Demander un devis', 'display_order': 4},

            # ANNUEL
            {'plan_type': 'essentiel', 'period': 'annual', 'price_eur': Decimal('88.42'), 'price_cfa': 58000, 'is_featured': False, 'featured_badge': '', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Essentiel', 'display_order': 1},
            {'plan_type': 'privilege', 'period': 'annual', 'price_eur': Decimal('105.49'), 'price_cfa': 69200, 'is_featured': False, 'featured_badge': '', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Privilège', 'display_order': 2},
            {'plan_type': 'elite', 'period': 'annual', 'price_eur': Decimal('121.96'), 'price_cfa': 80000, 'is_featured': True, 'featured_badge': '🔥 Meilleure offre', 'action_url': 'https://app.aude.ci', 'action_text': 'Choisir Elite', 'display_order': 3},
            {'plan_type': 'prestige', 'period': 'annual', 'price_eur': Decimal('0.00'), 'price_cfa': 0, 'is_featured': False, 'featured_badge': '', 'action_url': '/contact', 'action_text': 'Demander un devis', 'display_order': 4},
        ]

        for data in pricing_data:
            plan, created = PricingPlan.objects.update_or_create(
                plan_type=data['plan_type'],
                period=data['period'],
                defaults={
                    'price_eur': data['price_eur'],
                    'price_cfa': data['price_cfa'],
                    'is_featured': data['is_featured'],
                    'featured_badge': data['featured_badge'],
                    'action_url': data['action_url'],
                    'action_text': data['action_text'],
                    'is_active': True,
                    'display_order': data['display_order']
                }
            )
            status = "✅ Créé" if created else "♻️  Mis à jour"
            self.stdout.write(f"  {status}: {plan}")

        self.stdout.write(self.style.SUCCESS(f'✅ {len(pricing_data)} plans tarifaires traités\n'))

    def _seed_pricing_features(self, PricingPlan, PricingFeature):
        """Remplit la table PricingFeature"""
        self.stdout.write('🔄 Seeding PricingFeature...')

        features_data = {
            'essentiel': [
                {'text': 'Devis/factures', 'is_bold': False, 'order': 1},
                {'text': 'Tableau de bord', 'is_bold': False, 'order': 2},
                {'text': 'Messagerie interne', 'is_bold': False, 'order': 3},
                {'text': 'Gestion documentation', 'is_bold': False, 'order': 4},
                {'text': 'Support email', 'is_bold': False, 'order': 5},
            ],
            'privilege': [
                {'text': 'Tout l\'Essentiel +', 'is_bold': True, 'order': 1},
                {'text': 'Gestion des tâches', 'is_bold': False, 'order': 2},
                {'text': 'Planning et calendrier', 'is_bold': False, 'order': 3},
                {'text': 'Gestion des achats', 'is_bold': False, 'order': 4},
                {'text': 'Suivi des budgets', 'is_bold': False, 'order': 5},
                {'text': 'Gestion collaborateurs', 'is_bold': False, 'order': 6},
                {'text': 'Statistiques & pilotage', 'is_bold': False, 'order': 7},
            ],
            'elite': [
                {'text': 'Tout le Privilège +', 'is_bold': True, 'order': 1},
                {'text': 'Analyse budgétaire', 'is_bold': False, 'order': 2},
                {'text': 'Bibliothèque ouvrages', 'is_bold': False, 'order': 3},
                {'text': 'Bibliothèque devis', 'is_bold': False, 'order': 4},
                {'text': 'Assistance personnalisée', 'is_bold': False, 'order': 5},
                {'text': 'Formations spécialisées', 'is_bold': False, 'order': 6},
            ],
            'prestige': [
                {'text': 'Tout l\'Elite +', 'is_bold': True, 'order': 1},
                {'text': 'Fonctionnalités sur mesure', 'is_bold': False, 'order': 2},
                {'text': 'Intégrations personnalisées', 'is_bold': False, 'order': 3},
                {'text': 'Support premium', 'is_bold': False, 'order': 4},
                {'text': 'Formation sur site', 'is_bold': False, 'order': 5},
                {'text': 'Consultant dédié', 'is_bold': False, 'order': 6},
            ],
        }

        plans = PricingPlan.objects.all()
        feature_count = 0

        for plan in plans:
            features = features_data.get(plan.plan_type, [])

            for feature_data in features:
                PricingFeature.objects.update_or_create(
                    pricing_plan=plan,
                    feature_text=feature_data['text'],
                    defaults={
                        'is_bold': feature_data['is_bold'],
                        'display_order': feature_data['order']
                    }
                )
                feature_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ {feature_count} fonctionnalités créées\n'))

    def _seed_faq(self, FAQ):
        """Remplit la table FAQ"""
        self.stdout.write('🔄 Seeding FAQ...')

        faq_data = [
            {
                'question': 'Comment fonctionne l\'essai gratuit de 30 jours ?',
                'answer': 'L\'essai gratuit vous donne accès à toutes les fonctionnalités d\'Aude pendant 30 jours sans aucune restriction. Aucune carte bancaire n\'est requise pour commencer. À la fin de la période d\'essai, vous pouvez choisir votre formule d\'abonnement ou arrêter sans frais.',
                'icon_class': 'bi bi-plus-circle',
                'display_order': 1
            },
            {
                'question': 'Puis-je changer de formule à tout moment ?',
                'answer': 'Oui, vous pouvez upgrader ou downgrader votre formule à tout moment. Les changements prennent effet immédiatement et la facturation est ajustée au prorata. Pour les formules avec engagement, nous proposons des solutions flexibles.',
                'icon_class': 'bi bi-plus-circle',
                'display_order': 2
            },
            {
                'question': 'Mes données sont-elles sécurisées ?',
                'answer': 'Absolument. Toutes vos données sont chiffrées et stockées sur des serveurs sécurisés. Nous respectons le RGPD et vos données vous appartiennent entièrement. Sauvegarde automatique, redondance et sécurité bancaire sont incluses.',
                'icon_class': 'bi bi-plus-circle',
                'display_order': 3
            },
            {
                'question': 'Y a-t-il une formation pour utiliser Aude ?',
                'answer': 'Oui, nous proposons une formation personnalisée incluse dans toutes nos formules. Notre équipe vous accompagne dans la prise en main et l\'optimisation d\'Aude pour vos besoins spécifiques. Formations en ligne, tutoriels et support dédié sont disponibles.',
                'icon_class': 'bi bi-plus-circle',
                'display_order': 4
            },
        ]

        for data in faq_data:
            faq, created = FAQ.objects.update_or_create(
                question=data['question'],
                defaults={
                    'answer': data['answer'],
                    'icon_class': data['icon_class'],
                    'is_active': True,
                    'display_order': data['display_order']
                }
            )
            status = "✅ Créé" if created else "♻️  Mis à jour"
            self.stdout.write(f"  {status}: {faq.question}")

        self.stdout.write(self.style.SUCCESS(f'✅ {len(faq_data)} questions FAQ traitées\n'))

    def _seed_cta_section(self, CTASection):
        """Remplit la table CTASection"""
        self.stdout.write('🔄 Seeding CTASection...')

        cta_data = {
            'page': 'pricing',
            'title': 'Prêt à Démarrer avec Aude ?',
            'subtitle': 'Choisissez votre formule et commencez votre essai gratuit de 30 jours dès maintenant. Sans engagement, sans carte bancaire.',
            'primary_text': 'Commencer gratuitement',
            'primary_url': 'https://app.aude.ci',
            'primary_icon': 'bi bi-rocket-takeoff',
            'secondary_text': 'Nous contacter',
            'secondary_url': '/contact',
            'secondary_icon': 'bi bi-envelope',
            'highlight_1': '30 jours gratuits',
            'highlight_1_icon': 'bi bi-shield-lock',
            'highlight_2': 'Sans engagement',
            'highlight_2_icon': 'bi bi-credit-card-2-front-fill',
            'highlight_3': 'Support inclus',
            'highlight_3_icon': 'bi bi-headset',
            'is_active': True
        }

        cta, created = CTASection.objects.update_or_create(
            page=cta_data['page'],
            defaults={k: v for k, v in cta_data.items() if k != 'page'}
        )

        status = "✅ Créé" if created else "♻️  Mis à jour"
        self.stdout.write(f"  {status}: CTA Section - {cta.page}")
        self.stdout.write(self.style.SUCCESS('✅ Section CTA créée\n'))

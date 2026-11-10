from django.core.management.base import BaseCommand
from shop.models import Category

CATEGORIES = [
    "Chemise", "Ensemble", "Hoodies", "Jacket", "Gilet", "Short", "Tenue", "T-shirt",
    "Écharpe", "Pochette", "Stickers", "Casquette",
    "Baby tenue",
    "Cartable",
]

class Command(BaseCommand):
    help = "Crée les catégories de Wydad Store"

    def handle(self, *args, **options):
        for name in CATEGORIES:
            obj, created = Category.objects.get_or_create(name=name)
            self.stdout.write(f"{'Créée' if created else 'Existe déjà'} : {name}")
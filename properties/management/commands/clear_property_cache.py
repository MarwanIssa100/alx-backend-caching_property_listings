from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clear the property cache from Redis'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Clear all cache instead of just property cache',
        )

    def handle(self, *args, **options):
        if options['all']:
            cache.clear()
            self.stdout.write(
                self.style.SUCCESS('Successfully cleared all cache')
            )
        else:
            # Clear only the property cache
            cache.delete('all_properties')
            self.stdout.write(
                self.style.SUCCESS('Successfully cleared property cache (all_properties)')
            )

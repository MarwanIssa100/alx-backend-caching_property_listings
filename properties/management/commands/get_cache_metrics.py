from django.core.management.base import BaseCommand
from properties.utils import get_redis_cache_metrics
import json

class Command(BaseCommand):
    help = 'Get Redis cache performance metrics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--json',
            action='store_true',
            help='Output metrics in JSON format',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed metrics information',
        )

    def handle(self, *args, **options):
        # Get cache metrics
        metrics = get_redis_cache_metrics()
        
        if options['json']:
            # Output in JSON format
            self.stdout.write(json.dumps(metrics, indent=2))
        else:
            # Output in human-readable format
            if metrics['error']:
                self.stdout.write(
                    self.style.ERROR(f"Error: {metrics['error']}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("Redis Cache Metrics:")
                )
                self.stdout.write(f"  Hits: {metrics['keyspace_hits']:,}")
                self.stdout.write(f"  Misses: {metrics['keyspace_misses']:,}")
                self.stdout.write(f"  Total Requests: {metrics['total_requests']:,}")
                self.stdout.write(f"  Hit Ratio: {metrics['hit_ratio']:.4f} ({metrics['hit_ratio']*100:.2f}%)")
                
                if options['verbose']:
                    self.stdout.write("")
                    self.stdout.write("Detailed Information:")
                    self.stdout.write(f"  - Cache hits represent successful key retrievals")
                    self.stdout.write(f"  - Cache misses represent failed key retrievals")
                    self.stdout.write(f"  - Hit ratio indicates cache effectiveness")
                    self.stdout.write(f"  - Higher hit ratios indicate better cache performance")

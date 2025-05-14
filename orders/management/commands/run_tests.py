from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run tests with proper settings'

    def add_arguments(self, parser):
        parser.add_argument('test_labels', nargs='*', help='Test labels to run')

    def handle(self, *args, **options):
        test_labels = options['test_labels'] or ['orders.tests']
        verbosity = options['verbosity']

        self.stdout.write(self.style.SUCCESS('Running tests...'))

        call_command(
            'test',
            *test_labels,
            verbosity=verbosity,
            interactive=False,
        )
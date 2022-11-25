import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django Custom Commands To Pause Execution Until Database Is Available"""

    def handle(self, *args, **options):
        """handle Args And Options"""
        self.stdout.write('waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database Unavailable waiting 1 Second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database Available!'))

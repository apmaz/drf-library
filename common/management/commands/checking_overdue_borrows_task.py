from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        schedule, created = Schedule.objects.get_or_create(
            func="borrow.borrow_services.checking_overdue_borrows",
            schedule_type=Schedule.DAILY,
            repeats=-1,
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Schedule created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Schedule already exists"))

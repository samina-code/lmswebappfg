from django.core.management.base import BaseCommand
from backend.models import Semester, Student

class Command(BaseCommand):
    help = "Insert default semester and student data"

    def handle(self, *args, **kwargs):
        # Semester create or get
        semester_obj, created = Semester.objects.get_or_create(
            title="1st Semester",
            defaults={
                "start_date": "2025-01-01",
                "end_date": "2025-05-30"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Semester '{semester_obj.title}' created."))
        else:
            self.stdout.write(self.style.WARNING(f"Semester '{semester_obj.title}' already exists."))

        # Student create or get
        student, created = Student.objects.get_or_create(
            email="test@example.com",
            defaults={
                "name": "Test Student",
                "contact": "1234567890",
                "father_name": "Test Father",
                "semester": semester_obj,
                "status": "Active"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Student '{student.name}' created."))
        else:
            self.stdout.write(self.style.WARNING(f"Student '{student.name}' already exists."))

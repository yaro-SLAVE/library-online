from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument("--username", help="Admin's username", required=True)
        parser.add_argument("--password", help="Admin's password", required=True)

    def handle(self, *args, **options):
        username = options["username"]

        user = User.objects.filter(username=username).first()
        if user is None:
            user = User.objects.create_superuser(username=username, password=options["password"])
        else:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        print(f"Created/updated superuser {username}")

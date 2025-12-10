from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from library_service.models.user import UserProfile
from library_service.models.catalog import Library, LibraryDatabase

# TODO: async??

User = get_user_model()


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):  # pylint: disable=unused-argument
    Group.objects.get_or_create(name="Librarian")
    Group.objects.get_or_create(name="Reader")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  # pylint: disable=unused-argument
    try:
        instance.profile.save()
    except User.profile.RelatedObjectDoesNotExist:
        UserProfile.objects.create(user=instance)


@receiver(post_migrate)
def create_default_libraries(sender, **kwargs):
    if not Library.objects.exists():
        lib1 = Library.objects.create(
            description="ИРНИТУ",
            address="664074, Россия, г. Иркутск, ул. Лермонтова, 83."
        )
        LibraryDatabase.objects.create(database="ISTU", library=lib1)    
        print("Lib data created")
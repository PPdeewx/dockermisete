from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        import apps.users.signals
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='external')
        Group.objects.get_or_create(name='regular')
        Group.objects.get_or_create(name='manager')
        Group.objects.get_or_create(name='temporary')
        Group.objects.get_or_create(name='developer')
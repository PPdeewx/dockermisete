from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        import apps.users.signals
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='บุคลากรภายนอก')
        Group.objects.get_or_create(name='พนักงานประจำ')
        Group.objects.get_or_create(name='ผู้บริหาร')
        Group.objects.get_or_create(name='พนักงานชั่วคราว')
        Group.objects.get_or_create(name='developer')
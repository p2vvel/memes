from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, login, password=None):
        '''Used by python manage.py createuser'''
        MyUser.objects.create(email=self.normalize_email(email), login=login, password=password)
        # user = self.model()
    
    def create_superuser(self, email, login, password=None):
        '''Used by python manage.py createsuperuser'''
        MyUser.objects.create(email=self.normalize_email(email), login=login, password=password, is_superuser=True)


from django.contrib.auth.base_user import BaseUserManager


class CustomAccManager(BaseUserManager):
    
    def __init__(self, **extra_fields):
        print('AAA')
        super(BaseUserManager, self).__init__(**extra_fields)
    
    def create_user(self, email, password, username, phone, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        
        if not username:
            raise ValueError('Username must be set')

        if not phone:
            raise ValueError('Phone must be set')

        email = self.normalize_email(email)
        acc = self.model(email=email, username=username, phone=phone, **extra_fields)
        acc.set_password(password)
        acc.save()
        return acc

    def create_superuser(self, email, password, username, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_moder', True)
        extra_fields.setdefault('is_secretar', True)
        extra_fields.setdefault('is_expert', True)
        extra_fields.setdefault('is_vned', True)
        extra_fields.setdefault('is_analit', True)

        return self.create_user(email, password, username, phone, **extra_fields)
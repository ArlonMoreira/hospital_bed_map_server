from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

class UsersManager(BaseUserManager):

    #Responsável por criar o usuário
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError('Os usuários devem ter um endereço de e-mail')
        
        if not username:
            raise ValueError('Nome do usuário é obrigatório')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #Responsel por criar super usuário
    def create_superuser(self, email, username, password=None):

        user = self.create_user(
            email=email,
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    username = models.CharField(
        max_length=125,
        unique=True,
        blank=False,
        null=False
    )
    is_active = models.BooleanField(
        verbose_name='Ativo',
        default=True
    )
    is_admin = models.BooleanField(
        verbose_name='Administrador',
        default=False
    )
    is_superuser = models.BooleanField(
        verbose_name='Superusuário',
        default=False
    )
    objects = UsersManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    @property
    def is_staff(self):
        return self.is_admin    
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

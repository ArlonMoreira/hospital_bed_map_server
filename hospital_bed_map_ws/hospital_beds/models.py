from django.db import models
from ..utils import generate_hash_key

# Create your models here.
class Hospital(models.Model):
    id = models.CharField(
        verbose_name='Identificação',
        max_length=20,
        default=None,
        unique=True,
        primary_key=True
    )
    name = models.CharField(
        verbose_name='Nome',
        max_length=255,
        null=False,
        blank=False
    )
    acronym = models.CharField(
        verbose_name='Sigla',
        max_length=45,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Ativo',
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_hash_key()
        super(Hospital, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitais'



from django.db import models
from django.conf import settings
from ..utils import generate_hash_key

# Hospitais
class Hospital(models.Model):
    name = models.CharField(
        verbose_name='Nome do hospital',
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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitais'

# Tipo de acomodação
class TypeOfAccommodation(models.Model):
    name = models.CharField(
        verbose_name='Nome do tipo de acomodação',
        max_length=255,
        null=False,
        blank=False        
    )

    def __str__(self):
        return self.name    

    class Meta:
        verbose_name = 'Tipo de acomodação'
        verbose_name_plural = 'Tipos de acomodação'

# Unidades de saúde
class HealthUnits(models.Model):
    name = models.CharField(
        verbose_name='Nome da unidade de saúde',
        max_length=255,
        null=False,
        blank=False
    )
    hospital = models.ForeignKey(
        Hospital,
        verbose_name='Hospital',
        on_delete=models.SET_NULL,
        null=True,
        blank=True        
    )
    type_accommodation = models.ForeignKey(
        TypeOfAccommodation,
        verbose_name='Tipo de acomodação',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )    
    is_active = models.BooleanField(
        verbose_name='Ativo',
        default=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )      
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Unidade de saúde'
        verbose_name_plural = 'Unidades de saúde'    

# Leitos    
class HospitalBeds(models.Model):
    STATUS_CHOICES = (
        ('BLOQUEADO', 'BLOQUEADO'),
        ('OCUPADO', 'OCUPADO'),
        ('VAGO', 'VAGO')
    )

    id = models.CharField(
        verbose_name='Identificação',
        max_length=20,
        default=None,
        unique=True,
        primary_key=True
    ) 
    name = models.CharField(
        verbose_name='Nome do leito',
        max_length=25,
        null=False,
        blank=False
    )    
    health_units = models.ForeignKey(
        HealthUnits,
        verbose_name='Unidade de saúde',
        on_delete=models.SET_NULL,
        null=True,
        blank=True        
    )
    is_active = models.BooleanField(
        verbose_name='Ativo',
        default=True
    )
    is_extra = models.BooleanField(
        verbose_name='Extra',
        default=False
    )
    is_isolation = models.BooleanField(
        verbose_name='Isolamento',
        default=False
    )
    status = models.CharField('Status', max_length=45, choices=STATUS_CHOICES, blank=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_hash_key()
        super(Hospital, self).save(*args, **kwargs)    
    
    class Meta:
        verbose_name = 'Leito'
        verbose_name_plural = 'Leitos'      




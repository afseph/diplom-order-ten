from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AssetStatus(models.TextChoices):
    IN_USE = 'IN_USE', 'В эксплуатации'
    WRITTEN_OFF = 'WRITTEN_OFF', 'Списан'
    IN_REPAIR = 'IN_REPAIR', 'В ремонте'
    MOVED = 'MOVED', 'Перемещён'
    IN_STORAGE = 'IN_STORAGE', 'На складе'

class AssetType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Тип актива'
        verbose_name_plural = 'Типы активов'

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(AssetType, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=AssetStatus.choices, default=AssetStatus.IN_USE)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    def get_status_badge_class(self):
        """Return Bootstrap badge class based on status"""
        badge_classes = {
            'IN_USE': 'success',
            'WRITTEN_OFF': 'secondary',
            'IN_REPAIR': 'warning',
            'MOVED': 'info',
            'IN_STORAGE': 'primary'
        }
        return badge_classes.get(self.status, 'secondary')

class AssetLog(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Лог изменения'
        verbose_name_plural = 'Логи изменений'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.asset} - {self.action} ({self.timestamp})"

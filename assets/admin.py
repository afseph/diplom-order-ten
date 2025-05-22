from django.contrib import admin
from .models import Asset, AssetType, Location, AssetLog

@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'serial_number', 'status', 'location', 'responsible', 'purchase_date', 'value')
    list_filter = ('status', 'type', 'location')
    search_fields = ('name', 'serial_number', 'type__name', 'location__name')
    ordering = ('-created_at',)
    date_hierarchy = 'purchase_date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'type', 'serial_number', 'purchase_date', 'value')
        }),
        ('Статус и расположение', {
            'fields': ('status', 'location', 'responsible')
        }),
    )

@admin.register(AssetLog)
class AssetLogAdmin(admin.ModelAdmin):
    list_display = ('asset', 'action', 'user', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('asset__name', 'asset__serial_number', 'user__username')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

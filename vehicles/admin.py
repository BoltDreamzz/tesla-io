from django.contrib import admin
from .models import Vehicle, VehicleSharePurchase, VehiclePurchase

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'year', 'price', 'status', 'available_shares')
    list_filter = ('status', 'model', 'condition')
    search_fields = ('name', 'model')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model', 'year', 'condition', 'status')
        }),
        ('Pricing', {
            'fields': ('price', 'share_price', 'total_shares', 'available_shares')
        }),
        ('Specifications', {
            'fields': ('mileage', 'color', 'interior_color', 'battery_range', 'acceleration')
        }),
        ('Features', {
            'fields': ('features', 'autopilot', 'premium_audio')
        }),
        ('Media & Location', {
            'fields': ('image', 'location')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_sold']
    
    def mark_as_sold(self, request, queryset):
        queryset.update(status='sold')
    mark_as_sold.short_description = "Mark selected vehicles as sold"

@admin.register(VehicleSharePurchase)
class VehicleSharePurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'shares_purchased', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'vehicle__name')
    readonly_fields = ('transaction_reference',)

@admin.register(VehiclePurchase)
class VehiclePurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'purchase_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'vehicle__name')
    readonly_fields = ('transaction_reference',)
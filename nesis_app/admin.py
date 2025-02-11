from django.contrib import admin
from .models import Asset, CRMUser, CRMInteraction, Mission, Application, Partner


class CRMUserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'email', 'organization', 'created_at')
    search_fields = ('last_name', 'email', 'organization')
    ordering = ('-created_at',)

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('asset__name', 'crm_user', 'interaction_type', 'timestamp')
    list_filter = ('interaction_type', 'timestamp')
    search_fields = ('crm_user__last_name', 'crm_user__email', 'asset__name', 'interaction_type')
    ordering = ('-timestamp',)

admin.site.register(CRMUser, CRMUserAdmin)
admin.site.register(CRMInteraction, InteractionAdmin)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'launch_date')
    search_fields = ('name', 'category')
    list_filter = ('category', 'status')

class MissionAdmin(admin.ModelAdmin):
    list_display=('mission_id',)
admin.site.register(Mission,MissionAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    list_display=('app_id',)
admin.site.register(Application,ApplicationAdmin)

class PartnerAdmin(admin.ModelAdmin):
    list_display=('partner_id',)
admin.site.register(Partner,PartnerAdmin)
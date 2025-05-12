from django.contrib import admin

# Register your models here.
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'working_status', 'work_type', 'created_at')
    search_fields = ('user__full_name', 'role', 'working_status')
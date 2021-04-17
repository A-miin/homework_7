from django.contrib import admin
from .models import Type,Status, Issue, Project, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


# Register your models here.

class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    fields = ['id', 'name']
    readonly_fields = ['id']

class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    fields = ['id', 'name']
    readonly_fields = ['id']

class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'project','status' ]
    fields = ['id', 'summary', 'description', 'type', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at', 'id']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'begin_date', 'end_date']
    fields = ['id', 'name','description', 'begin_date', 'end_date','is_deleted', 'user']
    readonly_fields = ['id']

class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['avatar', 'githubLink', 'description']

class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]

User=get_user_model()
admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)

admin.site.register(Issue, IssueAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Project,ProjectAdmin)
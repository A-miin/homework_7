from django.contrib import admin
from .models import Type,Status, Issue, Project

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
    fields = ['id', 'name','description', 'begin_date', 'end_date']

admin.site.register(Issue, IssueAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Project,ProjectAdmin)
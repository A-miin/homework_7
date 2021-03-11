from django.contrib import admin
from .models import Type,Status, Issue

# Register your models here.

class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    fields = ['id', 'name']

class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    fields = ['id', 'name']

class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status','created_at','updated_at']
    fields = ['id', 'summary', 'description', 'type', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Issue, IssueAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Status, StatusAdmin)
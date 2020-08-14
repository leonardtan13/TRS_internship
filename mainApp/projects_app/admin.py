from django.contrib import admin
from .models import Customer, Project, WorkItem, Domain, Objective, Message
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address1',
        'address2',
        'city',
    )
    

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'proposaldate',
        'startdate',
        'enddate',
    )

    list_filter = ('proposaldate', 'startdate', 'objectives')
    

@admin.register(WorkItem)
class WorkItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    pass
    

@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display =("name", "description", "document_file", "workitem_name", "project_id")









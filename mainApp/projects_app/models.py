from django.contrib import admin
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth import (
    get_user_model
)

User = get_user_model()
# Create your models here.

class Objective(models.Model):
    description = models.CharField(max_length=165, default='')
    def __str__(self):
        return self.description
    class Meta:
        verbose_name = ("Objective")
        verbose_name_plural = ("Objectives")
    def get_absolute_url(self):
        return reverse("objective-detail", kwargs={"pk": self.pk})

class Customer(models.Model):
    name = models.CharField(max_length=35, blank=True, default='', verbose_name="Customer name")
    address1 = models.CharField(max_length=55, blank=True, default='', verbose_name = "Address 1")
    address2 = models.CharField(max_length=55, blank=True, default='', verbose_name = "Address 2")
    city = models.CharField(max_length=35, blank=True, default='', verbose_name="City")

    class Meta:
        verbose_name = ("Customer")
        verbose_name_plural = ("Customers")
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("customer-detail", kwargs={"pk": self.pk})

class Domain(models.Model):
    description = models.CharField(max_length=140, default='')
    # this manytomanyfield not required
    # workitems = models.ManyToManyField('WorkItem', blank=True)
    def __str__(self):
        return self.description
    class Meta:
        verbose_name = ("Domain")
        verbose_name_plural = ("Domains")
    def get_absolute_url(self):
        return reverse("domain-detail", kwargs={"pk": self.pk})
    class Admin: pass

class WorkItem(models.Model):
    description = models.CharField(max_length=180, default='')
    indomain = models.ForeignKey(Domain, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return "{}/{}".format(self.indomain.description,self.description)
    class Admin: pass
    def get_absolute_url(self):
        return reverse("workitem-detail", kwargs={"pk": self.pk})

class Project(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    objectives = models.ManyToManyField(Objective, blank=True)
    proposaldate = models.DateField(default=datetime.now, verbose_name="Proposal Date")
    startdate = models.DateField(default=datetime.now, verbose_name="Start Date")
    enddate = models.DateField(default=datetime.now, verbose_name="End Date")
    domains = models.ManyToManyField(Domain, blank=True)
    workitems = models.ManyToManyField(WorkItem, blank=True)
    fees = models.IntegerField(default=0)
    feesaftergrant = models.IntegerField(default=0, verbose_name="Fees after grant")
    billing1 = models.CharField(max_length=50, default="30% upon appointment of our services", verbose_name="First Billing")
    billing2 = models.CharField(max_length=50, default="60% upon issuance of draft report", verbose_name="Second Billing")
    billing3 = models.CharField(max_length=50, default="10% upon issuance of follow up report", verbose_name="Final Billing")
    proptemplate = models.CharField(max_length=50, default='sample.pptx')
    engatemplate = models.CharField(max_length=50, default='sample.docx')
    users = models.ManyToManyField(User, blank=True)
    
    PROP = "PROPOSAL"
    IP = "IN_PROGRESS"
    EN = "ENDED"

    status_choice = (
        (PROP, "Proposal"),
        (IP, "In progress"),
        (EN, "Ended"),
    )

    status = models.CharField(max_length=20, choices=status_choice, default=PROP)

    def __str__(self):
        return self.customer.name+self.proposaldate.strftime(":%Y-%m-%d")

    def get_absolute_url(self):
        return reverse("project", kwargs={"project_id": self.pk})
    class Admin: pass

#class MyModelAdmin(admin.ModelAdmin):
#    def formfield_for_manytomany(self, db_field, request, **kwargs):
#        if db_field.name == "cars":
#            kwargs["queryset"] = Car.objects.filter(owner=request.user)
#        return super(MyModelAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class Message(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, help_text="Enter description of document")
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)

    document_file = models.FileField(upload_to = "document", max_length=100, null=True, blank=True)
    workitem_name = models.ForeignKey(WorkItem, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Document")
        verbose_name_plural = ("Documents")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("message-detail", kwargs={"pk": self.pk})

class TableDictionary(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name = ("Table")
        verbose_name_plural = ("Tables")

    def __str__(self):
        return self.name
    class Admin: pass

class KeyValue(models.Model):
    table_dictionary = models.ForeignKey(TableDictionary, on_delete=models.CASCADE)
    key = models.CharField(max_length=240, default="")
    value = models.CharField(max_length=240, default="")
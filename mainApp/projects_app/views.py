from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import ProjectForm
from . import services
from .models import Customer, Message, Domain, Objective, Project, WorkItem, TableDictionary, KeyValue
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import User
from django.contrib import messages

# @method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")  
# @allowed_users(allowed_roles=['admin'])
# to be added after "login_required" decorators,
# currently has 3 roles that can be allowed, "admin", "consultant", "client"

##dkiong
def md(d, wl):
    domain = Domain(description=d)
    domain.save()
    for w in wl:
        item = WorkItem(description=w, indomain=domain)
        item.save()

def init(request):
    Domain.objects.all().delete()
    WorkItem.objects.all().delete()
    Objective.objects.all().delete()
    Customer.objects.all().delete()
    Project.objects.all().delete()
    Objective(description="To assess the adequacy of existing internal controls and determine the effectiveness of internal controls against established guidelines.").save()
    Objective(description="To provide practical and cost-effective recommendations to rectify internal control findings noted.").save()
    Objective(description="Tracking the implementation status and timeline of the follow-up actions that have been agreed with management.").save()
    md('General Control Environment and Financial Management',
       ['Organisational structure and reporting line',
        'Policies and procedures for key operational processes',
        'Approval matrices',
        'Management of conflict of interest ("COI")',
        'Segregation of duties for key business functions',
        'Business Continuity Plan ("BCP")',
        'Disaster Recovery Plan ("DRP")',
        'Risk management process/framework including policy and risk register',
        'Procedures to ensure compliance with Catalist rules and other relevant regulations',
        'Review and approval of SGX announcements',
        'Interested person transactions ("IPT")',
        'Whistle-blowing mechanism',
        'Budgeting and forecasting',
        'Establishment of contract signatories, review and approval of contracts and revision of terms in contracts',
        'Monitoring of contracts, licenses, permits and certifications',
        'Monthly and periodic financial reporting process including reconciliation and approval',
        'Journal entry processing',
        'Monitoring of compliance with local regulatory requirements and health, safety and environmental regulations'])
    md('Sales to Collection',
       ['Project tender preparation (including costing and basis of pricing) and approval',
        'Project contract vetting process and approval',
        'Monitoring of contractual obligations',
        'Credit evaluation and approval, including granting and monitoring of credit limits and terms',
        'Credit block and release procedures',
        'Processing of progress billings and invoicing',
        'Revenue recognition policies and processes',
        'Credit notes processing, including approval for discount and adjustment',
        'Accounts receivables and receipts recording',
        'Monitoring of accounts receivables',
        'Provision and/or write-off of doubtful debts'])
    md('Procurement to Payment',
       ['Purchase requisition (including sourcing, evaluation, tendering and awarding of suppliers/subcontractors)',
        'Processing of purchase orders and project contracts',
        'Monitoring of contractual obligations',
        'Comparison of quotes and tenders',
        'Monitoring of receipts and/or outstanding orders/contracts',
        'Receipts and acceptance of materials',
        'Purchase returns, claims processing and monitoring',
        'Progress claims processing and approval',
        'Supplier and subcontractors assessment, selection and periodic evaluation',
        'Supplier and subcontractors master files maintenance',
        'Accounts payable recording',
        'Reconciliation of suppliers and subcontractors\' statement of accounts',
        'Payment processing (in accordance with the Company’s approval matrix) and recording'])
    md('Project Management',
       ['Project initiation, planning and approval including feasibility studies, risk assessment, resources, costing, schedule, milestones',
        'Monitoring of project progress, quality and issues',
        'Tracking and rectification of project issues',
        'Accurate and timely accounting for project related transactions',
        'Monitoring of project milestones and costs, including explanation and approval for overrun of budgeted time and costs',
        'Variation Orders ("VOs") management',
        'Retention sum monitoring',
        'Post mortem evaluation',
        'Monitoring of bankers guarantee or performance bond, if any',
        'Retention of project documents'])
    md('Fixed Asset and Inventory Management',
       ['Capital expenditure budget monitoring',
        'Acquisition of fixed assets, justification and approval',
        'Receipt and quality check',
        'Movement of fixed assets and inventory including disposal, transfer and removal',
        'Fixed asset maintenance and repair',
        'Fixed asset register maintenance',
        'Capitalisation and depreciation policy',
        'Fixed asset and inventory verification and reconciliation',
        'Physical controls and security, including insurance coverage',
        'Impairment and write-off, including justification and approval'])
    md('Bank and Cash Management',
       ['Bank mandates including authorisation matrix and dual signatories',
        'Banking facilities including financing/borrowing procedures and approval',
        'Monitoring of bank covenants (if any)',
        'Bank account opening and closing',
        'Bank statement review for any unusual transactions',
        'Cashflow budgeting and forecasting',
        'Cheque, physical cash and bank tokens custody',
        'Bank reconciliation',
        'Fixed deposits, investments and fund transfers',
        'Petty cash management'])
    md('Human Resources and Payroll',
       ['Policies and procedures (including approval matrix)',
        'Recruitment',
        'Conflict of interest and independence declarations',
        'Performance appraisal (confirmation and periodic)',
        'Payroll processing',
        'Staff advances and borrowing (if any)',
        'Staff claims review (travelling and entertainment)',
        'Payment of salary',
        'Payroll report review and reconciliation',
        'Payroll and employee master files management',
        'Resignation and termination',
        'Staff training management',
        'Compliance with applicable manpower regulations',
        'Segregation of duties system access rights'])
    md('General IT Controls',
       ['Policies and procedures (including approval matrix)',
        'System change controls',
        'User access rights controls',
        'Backup and restoration',
        'Firewalls and anti-virus',
        'Password controls',
        'Physical security to server room and computer server',
        'Data security management',
        'Segregation of duties and system access rights'])
    c1 = Customer(name="F & F",address1="Winery Building", address2="22 Geylang Road", city="Singapore")
    c1.save()
    c2 = Customer(name="G & G",address1="YAH Building", address2="8 Morey Road", city="Singapore")
    c2.save()
    Project(customer=c1).save()
    Project(customer=c2).save()
    context = {'domains':Domain.objects.all() }
    return HttpResponse('<html><body>done</body></html>')
##dkiong

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

# Generic views
@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class CustomerListView(generic.ListView):
    model = Customer

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class DomainListView(generic.ListView):
    model = Domain

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ObjectiveListView(generic.ListView):
    model = Objective

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ProjectListView(generic.ListView):
    model = Project
    Project.objects.all().reverse()

# class WorkItemListView(generic.ListView): NOT USED 
#     model = WorkItem

@login_required
@allowed_users(allowed_roles=['consultant','admin'])
def workitem_list_view(request):
    domains = Domain.objects.all()
    workitems = WorkItem.objects.all()
    return render(request, 'projects_app/workitem_list.html', {"domains": domains, "workitems" : workitems})


# Customer views ------------------------------------------
@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class CustomerCreateView(CreateView):
    model = Customer
    fields = ['name', 'address1', 'address2', 'city']
    template_name = 'projects_app/customer/customer_form.html'

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = "projects_app/customer/customer_detail.html"

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['name', 'address1', 'address2', 'city']
    template_name = "projects_app/customer/customer_update.html"
    success_url = reverse_lazy('customers')

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = "projects_app/customer/customer_delete.html"
    success_url = reverse_lazy('customers')

# Objective views ------------------------------------------
@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ObjectiveCreateView(CreateView):
    model = Objective
    fields = ['description']
    template_name = 'projects_app/objective/objective_form.html'

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ObjectiveDetailView(generic.DetailView):
    model = Objective
    fields = ['description']
    template_name = "projects_app/objective/objective_detail.html"

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ObjectiveUpdateView(UpdateView):
    model = Objective
    fields = ['description']
    template_name = "projects_app/objective/objective_update.html"
    success_url = reverse_lazy('objectives')

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ObjectiveDeleteView(DeleteView):
    model = Objective
    template_name = "projects_app/objective/objective_delete.html"
    success_url = reverse_lazy('objectives')


# Domain views ------------------------------------------
@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class DomainCreateView(CreateView):
    model = Domain
    fields = ['description']
    template_name = 'projects_app/domain/domain_form.html'

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class DomainDetailView(generic.DetailView):
    model = Domain
    fields = ['description']
    template_name = "projects_app/domain/domain_detail.html"

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class DomainUpdateView(UpdateView):
    model = Domain
    fields = ['description']
    template_name = "projects_app/domain/domain_update.html"
    success_url = reverse_lazy('domains')

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class DomainDeleteView(DeleteView):
    model = Domain
    template_name = "projects_app/domain/domain_delete.html"
    success_url = reverse_lazy('domains')


# WorkItem views ------------------------------------------
@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class WorkItemCreateView(CreateView):
    model = WorkItem
    fields = ['description', 'indomain']
    template_name = 'projects_app/workitem/workitem_form.html'

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class WorkItemDetailView(generic.DetailView):
    model = WorkItem
    fields = ['description', 'indomain']
    template_name = "projects_app/workitem/workitem_detail.html"

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class WorkItemUpdateView(UpdateView):
    model = WorkItem
    fields = ['description', 'indomain']
    template_name = "projects_app/workitem/workitem_update.html"
    success_url = reverse_lazy('workitems')

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class WorkItemDeleteView(DeleteView):
    model = WorkItem
    template_name = "projects_app/workitem/workitem_delete.html"
    success_url = reverse_lazy('workitems')

# Project views ------------------------------------------
@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects_app/project/project_form.html"
    success_url = reverse_lazy('projects')

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "projects_app/project/project_delete.html"
    success_url = reverse_lazy('projects')

@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects_app/project/project_form.html'


@login_required
@allowed_users(allowed_roles=['consultant','admin'])
def project_addworkitem(request, pk):
    if request.method == "GET":
        project = get_object_or_404(Project, pk=pk)
        # get list of domains from project
        domains = project.domains.all()
        # list of workitems in the domain of the project
        workitems = [workitem for workitem in WorkItem.objects.all() if workitem.indomain in domains]
        current_workitems = project.workitems.all() # current workitems assigned to the project to prepopulate checkboxes
        return render(request, 'projects_app/project/project_add_workitem.html', {"project" : project, "workitems" : workitems, "domains" :domains, "current_workitems" : current_workitems})
    else:
        project_id = request.POST['project'] # getting project id from request data
        project = get_object_or_404(Project, pk=project_id)
        workitems = [x for x in request.POST] # getting workitems from user submitted form
        workitems = workitems[2:] # removing csrf token and project id which are hidden fields
        services.add_project_workitem(project, workitems) # calling function from services
        return HttpResponseRedirect(reverse('project', args=(project.id,)))

@login_required
@allowed_users(allowed_roles=['consultant','admin'])
def project(request, project_id):

    project = get_object_or_404(Project, pk=project_id)
    if request.user.groups.filter(name='admin').exists():
        pass
    elif request.user not in project.users.all():
        return HttpResponseRedirect(reverse('projects'))


    context = get_project_details(request, project_id)
    return render(request, 'projects_app/project/project.html', context)

@login_required
@allowed_users(allowed_roles=['consultant','admin'])
def project_progress(request, project_id):
    context = get_project_details(request, project_id)
    return render(request, 'projects_app/project/project_progress.html', context)

def get_project_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    workitem_list = project.workitems.all()
    objective_list = project.objectives.all()
    domain_list = project.domains.all()
    
    workitem_message_list = []
    domain_message_dict = dict()
    try:
        for workitem in workitem_list:
            messages = Message.objects.filter(workitem_name=workitem, project_id=project)
            if len(messages) != 0:
                workitem_message_list.append((len(messages), messages.last().date_added))
            else:
                workitem_message_list.append((0, None))

            # adding total messages into domain message list
            if len(messages) != 0 and workitem.indomain not in domain_message_dict:
                domain_message_dict[workitem.indomain] = (len(messages), messages.last().date_added)
            elif len(messages) != 0 and workitem.indomain in domain_message_dict:
                num_msg = len(messages) + domain_message_dict[workitem.indomain][0]
                last_posted = domain_message_dict[workitem.indomain][1]
                if last_posted < messages.last().date_added:
                    last_posted = messages.last().date_added
                tup = (num_msg, last_posted)
                domain_message_dict[workitem.indomain] = tup

    except:
        pass
    my_list = list(zip(workitem_list, workitem_message_list))
    # print (domain_message_dict)
    context = {
        'project':project,
        'workitem_list': workitem_list,
        'objective_list': objective_list,
        'domain_list': domain_list,
        'my_list': my_list,
        'domain_message_dict': domain_message_dict,

    }
    return context

@login_required
@allowed_users(allowed_roles=['consultant','admin'])
def project_workitems(request, project_id, workitem_id):
    project = get_object_or_404(Project, pk=project_id)
    workitem_list = project.workitems.all()
    workitem = workitem_list[workitem_id-1]
    wid = workitem_id
    message_list = []
    if request.method == "POST":
        messageText = request.POST['messageText']
        # print (request.FILES)
        f = None
        if request.FILES:
            f = request.FILES['document_file']
            storage_name = str(project.id) + "/" + workitem.indomain.description + "/" + f.name
        if messageText != "":
            message = Message(name=request.user.username, description=messageText, workitem_name=workitem, project_id=project)
            if f != None:
                message.document_file.save(storage_name, File(f))
            message.save()
        pass

    try:
        messages = Message.objects.filter(workitem_name=workitem, project_id=project)
        
        # print (len(messages))
        # print (messages.last().date_added)

        for message in messages:
            message_list.append(message)
    except:
        pass

    message_list = message_list[::-1]

    context = {
        'message_list': message_list,
        'project':project,
        'workitem': workitem,
        'wid': wid,
    }
    return render(request, 'projects_app/project/project_messages.html', context)

@login_required
@allowed_users(allowed_roles=['consultant','admin'])
def retrieve_file(request, message_id, project_id, workitem_id):
    message = get_object_or_404(Message, pk=message_id)
    # to be tested
    document_name = message.document_file.name.split("/")
    document_name = document_name[len(document_name)-1]

    return HttpResponseRedirect(reverse('project-workitems', kwargs={'project_id':project_id,"workitem_id":workitem_id}))

from .forms import ProjectStatusForm
@method_decorator(login_required, name="dispatch") 
@method_decorator(allowed_users(allowed_roles=['consultant','admin']), name="dispatch")  
class ProjectStatusUpdateView(UpdateView):
    model = Project
    form_class = ProjectStatusForm
    template_name = 'projects_app/project/project_status.html'




# Generate scripts views ----------------------------------------------------------------------------------------------------------------------------------
from . import GenProposal_script, GenEngagement_script
from project_track import settings

def getprojectinfo(project):
    pdict = dict()
    pdict["objectives"] = [x.description for x in project.objectives.all()]
    wdict = dict()
    for w in project.workitems.all():
        if w.indomain.description in wdict.keys():
            wdict[w.indomain.description].append(w.description)
        else:
            wdict[w.indomain.description] = [w.description]
    pdict["workitems"] = wdict
    pdict["name"] = project.customer.name
    pdict["date"] = project.proposaldate.strftime("%d %B %Y")
    pdict["startdate"] = project.startdate.strftime("%d %B %Y")
    pdict["enddate"] = project.enddate.strftime("%d %B %Y")
    pdict["cost1"] = str(project.fees)
    pdict["cost2"] = str(project.feesaftergrant)
    pdict["billings"] = [project.billing1,project.billing2,project.billing3]
    return pdict

def generateProposal(request, pk):
    project = Project.objects.get(id=pk)
    pdict = getprojectinfo(project)
    inf = settings.MEDIA_ROOT+'/template.pptx'
    outf = GenProposal_script.generateproposal(pdict, inf)
    with open(outf, 'rb') as fp:
        data = fp.read()
    response = HttpResponse(content_type='application/pptx')
    response['Content-Disposition'] = 'attachment; filename="proposal_%s.pptx"' % project.customer.name
    response.write(data)
    return response

def generateEngagement(request, pk):
    project_id = pk
    retrieved_project = Project.objects.get(id=pk)
    project = getprojectinfo(retrieved_project)
    inf = settings.MEDIA_ROOT+'/template.docx'
    
    document = GenEngagement_script.generate_doc(inf, project)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=generated_document.docx'
    document.save(response)
    
    return response

from django.db.models import Q
def add_user_page(request, pk):
    project = Project.objects.get(id=pk)
    user_list = project.users.all()
    
    # get all admins
    admin_list = User.objects.filter(groups__name='admin').values('username')

    # get all users that are alr authorized
    added_users = user_list.values('username')

    # allow the users to be added as those that are not yet authorized or non admins
    addable_users = User.objects.exclude(Q(username__in = added_users)|Q(username__in = admin_list))
    context = {
        'project':project,
        'user_list': user_list,
        'addable_users': addable_users,

    }
    return render(request, 'projects_app/project/project_add_user.html', context)

def add_user(request, pk):
    to_add = request.POST['added_user']
    project = Project.objects.get(id=pk)
    project.users.add(to_add)

    return HttpResponseRedirect(reverse('project-add-user-page', kwargs={'pk':pk}))

def remove_user(request, pk, uk):
    to_remove = User.objects.get(id=uk)
    project = Project.objects.get(id=pk)
    project.users.remove(to_remove)

    return HttpResponseRedirect(reverse('project-add-user-page', kwargs={'pk':pk}))

def retrieveTable(pk, uk):
    project = Project.objects.get(id=pk)
    dom = Domain.objects.filter(id=uk)[0]
    
    if (TableDictionary.objects.filter(name=str(pk)+","+str(uk))):
        table = TableDictionary.objects.filter(name=str(pk)+","+str(uk))[0]
    else: 
        table = TableDictionary(domain_id=dom, project_id=project, name=str(pk)+","+str(uk))
        table.save()
    return table

def add_table_column(request, pk, uk):
    new_column = request.POST.get('column_name', '')
    if new_column == "":
        messages.error(request, "Column name cannot be empty!")
        return HttpResponseRedirect(reverse('project-domain-table', kwargs={'pk':pk, 'uk':uk}))
    else:
        table = retrieveTable(pk, uk)
        key_value_queryset = KeyValue.objects.filter(table_dictionary=table)
        
        rowlists = [[]]

        for key_value in key_value_queryset:
            row_index =  int(key_value.key.split(",")[0])
            if row_index + 1 <= len(rowlists):
                rowlists[row_index].append(key_value.value)
            else:
                rowlists.append(list())
                rowlists[row_index].append(key_value.value)

        num_columns = (len(rowlists[0]))
        num_rows = len(rowlists)
        if num_rows == 0:
            num_rows += 1

        for i in range(num_rows):
            if i == 0:
                key = str(i) + "," + str(num_columns)
                key_value_pair = KeyValue(table_dictionary=table, key=key, value=new_column)
                key_value_pair.save()
            else:
                key = str(i) + "," + str(num_columns)
                key_value_pair = KeyValue(table_dictionary=table, key=key, value=" ")
                key_value_pair.save()
        messages.success(request, "Column successfully added.")
        return HttpResponseRedirect(reverse('project-domain-table', kwargs={'pk':pk, 'uk':uk}))

def add_table_row(request, pk, uk):

    table = retrieveTable(pk, uk)
    key_value_queryset = KeyValue.objects.filter(table_dictionary=table)
    
    rowlists = [[]]
    for key_value in key_value_queryset:
        row_index =  int(key_value.key.split(",")[0])
        if row_index + 1 <= len(rowlists):
            rowlists[row_index].append(key_value.value)
        else:
            rowlists.append(list())
            rowlists[row_index].append(key_value.value)
        
    num_columns = (len(rowlists[0]))
    num_rows = len(rowlists)
    if num_columns == 0:
        num_columns += 1

    for i in range(num_columns):
        key = str(num_rows) + "," + str(i)
        key_value_pair = KeyValue(table_dictionary=table, key=key, value=" ")
        key_value_pair.save()
    messages.success(request, "Row successfully added.")

    return HttpResponseRedirect(reverse('project-domain-table', kwargs={'pk':pk, 'uk':uk}))


def domain_table(request, pk, uk):

    table = retrieveTable(pk, uk)
    key_value_queryset = KeyValue.objects.filter(table_dictionary=table)
    if request.method == "POST":
        # saving data
        # request.POST.items() contains all the items passed through the form
        for key,value in request.POST.items():
            if "," in key:
                if (KeyValue.objects.filter(table_dictionary=table, key=key)):
                    key_value_pair = KeyValue.objects.filter(table_dictionary=table, key=key)[0]
                    key_value_pair.value = value
                else:
                    key_value_pair = KeyValue(table_dictionary=table, key=key, value=value)
                key_value_pair.save()
                
                # print (key + ":" + value)
        messages.success(request, "Table successfully saved.")

    # retrieving data
    columnlist = []
    rowlists = [[]]
    for key_value in key_value_queryset:
        row_index =  int(key_value.key.split(",")[0])
        if row_index + 1 <= len(rowlists):
            rowlists[row_index].append(key_value.value)
        else:
            rowlists.append(list())
            rowlists[row_index].append(key_value.value)


    # debugging
    # print (rowlists)
    # for key_value in key_value_queryset:
    #     print (key_value.key + ":" + key_value.value)

    columnlist = rowlists[0]
    # rowlists = rowlists[1:len(rowlists)]
    
    project = Project.objects.get(id=pk)
    dom = Domain.objects.filter(id=uk)[0]
    # print (columnlist)
    # print (rowlists)
    context = {
        'project':project,
        'uk':uk,
        'columnlist': columnlist,
        'rowlists': rowlists,
    }
    return render(request, 'projects_app/project/project_domain_table.html', context)

# TableDictionary.objects.all().delete()
# KeyValue.objects.all().delete()

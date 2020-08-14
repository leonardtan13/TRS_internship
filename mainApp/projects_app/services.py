# This file contains all the business logic / services
# Access the functions defined here by calling services.function_name() in views.py
from projects_app.models import Customer, Message, Domain, Objective, Project, WorkItem


def add_project_workitem(project, workitems):
    """
    This function takes in a project object and a list of work items to add to the project
    The list of work items added will replace the current work items that are tagged to the project
    """
    current_workitems = project.workitems.all()
    for w in current_workitems: # this for loop removes all workitems tied to the project
        project.workitems.remove(w)
    all_workitems = WorkItem.objects.all() # getting all workitems in DB
    for w in all_workitems:
        if w.description in workitems:
            project.workitems.add(w)
    
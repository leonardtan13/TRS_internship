from django import forms
from .models import Customer, Project
import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm(forms.ModelForm):

    # proposal_date = forms.DateField(widget=DateInput, required=False)

    class Meta:
        model = Project
        fields = ("customer", 'objectives', 'domains' , 'proposaldate', 'startdate', 'enddate','fees','feesaftergrant','billing1','billing2','billing3')
        widgets = {
            'objectives': forms.CheckboxSelectMultiple,
            'domains': forms.CheckboxSelectMultiple,
            'proposaldate': forms.SelectDateWidget,
            'startdate': forms.SelectDateWidget,
            'enddate': forms.SelectDateWidget,
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", 'address1', 'address2', 'city')

class ProjectStatusForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ("status",)
        widgets = {
            'status':forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))






from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from nesis_app.models import CustomerOrganization, Mission, Application, Partner

class DateInput(forms.DateInput):
    input_type = 'date'
class CustomerOrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerOrganizationForm, self).__init__(*args, **kwargs)


    class Meta:
        model = CustomerOrganization
        fields = ['name', 'acronym', 'country', 'address', 'url','last_interaction_date','stakeholder_type','value_for_nasa','downstream_partners','missions','role_for_mission','applications_used'
                  ,'role_per_application','point_of_contact','organization_needs']
        CHOICES = CustomerOrganization.CHOICES
        COUNTRIES=CustomerOrganization.COUNTRIES
        widgets = {
            'last_interaction_date': forms.DateInput(attrs={'type': 'date'}),
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter a name for the organization'}),
            'acronym': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter the acronym for the organization'}),
            'country':forms.Select(choices=COUNTRIES, attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Physical address', 'rows': 3}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a URL for the organization'}),
            'last_interaction_date': DateInput(attrs={'class': 'form-control w-25'}),
            'stakeholder_type': forms.Select(choices=CHOICES, attrs={'class': 'form-control'}),
            'value_for_nasa': forms.Textarea(attrs={'class': 'form-control','rows': 5}),
            'downstream_partners': forms.ModelMultipleChoiceField(
                queryset=Partner.objects.all(),
                widget=forms.CheckboxSelectMultiple,
            ),
            'missions':   forms.ModelMultipleChoiceField(
                queryset=Mission.objects.all(),
                widget=forms.CheckboxSelectMultiple
            ),
            'role_for_mission': forms.TextInput(attrs={'class': 'form-control'}),
            'applications_used': forms.ModelMultipleChoiceField(
                queryset=Application.objects.all(),
                widget=forms.CheckboxSelectMultiple
            ),
            'role_per_application': forms.TextInput(attrs={'class': 'form-control'}),
            'point_of_contact': forms.ModelMultipleChoiceField(
                queryset=User.objects.all(),
                widget=forms.CheckboxSelectMultiple
            ),
            'organization_needs': forms.Textarea(attrs={'class': 'form-control','rows': 5}),


        }

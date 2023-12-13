"""
This forms.py file contains the forms that will be displated in the frontend
The user can select the source of the panel as well as give the testID
This data is used in views.py
"""
from django import forms
# This touple is used in the class ContactForm,
# it gives the name of the choices of the ChoiceField
# as well as its values once selected
CHOICES = (
        ("NGTD", "NGTD"),
        ("PanelApp", "PanelApp"),
    )

class ContactForm(forms.Form):
    """
    A class to take in the arguments from the user interface 

    ...
    Attributes
    ----------
    panel_ID : forms.CharField
        Collects the testID from user
    PanelSource: forms.ChoiceField
        Allows the user to select the source of the panel either from the NGTD or PanelApp
    ...
    Methods
    -------
    """
    panel_ID = forms.CharField(label="Input Panel ID",required=True)
    PanelSource = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
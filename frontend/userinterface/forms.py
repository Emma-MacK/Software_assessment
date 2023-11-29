from django import forms

CHOICES = (
        ("NGTD", "NGTD"),
        ("PanelApp", "PanelApp"),
    )


class ContactForm(forms.Form):
    panel_ID = forms.CharField(label="Input Panel ID",required=True)
    PanelSource = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


from django.shortcuts import render, redirect

from userinterface.forms import ContactForm
from django. contrib import messages
from userinterface.ToolModule import tool

#print(sys.path)
"""
This views.py file takes in the scripts from the backend as well
as interact with the display of data. It
1) It imports the tool.py module
2) Creates a new form
3) Displays the output from tool.py
"""



def contact(request):
  """ 
  create a new form and display it on urls.py
  """
  form = ContactForm() # instantiate a new form here
  result(request)
  return render(request,
          'userinterface/contact.html',
          {'form': form}) # pass that form to the template



def result(request):

    """
    This function will take in the information in the contact form and will attempt to display it at the URL /results
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            panelID = form.cleaned_data["panel_ID"]
            panelSource = form.cleaned_data["PanelSource"]
            hgncList, successfulRequest = tool.tool(panelID,panelSource)
            # the messages will be displated through the logic in contact.html
            messages.success(request, panelID + "\n " + panelSource)
            if(successfulRequest):
                messages.add_message(request, messages.INFO, hgncList)
            else:
                messages.add_message(request, messages.INFO, "Was not able to return Gene Panel")

    else:
        form = ContactForm()
        messages.add_message(request, messages.INFO, "NO answer")


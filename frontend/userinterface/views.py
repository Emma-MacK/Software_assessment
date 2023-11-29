from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from userinterface.forms import ContactForm
from django. contrib import messages


import sys
sys.path.insert(0, "/home/raymondmiles/Software_assessment/src/ToolModule")
import tool
 # insert the path to the folder
sys.path.insert(0, "/home/raymondmiles/Software_assessment/frontend/userinterface")

def contact(request):
  form = ContactForm() # instantiate a new form here
  result(request)
  return render(request,
          'userinterface/contact.html',
          {'form': form}) # pass that form to the template


### This function will take in the information in the contact form and will attempt to display it at the URL /results

def result(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            panelID = form.cleaned_data["panel_ID"]
            panelSource = form.cleaned_data["PanelSource"]
            tool.tool(panelID,panelSource)
            #messages.add_message(request, messages.INFO, "Successful Request")
            messages.success(request, panelID + "\n " + panelSource)
    else:
        form = ContactForm()
        messages.add_message(request, messages.INFO, "NO answer")

    #return render(request, "userinterface/result.html", {"form": form})

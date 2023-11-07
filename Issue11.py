#!/usr/bin/env python

import requests

# get id
id = "R67"

# panelapp aerver
server = "https://panelapp.genomicsengland.co.uk/api/v1"
# insert R code 
ext = "/panels/" + id

# adds server and ext with id 
r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

#returns data
decoded = r.json()
print(repr(decoded))




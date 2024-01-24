## How to start

This code can be run from the Software_assessment/frontend folder. 

You can run by going into the frontend folder and typing:

```python
python manage.py runserver 8000
```

This will run the django frontend locally at http://127.0.0.1:8000/

To close the server you can type ctrl + C on the command line.
## What are the inputs and outputs

The user interfaces has a text field where the user can input the panel ID. The user then selects the panel source (NGTD or PanelApp). If the panelID is innapropriate to query panelApp the message returned in the front end will be "Was not able to return Gene Panel"


On clicking submit either the NGTD targeted genes entry or the PanelApp HGNC IOs will be displayed.


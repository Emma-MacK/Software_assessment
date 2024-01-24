# Installation Guide

Panel Manager v2, in it's current iteration, can be interacted with/communicate with in 3 different ways. It is recommended to consider your personal needs and install the programm accordingly.

In the first instance however you must start by cloning the git repository.

Either via http://


Or via ssh//

for example:

`git clone https://github.com/Emma-MacK/Software_assessment`

N.B. We ask that third party users create their own copy of the github repository before cloning it locally!

The environment for running the tool can be set up with the following commands

```
conda env create -n example_environment -f environment.yaml
conda activate example_environment
pip install -r requirements.txt

```
To exit the environment you can use

`conda deactivate`


## Docker

Alternatively to creating a conda environment, docker could be used for running commands.
Documentation on running docker can be found at:

[Running Docker](Running_Docker.md)

## Commandline

If you are planning to interact with Panel Manager through the commandline only this will give you the most functionality.
running the core tool will

- Print the NGTD file version currently being used
- Print the age of the NGTD and update to the latest version if necessary
- Print panel information
- Print the HGNC IDs of genes in the panel
- Query Variant Validator
- Use Variant Validator response to create a bed file

Example

`python src/tool_v2.py -ID R128`

/ should ask if json should automatically be pushed to database as this will be needed in their anyway

## Django

A Django app can be used for running the older version of the tool. This can print information on the gene panel, and return HGNC IDs of genes in a panel

Information on running the Django app can be found [here](FrontendDocs.md)


## Future developments ##

As this project progresses more features will be added.
Details of planned changes can be found in [The future developments document](Future_development.md)
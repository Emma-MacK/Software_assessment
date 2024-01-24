# Installation Guide

Panel Manager v2, in it's current iteration, can be interacted with/communicate with in 3 different ways. It is recommended to consider your personal needs and install the programm accordingly.

In the first instance however you must start by cloning the git repository.

Either via http://


Or via ssh//

for example:

`git clone https://github.com/Emma-MacK/Software_assessment`

N.B. We ask that third party users create their own copy of the github repository before cloning it locally!


conda create with yaml
install requirements.txt

## Docker
Alternatively to creating a conda environment, docker could be used for running commands.
Documentation on running docker can be found at:

[Running Docker](Running_Docker.md)

## Commandline
If you are planning to interact with Panel Manager through the commandline only this will give you the most functionality.
running the core tool will

- print panel information
- create a bed file
- add more info

/ should ask if json should automatically be pushed to database as this will be needed in their anyway

## Django

A Django app can be used for running the older version of the tool. This can print information on the gene panel, and return HGNC IDs of genes in a panel

Information on running the Django app can be found [here](FrontendDocs.md)
<!-- where would I make not of future development plans. -->
<!-- We would need to install django on a host machine and then make it externally available. - @ Raymond have you dont this before? -->
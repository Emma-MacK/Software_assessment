# Panel Assigner v1 (holding name) #

## APP usage ##
Using argParser the Rcode TestID is used to pull panel information from either the National Genomic Test Directory (NGTD) or PanelAppD

Required Inputs:
1) Test directory code: -ID followed by test code ("RXXX")
2) Panel source being used: -PanS followed by "NGTD" (ie National Genomic Test Directory) or "PanelApp"

e.g. python3 src/tool.py -ID <"RXXX"> -PanS <"NGTD"> or <"PanelApp">

N.B. It is important that when running the tool you run from root directory and specify the file directory of the python script. This is to ensure access to the excel file in the root directory

## Folder structure ##

```
Overview of the file structure
.
├── bin
│   └── README.md
├── docs
│   └── README.md
├── Draft_scripts
│   └── emma_get_bed.py
├── environment.yml
├── Issue11.py
├── LICENCE
├── Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx
├── README.md
├── src
│   ├── README.md
│   ├── requirements.txt
│   ├── tool.py
│   └── unusedclasses
│       └── argument_parser.py
├── test.py
└── tests
    └── README.md
```

## Branches ##

Main - the current minimally functional version of the product. The current release is v1
Develop - branch of product in the development. Branches will be merged into here to ensure changes don't clash
Issue branches - branches linked to an issue or requested change. Once happy will be merged into develop.

## Issue Process for user requirement ##

- new user requirement documented in issue
- bulletpoint broken down steps to meet requirement
- add issue to KanBan board


# How to run #

You can run by going into the frontend folder and typing:
python manage.py runserver

## Plans for future development ##

Any current plans for future development are recorded in git issues.The desired end product is a tool to manage gene panels for NHS National genomic test directory tests in the laboratory and use this to record the testing carried out for individual patients. 
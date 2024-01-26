# Panel Assigner v2 #

This tool is designed to take an R code and return a list of genes and bed files for the requested test. A database storing the panel request information, the gene informations, and the bedfile can be created by pushing the information produced by running the tool to the database.

## APP usage ##


Documentation on the installation and setup of the app can be found [here.](docs/Installation.md)

Required Inputs:
1) Test directory code: -ID followed by test code ("RXXX")

`python3 src/tool_v2.py -ID <"RXXX">`

This will start the tool which performs the following:

- Checking the most recent version of the NGTD is being used, and updating if required
- Check that R code is in the NGTD, and check if the user wants to continue if not
- Query PanelApp with the requested R code, retrun warnings if the R code does not correspond to a NGS panel
- From the PanelApp query, extract the HGNC IDs for genes in the requested panel
- Use the HGNC IDs to query Variant Validator, and create a bedfile and json file for each gene in the requested panel
- Logging of commands and requests throughout

The information produced by the tool can be pushed to a database for later retrieval and interaction. Details on how to interact with the database can be found [here.](docs/Running_database.md)

An earlier version of the tool is available in a webpage format as well. Details on running the interactive webpage can be found [here.](docs/FrontendDocs.md)

The tool can also be run using Docker. Details on using the docker can be found [here.](docs/Running_Docker.md)

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


## Plans for future development ##

Plans for future development are documented [here.](docs/Future_development.md)

Any current plans for future development are recorded in git issues.The desired end product is a tool to manage gene panels for NHS National genomic test directory tests in the laboratory and use this to record the testing carried out for individual patients. 

## Needing help ##

Need help running the tool? Details of how to request help can be found [here.](docs/Seeking_help.md)
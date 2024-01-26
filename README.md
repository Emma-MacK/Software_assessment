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

The output bed files will be stored in an output folder in a folder corresponding to the date and time the tool was run.

The information produced by the tool can be pushed to a database for later retrieval and interaction. Details on how to interact with the database can be found [here.](docs/Running_database.md)

An earlier version of the tool is available in a webpage format as well. Details on running the interactive webpage can be found [here.](docs/FrontendDocs.md)

The tool can also be run using Docker. Details on using the docker can be found [here.](docs/Running_Docker.md)

## Folder structure ##

Overview of existing folder structure

```
.
├── config
├── docs
├── frontend
│   ├── frontend
│   │   └── __pycache__
│   └── userinterface
│       ├── config
│       ├── migrations
│       │   └── __pycache__
│       ├── __pycache__
│       ├── static
│       │   └── userinterface
│       ├── templates
│       │   └── userinterface
│       └── ToolModule
│           └── __pycache__
├── images
├── output
│   ├── 25012024_101359
│   └── logs
├── src
│   └── database
├── test_directory_file
└── tests
    ├── bedfiles
    ├── gene_info_jsons
    ├── panel_info_jsons
    └── __pycache__
```

## Testing ##

Testing is still in development. Tests currently exist for the functions get_hgncIDs and call_transcript_make_bed. These can be run with `pytest` from the root directory

## Logging ##

Logging is performed throught the process of running the tool. The log is stored in `output/logs/runlog.log``

## Plans for future development ##

Plans for future development are documented [here.](docs/Future_development.md)

Any current plans for future development are recorded in git issues.The desired end product is a tool to manage gene panels for NHS National genomic test directory tests in the laboratory and use this to record the testing carried out for individual patients.

## Needing help ##

Need help running the tool? Details of how to request help can be found [here.](docs/Seeking_help.md)
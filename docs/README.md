# Project Goal #x

A tool to manage gene panels for NHS National genomic test directory tests in the laboratory

# Panel Assigner v1 (holding name) #

## APP usage ##
Using argParser the Rcode TestID is used to pull panel information from either the National Genomic Test Directory (NGTD) or PanelAppD

Required Inputs:
1) Test directory code: -ID followed by test code ("RXXX")
2) Panel source being used: -PanS followed by "NGTD" (ie National Genomic Test Directory) or "PanelApp"

e.g. python3 src/tool.py -ID <"RXXX"> -PanS <"NGTD"> or <"PanelApp">

N.B. It is important that when running the tool you run from root directory and specify the file directory of the python script. This is to ensure access to the excel file in the root directory

# Folder structure #

Overview of the files structure

Files:
modules.py – all the functions we create are held here to be called into the final script
tests.py, contains tests for each of the created functions, ensuring they work + also environment tests
main.py – the main script that calls the modules, runs the tests and performs the desired process.

For each added functionality, create and test function individually, add to modules.py, create a test in tests.py, add to main script.

# Branches #

Main - the current minimally functional version of the product. The current release
Develop - branch of product in the development. Branches will be merged into here to ensure changes don't clash
Issue branches - branches linked to an issue or requested change. Once happy will be merged into develop.

# Issue Process for user requirement #

- new user requirement documented in issue
- bulletpoint broken down steps to meet requirement
- add issue to KanBan board
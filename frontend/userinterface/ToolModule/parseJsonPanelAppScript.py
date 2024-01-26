"""
This function will handle the parsing of the
JSON returned from PanelApp into the necessary fields.
"""
import json
import os
import pandas as pd
import requests


def parse_json_panelapp(r, logfile):
    """
    This function will handle the parsing of
    the JSON returned from PanelApp into the necessary fields.
    It takes in the response object parses it and returns
    a dataframe object with the following columns:
    0   uniqueID
    1   hgnc_IDs
    2   gene_Name
    3   gene_Symbol
    4   OMIM_Gene
    """
    try:
        # check if the status code is 200 (OK)
        if r.status_code == 200:
            # Try to parse the response as json
            print("The request was successful!")
            decoded = r.json()
            # Extract gene list
            decoded_genes = decoded['genes']
            # get uniqueID
            unique_num = str(decoded['id']) + "_" + decoded['version']
            try:
                hgnc_IDs = []
                gene_names = []
                gene_symbols = []
                omim_genes = []
                for x in decoded_genes:
                    # strings
                    genes = x.get('gene_data', {}).get('hgnc_id')
                    gene_name = x.get('gene_data', {}).get('gene_name')
                    omim_gene = x.get('gene_data', {}).get('omim_gene')
                    gene_symbol = x.get('gene_data', {}).get('gene_symbol')
                    # Iteratively fill lists with gene data
                    hgnc_IDs.append(genes)
                    gene_names.append(gene_name)
                    gene_symbols.append(gene_symbol)
                    omim_genes.append(omim_gene)
                # prepare lists to enter dataframe
                zipped = list(zip(hgnc_IDs, gene_names,
                                  gene_symbols, omim_genes))
                # populate dataframe with lists
                df_columns = ['hgnc_IDs', 'gene_Name',
                              'gene_Symbol', 'OMIM_Gene']
                entries = pd.DataFrame(zipped, columns=df_columns)
                # insert uniqueID column
                entries.insert(0, 'uniqueID', unique_num)
                if logfile is True:
                    os.makedirs('logFiles', exist_ok=True)
                    entries.to_csv('logFiles/entries.csv')
                return entries
            except KeyError:
                print('KeyError:PanelApp output JSON doesn\' contain \
                \'gene_name\' or \'hgnc_id\' or \'omim_gene\' or \
                \'gene_symbol\' key')
            else:
                print("")
        else:
            # Raise an exception if the status code is not 200
            print("you shall not pass!")
            r.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Catch and print any requests exception
        print(e)
    except json.decoder.JSONDecodeError as e:
        # Catch and print any json decoding exception
        print(e)

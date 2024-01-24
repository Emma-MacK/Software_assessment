"""
This function will handle the parsing of the JSON returned from PanelApp into the necessary fields.
"""
import pandas as pd
import os 
import requests
import json
from json import JSONDecodeError
def parseJsonPanelAppFunction(r, logfile):
    """
    This function will handle the parsing of the JSON returned from PanelApp into the necessary fields.
    It takes in the response object parses it and returns a dataframe object with the following columns:
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
            #decoded_genes =decoded['genes'] #Extract gene list
            #uniqueNum = str(decoded['id']) + "_" + decoded['version'] # get uniqueID
            decoded_genes =decoded['genes'] #Extract gene list
            uniqueNum = str(decoded['id']) + "_" + decoded['version'] # get uniqueID
            try:
                hgncIDs = []
                geneNames = []
                geneSymbols = []
                omimGenes = []
                for x in decoded_genes:
                    genes = x.get('gene_data',{}).get('hgnc_id') # string
                    geneName = x.get('gene_data',{}).get('gene_name')
                    omimGene = x.get('gene_data',{}).get('omim_gene')
                    geneSymbol = x.get('gene_data',{}).get('gene_symbol')
                    #Iteratively fill lists with gene data
                    hgncIDs.append(genes)
                    geneNames.append(geneName)
                    geneSymbols.append(geneSymbol)
                    omimGenes.append(omimGene)
                zipped = list(zip(hgncIDs, geneNames,geneSymbols, omimGenes)) # prepare lists to enter dataframe
                entries = pd.DataFrame(zipped, columns=['hgnc_IDs', 'gene_Name', 'gene_Symbol', 'OMIM_Gene']) # populate dataframe with lists
                entries.insert(0, 'uniqueID', uniqueNum) #insert uniqueID column
                if logfile is True:
                    os.makedirs('logFiles', exist_ok=True)
                    entries.to_csv('logFiles/entries.csv')
                return(entries)
            except KeyError:
                print('KeyError:PanelApp output JSON doesn\' contain \'gene_name\' or \'hgnc_id\' or \'omim_gene\' or \'gene_symbol\' key')
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
    except JSONDecodeError:
        print('Response could not be serialized')

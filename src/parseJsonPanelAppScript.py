"""
This function will handle the parsing of the JSON returned from PanelApp into the necessary fields.
"""
import pandas as pd
import os 

def parseJsonPanelAppFunction(r, logfile):
    """
    This function takes in the response object parses it and returns a dataframe object with the following columns:
    0   uniqueID 
    1   hgnc_IDs     
    2   gene_Name    
    3   gene_Symbol  
    4   OMIM_Gene    
    """
    decoded = r.json()
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
        if logfile == True:
            os.makedirs('logFiles', exist_ok=True)  
            entries.to_csv('logFiles/entries.csv')
        return(entries)


    except KeyError:
        print('KeyError:PanelApp output JSON doesn\' contain \'gene_name\' or \'hgnc_id\' or \'omim_gene\' or \'gene_symbol\' key')

    else:
        print("")

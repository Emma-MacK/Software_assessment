import pandas as pd

test_code="R67"


# get an excel into a pandas dataframe, getting specific columns
xls = 'Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx'
test_directory_df = pd.read_excel(xls, 'R&ID indications', usecols="A:E", header=1)


panel = test_directory_df.loc[test_directory_df['Clinical indication ID'] == test_code]

print(panel['Target/Genes'].to_string(index=False))


# Description: First look at all given data


#========================================================================


# IMPORTS

import matplotlib.pyplot as plt
import argparse

from Bio import SeqIO
import pandas as pd

#========================================================================


# FASTA PREPROCESSING: Read in alignment with 5709 seqs x 18603 pos
#                      Compute completion


with open("DataBackUp_5709Seq/Supermatrix5079Seq.fa", "r") as filein:
    
    fasta = [i.split('\n') for i in filein.read().strip().split('\n\n')]
    
    SeqIDsTemp = fasta[0][::2]
    SeqIDs = [EachString.strip('>') for EachString in SeqIDsTemp]
    
    Seqs = fasta[0][1::2]
    Completion = [len(EachString) - EachString.count('-') for EachString in Seqs]
    
TempDict = {'db_id' : SeqIDs, 'Completion' : Completion}
dfFasta = pd.DataFrame(TempDict)


#========================================================================


# CSV PREPROCESSING: Read in dataframe with 5938 rows x 34 columns
#                    Merge completion

dfCSV = pd.read_csv("AllMitogenomesMaster_2021-04-17v2021-04-25.csv")
df = pd.merge(dfCSV, dfFasta, on="db_id")


#========================================================================


# DROP NON-NEGOTIABLES

df = df[df.Completion.notna()]
# Cannot not have actualy sequence

df = df[df.Completion > 10000]
# Cannot have a vastly incomplete sequence

df = df.drop(df[
        (df.species.isna()) &
        (df.genus.isna()) &
        (df.tribe.isna()) &
        (df.subfamily.isna()) &
        (df.family.isna()) &
        (df.superfamily.isna()) &
        (df.infraorder.isna())
    ].index)
# Cannot not have any membership information


# DROP NEGOTIABLES, EXPERIMENTALLY

AllColumns = df.columns.values.tolist()
for Col in AllColumns:
    if len(df[Col].dropna().unique()) <= 1:
         df = df.drop([Col], axis=1)
         # Drop all cols that are all NaNs
         # or all NaNs + one other unique value
         # e.g. print(df['class'].dropna().unique()) returns 'Insecta'...
    else:
        NaNCount = (df[Col].isna()).sum()
        DataCount = len(df) - NaNCount   
        print (f"{Col}: {DataCount}/{len(df)} not NaNs")
        print(f"{len(df[Col].dropna().unique())} unique not NaN entries.")
        print("\n")


#========================================================================


# DECIDE ON INDEXING:

df = df.set_index(['family']).sort_index()
# 3015/3179 not NaNs with 127 unique not NaN entries.

print(df.index.value_counts()[0:10])
# Top ten families
    
CurculionidaeDF = df[df.index == 'Curculionidae'] # 511 entries
StaphylinidaeDF = df[df.index == 'Staphylinidae'] # 385 entries
CerambycidaeDF = df[df.index == 'Cerambycidae']   # 164 entries
ScarabaeidaeDF = df[df.index == 'Scarabaeidae']   # 127 entries
CarabidaeDF = df[df.index == 'Carabidae']         # 115 entries
TenebrionidaeDF = df[df.index == 'Tenebrionidae'] # 81 entries
MordellidaeDF = df[df.index == 'Mordellidae']     # 76 entries
CoccinellidaeDF = df[df.index == 'Coccinellidae'] # 71 entries
NitidulidaeDF = df[df.index == 'Nitidulidae']     # 70 entries
ElateridaeDF = df[df.index == 'Elateridae']       # 50 entries


#========================================================================



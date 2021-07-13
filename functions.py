

# Description: First look at all given data


#========================================================================


# IMPORTS

import matplotlib.pyplot as plt
import argparse

from Bio import SeqIO
import pandas as pd


#========================================================================


def AppendSeqCompletion(CSVPath, FastaPath):
    
    """
    Reads in CSV file. Append completion score to sequence.
    Reads in alignment as fasta file, see how complete they are.
    
    In: (2 item) Strings where strings contain relative path to metadata csv file and its assocaited alignment/fasta file.
    Out: (1 item) Pandas dataframe with all CSV columns and % Completion.
    """
    
    CSVDF = pd.read_csv(str(CSVPath))
    
    with open(str(FastaPath), "r") as filein:
        fasta = [i.split('\n') for i in filein.read().strip().split('\n\n')]
    SeqIDsTemp = fasta[0][::2]
    SeqIDs = [EachString.strip('>') for EachString in SeqIDsTemp]
    Seqs = fasta[0][1::2]
    Completion = [1 - (EachString.count('-')/len(EachString)) for EachString in Seqs]
    TempDict = {'db_id' : SeqIDs, 'Completion' : Completion}
    FastaDF = pd.DataFrame(TempDict)

    Outdf = pd.merge(CSVDF, FastaDF, on="db_id")

    return Outdf

 #========================================================================


def CleanData(df, cutoff):
    
    """
    Reads in dataframe and drop the non-negotiables.
    NaNs in the genus/species columns are filled.
    
    In: (2 item) Dataframe representing all metadata with % completion.
                 Min % Complettion required as float (e.g. 0.90)
    Out: (1 item) Cleaned df with (complete) sequence representation, at least *some* phylo membership information, and useful columns.
    """
    
    df = df[df.Completion.notna()]
    # Cannot not have actualy sequence

    df = df[df.Completion > float(cutoff)]
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

    AllColumns = df.columns.values.tolist()
    for Col in AllColumns:
        if len(df[Col].dropna().unique()) <= 1:
            df = df.drop([Col], axis=1)
            # Drop all cols that are all NaNs
            # or all NaNs + one other unique value
            # e.g. print(df['class'].dropna().unique())
            # returns 'Insecta'
    
    FillNaNValues = {"genus": "Unknown-genus", "species": "Unknown-species"}
    Outdf = df.fillna(value = FillNaNValues)

    return Outdf


#========================================================================


def WriteRenamedFasta(df, ReadPath, WritePath):
    
    df = df.set_index(['db_id']).sort_index()
    df.index = '>' + df.index.astype(str)

    NameDict = {}
    for index, row in df.iterrows():
        CommonName = f">{row['genus']}_{row['species']}_({row['family']})"
        NameDict[index] = CommonName

    with open(str(ReadPath), "r") as filein:
        fasta = [i.split('\n') for i in filein.read().strip().split('\n\n')]
    SeqIDs = fasta[0][::2]
    Seqs = fasta[0][1::2]
    SeqsDict = dict(zip(SeqIDs, Seqs))

    FastaOut = open(WritePath, "a")
    for db_id, NewName in NameDict.items():
        FastaOut.write(NewName + '\n')
        FastaOut.write(SeqsDict[db_id] + '\n')
    FastaOut.close()

    #========================================================================

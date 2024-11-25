

# Description: Functions for taking a first look at all given data


#========================================================================


# IMPORTS

import pandas as pd

def AppendSeqCompletion(CSVPath, FastaPath):
    
    """
    Reads in CSV file. Append completion score to enrty if entry in Fasta.
    Reads in alignment as fasta file for completion score.
    
    In: (2 items) Strings where strings contain relative path to metadata csv file and its assocaited alignment/fasta file.
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


def CleanRows(df):
    
    """
    Reads in dataframe and drop the non-negotiables.
    NaNs in the genus/species columns are filled.
    
    In: (1 items) Dataframe representing all metadata with % completion.
    Out: (1 item) Cleaned df with at least *some* phylo membership information, and useful columns.
    """
    
    df = df[df.Completion.notna()]
    # Cannot not have actual sequence

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

    return df


#========================================================================


def CleanCols(df):
    
    AllColumns = df.columns.values.tolist()
    for Col in AllColumns:
        if len(df[Col].dropna().unique()) <= 1:
            df = df.drop([Col], axis=1)
            # Drop all cols that are all NaNs
            # or all NaNs + one other unique value
            # e.g. print(df['class'].dropna().unique())
            # returns 'Insecta'
            print(f"{Col}: Dropped. One or fewer not NaN entries.")
        else:
            NaNCount = (df[Col].isna()).sum()
            DataCount = len(df) - NaNCount
            print(f"{Col}: {DataCount}/{len(df)} not NaNs")
            print(f"{len(df[Col].dropna().unique())} unique not NaN entries.")

    return df

            
#========================================================================


def WriteRenamedFasta(df, ReadPath, WritePath):

    """
    Reads in old fasta, and renames all entries with respect to
    info contained in dataframe. Write new names and seqs to new file."
    
    In: (3 items) Dataframe containing db_id and new names
                  ReadPath to old fasta
                  WritePath to new fasta
    Out: (1 item) Fasta file with renamed entries.
    """
    
    df = df.reset_index(level='family')
    df = df.set_index(['db_id']).sort_index()
    df.index = '>' + df.index.astype(str)

    NameDict = {}
    for index, row in df.iterrows():
        CommonName = f">{row['species']} ({row['family']})"
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

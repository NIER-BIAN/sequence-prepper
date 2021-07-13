

# Description: Linka's sequence prepper


# I want this tool to:
# Look here in this database -Database
# Look here in this fasta for the sequences -FastaIn
# but only let in almost complete sequences -MinCompletion
# I want these families -Families
# Fill "NaN"s with "unknown genus"/"unknown species"
# Rename them with Genus Species (Family)
# in a separate fasta file -FastaOut

#========================================================================


# IMPORTS

from functions import *
import pandas as pd

#========================================================================


def run(args):

    PathToDB = args.Database
    PathToFastaIn = args.FastaIn
    CompCutoff = args.MinCompletion
    TargetFamilies = args.Families.split(' ')
    FastaOut = args.FastaOut
    
    DF = AppendSeqCompletion(PathToDB, PathToFastaIn)
    print(len(DF))
    DFRemoveNaNs = CleanData(DF, CompCutoff)
    print(len(DFRemoveNaNs))
    DFCherryPicked = DFRemoveNaNs.loc[
        DFRemoveNaNs['family'].isin(TargetFamilies)
    ]
    print(len(DFCherryPicked))
    
    WriteRenamedFasta(DFCherryPicked, PathToFastaIn, FastaOut)

#========================================================================


def main():
    parser = argparse.ArgumentParser(description ="python SequencePrepper.py -Database *.csv -FastaIn Supermatrix5079Seq.fa -Families 'Staphylinidae Elateridae' -FastaOut Test.fa")
    parser.add_argument("-Database", help="Relative path of database containing renaming references.", required=True, dest="Database", type=str)
    parser.add_argument("-FastaIn", help="Relative path of fasta containing the actual sequences.", required=True, dest="FastaIn", type=str)
    parser.add_argument("-MinCompletion", help="Required percentage completion of sequences as float e.g. 0.50.", default=0.50, dest="MinCompletion", type=float)
    parser.add_argument("-Families", help="The list of families wanted in the outfile. List must be quoted and separated by a single space, like 'Staphylinidae Elateridae Nitidulidae'.", required=True, dest="Families", type=str)
    parser.add_argument("-FastaOut", help="Name of output fasta to be written at the end.", required=True, dest="FastaOut", type=str)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

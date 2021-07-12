# Description: Linka's sequence grepper

# I want this tool to:
# Look here in this database -Database
# Look here in this fasta -FastaIn
# Pull out these families -Families
# Fill "NaN"s under Genus/Species with "unknown genus"/"unknown species"
# Rename them with Genus Species (Family)
# in a separate fasta file -FastaOut
# and I want them already renamed

#========================================================================

# IMPORTS

from functions import *

#========================================================================


def run(args):

    PathToDB = args.db
    PathToFasta = args.fasta
    
    GenBank, CommonName = [], []
    for seq_record in SeqIO.parse(PathToGB, "genbank"):
        GenBank.append(">" + seq_record.name)
        CommonName.append(seq_record.annotations["source"][14:])

    NameDict = dict(zip(GenBank, CommonName))
    # NameDict['>NC_042922'] = "Himaloaesalus gaoligongshanus"
    # NameDict['>NC_042614'] = "Sinodendron rugosum"

    fasta = open(PathToFasta)
    newfasta= open(f"{PathToFasta}_renamed", "a")

    for line in fasta:
        if line.startswith('>'):
            line = line.strip('\n')
            newname= NameDict[line]
            newfasta.write('>' + newname + '\n')
        else:
            newfasta.write(line)

    fasta.close()
    newfasta.close()


#========================================================================


def main():
    parser.add_argument("-Database", help="Relative path of database containing renaming references.", required=True, dest="Database", type=str)
    parser.add_argument("-FastaIn", help="Relative path of fasta containing the actual sequences.", required=True, dest="FastaIn", type=str)
    parser.add_argument("-Families", help="The list of families wanted in the outfile. List must be quoted and separated by a single space, like 'Staphylinidae Elateridae Nitidulidae'.", required=True, dest="Families", type=list)
    parser.add_argument("-FastaOut", help="Name of output fasta to be written at the end.", required=True, dest="FastaOut", type=str)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

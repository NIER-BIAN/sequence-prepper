

# Description: Functions for taking a first look at all given data

# Clean Rows second round, look for complete sequences (MinCompletion)
# And specified families (TargetFamilies)

# Fill "NaN"s with "unknown genus"/"unknown species"
# Rename them like this: Genus Species, family
# Write to a separate fasta file (FastaOut)


#========================================================================


from functions import *
import pandas as pd


#========================================================================


# Look here in this database (CSVPath)
# Look here in this fasta for the sequences (FastaPath)
# AppendSeqCompletion

CSVPath = "AllMitogenomesMaster_2021-04-17v2021-04-25.csv"
FastaPath = "Supermatrix5079Seq.fa"

DF = AppendSeqCompletion(CSVPath, FastaPath)
print(f"Read in full database with {len(DF)} entries.")
print("\n")


#========================================================================


# Clean Rows first round, drop meaningless rows (no sequence, no tax info)
# Clean Cols, drop meaningless cols

DFCleanRowsOnly = CleanRows(DF)
print("Dropped entries without sequences")
print("Dropped sequences with no taxonomic membership whatsoever.")
print(f"Now working on cleaned database with {len(DFCleanRowsOnly)} entries.")
print("\n")

print(f"Cleaning Cols")
DFCleansed = CleanCols(DFCleanRowsOnly)
print("\n")


#========================================================================


# What do you even have? How many entries in each families
# And how complete are they?
# Write out CSV report describing final availability

DFIndexed = DFCleansed.set_index(['family']).sort_index()
# 3015/3179 not NaNs with 127 unique not NaN entries.
# 488/498 not NaNs with 144 unique not NaN entries.

FamilyCounts = DFIndexed.index.value_counts()
# Which families are most numerous

FamilyCompletion = DFIndexed['Completion'].groupby(['family']).mean()
# Which families are most complete

FamilyMinCompletion = DFIndexed['Completion'].groupby(['family']).min()

CursoryGlanceReport = pd.DataFrame(dict(Counts = FamilyCounts, AverageCompletion = FamilyCompletion, MinimalCompletion = FamilyMinCompletion)).sort_values(by=['Counts'], ascending=False)

CursoryGlanceReport.to_csv("498SeqAvailabilityReport.csv")


#========================================================================


# Set your standards and commit to choosing them
# Keep in mind how they were aligned.

MinCompletion = 0.50
# Cherrypick the non-overlap

DFCompletionFiltered = DFIndexed[DFIndexed.Completion >= MinCompletion]
print(f"Cherrypicked sequences that are at least {MinCompletion*100}% complete.")
print("\n")
print(f"Now working on completion-filtered database with {len(DFCompletionFiltered)} entries.")


#========================================================================


# Fill NaNs
# Write out CSV report describing family-wise completion now that
# completion has been filtered

FillNaNValues = {"genus": "UnknownGenus", "species": "UnknownSpecies"}
DFFilledNAs = DFCompletionFiltered.fillna(value = FillNaNValues)
print(f"Filled NaNs.")

FamilyCounts = DFFilledNAs.index.value_counts()
# Which families are most numerous
FamilyCompletion = DFFilledNAs['Completion'].groupby(['family']).mean()
# Which families are most complete
FamilyMinCompletion = DFFilledNAs['Completion'].groupby(['family']).min()

SecondRoundReport = pd.DataFrame(dict(Counts = FamilyCounts, AverageCompletion = FamilyCompletion, MinimalCompletion = FamilyMinCompletion)).sort_values(by=['Counts'], ascending=False)


#========================================================================


# Pick top N families
# Write out CSV report describing what was finally chosen

N = 10
TargetFamilies = list(SecondRoundReport.index[0:N])
DFCompAndFamFiltered = DFFilledNAs.loc[
    DFFilledNAs.index.isin(TargetFamilies)
    ]
print(f"Filtered for families: {TargetFamilies}.")
print(f"Now working on completion-and-family-filtered database with {len(DFCompAndFamFiltered)} entries.")

FamilyCounts = DFCompAndFamFiltered.index.value_counts()
# Which families are most numerous
FamilyCompletion = DFCompAndFamFiltered['Completion'].groupby(['family']).mean()
# Which families are most complete
FamilyMinCompletion = DFCompAndFamFiltered['Completion'].groupby(['family']).min()

FinalRoundReport = pd.DataFrame(dict(Counts = FamilyCounts, AverageCompletion = FamilyCompletion, MinimalCompletion = FamilyMinCompletion)).sort_values(by=['Counts'], ascending=False)

FinalRoundReport.to_csv("498SeqFinalReport.csv")


#========================================================================


# Set your standards and commit to choosing them
# Keep in mind how they were aligned.

FastaOut = "498_Top10Fam_Completion80.fasta"
WriteRenamedFasta(DFCompAndFamFiltered, FastaPath, FastaOut)


#========================================================================

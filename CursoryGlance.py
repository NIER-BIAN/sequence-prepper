# First look at the whole dataset

def LinkaGlance(df):
    
    AllColumns = df.columns.values.tolist()
    for Col in AllColumns:
        if len(df[Col].dropna().unique()) <= 1:
            df = df.drop([Col], axis=1)
            # Drop all cols that are all NaNs
            # or all NaNs + one other unique value
            # e.g. print(df['class'].dropna().unique())
            # returns 'Insecta'
            print(f"Dropped column: {col}")
        else:
            NaNCount = (df[Col].isna()).sum()
            DataCount = len(df) - NaNCount
            
        print(f"{Col}: {DataCount}/{len(df)} not NaNs")
        print(f"{len(df[Col].dropna().unique())} unique not NaN entries.")
        print("\n")

# df = df.set_index(['family']).sort_index()
# 3015/3179 not NaNs with 127 unique not NaN entries.
# print(df.index.value_counts()[0:10])
# Top ten families

    # CurculionidaeDF = df[df.index == 'Curculionidae'] # 511 entries
    # StaphylinidaeDF = df[df.index == 'Staphylinidae'] # 385 entries
    # CerambycidaeDF = df[df.index == 'Cerambycidae']   # 164 entries
    # ScarabaeidaeDF = df[df.index == 'Scarabaeidae']   # 127 entries
    # CarabidaeDF = df[df.index == 'Carabidae']         # 115 entries
    # TenebrionidaeDF = df[df.index == 'Tenebrionidae'] # 81 entries
    # MordellidaeDF = df[df.index == 'Mordellidae']     # 76 entries
    # CoccinellidaeDF = df[df.index == 'Coccinellidae'] # 71 entries
    # NitidulidaeDF = df[df.index == 'Nitidulidae']     # 70 entries
    # ElateridaeDF = df[df.index == 'Elateridae']       # 50 entries

import pandas as pd

INPUT_FILE = "School_Email_Lead_List__Sample.xlsx"
OUTPUT_FILE = "School_Email_Lead_List_Combined.csv"

def merge_all_tabs(input_file, output_file):
    print(f"Reading: {input_file}")
    xl = pd.read_excel(input_file, sheet_name=None, header=None)

    all_dfs = []

    for sheet_name, df in xl.items():

        if sheet_name == "Example of PTOsPTAs":
            state = "Example"
            df.columns = df.iloc[0]
            df = df.iloc[1:].reset_index(drop=True)
        else:
            state = str(df.iloc[0, 0])
            df.columns = df.iloc[1]
            df = df.iloc[2:].reset_index(drop=True)

        new_cols = []
        seen = {}
        for col in df.columns:
            s = str(col).strip()
            if s in seen:
                seen[s] += 1
                new_cols.append(f"{s}_{seen[s]}")
            else:
                seen[s] = 0
                new_cols.append(s)
        df.columns = new_cols

        col_map = {}
        for col in df.columns:
            s = col.strip().lower()
            if s == "district" and "District" not in col_map.values():
                col_map[col] = "District"
            elif s == "type" and "Type" not in col_map.values():
                col_map[col] = "Type"
            elif s == "school" and "School" not in col_map.values():
                col_map[col] = "School"
            elif s in ["email", "pto/pta email"] and "Email" not in col_map.values():
                col_map[col] = "Email"

        df = df.rename(columns=col_map)

        keep = [c for c in ["District", "Type", "School", "Email"] if c in df.columns]
        df = df[keep].copy()
        df["State"] = state

        if "Email" in df.columns:
            df["Email"] = df["Email"].astype(str)
            df = df[df["Email"].str.contains("@", na=False)]
            df = df[df["Email"] != "nan"]

        print(f"  {sheet_name}: {len(df)} emails found")
        all_dfs.append(df)

    combined = pd.concat(all_dfs, ignore_index=True)
    combined = combined[["State", "District", "Type", "School", "Email"]]
    combined.to_csv(output_file, index=False)
    print(f"\nDone! {len(combined)} total rows saved to: {output_file}")


if __name__ == "__main__":
    merge_all_tabs(INPUT_FILE, OUTPUT_FILE)

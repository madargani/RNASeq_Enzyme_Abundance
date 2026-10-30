#!/usr/bin/env python3
"""Pivot Atha.epscor.meanTPM.csv from wide to long format.

Input (wide): one column per condition, one row per id
Output (long): one row per id/condition combination with columns:
    id, condition, value
"""

from pathlib import Path

import numpy as np
import pandas as pd

# Project root is the directory containing this script
ROOT = Path(__file__).resolve().parent
INPUT_FILE = ROOT / "projects" / "halpha" / "Atha.epscor.meanTPM.csv"
OUTPUT_FILE = (
    ROOT / "projects" / "halpha" / "rnaseq-data" / "Atha.epscor.meanTPM.long.csv"
)


def main():
    # Read wide-format CSV (first column is the id, rest are conditions)
    df = pd.read_csv(INPUT_FILE)

    # The first column (the id column) has no header in the file; rename it
    df = df.rename(columns={df.columns[0]: "id"})

    # Melt: turn each condition column into its own row
    long_df = df.melt(
        id_vars=["id"],  # column to keep as identifier
        var_name="condition",  # new column holding condition names
        value_name="value",  # new column holding expression values
    )

    # Sort for tidiness, then reset index
    long_df = long_df.sort_values(["id", "condition"]).reset_index(drop=True)

    # Add value_std, value_std_log, value_log
    long_df["value_std"] = 0
    long_df["value_log"] = np.log(long_df["value"])
    long_df["value_std_log"] = 0

    # Write output
    long_df.to_csv(OUTPUT_FILE, index=False, sep="\t")

    print(f"Read {len(df)} rows x {len(df.columns)} columns from {INPUT_FILE}")
    print(f"Wrote {len(long_df)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

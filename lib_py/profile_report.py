"""
Generate Profiling Report
"""
import os
import pandas as pd
from pandas_profiling import ProfileReport
import sqlite3

def main():
    """
    Generate profiling report from DWH
    """
    with sqlite3.connect(os.path.join("output", "dwh.sqlite3")) as con:
        df = pd.read_sql_query("SELECT * FROM movies", con=con)
    report = ProfileReport(df, minimal=True, title="Movies aus SQL")
    report.to_file(os.path.join("output", "movies_report.html"))

if __name__ == "__main__":
    main()
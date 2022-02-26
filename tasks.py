import os
from invoke import task

@task
def welcome(c):
    print("Hallo und herzlich willkommen!")

@task
def mydir(c):
    print("Dein aktuelles Arbeitsverzeichnis ist:")
    c.run("pwd")

#@task
#def report(c):
#    import pandas as pd
#    from pandas_profiling import ProfileReport
#    df = pd.read_csv(os.path.join("input", "movies_metadata.csv"))
#    report = ProfileReport(df, minimal=True, title="Aus invoke")
#    report.to_file(os.path.join("output", "invoke_report.html"))

@task
def dwh(c):
    c.run("python lib_py/01_etl_mkoe.py")


@task
def full(c):
    welcome(c)
    mydir(c)
    dwh(c)
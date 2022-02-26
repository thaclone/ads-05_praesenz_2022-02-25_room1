from invoke import task
import os

@task
def welcome(c):
    print("Hallo und herzlich willkommen!")
    
@task
def mydir(c):
    print("Ihr aktueller Pfad lautet: ")
    c.run("pwd")
   

@task
def setup(c):
    if not os.path.exists("output"):
        print("Create output folder")
        c.run("mkdir output")
    else:
        print("Folder already exists")
   
@task
def runetl(c):
    print("ETL Prozess wird ausgeführt")
    c.run("python py_lib/01_etl_hma.py")
    
@task
def full(c):
    welcome(c)
    mydir(c)
    setup(c)
    
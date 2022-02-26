import os
from invoke import task

@task
def clear_output(c):
    """Clear output directory"""
    if os.path.exists("output"):
        c.run("rm -r output")

@task
def setup(c):
    """Setup directories"""
    if not os.path.exists("output"):
        c.run("mkdir output")

@task
def dwh(c, pty=True):
    """Generate DWH"""
    c.run("python lib_py/dwh.py")

@task
def report(c):
    """Generate profiling report from DWH"""
    from lib_py import profile_report
    profile_report.main()

@task
def apidoc(c):
    """Generate RST docs for lib_py"""
    lib_py_doc_path = os.path.join("docs", "lib_py")
    if os.path.exists(lib_py_doc_path):
        c.run("rm -r %s" % lib_py_doc_path)
    c.run("sphinx-apidoc lib_py -o %s -H Software" % lib_py_doc_path)

@task
def docs(c):
    """Generate HTML docs including lib_py"""
    build_path = os.path.join("_build", "html")
    apidoc(c)
    if os.path.exists(build_path):
        c.run("rm -r %s" % build_path)
    c.run("sphinx-build . %s" % build_path)

@task
def full(c):
    """Full build of our project"""
    clear_output(c)
    setup(c)
    dwh(c)
    report(c)
    docs(c)
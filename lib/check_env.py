"""
check module
Check settings
AUTHER:LUCAS
DATE:20220810
"""

import sys
import os
import subprocess
def python_version():
    """
    Check the current version of python
    """
    
    # required python versions ( 3.7-3.8)
    required_python_version_major = [3]
    required_python_version_minor = [7,8]
    
    # check for either of the required versions
    pass_check=False
    try:
        for major, minor in zip(required_python_version_major, required_python_version_minor):
            if (sys.version_info[0] == major and sys.version_info[1] >= minor):
                pass_check=True
    except (AttributeError,IndexError):
        sys.exit("CRITICAL ERROR: The python version found (version 1) " +
            "does not match the version required (version "+
            str(required_python_version_major)+"."+
            str(required_python_version_minor)+"+)")  

    if not pass_check:
        sys.exit("CRITICAL ERROR: The python version found (version "+
            str(sys.version_info[0])+"."+str(sys.version_info[1])+") "+
            "does not match the version required (version "+
            str(required_python_version_major)+"."+
            str(required_python_version_minor)+"+)")

def software():
    diamond_=subprocess.getstatusoutput('diamond --version')
    if diamond_[0]!=0:
        sys.exit("CRITICAL ERROR: The diamond not found")
    hmmsearch_=subprocess.getstatusoutput('hmmsearch -h')
    if hmmsearch_[0]!=0:
        sys.exit("CRITICAL ERROR: The hmmsearch not found")
    parallel_=subprocess.getstatusoutput('parallel -V')
    if parallel_[0]!=0:
        sys.exit("CRITICAL ERROR: The parallel not found")
    seqkit_=subprocess.getstatusoutput('seqkit --help')
    if seqkit_[0]!=0:
        sys.exit("CRITICAL ERROR: The seqkit not found")
    prodigal_=subprocess.getstatusoutput('prodigal -h')
    if prodigal_[0]!=0:
        sys.exit("CRITICAL ERROR: The prodigal not found")

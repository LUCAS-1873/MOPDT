#!/usr/bin/env python
"""
MOPDT : Methane-Oxidation Protein DetecTor (MOPDT)

MOPDT is a pipeline for efficiently and accurately detecting Methane-Oxidation Protein.

To Run: MOPDT -I <input.fastq> -O <output_dir>

AUTHER: LUCAS
DATE:20240314
VERSION:0.0.1
"""

import warnings
warnings.filterwarnings("ignore")
import sys
import os
import lib.set_arg as arg
from lib.run_main import MOPDT_main,MOPDT_gene_call
#configure software path


print("#"*50)
print("MOPDT Start to deal with {}!".format(arg.IN()))
print("#"*50)

#with open("{}/QPP_Database/end_result/total_uniq_gene_len".format(sys.path[0])) as f:
#    initial_uniq_len=int(f.read())


def main():
    # Try to load one of the MOPDT modules to check the installation
    try:
        import lib.check_env as check
    except ImportError:
        sys.exit("CRITICAL ERROR: Unable to find the MOPDT python package." +
            " Please check your install.") 

    # Check the python version
    check.python_version()
    # Check the necessary software
    check.software()
    #run
    OUT=arg.OUT()
    while OUT.endswith("/"):
        OUT=OUT[:-1]
   
    NUCL=arg.NUCL()
    if arg.GENOME():
        if not NUCL:
            sys.exit("--genome must used with --nucl")
    if NUCL:
        #如果是nucl，则使IN变量读入MOPDT_gene_call 返回的 值，作为下面MOPDT_main的输入
        IN=MOPDT_gene_call(IN=arg.IN(),
                OUT=OUT,
                GENOME=arg.GENOME())
    else:
        IN=arg.IN()



    MOPDT_main(IN=IN,
            OUT=OUT,
            LEVEL=arg.LEVEL(),
            Intermediate=arg.Intermediate(),
            THREAD=arg.thread(),
            NO_CHECK=arg.NO_CHECK(),
            DIAMOND_DB="{}/DB/MOPD_rep.dmnd".format(sys.path[0]),
            CHECK_DB="{}/DB/check_db.dmnd".format(sys.path[0]),
            HMM_DB='{}/DB/HMM/'.format(sys.path[0]).format(sys.path[0]),
            HMM_DB_KO='{}/DB/HMM_kofam/'.format(sys.path[0]).format(sys.path[0])
            )

if __name__=='__main__':
    main()
print("#"*50)
print("MOPDT END")
print("#"*50)

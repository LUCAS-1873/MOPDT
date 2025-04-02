"""
Set arguments
"""
import argparse
import os
VERSION='0.0.1'
max_cpu_num=os.popen('cat /proc/cpuinfo |grep \'processor\'|wc -l').readlines()[0].strip()
parser = argparse.ArgumentParser(description='MOPDT: Methane-oxidation protein Detector',epilog=" Version: {}".format(VERSION))
parser.add_argument("-I",dest="fasta",help="The input sequence, require in fasta format, the default is protein sequecne; if input is nucleic acid sequence, add --nucl",required=True)
parser.add_argument("-O",dest="out_dir",help="Directory to write output files",required=True)
parser.add_argument("-j","--thread", type=int, help="Number of threads/processes" ,default=max_cpu_num)
parser.add_argument("-L","--level", type=str, help="Select the degree of Strictness; You can input loose|strict|default" ,default='default')
parser.add_argument("--nucl", action='store_true',  help="set this to tell MOPDT the input file is nucleic acid sequence, default is False, If this set , MOPDT will auto-gene call using prodigal.")
parser.add_argument("--intermediate", action='store_true', help="Whether remain the intermediate files, default is False.")
parser.add_argument("--genome", action='store_true',  help="Set this to tell MOPDT the input file is the genome of complete/draft bacteria ;set this only affect gene calling from prodigal ")
parser.add_argument("--no_check", action='store_true',  help="Set this to skip the check procedure, not recommend, only if you have run with other protein annotation steps with such as eggNOG/Prokka...; And use MOPDT to explore the potential MOP further.")
parser.add_argument("--version", action="version", version=VERSION)

args = parser.parse_args()

def IN():
    return args.fasta
def OUT():
    return args.out_dir
def thread():
    return args.thread
def LEVEL():
    return args.level
def NUCL():
    return args.nucl
def Intermediate():
    return args.intermediate
def GENOME():
    return args.genome
def NO_CHECK():
    return args.no_check

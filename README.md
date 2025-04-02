![](./Logo.jpg)

# Methane-Oxidation Protein/Gene DetecTor (MOPDT)
It includes MOPDT and MOPDT-Abun. *MOPDT* is a Pipeline for the Rapid Prediction of Methane-Oxidation Protein/Gene in Prokaryotic Genomes and Metagenomes.  And *MOPDT-Abun* is a supplementary tool of MOPDT to quickly estimate the Methane-Oxidation Gene abundance with input Fastq format.

## Installation
### Step 1. Install dependent softwares
We suggest using mamba instead of conda to speed up the installation.

Firstly, you need to install **ifeature**. MOPDT is dependent on it.
```
# With mamba, you will create an environment for MOPDT and activate it before being able to use it.
mamba create -n MOPDT python==3.7 -y
mamba activate MOPDT

# Next, you will install the iFeatureOmegaCLI(version) python enviroment.
mamba create -n MOPDT python==3.7.12 -y
mamba activate MOPDT
pip3 install iFeatureOmegaCLI==1.0.2
pip3 install biopython==1.81
pip3 install rdkit==2023.3.2
pip3 install xgboost==1.6.2

# Next, install dependent softwares 
mamba install diamond==2.0.2 -y -c bioconda
mamba install prodigal==2.6.3 -y -c bioconda
mamba install seqkit==2.3.0 -y -c bioconda
mamba install hmmer==3.3.1 -y -c bioconda
```

### Step 2. Download the database of MOPDT
You can download database through https://zenodo.org/records/## .

### Step 3. Download the main software of MOPDT
```
git clone https://github.com/LUCAS-1873/MOPDT/
```

## Usage

### MOPDT.py -The main software to predict Methane-Oxidation Protein/Gene in Prokaryotic Genomes and Metagenomes
### MOPDT-Abun.py -The tool can help to

#### Quickly start
```
## Input protein file and then output
MOPDT.py -I Input.faa -O Output
# "Input.faa" is the protein file that you want to know if these proteins are Methane-oxidation proteins.
# "Output" is the directory in which the results which stored
```
```
## Input nucleic acid file and then output
MOPDT.py --nucl -I Input.fa -O Output
# Add '--nucl' MOPDT will perform gene calling first.
# "Input.fa" is the nucleic acid sequencing file that you want to know if the genes coding by these nucleic acid sequence are Methane-oxidation Genes.
# "Output" is the directory in which the results which stored
```
```
# Also, you can use '-j' to make MOPDT use multi-threads to speed up
MOPDT.py --nucl -j 100 -I Input.fa -O Output 
```



```
MOPDT.py [-h] -I FASTA -O OUT_DIR [-j THREAD] [-L LEVEL] [--nucl]
                [--intermediate] [--genome] [--no_check] [--version]

MOPDT: Methane-oxidation protein Detector

optional arguments:
  -h, --help            show this help message and exit
  -I FASTA              The input sequence, required in fasta format, the
                        default is protein sequence; if the input is a nucleic acid
                        sequence, add --nucl
  -O OUT_DIR            Directory to write output files
  -j THREAD, --thread THREAD
                        Number of threads/processes
  -L LEVEL, --level LEVEL
                        Select the degree of Strictness; You can input
                        loose|strict|default
  --nucl                set this to tell MOPDT the input file is a nucleic acid
                        sequence, the default is False, If this is set, MOPDT will
                        auto-gene call using prodigal.
  --intermediate        Whether remain the intermediate files, the default is
                        False.
  --genome              Set this to tell MOPDT the input file is the genome of
                        complete/draft bacteria; set this only affect gene
                        calling from prodigal
  --no_check            Set this to skip the check procedure, not recommend,
                        only if you have run with other protein annotation
                        steps with such as eggNOG/Prokka...; And use MOPDT to
                        explore the potential MOP further.
  --version             show the program's version number and exit
```
-----------------
Depending on the tools used, you may want to cite also:  
DIAMOND: Buchfink B, Xie C, Huson D H. Fast and sensitive protein alignment using DIAMOND[J]. Nature methods, 2015, 12(1): 59-60.  
SEQKIT: Shen W, Le S, Li Y, et al. SeqKit: a cross-platform and ultrafast toolkit for FASTA/Q file manipulation[J]. PloS one, 2016, 11(10): e0163962.  

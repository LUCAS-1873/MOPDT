![](./Logo.jpg)

# Methane-Oxidation Protein/Gene DetecTor (MOPDT)
It includes MOPDT and MOPDT-Abun. *MOPDT* is a Pipeline for the Rapid Prediction of Methane-Oxidation Protein/Gene in Prokaryotic Genomes and Metagenomes.  And *MOPDT-Abun* is a supplementary tool of MOPDT to quickly estimate the Methane-Oxidation Gene abundance with input Fastq format.

## Installation
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

Downloading MAIN software and the database of MOPDT


geNomad depends on a database that contains the profiles of the markers that are used to classify sequences, their taxonomic information, their functional annotation, etc. So, you should first download the database to your current directory:
-----------------
Depending on the tools used, you may want to cite also:
DIAMOND: Buchfink B, Xie C, Huson D H. Fast and sensitive protein alignment using DIAMOND[J]. Nature methods, 2015, 12(1): 59-60.
SEQKIT: Shen W, Le S, Li Y, et al. SeqKit: a cross-platform and ultrafast toolkit for FASTA/Q file manipulation[J]. PloS one, 2016, 11(10): e0163962.

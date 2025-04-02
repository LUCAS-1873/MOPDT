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
```
Next, you will install the iFeatureOmegaCLI(version) python environment.
```
mamba create -n MOPDT python==3.7.12 -y
mamba activate MOPDT
pip3 install iFeatureOmegaCLI==1.0.2
pip3 install biopython==1.81
pip3 install rdkit==2023.3.2
pip3 install xgboost==1.6.2
```
Next, install dependent software 
```
mamba install diamond==2.0.2 -y -c bioconda
mamba install prodigal==2.6.3 -y -c bioconda
mamba install seqkit==2.3.0 -y -c bioconda
mamba install hmmer==3.3.1 -y -c bioconda
```

### Step 2. Download the database of MOPDT
You can download the database through https://zenodo.org/records/## .

### Step 3. Download the main software of MOPDT
```
git clone https://github.com/LUCAS-1873/MOPDT/
```

## Usage

##### MOPDT.py -The main software to predict Methane-Oxidation Protein/Gene in Prokaryotic Genomes and Metagenomes
##### MOPDT-Abun.sh -The script can help to rapidly estimate  Methane-Oxidation Gene Relative abundance from raw reads file

#### Quickly start
##### MOPDT
Input protein file and then output
`MOPDT.py -I Input.faa -O Output`
"Input.faa" is the protein file that you want to know if these proteins are Methane-oxidation proteins.
"Output" is the directory in which the results which stored

Input nucleic acid file and then output
`MOPDT.py --nucl -I Input.fa -O Output`
Add '--nucl' MOPDT will perform gene calling first.
"Input.fa" is the nucleic acid sequencing file that you want to know if the genes coding by these nucleic acid sequence are Methane-oxidation Genes.
"Output" is the directory in which the results which stored

Also, you can use '-j' to make MOPDT use multi-threads to speed up
`MOPDT.py --nucl -j 100 -I Input.fa -O Output`
##### MOPDT-Abun
Usage: MOPDT-Abun.sh output threads x1.fq/fa x2.fq/fa

Input with single-read Fastq/Fasta file with 100 threads to output_dir
Fastq:
`MOPDT-Abun.sh output_dir 100 single.fq`
Fasta:
`MOPDT-Abun.sh output_dir 100 single.fa`

MOPDT-Abun support pair reads input with 100 threads to output_dir
`MOPDT-Abun.sh output_dir 100 r1.fq r2.fq`
**Make sure the two files with the same header**

-----------------
Depending on the tools used, you may want to cite also:  
Diamond: Buchfink B, Xie C, Huson D H. Fast and sensitive protein alignment using DIAMOND[J]. Nature methods, 2015, 12(1): 59-60.  
Seqkit: Shen W, Le S, Li Y, et al. SeqKit: a cross-platform and ultrafast toolkit for FASTA/Q file manipulation[J]. PloS one, 2016, 11(10): e0163962.   
HMMER: Finn, R. D., Clements, J., & Eddy, S. R. (2011). HMMER web server: interactive sequence similarity searching. Nucleic acids research, 39(suppl_2), W29-W37.  
iFeatureOmega: Chen, Z., Liu, X., Zhao, P., Li, C., Wang, Y., Li, F., ... & Song, J. (2022). iFeatureOmega: an integrative platform for engineering, visualization and analysis of features from molecular sequences, structural and ligand data sets. Nucleic acids research, 50(W1), W434-W447.  
Prodigal: Hyatt, D., Chen, G. L., LoCascio, P. F., Land, M. L., Larimer, F. W., & Hauser, L. J. (2010). Prodigal: prokaryotic gene recognition and translation initiation site identification. BMC bioinformatics, 11, 1-11.  


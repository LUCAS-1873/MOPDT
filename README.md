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

mamba install diamond==2.0.2.140 -y -c bioconda
mamba install prodigal==2.6.3 -y -c bioconda
mamba install seqkit==2.3.0 -y -c bioconda
mamba install hmmer==3.3.1 -y -c bioconda
```
Secondly, you need to solve other dependent Python package

Pixi allows you to install geNomad as a globally available command for easy execution.

pixi global install -c conda-forge -c bioconda genomad



# Create an environment for **MOPDT**
mamba create -n genomad -c conda-forge -c bioconda genomad
# Activate the geNomad environment
mamba activate genomad


# Run the image
docker run --rm -ti -v "$(pwd):/app" antoniopcamargo/genomad

Downloading the database
geNomad depends on a database that contains the profiles of the markers that are used to classify sequences, their taxonomic information, their functional annotation, etc. So, you should first download the database to your current directory:

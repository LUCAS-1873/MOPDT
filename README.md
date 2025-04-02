![](./Logo.jpg)

# Methane-Oxidation Protein/Gene DetecTor (MOPDT)
**MOPDT** includes MOPDT and MOPDT-Abun.  
**MOPDT** is a Pipeline for the Rapid Prediction of Methane-Oxidation Protein/Gene in Prokaryotic genomes and Metagenomes.  
**MOPDT-Abun** is a supplementary tool of MOPDT to quickly estimate the Methane-Oxidation Gene abundance with input Fastq format.

## Installation

First, you need to install **MOPDT**. There's a couple of ways to do that (read more about it in the documentation), but two convinient options are using Pixi or Mamba. Both of them will handle the installation of all dependencies for you.

Pixi allows you to install geNomad as a globally available command for easy execution.

pixi global install -c conda-forge -c bioconda genomad

With Mamba, you will create an environment for geNomad and activate it before being able to use it.

# Create an environment for **MOPDT**
mamba create -n genomad -c conda-forge -c bioconda genomad
# Activate the geNomad environment
mamba activate genomad


# Run the image
docker run --rm -ti -v "$(pwd):/app" antoniopcamargo/genomad

Downloading the database
geNomad depends on a database that contains the profiles of the markers that are used to classify sequences, their taxonomic information, their functional annotation, etc. So, you should first download the database to your current directory:

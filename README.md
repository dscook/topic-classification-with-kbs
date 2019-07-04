# Text Topic Classification with Knowledge Bases

## Environment Setup

### Python

Python is used as the programming language and a *nix Operating System is expected, i.e. Linux or Mac.
To setup your Python environment:

1. `cd <this_directory>`
1. `python3 -m venv env`
1. `pip install -r requirements.txt`

### Knowledge Base Topic Hierarchies

The code expects a SPARQL over HTTP server to be running to access the knowledge base topic hierarchies for DBpedia
and MeSH.
Apache Jena Fuseki is used as the SPARQL over HTTP server.

1. Download Apache Jena Fuseki from https://jena.apache.org/download/ (version 3.11.0 was used in the experiments).
1. Untar: `tar -zxvf apache-jena-fuseki-3.11.0.tar.gz`
1. Start: `cd  apache-jena-fuseki-3.11.0/` followed by `./fuseki-server`.
1. Create two datasets for `DBpedia` and `MeSH` from the `manage datasets` tab at http://localhost:3030/.
   Select Persistent (TDB2) as the storage mechanism.

The RDF data for both DBpedia and MeSH must now be loaded into these Jena datasets.  From the `manage datasets` tab
at http://localhost:3030/:

1. For DBpedia upload the following datasets downloaded from https://wiki.dbpedia.org/downloads-2016-10 in `ttl`
   format: Anchor Texts, Article Categories and SKOS Categories.
   Note you will need to unbzip them `bzip2 -d <filename>`.
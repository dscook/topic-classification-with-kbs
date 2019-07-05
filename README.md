# Text Topic Classification with Knowledge Bases

## Environment Setup

### Python

Python is used as the programming language and a *nix Operating System is expected, i.e. Linux or Mac.
To setup your Python environment:

1. `cd <this_directory>`
1. `python3 -m venv env`
1. `source env/bin/activate`
1. `pip install -r requirements.txt`

Before any Python code is run on terminal restarts remember to re-activate the virtual environment:

1. `source env/bin/activate`

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
1. For MeSH upload the `mesh2019.nt` file downloaded from ftp://ftp.nlm.nih.gov/online/mesh/rdf/2019/.

### Root Topic Filtering

The RDF topic hierarchies must be pruned so the only topics accessible are those that relate to the classification
problem at hand.
This is done for both DBpedia and MeSH, however in the latter case everything is simply marked as accessible as MeSH
only contains medical topics and does not need filtering like the general purpose knowledge base of DBpedia.
For DBpedia:

1. Edit `kb-classifier/kb_common.py` so that `dataset = 'rcv1_wiki'`.
1. Run the topic hierarchy pruner: `cd kb-classifier` then `python prune.py`.

For MeSH:

1. Edit `kb-classifier/kb_common.py` so that `dataset = 'uvigomed_mesh'`.
1. Run the topic hierarchy pruner: `cd kb-classifier` then `python prune.py`.

### Phrase Cache Priming

The phrase cache needs primining with the phrases that exist in both the DBpedia and MeSH knowledge bases.
This enables DB lookups to occur only when it is known a resource exists for the phrase in the knowledge base thus
avoiding network and disk overhead to try and lookup a phrase that does not exist in the knowledge base.

For DBpedia:

1. Edit the `kb-classifier/phrase-generation-wiki/cleanup_anchors.py` file to contain the location where the Anchor
Texts, `anchor_text_en.ttl`, from DBpedia were downloaded to earlier.
1. Execute the cleanup anchors script, `cd kb-classifier/phrase-generation-wiki` followed by
`python cleanup_anchors.py`.
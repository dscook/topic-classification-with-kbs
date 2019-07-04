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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlDao:
    """
    Access layer for DBpedia SPARQL queries.
    """
    
    def __init__(self, sparql_query_url):
        """
        :param sparqlQueryUrl: The SPARQL query endpoint address.
        """
        self.sparql_query_url = sparql_query_url
        self.sparql = SPARQLWrapper("http://localhost:3030/DBpedia/query")
        self.sparql.setReturnFormat(JSON)
        
        # Namespaces for use in queries
        self.NS_DBPEDIA = 'http://dbpedia.org/resource/'
        self.NS_SKOS = 'http://www.w3.org/2004/02/skos/core#'
        self.PREFIX_SKOS = 'PREFIX skos: <{}>'.format(self.NS_SKOS)


    def get_child_topics(self, topic):
        """
        Given a topic name, gets its child topics.
        
        :param topic: the topic to find the children of.
        :returns: a list of the child topic names.
        """        
        self.sparql.setQuery(f"""
            {self.PREFIX_SKOS}
            SELECT ?subject
            WHERE {{ ?subject skos:broader <http://dbpedia.org/resource/Category:{topic}> }}
            """)
        results = self.sparql.query().convert()
        
        child_topics = []
        for result in results['results']['bindings']:
            # Strip the namespace from each topic
            child_topic = result['subject']['value'][len(self.NS_DBPEDIA + 'Category:'):]
            child_topics.append(child_topic)
            
        return child_topics
        
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlDao:
    """
    Access layer for DBpedia SPARQL queries.
    """
    
    def __init__(self, endpoint_url):
        """
        :param endpoint_url: The SPARQL endpoint address.
        """
        self.sparql_query = SPARQLWrapper(endpoint_url + 'query')
        self.sparql_query.setReturnFormat(JSON)
        self.sparql_update = SPARQLWrapper(endpoint_url + 'update')
        self.sparql_update.setReturnFormat(JSON)
        
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
        self.sparql_query.setQuery(f"""
            {self.PREFIX_SKOS}
            SELECT ?subject
            WHERE {{ ?subject skos:broader <http://dbpedia.org/resource/Category:{topic}> }}
            """)
        results = self.sparql_query.query().convert()
        
        child_topics = []
        for result in results['results']['bindings']:
            # Strip the namespace from each topic
            child_topic = result['subject']['value'][len(self.NS_DBPEDIA + 'Category:'):]
            child_topics.append(child_topic)
            
        return child_topics
    
    
    def mark_as_accessible(self, topic):
        """
        Given a topic, adds a triple to indicate it is accessible.
        
        :param topic: the topic to mark as accessible.
        """
        self.sparql_update.setQuery(f"""
            PREFIX dsc38: <http://www.bath.ac.uk/dsc38/ontology#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

            INSERT DATA 
            {{
	            <http://dbpedia.org/resource/Category:{topic}> dsc38:reachable "true"^^xsd:boolean
            }}
            """)
        result = self.sparql_update.query()
        if result.response.code != 200:
            raise Exception('Failed to mark topic as accessible')
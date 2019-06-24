#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlDao:
    """
    Access layer for MeSH SPARQL queries.
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
        self.NS_RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
        self.PREFIX_RDF = 'PREFIX rdf: <{}>'.format(self.NS_RDF)
        self.NS_MESHV = 'http://id.nlm.nih.gov/mesh/vocab#'
        self.PREFIX_MESHV = 'PREFIX meshv: <{}>'.format(self.NS_MESHV)
        self.NS_MESH = 'http://id.nlm.nih.gov/mesh/2019/'
        self.PREFIX_MESH = 'PREFIX mesh: <{}>'.format(self.NS_MESH)

    
    def get_parent_topics(self, topic):
        """
        Given a topic name, gets its parent topics.
        
        :param topic: the topic to find the parents of.
        :returns: a list of the parent topic names.
        """
        pass
    

    def get_child_topics(self, topic):
        """
        Given a topic name, gets its child topics.
        
        :param topic: the topic to find the children of.
        :returns: a list of the child topic names.
        """
        pass


    def mark_as_accessible(self, topic):
        """
        Given a topic, adds a triple to indicate it is accessible.
        
        :param topic: the topic to mark as accessible.
        """
        pass


    def get_resource_for_phrase(self, phrase):
        """
        Given a phrase, gets any corresponding resource that is accessible.
        
        :param phrase: the phrase to lookup.
        """
        self.sparql_query.setQuery(f"""
            {self.PREFIX_RDF}
            {self.PREFIX_MESHV}
            {self.PREFIX_MESH}
            
            SELECT ?descriptor
            WHERE {{
                ?term meshv:prefLabel "{phrase}"@en .
                ?concept ?predicate1 ?term .
                ?concept rdf:type meshv:Concept .
                ?descriptor ?predicate2 ?concept .
                ?descriptor rdf:type meshv:TopicalDescriptor
            }}
            """)
        results = self.sparql_query.query().convert()
        resources = self.extract_matches_from_results(results, 'descriptor', prefix_to_remove=self.NS_MESH)
        
        if len(resources) > 1:
            raise Exception('Coding Error: A phrase ({}) should not refer to more than one resource'.format(phrase))
        
        to_return = None
        if len(resources) == 1:
            to_return = resources[0]
        return to_return


    def get_topics_for_resource(self, resource):
        """
        Given a resource, get the list of immediate topics that are associated with that resource.
        
        :param resource: the resource to lookup.
        :returns: the list of topic names associated with the resource or an empty list if
                  the resource couldn't be matched to any topics.
        """
        pass
    

    def extract_matches_from_results(self, results, bound_variable, prefix_to_remove):
        """
        Given a SPARQL results set extract the bound variable.
        
        :param results: the SPARQL results set.
        :param bound_variable: the variable name that has been bound to.
        :param prefix_to_remove: any prefix to remove from the bound variable.
        :returns: a list of the matches found.
        """
        matches = []
        for result in results['results']['bindings']:
            # Strip the namespace from each topic
            match = result[bound_variable]['value'][len(prefix_to_remove):]
            matches.append(match)
        return matches
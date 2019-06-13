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
        self.PREFIX_DBPEDIA = 'PREFIX dbpedia: <{}>'.format(self.NS_DBPEDIA)
        self.NS_SKOS = 'http://www.w3.org/2004/02/skos/core#'
        self.PREFIX_SKOS = 'PREFIX skos: <{}>'.format(self.NS_SKOS)
        self.NS_DBPEDIA_OWL = 'http://dbpedia.org/ontology/'
        self.PREFIX_DBPEDIA_OWL = 'PREFIX dbpediaowl: <{}>'.format(self.NS_DBPEDIA_OWL)
        self.NS_DUBLIN_CORE = 'http://purl.org/dc/terms/'
        self.PREFIX_DUBLIN_CORE = 'PREFIX dct: <{}>'.format(self.NS_DUBLIN_CORE)
        self.NS_XSD = 'http://www.w3.org/2001/XMLSchema#'
        self.PREFIX_XSD = 'PREFIX xsd: <{}>'.format(self.NS_XSD)
        self.NS_DSC38 = 'http://www.bath.ac.uk/dsc38/ontology#'
        self.PREFIX_DSC38 = 'PREFIX dsc38: <{}>'.format(self.NS_DSC38)

    
    def get_parent_topics(self, topic):
        """
        Given a topic name, gets its parent topics.
        
        :param topic: the topic to find the parents of.
        :returns: a list of the parent topic names.
        """
        self.sparql_query.setQuery(f"""
            {self.PREFIX_SKOS}
            {self.PREFIX_DSC38}
            {self.PREFIX_XSD}
            
            SELECT ?object
            WHERE {{ 
                <http://dbpedia.org/resource/Category:{topic}> skos:broader ?object .
                ?object dsc38:reachable "true"^^xsd:boolean
            }}
            """)
        results = self.sparql_query.query().convert()
        parent_topics = self.extract_matches_from_results(results, 'object', prefix_to_remove=self.NS_DBPEDIA + 'Category:')
        
        return parent_topics


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
        child_topics = self.extract_matches_from_results(results, 'subject', prefix_to_remove=self.NS_DBPEDIA + 'Category:')
        
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

    
    def get_resource_for_phrase(self, phrase):
        """
        Given a phrase, gets any corresponding resource that is accessible.
        
        :param phrase: the phrase to lookup.
        """
        # Resources have spaces replaced with underscores and first letter always as a capital
        phrase_as_resource = '_'.join(phrase.split())
        if len(phrase_as_resource) > 1:
            phrase_as_resource = phrase_as_resource[0].upper() + phrase_as_resource[1:]
        
        self.sparql_query.setQuery(f"""
            {self.PREFIX_DUBLIN_CORE}
            {self.PREFIX_DSC38}
            {self.PREFIX_XSD}
            
            SELECT ?topic
            WHERE {{ 
                <http://dbpedia.org/resource/{phrase_as_resource}> dct:subject ?topic .
                ?topic dsc38:reachable "true"^^xsd:boolean
            }}
            """)
        results = self.sparql_query.query().convert()
        
        to_return = None
        if len(results['results']['bindings']) > 0:
            to_return = phrase_as_resource
        
        return to_return
        

    def get_resource_for_phrase_from_redirect(self, phrase):
        """
        Given a phrase, gets any corresponding resource (from a redirect) that is accessible.
        
        :param phrase: the phrase to lookup.
        """
        # Resources have spaces replaced with underscores and first letter always as a capital
        phrase_as_resource = '_'.join(phrase.split())
        if len(phrase_as_resource) > 1:
            phrase_as_resource = phrase_as_resource[0].upper() + phrase_as_resource[1:]
        
        self.sparql_query.setQuery(f"""
            {self.PREFIX_DBPEDIA_OWL}
            {self.PREFIX_DUBLIN_CORE}
            {self.PREFIX_DSC38}
            {self.PREFIX_XSD}
            
            SELECT DISTINCT ?resource
            WHERE {{ 
              <http://dbpedia.org/resource/{phrase_as_resource}> dbpediaowl:wikiPageRedirects ?resource .
              ?resource dct:subject ?topic .
              ?topic dsc38:reachable "true"^^xsd:boolean
            }}
            """)
        
        results = self.sparql_query.query().convert()
        resources = self.extract_matches_from_results(results, 'resource', prefix_to_remove=self.NS_DBPEDIA)
        
        if len(resources) > 1:
            raise Exception('Coding Error: A redirect should not refer to more than one resource')
        
        to_return = None
        if len(resources) == 1:
            to_return = resources[0]
        return to_return
    
    
    def get_resources_for_phrase_from_anchor(self, phrase):
        """
        Given a phrase, gets any corresponding resources (from hyperlink anchor text) that are accessible.
        
        :param phrase: the phrase to lookup.
        """
        self.sparql_query.setQuery(f"""
            {self.PREFIX_DBPEDIA_OWL}
            {self.PREFIX_DUBLIN_CORE}
            {self.PREFIX_DSC38}
            {self.PREFIX_XSD}
            
            SELECT DISTINCT ?resource
            WHERE {{ 
                ?resource dbpediaowl:wikiPageWikiLinkText "{phrase}"@en .
                ?resource dct:subject ?topic .
                ?topic dsc38:reachable "true"^^xsd:boolean
            }}
            """)
        results = self.sparql_query.query().convert()
        resources = self.extract_matches_from_results(results, 'resource', prefix_to_remove=self.NS_DBPEDIA)
        return resources

    def get_topics_for_phrase(self, phrase):
        """
        Given a phrase, get the list of topics that are associated with that phrase.
        
        :param phrase: the phrase to lookup.
        :returns: the list of topic names associated with the phrase or an empty list if
                  the phrase couldn't be matched to any topics.
        """
        self.sparql_query.setQuery(f"""
            {self.PREFIX_DBPEDIA_OWL}
            {self.PREFIX_DUBLIN_CORE}
            {self.PREFIX_DSC38}
            {self.PREFIX_XSD}
            
            SELECT ?topic
            WHERE {{ 
                ?subject dbpediaowl:wikiPageWikiLinkText "{phrase}"@en .
                ?subject dct:subject ?topic .
                ?topic dsc38:reachable "true"^^xsd:boolean
            }}
            """)
        results = self.sparql_query.query().convert()
        topics = self.extract_matches_from_results(results, 'topic', prefix_to_remove=self.NS_DBPEDIA + 'Category:')
            
        return topics
    
    
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
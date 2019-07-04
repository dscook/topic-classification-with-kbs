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
            {self.PREFIX_RDF}
            {self.PREFIX_MESHV}
            {self.PREFIX_MESH}
            {self.PREFIX_DSC38}
            {self.PREFIX_XSD}
            
            SELECT ?ancestorTreeNum
            WHERE {{
                    mesh:{topic} meshv:parentTreeNumber ?ancestorTreeNum .
                    ?ancestorTreeNum dsc38:reachable "true"^^xsd:boolean
            }}
            """)
        results = self.sparql_query.query().convert()
        parent_topics = self.extract_matches_from_results(results, 'ancestorTreeNum', prefix_to_remove=self.NS_MESH)
        
        return parent_topics


    def get_child_topics(self, topic):
        """
        Given a topic name, gets its child topics.
        
        :param topic: the topic to find the children of.
        :returns: a list of the child topic names.
        """
        self.sparql_query.setQuery(f"""
            {self.PREFIX_RDF}
            {self.PREFIX_MESHV}
            {self.PREFIX_MESH}
            
            SELECT ?childTreeNum
            WHERE {{
                    ?childTreeNum meshv:parentTreeNumber mesh:{topic}
            }}
            """)
        results = self.sparql_query.query().convert()
        child_topics = self.extract_matches_from_results(results, 'childTreeNum', prefix_to_remove=self.NS_MESH)
        
        return child_topics


    def mark_as_accessible(self, topic):
        """
        Given a topic, adds a triple to indicate it is accessible.
        
        :param topic: the topic to mark as accessible.
        """
        self.sparql_update.setQuery(f"""
            {self.PREFIX_MESH}
            {self.PREFIX_DSC38}
            {self.PREFIX_XSD}

            INSERT DATA 
            {{
	            mesh:{topic} dsc38:reachable "true"^^xsd:boolean
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
        self.sparql_query.setQuery(f"""
            {self.PREFIX_RDF}
            {self.PREFIX_MESHV}
            {self.PREFIX_MESH}
            {self.PREFIX_DSC38}
            {self.PREFIX_XSD}
            
            SELECT DISTINCT ?concept
            WHERE {{
                {{{{?term meshv:prefLabel "{phrase}"@en}} UNION {{?term meshv:altLabel "{phrase}"@en}}}} .
                ?concept ?predicate ?term
            }}
            """)
        results = self.sparql_query.query().convert()
        resources = self.extract_matches_from_results(results, 'concept', prefix_to_remove=self.NS_MESH)
                            
        if resources:
            
            # Filter resources that aren't actually concepts
            concepts = []
            
            for resource in resources:
                self.sparql_query.setQuery(f"""
                    {self.PREFIX_RDF}
                    {self.PREFIX_MESHV}
                    {self.PREFIX_MESH}
                    {self.PREFIX_DSC38}
                    {self.PREFIX_XSD}
                    
                    SELECT 1
                    WHERE {{
                        mesh:{resource} rdf:type meshv:Concept
                    }}
                    """)
                results = self.sparql_query.query().convert()
                extracted_concepts = self.extract_matches_from_results(results, '.0', prefix_to_remove=self.NS_MESH)
                if extracted_concepts:
                    concepts.append(resource)
        
            if len(concepts) > 1:
                raise Exception('Coding Error: A phrase ({}) should not refer to more than one concept'.format(phrase))
            
            # Get the resource (aka concept)
            concept = None
            if len(concepts) == 1:
                concept = concepts[0]
                
            if concept:
                # Ensure the concept is reachable
                self.sparql_query.setQuery(f"""
                    {self.PREFIX_RDF}
                    {self.PREFIX_MESHV}
                    {self.PREFIX_MESH}
                    {self.PREFIX_DSC38}
                    {self.PREFIX_XSD}
                    
                    SELECT DISTINCT ?descriptor
                    WHERE {{
                        ?descriptor ?predicate mesh:{concept} .
                        ?descriptor rdf:type meshv:TopicalDescriptor
                    }}
                    """)
                results = self.sparql_query.query().convert()
                descriptors = self.extract_matches_from_results(results, 'descriptor', prefix_to_remove=self.NS_MESH)
                
                for descriptor in descriptors:
                    self.sparql_query.setQuery(f"""
                        {self.PREFIX_RDF}
                        {self.PREFIX_MESHV}
                        {self.PREFIX_MESH}
                        {self.PREFIX_DSC38}
                        {self.PREFIX_XSD}
                        
                        SELECT DISTINCT ?topic
                        WHERE {{
                            mesh:{descriptor} meshv:treeNumber ?topic .
                            ?topic dsc38:reachable "true"^^xsd:boolean
                        }}
                        """)
                    results = self.sparql_query.query().convert()
                    topics = self.extract_matches_from_results(results, 'topic', prefix_to_remove=self.NS_MESH)
                    
                    # We can reach some topics, return the concept
                    if len(topics) >= 1:
                        return concept
            
        # Could not find a matching concept or it is not reachable
        return None


    def get_topics_for_resource(self, resource):
        """
        Given a resource, get the list of immediate topics that are associated with that resource.
        
        :param resource: the resource to lookup.
        :returns: the list of topic names associated with the resource or an empty list if
                  the resource couldn't be matched to any topics.
        """
        self.sparql_query.setQuery(f"""
            {self.PREFIX_RDF}
            {self.PREFIX_MESHV}
            {self.PREFIX_MESH}
            {self.PREFIX_DSC38}
            {self.PREFIX_XSD}
            
            SELECT DISTINCT ?descriptor
            WHERE {{
            	    ?descriptor ?predicate mesh:{resource} .
                ?descriptor rdf:type meshv:TopicalDescriptor
            }}
            """)
        results = self.sparql_query.query().convert()
        descriptors = self.extract_matches_from_results(results, 'descriptor', prefix_to_remove=self.NS_MESH)
        
        topics = []
        
        for descriptor in descriptors:
            self.sparql_query.setQuery(f"""
                {self.PREFIX_RDF}
                {self.PREFIX_MESHV}
                {self.PREFIX_MESH}
                {self.PREFIX_DSC38}
                {self.PREFIX_XSD}
                
                SELECT DISTINCT ?topic
                WHERE {{
                    mesh:{descriptor} meshv:treeNumber ?topic .
                    ?topic dsc38:reachable "true"^^xsd:boolean
                }}
                """)
            results = self.sparql_query.query().convert()
            extracted_topics = self.extract_matches_from_results(results, 'topic', prefix_to_remove=self.NS_MESH)
            topics.extend(extracted_topics)
        
        if not topics:
            raise Exception('Coding Error: no topics found for resource ({})'.format(resource))
            
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
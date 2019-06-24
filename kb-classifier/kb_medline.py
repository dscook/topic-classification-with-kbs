#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lookup_cache_mesh import LookupCache
from sparql_dao_mesh import SparqlDao

def lookup_cache_init():
    return LookupCache()

def dao_init():
    return SparqlDao(endpoint_url='http://localhost:3030/MeSH/')

topic_depth=8

wiki_topics_to_index = {
    'Bacterial Infections and Mycoses': 0,
    'Virus Diseases': 1,
    'Parasitic Diseases': 2,
    'Neoplasms': 3,
    'Musculoskeletal Diseases': 4,
    'Digestive System Diseases': 5,
    'Stomatognathic Diseases': 6,
    'Respiratory Tract Diseases': 7,
    'Otorhinolaryngologic Diseases': 8,
    'Nervous System Diseases': 9,
    'Eye Diseases': 10,
    'Male Urogenital Diseases': 11,
    'Female Urogenital Diseases and Pregnancy Complications': 12,
    'Cardiovascular Diseases': 13,
    'Hemic and Lymphatic Diseases': 14,
    'Congenital, Hereditary, and Neonatal Diseases and Abnormalities': 15,
    'Skin and Connective Tissue Diseases': 16,
    'Nutritional and Metabolic Diseases': 17,
    'Endocrine System Diseases': 18,
    'Immune System Diseases': 19,
    'Disorders of Environmental Origin': 20,
    'Animal Diseases': 21,
    'Pathological Conditions, Signs and Symptoms': 22,
    'Occupational Diseases': 23,
    'Chemically-Induced Disorders': 24,
    'Wounds and Injuries': 25
}

wiki_topics_to_actual_topics = {
    'Bacterial Infections and Mycoses': 0,
    'Virus Diseases': 1,
    'Parasitic Diseases': 2,
    'Neoplasms': 3,
    'Musculoskeletal Diseases': 4,
    'Digestive System Diseases': 5,
    'Stomatognathic Diseases': 6,
    'Respiratory Tract Diseases': 7,
    'Otorhinolaryngologic Diseases': 8,
    'Nervous System Diseases': 9,
    'Eye Diseases': 10,
    'Male Urogenital Diseases': 11,
    'Female Urogenital Diseases and Pregnancy Complications': 12,
    'Cardiovascular Diseases': 13,
    'Hemic and Lymphatic Diseases': 14,
    'Congenital, Hereditary, and Neonatal Diseases and Abnormalities': 15,
    'Skin and Connective Tissue Diseases': 16,
    'Nutritional and Metabolic Diseases': 17,
    'Endocrine System Diseases': 18,
    'Immune System Diseases': 19,
    'Disorders of Environmental Origin': 20,
    'Animal Diseases': 21,
    'Pathological Conditions, Signs and Symptoms': 22,
    'Occupational Diseases': 23,
    'Chemically-Induced Disorders': 24,
    'Wounds and Injuries': 25
}
#!/usr/bin/env python3
"""
Inserting a document in python
"""


def insert_school(mongo_collection, **kwargs):
    """Inserting a new document"""
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id

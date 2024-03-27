#!/usr/bin/env python3
"""
Script that updates all topics of a document based on name
"""


def update_topics(mongo_collection, name, topics):
    """Function that updates topics"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})

#!/usr/bin/env python3
"""
Returns list by matching with a topic
"""


def schools_by_topic(mongo_collection, topic):
    """Function that returns schools that match a certain topic"""
    return mongo_collection.find({"topics": topic})

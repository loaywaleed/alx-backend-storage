#!/usr/bin/env python3
"""
Module that contains a list all function
"""


def list_all(mongo_collection):
    """Function that lists all documents"""
    return list(mongo_collection.find())

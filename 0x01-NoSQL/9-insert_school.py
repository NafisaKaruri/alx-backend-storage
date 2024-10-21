#!/usr/bin/env python3
"""
Module to insert a new document into a MongoDB collection.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document in a collection based on keyword arguments.

    Args:
        mongo_collection: The pymongo collection object.
        **kwargs: Keyword arguments representing the document fields.

    Returns:
        The new document's _id.
    """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id

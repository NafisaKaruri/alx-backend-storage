#!/usr/bin/env python3
"""
Module to list all douments in MongoDB collection.
"""


def list_all(mongo_collection):
    """
    List all documents in a collection.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of documents in the collection, or an empty lis if no documentsl
    """
    return mongo_collection.find()

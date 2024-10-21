#!/usr/bin/env python3
"""
Module to find schools by a specific topic in a MongoDB collection.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Return a list of schools that have a specific topic.

    Args:
        mongo_collection: The pymongo collection object.
        topic (str): The topic to search for.

    Returns:
        A list of school documents that include the specified topic.
    """
    return mongo_collection.find({"topics": topic})

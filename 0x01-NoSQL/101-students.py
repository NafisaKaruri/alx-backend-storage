#!/usr/bin/env python3
"""
Module to retrieve top students sorted by average score.
"""


def top_students(mongo_collection):
    """
    Returns a list of students sorted by average score.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of students with their averageScore included.
    """
    return list(mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]))

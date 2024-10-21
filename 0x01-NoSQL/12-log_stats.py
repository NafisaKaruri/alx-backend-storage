#!/usr/bin/env python3
"""
Script to analyze Nginx logs stored in MongoDB.
"""
from pymongo import MongoClient


def log_stats():
    """
    Prints statistics of logs in the Nginx collection.
    """
    # Connect to MongoDB instance using MongoClient
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    # Count documnents
    total = logs_collection.count_documents({})

    # Count methods
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})

    # Count GET request to hte /status pth
    path = logs_collection.count_documents(
        {"method": "GET", "path": "/status"})

    # Print the results
    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")


if __name__ == "__main__":
    log_stats()

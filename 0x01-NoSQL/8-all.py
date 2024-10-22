#!/usr/bin/env python3
"""
Author: Gadoskey
File: 8-all.py
Description: A Python function that lists all documents in a collection
"""

def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.
    
    param: mongo_collection - A pymongo collection object.
    return: A list of all documents in the collection, or an empty list if no documents exist.
    """
    doc_list = list(mongo_collection.find())
    # Convert the cursor to a list

    if len(doc_list) == 0:
        # Returns an empty list if no documents in the collection
        return []

    return doc_list

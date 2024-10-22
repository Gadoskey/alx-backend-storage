#!/usr/bin/env python3
"""
Author: Gadoskey
File: 8-all.py
Description: A Python function that lists all documents in a collection
"""


def list_all(mongo_collection):
    # A function that lists all documents in a collection
    doc_list = mongo_collection.find()

    if doc_list.count() == 0:
        # Returns an empty list if no document in the collection
        return []

    return doc_list

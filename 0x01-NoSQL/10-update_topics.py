#!/usr/bin/env python3
""" Change school topics """


def update_topics(mongo_collection, name, topics):
    """ Change school topics based on the name """
    return mongo_collection.update_many(
        {"name": name}, {"$set": {"topics": topics}})

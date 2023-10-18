#!/usr/bin/env python3
""" Log stats """

from pymongo import MongoClient


def print_nginx_req_logs(nginx_collection):
    """ Prints nginx request logs stats with top 10 IPs """
    print("{} logs".format(nginx_collection.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        req_count = len(list(nginx_collection.find({"method": method})))
        print("\tmethod {}: {}".format(method, req_count))
    status_checks_count = len(list(
        nginx_collection.find({"method": "GET", "path": "/status"})))
    print("{} status check".format(status_checks_count))


def print_top_10_ips(server_collection):
    """ Prints top 10 IPs with most requests """
    print("IPs:")
    req_logs = server_collection.aggregate([
        {
            "$group": {"_id": "$ip", "count": {"$sum": 1}}
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": 10
        },
        ])
    for req in req_logs:
        ip = req["_id"]
        ip_reqs = req["count"]
        print("\t{}: {}".format(ip, ip_reqs))


def run():
    """ Runs print_nginx_req_logs """
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_req_logs(client.logs.nginx)
    print_top_10_ips(client.logs.nginx)


if __name__ == "__main__":
    run()

#!/usr/bin/env python

'''
Dynamic inventory script for Ansible, in Python
'''
import argparse
import mysql.connector
from mysql.connector import Error
import json


class Inventory(object):
    """ creates the dynamic inventory """
    server = ""
    user = ""
    pwd = ""
    db = ""
    target = ""

    def __init__(self):
        self.inventory = {}
        self.target = self.read_cli_args()
        self.conn = None

    def example_inventory(self):
        return {
            'group': {
                'hosts': ['192.168.28.71', '192.168.28.72'],
            },
        }

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    def getInventory(self):
        """ collect the inventory for hosts in self.target """
        # here we call our MySQL Inventory
        self.getInventoryMySQL()
        # print(json.dumps(self.inventory))

    def connect(self, my_server, my_user, my_pwd, my_db):
        """ connect to MySQL Server """
        print("Connecting to: %s@%s" % (my_user, my_server))
        print("DB: %s" % my_db)

        config = {
            'user': my_user,
            'password': my_pwd,
            'host': "%s" % my_server,
            'database': my_db
        }

        try:
            self.conn = mysql.connector.connect(**config)
        except Error as e:
            print("Access denied for user '%s'@'%s'" % (my_user, my_server))
            print(e)

    def query(self, sql):
        if self.conn is None:
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()

            print('Total Row(s):', cursor.rowcount)
            for row in rows:
                print(row)
        except Error as e:
            print(e)

        finally:
            cursor.close()

    def close(self):
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()

    def getInventoryMySQL(self):
        self.server = "192.168.1.100"
        self.user = "admintools"
        self.pwd = "XYZ123"
        self.db = "admintools"
        self.target = "all"

        self.connect(self.server, self.user, self.pwd, self.db)
        self.query("SELECT * FROM mac")
        self.close()

    def read_cli_args(self):
        """ Read the command line args passed to the script """
        # see https://www.golinuxcloud.com/python-argparse/
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--user',
                            default='ansible',
                            dest='user',
                            help='MySQL Username',
                            type=str,
                            required=True
                            )
        parser.add_argument('-p', '--password',
                            dest='pwd',
                            help='MySQL Password',
                            type=str,
                            required=True
                            )
        parser.add_argument('-s', '--server',
                            dest='server',
                            help='MySQL Server',
                            type=str,
                            required=True
                            )
        parser.add_argument('-d', '--databse',
                            dest='db',
                            help='MySQL Database',
                            type=str,
                            required=True
                            )

        parser.add_argument('-g', '--group',
                            default='all',
                            dest='group',
                            help='The group of hosts',
                            type=str
                            )

        args = parser.parse_args()

        self.server = args.server
        self.user = args.user
        self.pwd = args.pwd
        self.db = args.db
        return args.group


def main():
    inventory = Inventory()
    inventory.getInventory()


if __name__ == "__main__":
    main()

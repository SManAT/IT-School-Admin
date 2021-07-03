#!/usr/bin/env python

'''
Dynamic inventory script for Ansible, in Python
'''
import argparse
import json


class Inventory(object):
    """ creates the dynamic inventory """

    def __init__(self):
        self.inventory = {}
        self.target = self.read_cli_args()

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

    def getInventoryMySQL(self):
        pass

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

        parser.add_argument('-g', '--group',
                            default='all',
                            dest='group',
                            help='The group of hosts',
                            type=str
                            )

        args = parser.parse_args()
        print(f'Username is "{args.user}"')
        print(f'Password is "{args.pwd}"')
        print(f'Group is "{args.group}"')


def main():
    inventory = Inventory()
    inventory.getInventory()


if __name__ == "__main__":
    main()

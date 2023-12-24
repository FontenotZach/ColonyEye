########################################################################################################################
#
#   File: CageNetwork.py
#   Purpose: The entire ColonyRack system fits in this object
#
########################################################################################################################

import yaml
from yaml import CLoader as Loader
import os

yaml_path = os.path.join(os.getcwd(), os.pardir, 'config.yaml')

with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)


class CageNetwork:
    def __init__(self, nodes):
        self.nodes = nodes
        self.colony_id = data.get('colony')[0].get('name')

    def add_node(self, node):
        self.nodes.append(node)

    def to_string(self):
        output = ''
        output += '\n\nColonyRack Info:'
        for node in self.nodes:
            output += '\n\n\tNode ' + str(node.node_id)
            for connection in node.connections:
                output += '\n\t\tConnection ' + str(connection.connection_id) + ': '
                output += str(connection.cage_node_1.node_id) + ' to ' + str(connection.cage_node_2.node_id)

        output += '\n\n'
        return output

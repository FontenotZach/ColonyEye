########################################################################################################################
#
#   File: CageConnection.py
#   Purpose: Connections between cages in ColonyRack
#
########################################################################################################################

class CageConnection:

    def __init__(self, cage_node_1, cage_node_2, connection_id):
        self.cage_node_1 = cage_node_1
        self.cage_node_2 = cage_node_2
        self.connection_id = connection_id

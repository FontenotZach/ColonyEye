class CageNode:

    def __init__(self, node_id, connections):
        self.node_id = node_id
        self.connections = connections
        self.quality = None
        self.traffic = []

    def add_connection(self, cage_node):
        self.connections.append(cage_node)

    def contains_connection(self, rfid_id):

        contains = False

        for connection in self.connections:
            if connection.connection_id == rfid_id:
                contains = True

        return  contains

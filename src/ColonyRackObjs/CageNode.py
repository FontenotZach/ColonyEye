class CageNode:

    def __init__(self, node_id, connections):
        self.node_id = node_id
        self.connections = connections
        self.quality = None
        self.traffic = []

    def add_connection(self, cage_node):
        self.connections.append(cage_node)


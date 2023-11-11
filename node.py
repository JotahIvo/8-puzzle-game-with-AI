
class Node:
    def __init__(self, state, parent_node, g, h):
        self.state = state
        self.parent_node = parent_node
        self.g = g
        self.h = h

    def __eq__(self, node):
        return self.state == node.state

    def __repr__(self):
        return str(self.state)

    def get_state(self):
        return self.state
# imports
from treelib import Node, Tree
import math


def createtree(mydataframe):
    tree = Tree()
    for index, row in mydataframe.iterrows():
        if row['parent_id'] is None:
            return None

        if math.isnan(row["parent_id"]) or row["parent_id"] == 'nan':
            tree.create_node(data=row, identifier=row['id'])

        else:
            tree.create_node(data=row, identifier=row['id'], parent=int(row["parent_id"]))

    # print_tree(tree)
    return tree


def print_tree(tree, level=0):
    node = tree.get_node(tree.root)
    print()
    print("\t" * level + str(node.identifier) + " " + str(node.data['operation']) + " " + str(node.data['object_name'])
          + " " + str(node.data['access_predicates']) + " " + str(node.data['projection']))
    for c in tree.children(tree.root):
        print_tree(tree.subtree(c.identifier), level + 1)

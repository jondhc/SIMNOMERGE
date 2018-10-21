import os
import lxml.etree as ET

paths = []

def open_docs(directory):
    trees = []
    for docName in os.listdir(directory):
        if docName.endswith(".xml"):
            path = directory + "win_tale.xml"
            tree = parse(path)
            trees.append(tree)
    return trees

def parse(path):
    return ET.parse(path)

def get_contexts(tree):
    for element in tree.iter():
        if not element:
            paths.append(tree.getpath(element))


if __name__ == '__main__':
    trees = open_docs("./Collection/")
    for tree in trees:
        get_contexts(tree)
    print(paths)


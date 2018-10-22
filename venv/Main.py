import os
import lxml.etree as ET
import nltk
from nltk.tokenize import word_tokenize

paths = []
trees = []
number_of_elements = 0

def open_docs(directory):
    for docName in os.listdir(directory):
        if docName.endswith(".xml"):
            path = directory + docName
            tree = parse(path)
            trees.append(tree)

def parse(path):
    return ET.parse(path)

def get_leaves_contexts(tree):
    for element in tree.iter():
        if not element:
            paths.append(tree.getpath(element))
            tokenize_leave(element.text)

def get_all_leaves_contexts():
    for tree in trees:
        get_leaves_contexts(tree)

def tokenize_leave(leave_content):
    text = str(leave_content)
    tokens_list = word_tokenize(text)


if __name__ == '__main__':
    open_docs("./Collection/")
    get_all_leaves_contexts()



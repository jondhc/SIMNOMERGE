import os
import lxml.etree as et
import nltk
from nltk.tokenize import word_tokenize

paths = []
trees = []
ctdf_dictionary = {}


def open_docs(directory):
    for docName in os.listdir(directory):
        if docName.endswith(".xml"):
            path = directory + docName
            tree = parse(path)
            trees.append(tree)


def parse(path):
    return et.parse(path)


def get_leaves_contexts(tree):
    doc_name = "test"  # TEMPORARY VAR FOR DOC NAME
    for element in tree.iter():
        if not element:
            paths.append(tree.getpath(element))
            terms = tokenize_leave(element.text)
            for term in terms:
                if len(term) > 0 and term != "." and term != ",":
                    store_in_ctdf_dictionary(tree.getpath(element), term, doc_name)


def get_all_leaves_contexts():
    for tree in trees:
        get_leaves_contexts(tree)


def tokenize_leave(leave_content):
    text = str(leave_content)
    tokens_list = word_tokenize(text)
    return tokens_list


def store_in_ctdf_dictionary(context, term, document):
    context = context + "/" + term
    ctdf_dictionary.setdefault(context, []).append(document)


if __name__ == '__main__':
    open_docs("./Collection/")
    get_all_leaves_contexts()
    print(ctdf_dictionary)

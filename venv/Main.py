import os
import pprint
import lxml.etree as et
import nltk
import collections
from nltk.tokenize import word_tokenize

trees = {}
ctd_dictionary = {}
ctdf_dictionary = {}

def showDictionary(dictionary):
    pp = pprint.PrettyPrinter(indent = 2)
    pp.pprint(list(dictionary.items()))


def open_docs(directory):
    for doc_name in os.listdir(directory):
        if doc_name.endswith(".xml"):
            path = directory + doc_name
            tree = parse(path)
            trees[doc_name] = tree


def parse(path):
    return et.parse(path)


def get_leaves_contexts(tree, doc_name):
    for element in tree.iter():
        if not element:
            path = tree.getpath(element)
            terms = tokenize_leave(element.text)
            for term in terms:
                if len(term) > 0 and term != "." and term != ",":
                    store_in_ctd_dictionary(path, term, doc_name)


def get_all_leaves_contexts():
    for (doc_name, tree) in trees.items():
        get_leaves_contexts(tree, doc_name)


def tokenize_leave(leave_content):
    text = str(leave_content)
    tokens_list = word_tokenize(text)
    return tokens_list


def store_in_ctd_dictionary(context, term, document):
    context = context + "/" + term
    ctd_dictionary.setdefault(context, []).append(document)

def create_ctdf_dictionary():
    for (context_and_term, documents) in ctd_dictionary.items():
        documents_frequency = collections.Counter(documents)
        ctdf_dictionary.setdefault(context_and_term, documents_frequency)


if __name__ == '__main__':
    open_docs("./Collection/")
    get_all_leaves_contexts()
    create_ctdf_dictionary()
    showDictionary(ctdf_dictionary)
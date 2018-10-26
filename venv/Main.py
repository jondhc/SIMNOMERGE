import os
import pprint
import lxml.etree as et
import nltk
import collections
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

trees = {}
ctd_dictionary = {}
ctdf_dictionary = {}
weights_dictionary = {}
normalizer = {}

def show_dictionary(dictionary):
    pp = pprint.PrettyPrinter(indent=2)
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
            #terms = word_tokenize(str(element.text))
            for term in terms:
                if len(term) > 0 and term != "." and term != ",":
                    store_in_ctd_dictionary(path, term, doc_name)


def get_all_leaves_contexts():
    for (doc_name, tree) in trees.items(): #Iterar sobre una lista de duplas (doc_name, tree)
        get_leaves_contexts(tree, doc_name)


def tokenize_leave(leave_content):
    text = str(leave_content)
    stopwords_list = stopwords.words('english')
    stopwords_list.append(",")
    stopwords_list.append(".")
    stopwords_set = set(stopwords_list)
    tokens_list = word_tokenize(text)
    tokens_list_without_stopwords = []
    for token in tokens_list:
        if token not in stopwords_set:
            tokens_list_without_stopwords.append(token)
    return tokens_list_without_stopwords


def store_in_ctd_dictionary(context, term, document):
    context = context + "/" + term
    ctd_dictionary.setdefault(context, []).append(document)


def create_ctdf_dictionary():
    for (context_and_term, documents) in ctd_dictionary.items():
        documents_frequency = collections.Counter(documents)
        ctdf_dictionary.setdefault(context_and_term, documents_frequency)


def create_weights_dictionary():
    for (context_and_term, documents_and_frequency) in ctdf_dictionary.items():
        weight = math.log10((len(trees)) / len(documents_and_frequency))
        weights_dictionary[context_and_term] = weight

def create_ctdw_dictionary():
    for (context_and_term, documents_and_frequency) in ctdf_dictionary.items():
        for document_and_frequency in documents_and_frequency:
            ctdf_dictionary[context_and_term][document_and_frequency] = ctdf_dictionary[context_and_term][document_and_frequency] * weights_dictionary[context_and_term]

def normalizar():
    for key in trees:
        normalizer[key] = 0

    for (context_and_term, document_and_weight) in ctdf_dictionary.items():
        for (document, weight) in document_and_weight.items():
            normalizer[document] += math.pow(weight, 2)

    for doc in normalizer:
        normalizer[doc] = math.sqrt(normalizer[doc])


def context_resemble(cquery,cdocument):
    cquery = cquery.split('/')
    cdocument = cdocument.split('/')
    if len(cquery) > len (cdocument):
        result = 0
    elif len(cquery) == len(cdocument):
        if cquery == cdocument:
            result = 1
        else:
            result = 0
    else:
        notFound= False
        subCdoc = cdocument
        for i in range(len(cquery)):
            for j in range(len(subCdoc)):
                if(subCdoc[j]==cquery[i]):
                    subCdoc = subCdoc[j:len(subCdoc)]
                    break
                elif j == len(subCdoc)-1:
                    result = 0
                    notFound = True
                    break
            if notFound:
                break
        if not notFound:
            result = (1 + len(cquery))/(1 + len(cdocument))
    return result



def sinNoMerge(query):
    score = {}
    for key in trees:
        score[key] = 0
    text=""
    queries=[]
    query = query.split('/')
    contenido = tokenize_leave(query.pop())
    #contenido = word_tokenize(str(query.pop()))
    #weight = 0
    for element in query:
        text = text + "/" + element
    for word in contenido:
        queries.append(text +"/"+word)
    for i in queries:
        weight = weights_dictionary[i]
        for context,x in weights_dictionary.items():
            if context_resemble(i,context) > 0:
                postings = ctdf_dictionary[context]
                for posting in postings: ####
                    x = context_resemble(i,context)*weight*ctdf_dictionary[context][posting]
                    #score[posting.keys()[0]] += x
                    score[posting] += x
    for key in score:
        score[key] = score[key]/normalizer[key]
    return score



if __name__ == '__main__':
    query1 = 'PLAY/ACT[1]/SCENE[1]/SPEECH[22]/LINE[8]/speech'
    query2 = 'PLAY/ACT[4]/SCENE[1]/STAGEDIR[2]/Exeunt'
    query3 = 'PLAY/ACT[4]/SCENE[5]/SPEECH[11]/LINE[6]/honest'
    query4 = 'PLAY/ACT[1]/SCENE[1]/SPEECH[2]/LINE/Nay, answer me: stand, and unfold yourself.'
    #query5 = 'PLAY/FM/P[1]/ASCII text placed in the public domain by Moby Lexical Tools, 1992.'
    open_docs("./Collection/")
    get_all_leaves_contexts()
    create_ctdf_dictionary()
    create_weights_dictionary()
    create_ctdw_dictionary()
    normalizar()
    show_dictionary(sinNoMerge(query3))
    #show_dictionary(ctdf_dictionary)
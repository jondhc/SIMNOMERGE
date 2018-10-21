import os
import xml.etree.ElementTree as ET

paths = []

def openDocs(directory):
    for docName in os.listdir(directory):
        if docName.endswith(".xml"):
            tags = []
            path = directory + "win_tale.xml"
            tree = parse(path)
            for element in tree.iter():
                tags.append(element.tag)
                if not element:
                    tags.append(element.text)
                    paths.append(tags)
                    tags = []
    print(paths)

def parse(path):
    return ET.parse(path)

def getContexts(node):
    return null


openDocs("./Collection/")
import xml.dom.minidom
import re
import requests
import json
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch

def insertEnter1(matched):
    subStr = matched.group()
    return subStr[:2] + '\n' + subStr[-1]

def insertEnter2(matched):
    subStr = matched.group()
    return subStr[:2] + '\n' + subStr[-2:]

def removeEnter(matched):
    subStr = matched.group()
    return subStr[:2] + subStr[-1]

def abstractHandler(abstract_sec):
    simple_para = abstract_sec.getElementsByTagName('ce:simple-para')[0]
    paratext = ""
    for childNode in simple_para.childNodes:
        if childNode.nodeName == '#text':
            subStr = childNode.data
            removedEnter = re.sub('\n', '', subStr)
            removedSpace = re.sub('\s\s+', '', removedEnter)
            processed = re.sub('\.\s[A-Z]', insertEnter1, removedSpace)
            processed = re.sub('\.\s[0-9][a-zA-Z]', insertEnter2, processed)
            if processed[-2:] == '. ':
                processed += '\n'
            paratext += processed
        elif childNode.nodeName == 'ce:inf':
            paratext += childNode.firstChild.data.strip()
    paratext = re.sub('\.\s\n[\[\(]', removedEnter, paratext)
    sentCut = paratext.split('\n')
    temp = []
    for sent in sentCut:
        if len(sent.strip()) > 5:
            temp.append(sent)
    paratext = '\n'.join(temp)
    if paratext != "":
        paratext += '\n'
    return paratext

def paraHandler(para):
    paratext = ""
    for childNode in para.childNodes:
        if childNode.nodeName == "#text":
            subStr = childNode.data
            removedEnter = re.sub('\n', '', subStr)
            removedSpace = re.sub('\s\s+', '', removedEnter)
            processed = re.sub('\.\s[A-Z]', insertEnter1, removedSpace)
            processed = re.sub('\.\s[0-9][a-zA-Z]', insertEnter2, processed)
            if processed[-2:] == '. ':
                processed += '\n'
            paratext += processed
        elif childNode.nodeName == 'ce:cross-ref':
            paratext += childNode.firstChild.data.strip()
        elif childNode.nodeName == 'ce:list':
            paratext += '\n'
            listParas = childNode.getElementsByTagName('ce:para')
            for listpara in listParas:
                paratext += paraHandler(listpara)
    paratext = re.sub('\.\s\n[\[\(]', removedEnter, paratext)
    sentCut = paratext.split('\n')
    temp = []
    for sent in sentCut:
        if len(sent.strip()) > 5:
            temp.append(sent)
    paratext = '\n'.join(temp)
    if paratext != "":
        paratext += '\n'
    return paratext

def sectionHandler(section, output):
    for node in section.childNodes:
        if node.nodeName == "ce:section-title":
            title = node.firstChild.data
            output.write(title + '\n')
        elif node.nodeName == "ce:para":
            output.write(paraHandler(node))
        elif node.nodeName == "ce:section":
            sectionHandler(node, output)

con_file = open("config.json")
config = json.load(con_file)
con_file.close()

client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']
doc_srch = ElsSearch("6G",'sciencedirect')
print(">>> Fetching search results ...")
doc_srch.execute(client, get_all = False)
total_paper_num = doc_srch.num_res
print(f">>> Find {total_paper_num} papers ...")

for i, paper in enumerate(doc_srch.results):
    print("-------------------------------------------------------------\n")
    doi = paper['dc:identifier'][4:]
    url = 'https://api.elsevier.com/content/article/doi/' + doi + '?APIKey=' + config['apikey']
    
    requestTimes = 0
    getResult = False
    while (requestTimes < 5):
        try:
            print(f">>> Fetching paper {i + 1}/{total_paper_num} ...")
            response = requests.get(url)
            getResult = True
            break
        except:
            print(f">>> Fetching Failed ...")
            requestTimes += 1
    if not getResult:
        print()
        continue

    dom = xml.dom.minidom.parseString(response.content)
    root = dom.documentElement
    sections = root.getElementsByTagName("ce:sections")
    if len(sections) != 0:
        txtFile = open(f'./results/paper{i + 1}.txt', 'a', encoding='utf-8')
        try:
            title = root.getElementsByTagName("ce:title")[0].firstChild.data
            print(title)
            txtFile.write(title + '\n')
        except:
            pass

        try:
            txtFile.write(abstractHandler(root.getElementsByTagName("ce:abstract-sec")[0]))
        except:
            pass

        try:
            for section in sections[0].childNodes:
                sectionHandler(section, txtFile)
        except:
            pass
    txtFile.close()
    print()

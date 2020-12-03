from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import json

def get_info(data, file):
    f = open(file, encoding="utf8")
    info = f.read()
    f.close()
    bot_info = json.loads(info)
    return bot_info[data]

SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
DOCUMENT_ID = get_info("Docs_ID", "BotInfo.json")




def get_credentials():
    store = file.Storage('DocGet/token.json')
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('DocGet/credentials.json', SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials

def read_paragraph_element(element):
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_strucutural_elements(elements):
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text


def main():
    credentials = get_credentials()
    http = credentials.authorize(Http())
    docs_service = discovery.build(
        'docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    doc = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
    doc_content = doc.get('body').get('content')
    return read_strucutural_elements(doc_content)


def run():
    def ContentSetup(content, divider, divider2):
        VARIABLES = content.split(divider)[0].strip("\n")
        INFO = content.split(divider)[1].strip("\n")
        INFO = INFO.split(divider2)[0]
        INFO2 = content.split(divider2)[1].strip("\n")
        return VARIABLES, INFO, INFO2
    lineWords = []
    content = main()
    for x in content.splitlines():
        if x.startswith("#"):
            pass
        else:
            lineWords = lineWords + [x + "\n"]

    divider = "/=/=/=/=/=/"
    divider2 = "/-/-/-/-/-/"
    content = ""
    content = content.join(lineWords)
    SetupVars, Rules, Info = ContentSetup(content, divider, divider2)
    msgPrefix = SetupVars.split("Prefix = ")[1].split("\n")[0]
    msgSuffix = SetupVars.split("Suffix = ")[1].split("\n")[0]
    return msgPrefix, msgSuffix, Rules, Info

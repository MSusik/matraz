import sys
import requests
import re

from contact import get_readme

def detect_url(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def search_readme(readme, regex):
    DOCS_REGEX = re.compile(regex)
    docs = DOCS_REGEX.search(readme)
    return (docs != None) and (docs.end() != 0)

def has_docs(owner, repo):
    prefix = 'https://github.com/' + owner + '/' + repo + '/tree/master/'
    suffixes = [ 'doc', 'docs', 'Doc', 'Docs', 'documentation',
            'documentations', 'Documentation', 'Documentations' 'DOC', 'DOCS',
            'DOCUMENTATION', 'DOCUMENTATIONS' ]

    for suffix in suffixes:
        if detect_url(prefix + suffix):
            return True

    readme = get_readme(owner, repo)
    regexes = [ 'doc', 'docs', 'Doc', 'Docs', 'documentation',
            'documentations', 'Documentation', 'Documentations' 'DOC', 'DOCS',
            'DOCUMENTATION', 'DOCUMENTATIONS' ]
    for regex in regexes:
        if search_readme(readme, '### ' + regex + '\s'):
            return True

    return False

# tests
def run_tests():
    assert True == has_docs("mathemage", "Matrixpp"), "mathemage/Matrixpp"              # docs/
    assert True == has_docs("MSusik", "beard"), "MSusik/beard"                          # doc/
    assert True == has_docs("RocketChat", "Rocket.Chat"), "RocketChat/Rocket.Chat"      # "Documentation" in README.md
    assert False == has_docs("dzenbot", "dznemptydataset"), "dzenbot/dznemptydataset"   # documention undetected yet available
    assert False == has_docs("MSusik", "matraz"), "MSusik/matraz"                       # nothing

if __name__ == "__main__":
    run_tests()

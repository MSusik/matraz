import sys
import requests
import re


def has_docs(owner, repo, readme):
    prefix = 'https://github.com/' + owner + '/' + repo + '/tree/master/'

    directories = re.compile('\W[Dd][Oo][Cc](([Ss])|([Uu][Mm][Ee][Nn][Tt][Aa][Tt][Ii][Oo][Nn]))?\W')

    for suffix in affixes:
        if detect_url(prefix + suffix):
            return True

    for regex in affixes:
        if search_readme(readme, '### ' + regex + '\s'):
            return True

    return False

import sys
import requests
import re

from utils import get_readme


def has_docs(owner, repo, readme):
    url = 'https://api.github.com/repos/' + owner + '/' + repo + \
        '/git/trees/master'

    try:
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
        directories = re.compile('^[Dd][Oo][Cc](([Ss])|([Uu][Mm][Ee][Nn][Tt][Aa][Tt][Ii][Oo][Nn]))?$')
        for path in response['tree']:
            if "path" in path and directories.match(path["path"]):
                return True
    except requests.exceptions.RequestException:
        pass

    readme_re = re.compile('(# )?[Dd][Oo][Cc](([Ss])|([Uu][Mm][Ee][Nn][Tt][Aa][Tt][Ii][Oo][Nn]))?(\n[=-~])?')
    match = readme_re.search(readme)
    if match:
        if match.groups()[0] or match.groups()[4]:
            return True

    return False

import base64
import requests


def get_readme(owner, repo):
    repo_name = owner + '/' + repo
    url = 'https://api.github.com/repos/' + repo_name + '/readme'

    r = requests.get(url)
    try:
        r.raise_for_status()
        j = r.json()
    except requests.exceptions.RequestException:
        return ""

    return base64.decodestring(j[u'content'])


def get_repo_info(owner, repo):
    url = 'https://api.github.com/repos/' + owner + '/' + repo

    r = requests.get(url, headers={'Accept':
                                   'application/vnd.github.drax-preview+json'})
    try:
        r.raise_for_status()
        j = r.json()
    except requests.exceptions.RequestException:
        return {}

    return j

import base64
import json
import requests
import sys


def get_contact_for_user(owner):
    url = 'https://api.github.com/users/' + owner

    r = requests.get(url)
    try:
        r.raise_for_status()
        j = r.json()
    except requests.exceptions.RequestException:
        return ""

    return j['email']


def get_contact_for_org(owner, repo, repo_info, readme):

    if repo_info:
        if repo_info['has_issues']:
            contact = 'https://github.com/' + owner + '/' + repo + '/issues'
            return contact
        else:
            import re

            EMAIL_REGEX = re.compile('[^@\s]+@[^@\s]+\.[^@\s]+')
            first_email = EMAIL_REGEX.search(readme)

            if first_email:
                return first_email.string[first_email.start():
                                          first_email.end()]
            else:
                return ""
    return ""


def get_contact(owner, repo, repo_info, readme):
    user_contact = get_contact_for_user(owner)
    if user_contact:
        return user_contact
    return get_contact_for_org(owner, repo, repo_info, readme)

import requests


def get_doi(repo_url):
    '''Fetch doi from Zenodo, if available.

    Parameters
    ----------
    :param repo_url: string
        Url in from of 'https://github.com/[owner]/[repo]' . Don't add 'www'
        in front of 'github.com'.

    :param access_token: string
        Token from zenodo

    Returns
    -------
    :return: tuple
        (doi, link to doi service)
    '''
    zenodo_url = "https://zenodo.org/search"
    params = {
        "of": "recjson",
        "p": repo_url
    }
    response = requests.get(zenodo_url, params=params)

    try:
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return '', ''

    content = response.json()

    if content:
        return content[0]["doi"], "http://dx.doi.org/" + content[0]["doi"]

    return '', ''

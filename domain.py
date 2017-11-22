from urllib.parse import urlparse

def get_sub_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return 'It didn`t work'

def get_domain_name(url):
    try:
        results = get_sub_domain(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return 'It didn`t work'
def get_wiki_id(resource: str) -> str:
    '''Return Wikidata id (e.g. P31 or Q42).'''
    if "www.wikidata.org" in resource and "/" in resource:
        index = resource.rindex("/")
        return resource[index + 1:]
    return resource

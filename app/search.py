from flask import current_app

# Ces fonctions commencent toutes par vérifier si app.elasticsearchis None, 
# et dans ce cas, retournent la valeur sans rien faire. Ainsi, lorsque le serveur Elasticsearch 
# n'est pas configuré, l'application continue de s'exécuter sans la fonction 
# de recherche et sans générer d'erreur. Ceci est simplement pratique 
# lors du développement ou de l'exécution de tests unitaires.

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, document=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        query={'multi_match': {'query': query, 'fields': ['*']}},
        from_=(page - 1) * per_page,
        size=per_page)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
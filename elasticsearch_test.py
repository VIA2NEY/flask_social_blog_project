from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')

# es.index(index='my_index', id=1, document={'text': 'this is a test'})

# es.index(index='my_index', id=2, document={'text': 'a second test'})

# print(es.search(index='my_index', query={'match': {'text': 'this test'}}))

# es.indices.delete(index='my_index')


# -------------------------------------

from app.search import add_to_index, remove_from_index, query_index
from app.models import Post
for post in Post.query.scalar():
     add_to_index('posts', post)
# query_index('posts', 'one two three four five', 1, 100)
# # ([15, 13, 12, 4, 11, 8, 14], 7)
# query_index('posts', 'one two three four five', 1, 3)
# # ([15, 13, 12], 7)
# query_index('posts', 'one two three four five', 2, 3)
# ([4, 11, 8], 7)
query_index('posts', 'one two three four five', 3, 3)
# ([14], 7)


# -----------------------------

from app import create_app, db
app = create_app()
app.app_context().push()
from app.models import Post
Post.reindex()
query, total = Post.search('Hi there', 1, 5)
total
# 3
query.all()
# [<Post Hi y'all>, <Post Hi everyone i'm jean>, <Post Hi it's my first post here>]
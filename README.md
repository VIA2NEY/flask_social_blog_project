# SOCIAL BLOG APPLICATION

## Tuto Link

- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world



## Database migrations

- J'utilise Flask-migrate pour effectuer les migrations de la base de données. 


  - Voila les etapes pour la premier migration

    1. flask db init

    2. flask db migrate -m "first migration"

    3. flask db upgrade


  - Voila les etapes pour la prochaine migration

    1. flask db migrate -m "nom de migration"

    2. flask db upgrade
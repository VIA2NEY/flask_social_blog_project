# SOCIAL BLOG APPLICATION


<details>
<summary>Internationalization (i18n) et localisation(l10n) Avec Flask-Babel</summary>

- **Instalation et initialisation de Flask-Babel**

  - `pip install flask-babel`

  - importer `from flask_babel import _, lazy_gettext as _l` et ajouter _l("nom de la clef de traduction") dans un fichier .py et {{ _("nom de la clef de traduction") }} dans le template html

  - 

- **Configuration de Flask-Babel**

  - Creer le fichier babel.cfg dans le repertoire de l'application pour indiquer à `pybabel` quels fichiers doivent être analysés à la recherche de textes traduisibles exemples:
    [python: app/**.py]
    [jinja2: app/templates/**.html]

  - Executer la commande ``pybabel extract -F babel.cfg -k _l -o messages.pot .`` pour extraire les textes traduisibles; ça vas generere un fichier messages.pot

  - Executer la commande ``pybabel init -i messages.pot -d app/translations -l fr`` pour initialiser la traduction francaise; ca vas generer deux fichiers: messages.fr.po et messages.fr.mo dans un dossier translations

  - Une fois les fichier generer vous pouvez traduire le contenu du fichier messages.po et remplacer les "msgstr" par vos traductions manuellement ou utiliser des outis comme [Poedit](https://poedit.net) pour traduire le contenu du fichier messages.po

  - Executer la commande ``pybabel compile -d app/translations`` pour compiler les fichiers de traduction et mettre à jour le fichier messages.mo

- **Mettre à jour avec de nouvelles traductions**

  - Executer la commande ``pybabel extract -F babel.cfg -k _l -o messages.pot .`` puis ``pybabel update -i messages.pot -d app/translations`` pour mettre à jour les fichiers de traduction et mettre à jour le fichier messages.mo

</details>

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
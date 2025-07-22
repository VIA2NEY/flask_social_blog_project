# SOCIAL BLOG APPLICATION


<details>
<summary>Internationalization (i18n) et localisation(l10n) Avec Flask-Babel</summary>

- **Instalation et initialisation de Flask-Babel**

  - `pip install flask-babel`

  - importer `from flask_babel import _, lazy_gettext as _l` et ajouter _l("nom de la clef de traduction") dans un fichier .py et {{ _("nom de la clef de traduction") }} dans le template html

  - 

- **Configuration de Flask-Babel**

  - Creer le fichier `babel.cfg` dans le repertoire de l'application pour indiquer à `pybabel` quels fichiers doivent être analysés à la recherche de textes traduisibles exemples:
    [python: app/**.py]
    [jinja2: app/templates/**.html]

  - Executer la commande ``pybabel extract -F babel.cfg -k _l -o messages.pot .`` pour extraire les textes traduisibles; ça vas generere un fichier messages.pot

  - Executer la commande ``pybabel init -i messages.pot -d app/translations -l fr`` pour initialiser la traduction francaise; ca vas generer deux fichiers: messages.fr.po et messages.fr.mo dans un dossier translations

  - Une fois les fichier generer vous pouvez traduire le contenu du fichier messages.po et remplacer les "msgstr" par vos traductions manuellement ou utiliser des outis comme [Poedit](https://poedit.net) pour traduire le contenu du fichier messages.po

  - Executer la commande ``pybabel compile -d app/translations`` pour compiler les fichiers de traduction et mettre à jour le fichier messages.mo

- **Mettre à jour avec de nouvelles traductions**

  - Executer la commande ``pybabel extract -F babel.cfg -k _l -o messages.pot .`` puis ``pybabel update -i messages.pot -d app/translations`` pour mettre à jour les fichiers de traduction et mettre à jour le fichier messages.mo

</details>


<details>
<summary>Ajout du fichier app/cli.py pour ajouter des commandes personnaliser à la commande flask</summary>

- Ce fichier contient les commandes personnaliser pour le volet de traduction ajouter aux commandes de flask. Ces commandes seront accessible depuis le terminal et les voici.

  - `flask translate init LANG` pour ajouter une nouvelle langue
  - `flask translate update` pour mettre à jour tous les langues après avoir modifié les marqueurs de langage _() et _l()
  - `flask translate compile` pour compiler tous les depots de langues apres avoir modifie les marqueurs de langage _() et _l()

- Plus d'informations:

Console 
```
flask --help
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  An application to load must be given with the '--app' option, 'FLASK_APP'
  environment variable, or with a 'wsgi.py' or 'app.py' file in the current
  directory.

Options:
  -e, --env-file FILE   Load environment variables from this file, taking
                        precedence over those set by '.env' and '.flaskenv'.
                        Variables set directly in the environment take highest
                        precedence. python-dotenv must be installed.
  -A, --app IMPORT      The Flask application or factory function to load, in
                        the form 'module:name'. Module can be a dotted import
                        or file path. Name is not required if it is 'app',
                        'application', 'create_app', or 'make_app', and can be
                        'name(args)' to pass arguments.
  --debug / --no-debug  Set debug mode.
  --version             Show the Flask version.
  --help                Show this message and exit.

Commands:
  db         Perform database migrations.
  routes     Show the routes for the app.
  run        Run a development server.
  shell      Run a shell in the app context.

Commands:
  db         Perform database migrations.
  routes     Show the routes for the app.
  run        Run a development server.
  shell      Run a shell in the app context.
  ->translate  Translation and localization commands.<- Viens d'etre ajouter grace a app/cli.py
```
PUIS
```
flask translate --help
Usage: flask translate [OPTIONS] COMMAND [ARGS]...

  Translation and localization commands.

Options:
  --help  Show this message and exit.

Commands:
  compile  Compile all languages.
  init     Initialize a new language.
  update   Update all languages.
```
</details>

<details>
<summary>Instalation de ElasticSearch Via Docker</summary>

CMD : `docker run --name elasticsearch -d --rm -p 9200:9200 --memory="2GB" -e discovery.type=single-node -e xpack.security.enabled=false docker.elastic.co/elasticsearch/elasticsearch:9.0.3 `
</details>


<details>
<summary>Instalation de Vagrant et de VirtualBox</summary>

 1. Installer Vagrant depuis la doc officielle: https://www.vagrantup.com/downloads.html puis redemarrer le pc pour que les modifications soient prises en compte 
 2. Installer VirtualBox depuis la doc officielle : https://www.virtualbox.org/wiki/Downloads
 3. executer dans la console la commande vagrant init <nom du système d'exploitation> dans notre cas ``vagrant init ubuntu/jammy64``
 4. En cas de deconnexion les étapes pour ce reconnecter sont les suivantes:

    - `vagrant status`: Pour verifier si vagrant est bien installé et que la machine virtuelle est bien allumée ou non

    - `vagrant up`: Dans le cas ou la machine virtuelle n'est pas allumée, allumer la machine virtuelle

    - `vagrant ssh`: Pour se connecter au terminal de la machine virtuelle

    - `vagrant halt`: Pour arreter la machine virtuelle

    - `vagrant reload`: Dans le cas ou vous apportez des changement dans le fichier Vagrantfile, Pour redemarrer la machine virtuelle puis se connecter au terminal de la machine virtuelle avec la commande `vagrant ssh`

    > **ATTENTION** : 
    - Pour pouvoir acceder deployer l'applicattion grace à la machine virtuelle, il faut aller dans la console vagrant et executer la commande `vagrant ssh` puis executer la commande `cd /project_name` pour acceder a l'application puis activer l'environment virtuelle `source venv/bin/activate` et enfin executer la commande  `gunicorn -b 0.0.0.0:8000 microblog:app` pour lancer l'application web
      >> Pour le cas ou l'application a deja ete cloner via git     
    - Pour pouvoir acceder a l'application web sur la machine hote, il faut utiliser l'adresse suivante `http://192.168.56.10:8000` et desactiver le pare-feu ou autoriser l'acces aux port 8000 dans le pare-feu pour pouvoir acceder au site.

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

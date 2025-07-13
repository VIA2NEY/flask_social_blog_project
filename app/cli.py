from flask import Blueprint
import os
import click

"""Améliorations de la ligne de commande(Command-Line Enhancements)

Ce fichier contient des commandes personnalisées intégrées à la commande flask.
Ici pour mettre à jour et compiler les fichiers de traduction.
Je vais donc créer quelques commandes simples qui déclenchent les commandes pybabel 
avec tous les arguments spécifiques à cette application. Les commandes que je vais ajouter sont les suivantes :

° flask translate init LANG:    pour ajouter une nouvelle langue
° flask translate update:       pour mettre à jour tous les dépôts de langues
° flask translate compile:      pour compiler tous les dépôts de langues

L'étape d'extraction babel ne sera pas une commande, car la génération du fichier messages.pot 
est toujours une condition préalable à l'exécution des commandes init ou update, 
de sorte que la mise en œuvre de ces commandes générera le fichier de modèle 
de traduction en tant que fichier temporaire.

"""

bp = Blueprint('cli', __name__, cli_group=None)

@bp.cli.group()
def translate():
    """Translation and localization commands."""
    pass


@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')
import mysql.connector

import click # nos permite escribir comendos en la terminal
from flask import current_app, g # g es una variable global para asignarle 
# valores se usara para guardar el usuario
from flask.cli import with_appcontext # para ejercutar script y acceder a
# las variables que se encuentran en la configuracion de la aplicacion
from .schema import instructions

def get_db(): # para obtener la base de datos y el cursor
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database = current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary = True)
        
        return g.db, g.c

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()


def init_db(): #vamos a traernos la base de datos
    db, c = get_db()
    for i in instructions:
        c.execute(i)

    db.commit()

    
@click.command('init-db') # nombre con el que se llamara en tabla de comando flask init_db
@with_appcontext # para se escriba ene el contexto de db definido en get_db
def init_db_command():
    init_db() # ejecuta la logica para poder correr los script
    click.echo('bases de datos inicializada') # iniciamos el script

def init_app(app): # se ejecutara cadavez despues de cada peticion que se haga  
    # la  base de datos 
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


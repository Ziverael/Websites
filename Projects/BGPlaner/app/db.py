import mysql.connector
from mysql.connector import errorcode
from flask import jsonify, current_app, g
from flask_login import UserMixin
import click

class Database():
    def __init__(self, schema_):
        """sumary_line
        
        Args
        ----
        schema_ [srting]    path to sql schema for the database
        """
        self.connection = Connection(
            current_app.config["MYSQL_HOST"],
            current_app.config["MYSQL_USER"],
            current_app.config["MYSQL_PASSWORD"],
            current_app.config["MYSQL_DATABASE"]
        )
        self.connection.open_connection()
        with open(schema_, 'r') as f:
            self.schema = f.read()
    
    def build_tables(self):
        if self.connection.is_open():
            with self.connection.connection.cursor() as cursor:
                try:
                    cursor.execute(self.schema)
                    cursor.commit()
                except:
                    self.close_db()
            return True
        return False
    
    def query(self, query_, params_ = None, **kwargs):
        return self.connection.query(query_, params_, **kwargs)
    
    def commit(self):
        self.connection.commit()        

    def reconnect(self):
        if self.connection.is_open():
            self.connection.open_connection()
            return True
        return False
    
    def get_db(self):
        if not self.connection.is_open():
            self.connection.open_connection()
        return self.connection

    def close_db(self, e = None):
        if self.connection.is_open():
            self.connection.close_connection()
            return True
        return False
    


class Connection():
    def __init__(self, host, user, pass_, db):
        self.host = host
        self.user = user
        self.password = pass_
        self.db = db
        self.connection = None
        
        self.isOpen = False
    
    def open_connection(self, verbose = False):
        if verbose:
            print("Connecting to the server...")
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.db
            )
            self.isOpen = True

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        if verbose:
            print("[DONE]\tConnection opened.")
            
    
    def close_connection(self, verbose = False):
        if self.isOpen:
            self.connection.close()
            self.isOpen = False
            if verbose:
                print("[DONE]\tConnection closed.")
            return True
        if verbose:
            print("[FAILED]\tConnection is closed already.")
        return False
    
    def query(self, query : str, params : tuple = None, results :str = "all", verbose = False):
        """Query database. Query is performed by mqsql Cursor.
        To perform query one shoud pass SQL query. More about syntax and connector using you can read here
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

        Args
        ----
        results  string representing number of results type. Valid values are "all" and "one"
        """
        
        if self.isOpen:
            qu = self.connection.cursor()
            if verbose:
                print("Run query:")
            qu.execute(query, params)
            # try:
                # qu.execute(query, params)
            # except:
                # raise ValueError("Invalid query")
            if results == "all":
                resp = qu.fetchall()
            elif results == "one": 
                resp = qu.fetchone()
            else:
                raise ValueError("Invalid fetch type")
            # resp = jsonify(resp)
            # resp.status_code = 200
            if verbose:
            #     print("Results\n--------")
            #     for i in out:
            #         print(row)
                print("Closing query")
            qu.close()
            print(resp, "Response type:", type(resp))
            return resp
            

        if verbose:
            print("[FAILED]\tNot connected to database.")
            return False
    
    def commit(self):
        self.connection.commit()

    def __del__(self):
        self.close_connection(True)
    
    def is_open(self):
        return self.isOpen


###APP INTERFACE###

@click.command("init-db")
def init_db_command():
    if 'db' not in g:
        g.db = Database("schema.sql")
        g.db.build_tables()
        click.echo("Database initialized.")


def get_db():
    """Get database object from global handler"""
    if 'db' not in g:
        g.db = Database("schema.sql")
    return g.db


def init_app(app):
    @app.teardown_appcontext
    def teardown_db(e):
        db = g.pop('db', None)
        if db is not None:
            db.close_db()
    app.cli.add_command(init_db_command)

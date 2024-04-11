import sqlite3

def get_db() :
    con=sqlite3.connect("tables.sqlite")
    con.row_factory=sqlite3.Row
    return con
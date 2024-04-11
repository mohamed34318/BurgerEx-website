from database import get_db

def create_tables() :
    con=get_db()
    with open ("tables.sql") as tables :
        con.executescript(tables.read())
    con.close()
    return

if __name__=="__main__" :
    create_tables()

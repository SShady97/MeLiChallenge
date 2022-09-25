from .conexion import conexion

def createDB():
    con = conexion()
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS archivo (ID_FILE text UNIQUE, NAME text, EXT text, OWNER text, VISIBILITY text, MODIFIED_TIME text, WAS_PUBLIC boolean DEFAULT False)''')
    con.commit()
    con.close()

def saveFiles(id_file, name, ext, owner, visibility, modified_time, public):
    con = conexion()
    cur = con.cursor()
    cur.execute("INSERT INTO archivo VALUES ('{}','{}','{}','{}','{}','{}', {})".format(id_file, name, ext, owner, visibility, modified_time, public))
    con.commit()
    con.close()

def updateFile(id_file, name, ext, owner, visibility, modified_time, public):
    con = conexion()
    cur = con.cursor()
    if public == True:
        cur.execute(
            "UPDATE archivo SET NAME = '{}', EXT = '{}', OWNER = '{}', VISIBILITY = '{}', MODIFIED_TIME = '{}', WAS_PUBLIC = {} WHERE ID_FILE = '{}'".format(
                name, ext, owner, visibility, modified_time, public, id_file))
    else:
        cur.execute(
            "UPDATE archivo SET NAME = '{}', EXT = '{}', OWNER = '{}', VISIBILITY = '{}', MODIFIED_TIME = '{}' WHERE ID_FILE = '{}'".format(
                name, ext, owner, visibility, modified_time, id_file))
    con.commit()
    con.close()

def deleteDB():
    con = conexion()
    cur = con.cursor()
    cur.execute("DELETE FROM archivo")
    print("Archivos eliminados con éxito!")
    con.commit()
    con.close()

def getFile(id_file):
    con = conexion()
    cur = con.cursor()
    cur.execute("SELECT * FROM archivo WHERE archivo.id_file = '{}'".format(id_file))
    file = cur.fetchone()
    return file

def getHistoricalPublicDocs():
    con = conexion()
    cur = con.cursor()
    cur.execute("SELECT name FROM archivo WHERE archivo.was_public = True")
    historical_public_docs = cur.fetchall()
    return historical_public_docs


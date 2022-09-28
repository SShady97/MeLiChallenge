from functions.db.database import saveFiles, getFile, updateFile
from functions.mail import sendEmail
from functions.date import setToLocalTime
from datetime import datetime

def getAllFolders(service):
    # Call the Drive v3 API
    # Se obtienen todas las carpetas de la unidad de drive del usuario.
    folders_results = service.files().list(
        q="mimeType='application/vnd.google-apps.folder' and trashed = false and 'me' in owners",
        pageSize=1000, fields="nextPageToken, files(id, name)").execute()
    folders = folders_results.get('files', [])
    return folders

def getFilesByFolder(service, folders):
    all_files = []
    for folder in folders:
        files_results = service.files().list(
            q="'{}' in parents and trashed = false and mimeType != 'application/vnd.google-apps.folder' and 'me' in owners".format(
                folder['id']),
            pageSize=1000,
            fields="nextPageToken, files(permissions, mimeType, id, name, fileExtension, modifiedTime, owners, fileExtension, shared)").execute()
        files = files_results.get('files', [])
        if files:
            all_files.extend(files)
    return all_files

def getRootFiles(service):
    root_results = service.files().list(q="'me' in owners and 'root' in parents and mimeType != 'application/vnd.google-apps.folder' and mimeType != 'application/vnd.google-apps.shortcut'",
            pageSize=1000, fields="nextPageToken, files(permissions, mimeType, id, name, fileExtension, modifiedTime, owners, fileExtension, shared)").execute()
    root_files = root_results.get('files', [])
    return root_files

def processData(service, files):
    to_private = []
    for count, item in enumerate(files):
        # Se excluyen las carpetas y los accesos directos de los archivos si es que existen
        id_file = item['id']
        name = item['name']
        # Se busca en el array de permisos del archivo si tiene el permiso "anyoneWithLink".
        permission_public = ['anyoneWithLink' in permission['id'] for permission in item['permissions']]
        owner = item['owners'][0]['displayName']
        modified_time = item['modifiedTime']
        # Si el acceso del archivo esta configurado como "Cualquier persona con el enlace"
        # Se define la variable public como True para tener registro de que el archivo fue publico
        # Luego se cambia el acceso del archivo a "Restringido"
        if True in permission_public:
            public = True
            to_private.append(item)
            service.permissions().delete(
                fileId=id_file,
                permissionId='anyoneWithLink').execute()
            modified_time = datetime.utcnow().isoformat() + 'Z'
        else:
            public = False
        if 'fileExtension' in item:
            ext = item['fileExtension']
        else:
            ext = ""
        visibility = "Private"
        db_file = getFile(id_file)
        modified_time = setToLocalTime(modified_time)
        # Si el archivo ya existe en la base de datos se actualiza, en caso contrario, se crea.
        if db_file:
            updateFile(id_file, name, ext, owner, visibility, modified_time, public)
        else:
            saveFiles(id_file, name, ext, owner, visibility, modified_time, public)
        if count == len(files) - 1:
            print("Se han creado y/o actualizado archivos en la base de datos!")
        # Si se cambio el acceso general de algun documento se llama a la funcion sendEmail que envia el correo electronico
    if to_private:
        print("Se han encontrado {} archivos públicos!\n".format(len(to_private)))
        sendEmail(to_private)
    else:
        print("No se han encontrado archivos públicos!\n")




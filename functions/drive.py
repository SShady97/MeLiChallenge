from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from functions.db.database import saveFiles, getFile, updateFile
from functions.mail import sendEmail
from functions.date import setToLocalTime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def getDrive():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./token.json'):
        creds = Credentials.from_authorized_user_file('./token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials.json', SCOPES)
            creds = flow.run_console(authorization_prompt_message='Por favor visite esta URL para autorizar esta aplicación: {url}' , authorization_code_message='Ingrese el código de autorización: ')
        # Save the credentials for the next run
        with open('./token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
        to_private = []
        # Call the Drive v3 API
        # Se obtienen los archivos que son de mi propiedad.
        results = service.files().list(q="'me' in owners",
            pageSize=1000, fields="nextPageToken, files(mimeType, id, name, fileExtension, modifiedTime, owners, fileExtension, shared)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
            return

        for count, item in enumerate(items):
            # Se excluyen los accesos directos de los archivos si es que existen
            if(item['mimeType'] != 'application/vnd.google-apps.shortcut'):
                id_file = item['id']
                name = item['name']
                owner = item['owners'][0]['displayName']
                modified_time = item['modifiedTime']
                # Si el acceso del archivo esta configurado como "Cualquier persona con el enlace"
                # Se define la variable public como True para tener registro de que el archivo fue publico
                # Luego se cambia el acceso del archivo a "Restringido"
                if item['shared']:
                    public = True
                    to_private.append(item)
                    service.permissions().delete(
                        fileId=id_file,
                        permissionId='anyoneWithLink').execute()
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
            if count == len(items)-1:
                print("Se han creado y/o actualizado archivos en la base de datos!")
        # Si se cambio el acceso general de algun documento se llama a la funcion sendEmail que envia el correo electronico
        if len(to_private) > 0:
            print("Se han encontrado {} archivos públicos!\n".format(len(to_private)))
            sendEmail(to_private)
        else:
            print("No se han encontrado archivos públicos!\n")
    except HttpError as error:
        print(f'An error occurred: {error}')



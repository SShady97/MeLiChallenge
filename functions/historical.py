from functions.db.database import getHistoricalPublicDocs

def getHistorical():
    historical = getHistoricalPublicDocs()
    if len(historical) > 0:
        print('Se han encontrado {} registros dentro del historico de archivos públicos:'.format(len(historical)))
    else:
        print('No se encontraron archivos!')
    for name in historical:
        print('- {}'.format(name[0]))

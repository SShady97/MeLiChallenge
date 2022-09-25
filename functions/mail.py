import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

def sendEmail(files):
    try:
        content = "El acceso general de los siguientes archivos que tienes en tu unidad de Google Drive se ha cambiado a 'Restringido': \n"
        for file in files:
            content += "- " + file['name'] + "\n"
        to_addrs = files[0]['owners'][0]['emailAddress']
        load_dotenv()
        user = os.getenv('EMAIL_USER')
        password = os.getenv('EMAIL_APP_PASS')
        msg = EmailMessage()
        msg['Subject'] = 'Cambio en el acceso general de tus archivos de Google Drive'
        msg['From'] = 'MeLi Challenge'
        msg['To'] = to_addrs
        msg.set_content(content)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(user, password)
        server.send_message(msg)
        server.quit()
        print("Email enviado con éxito! \n")
    except:
        print("Ha ocurrido un error con el envio del email! \n")









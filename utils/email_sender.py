# -encoding: cp1252 -*-

import smtplib
from email.header import Header


def envia_email_imagem(destinatarios, copia, assunto, corpo, imagem, cor):
    #try:
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
  
    cores = {
             'red': {'hex': '#8C0B11', 'bola': 'red_bola.png', 'linha': 'red_line.png', 'banner': 'red_banner.png'},
             'orange': {'hex': '#ECB700','bola': 'orange_bola.png', 'linha': 'orange_line.png', 'banner': 'orange_banner.png'},
             'green': {'hex': '#94BD15','bola': 'green_bola.png', 'linha': 'green_line.png', 'banner': 'green_banner.png'},
             'blue': {'hex': '#7092BE','bola': 'blue_bola.png', 'linha': 'blue_line.png', 'banner': 'blue_banner.png'},
             }


    corpo = corpo.replace('{cor_bg_hex}', cores[cor]['hex'])
    strFrom = 'ti.monitoria@cnova.com'
    strTo = ';'.join(destinatarios)
    strCopia = ';'.join(copia)
    
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = Header(assunto, "cp1252")
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot['CC'] = strCopia
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    #print(corpo)
    body = MIMEText(corpo, 'html', _charset='cp1252')
    msgAlternative.attach(body)

    msgImage = MIMEImage(imagem)
    msgImage.add_header('Content-ID', '<imagem_grafico>')
    msgRoot.attach(msgImage)
   
    caminho_imagens = '/usr/local/share/zabbix/alertscripts/templates/images/'   
 
    with open(caminho_imagens + cores[cor]['bola'], 'rb') as arquivo:
        msgImage = MIMEImage(arquivo.read())    
        msgImage.add_header('Content-ID', '<bola>')
        msgRoot.attach(msgImage)

    with open(caminho_imagens + cores[cor]['linha'], 'rb') as arquivo:
        msgImage = MIMEImage(arquivo.read())
        msgImage.add_header('Content-ID', '<linha>')
        msgRoot.attach(msgImage)

    with open(caminho_imagens + cores[cor]['banner'], 'rb') as arquivo:
        msgImage = MIMEImage(arquivo.read())
        msgImage.add_header('Content-ID', '<banner>')
        msgRoot.attach(msgImage)


    with open(caminho_imagens + 'cnova.png', 'rb') as arquivo:
        msgImage = MIMEImage(arquivo.read())
        msgImage.add_header('Content-ID', '<cnova>')
        msgRoot.attach(msgImage)

    with open(caminho_imagens + 'listras.jpg', 'rb') as arquivo:
        msgImage = MIMEImage(arquivo.read())
        msgImage.add_header('Content-ID', '<listras>')
        msgRoot.attach(msgImage)


    s = smtplib.SMTP('mailer-corp001.dc.nova')
    s.sendmail(strFrom, destinatarios + copia, msgRoot.as_string())
    s.quit()
    #    return True
    #except Exception as e:
    #    print(e)
    #    return False





    


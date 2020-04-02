#!/usr/bin/env python

import os

mail_to='["997472490@qq.com","zpzhu@nao.cas.cn","dxu@nao.cas.cn","445360071@qq.com","sg1@dark-cosmology.dk"]'
#mail_to='["445360071@qq.com",]'
email_keys={'mail_to':mail_to}




def send_email(gcn_keys, visibility_keys, identification_keys, email_keys=email_keys):
    email_name = gcn_keys['fol']+'/'+gcn_keys['gcn_name']+'/'+'mail_'+gcn_keys['gcn_name']+'.py'
    for i in gcn_keys:
        globals()[i] = gcn_keys[i]
    Files = []
    try:
        Files.append(gcn_keys['_voname'])
        Files.append(gcn_keys['ds9_reg'])
        #probably not exist;keep it last one
        Files.append(gcn_keys['gcn_img'])
    except:
        pass
    identification_list=''
    list_keys=['Xinglong','Nanshan','CNEOST','NOT','Cerro Paranal','Mauna Kea']
    for i in list_keys:
        #print(visibility_keys[i])
        identification_list=identification_list+'\n<br/><a href="'+visibility_keys[i]+'">'+i+' : '+visibility_keys[i]+'</a><br/>\n\n'
    #for i in identification_keys:
    #    Files.append(identification_keys[i])
    try:
        globals()['dsslink']=identification_keys['dsslink']
    except:
        globals()['dsslink']='unknown'
    try:
        Files.append(identification_keys['pngname10'])
        Files.append(identification_keys['pngname3'])
    except:
        pass
    print(Files)
    mail_to = email_keys['mail_to']
    print(mail_to)
    str_mail = """#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
import os, mimetypes

def add_attachment(filepath):
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    if maintype == 'text':
        fp = open(filepath)
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'image':
        fp = open(filepath, 'rb')
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'audio':
        fp = open(filepath, 'rb')
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(filepath, 'rb')
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)

    baseName = os.path.basename(filepath)
    attachment.add_header('Content-Disposition', 'attachment', filepath=filepath,  filename=baseName)
    msg.attach(attachment)
    print(filepath, 'added')


username = 'transient@nao.cas.cn'
password = 'naoc@2019'

sender = 'transient@nao.cas.cn' ## 发件人邮箱, 多人逗号分开
#receiver = ['zpzhu@nao.cas.cn','997472490@qq.com','741144164@qq.com'] ## 收件人邮箱, 多人逗号分开
receiver =  %(mail_to)s

subject = 'GRB%(grb_time)s [ %(gcn_Packet_Type)s ] \\'s  visibility and  finding chart  '
mail_content = \"\"\"
<html>
    <h3> Content of GRB mail from P920 </h3>
    <br/><br/> GRB%(grb_time)s UT<br/>
    Packet_Type : %(gcn_Packet_Type)s %(Packet_Type)s<br/>
    1. ivorn: %(gcn_name)s.xml <br/>
    2. ra,dec =  (  %(ra)s      %(dec)s  ) deg<br/>
    3. err = %(radius)s deg<br/>
    4. Sun_Distance =   %(Sun_Distance)s deg<br/>
    5. MOON_Distance =   %(MOON_Distance)s deg<br/>
    6. dss image link %(dsslink)s <br/>
    7. http://catserver.ing.iac.es/staralt/index.php <br/>
%(identification_list)s<br/>
    <br/>Finding Chart(s) is attached to this mail. <br/>
</html>
\"\"\"
msg = MIMEMultipart()
msg.add_header('From',username)
#msg.add_header('To',receiver)
msg.add_header('Subject',subject)
msg.add_header('Date',subject)
msg.attach(MIMEText(mail_content, 'html'))
#toaddrs = [receiver]

msg['To'] = ','.join(receiver)

#Files=['$file_out','$image_raw','$fits_raw']
Files=%(Files)s

for filepath in Files:
    try:
        ctype, encoding = mimetypes.guess_type(filepath)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        if maintype in['image','audio']:
            add_attachment(filepath)
        else:
            baseName = os.path.basename(filepath)
            att = MIMEApplication(open(filepath,'rb').read())
            att.add_header('Content-Disposition', 'attachment', filename=baseName)
            msg.attach(att)
            print(filepath, 'added')
    except:
       print(filepath, 'not added')


mail_server = 'smtp.cnic.cn'
mail_server_port = 25
server = smtplib.SMTP(mail_server, mail_server_port)
server.ehlo()
server.starttls()
server.login(username, password)
server.sendmail(sender, receiver, msg.as_string())
server.quit()

print('email done.')

#os.system('echo "6"')
"""
    with open(email_name,'w') as em:
        em.write(str_mail % dict(mail_to = mail_to, gcn_name = gcn_name, grb_time = grb_time, gcn_Packet_Type = gcn_Packet_Type, Packet_Type = Packet_Type, ra = ra, dec = dec, radius = radius, Sun_Distance = Sun_Distance, MOON_Distance = MOON_Distance, identification_list = identification_list, Files = Files, dsslink = dsslink ))
    os.system('python3 '+email_name)
    return


if __name__ == "__main__":
    #name = SWIFT#Actual_Point_Dir_2019-10-28T13:30:33.87_355431105-143, ra = 277.327, dec = 64.1598, radius = 0, Sun_Distance = 91.37, MOON_Distance = 86.68
    gcn_keys= {'gcn_name':'test','grb_time':'190000.000', 'gcn_Packet_Type':'SWIFT_XRT', 'Packet_Type':'61', 'ra':'277.327', 'dec':'64.1598', 'radius':'0', 'Sun_Distance':'91.37', 'MOON_Distance':'86.68', 'gcn_img':'','fol':'./'}
    send_email(gcn_keys,{},{})

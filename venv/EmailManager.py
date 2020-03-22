# coding = utf-8
import imaplib
import email
import re
import logging

from email.parser import BytesParser
from email.utils import parseaddr
from unblocker import unblocker_class
#IMAP ssl设置
host = 'imap.sina.com'
user = 'appleidjiesuoba@sina.com'
passwd = '#####'
#获取邮箱文件夹，INBOX表示默认收件箱
mail_directory = 'INBOX'
log_level = logging.DEBUG   #log记录等级
appleid_pas="####"     #Apple id 的密码

logging.basicConfig(filename='mail.log',level=log_level,format='%(asctime)s - %(levelname)s - %(message)s',datefmt="%Y/%m/%d %H:%M:%S %p")

conn = imaplib.IMAP4_SSL(host,993)
#print(conn)
conn.login(user,passwd)
conn.select(mail_directory,readonly = False)    #选择收件箱并可选标记已读
status, data = conn.search(None, 'Unseen')  #搜索未读邮件
email_list = list(reversed(data[0].split()))
def decode_str(s):
    try:
        subject = email.header.decode_header(s)
    except:
        # print('Header decode error')
        return None
    sub_bytes = subject[0][0]
    sub_charset = subject[0][1]
    if None == sub_charset:
        subject = sub_bytes
    elif 'unknown-8bit' == sub_charset:
        subject = str(sub_bytes, 'utf8')
    else:
        subject = str(sub_bytes, sub_charset)
    return subject

def markasread(num):
    conn.store(num, '+FLAGS', 'Seen')
    logging.info("Mark main ID：%s as read"%num)

def findurl(string):
    url = re.search('.*(https://iforgot.apple.com/verify/email\?key=.*)', string)
    # print(type(url))
    # print(url.group(1))
    return url.group(1)

def get_email(num, conn):

    typ, content = conn.fetch(num, '(RFC822)')
    msg = BytesParser().parsebytes(content[0][1])
    #print(msg)
    sub = msg.get('Subject')
    sender = msg.get('X-Sender')
    date = msg.get('Date')
    for part in msg.walk():
        # fileName = part.get_filename()
        # fileName = decode_str(fileName)
        # if None != fileName:
        #     print('+++++++++++++++++++')
        #     print(fileName)
        if not part.is_multipart():
            #print('+++++++++++++++++++')
            #print(part.get_payload(decode=True).decode('utf-8'))
            print(num, decode_str(sub),decode_str(sender),decode_str(date))
            return part.get_payload(decode=True).decode('utf-8')

    #print(num, decode_str(sub),decode_str(sender))
for num in email_list:
    r=get_email(num, conn)
    url=findurl(r)
    print(url)
    result=unblocker_class(url,appleid_pas).unblocker()
    #print(result)
    if result == True:
        markasread(num)
        logging.info('Apple ID Unblocked！')
    elif result['err_no'] == '1':
        logging.error("Failure in fetching url！Url:{} is invalid! Reason:{}".format(url,result['err_msg']))
        markasread(num)
    elif result['err_no'] == '2':
        logging.error("Failure in acessing Apple！Pls change your ip ：%s" %result['err_msg'])
    elif result['err_no'] == '3':
        logging.error("Failure！Wrong Apple password ")


conn.close()
conn.logout()

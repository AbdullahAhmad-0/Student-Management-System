import os
from datetime import datetime


class Log_Generator:
    current_folder = os.getcwd()
    if os.path.basename(current_folder) == 'Library_Files':
        main_folder = os.path.dirname(current_folder)
    else:
        main_folder = current_folder
    temp_log_folder = f'{main_folder}\\Temp'

    def __int__(self):
        self.createLog()

    def addLog(self, log_text):
        now = datetime.now()
        date_time = now.strftime("[%Y-%m-%d %H:%M:%S]")
        date = now.strftime("%Y-%m-%d")
        f = open(f'{self.temp_log_folder}\\Log File {date}.txt', 'a')
        f.write(f'{date_time} {log_text}\n')
        f.close()

    def startLog(self):
        now = datetime.now()
        date_time = now.strftime("[%Y-%m-%d %H:%M:%S]")
        date = now.strftime("%Y-%m-%d")
        f = open(f'{self.temp_log_folder}\\Log File {date}.txt', 'a')
        f.write(f'Log File Started {date_time}\n')
        f.close()

    def createLog(self):
        now = datetime.now()
        date_time = now.strftime("[%Y-%m-%d %H:%M:%S]")
        date = now.strftime("%Y-%m-%d")
        f = open(f'{self.temp_log_folder}\\Log File {date}.txt', 'w')
        f.write(f'Log File Created {date_time}\n')
        f.close()

    def closeLog(self):
        now = datetime.now()
        date_time = now.strftime("[%Y-%m-%d %H:%M:%S]")
        date = now.strftime("%Y-%m-%d")
        f = open(f'{self.temp_log_folder}\\Log File {date}.txt', 'a')
        f.write(f'Log File Ended {date_time}\n\n')
        f.close()

    def findLog(self):
        try:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            f = open(f'{self.temp_log_folder}\\Log File {date}.txt', 'r')
            f.read()
            f.close()
            return True
        except:
            return False

    def readLog(self, date):
        try:
            f = open(f'{self.temp_log_folder}\\Log File {date}.txt', 'r')
            log = f.read()
            f.close()
            return log
        except:
            return None

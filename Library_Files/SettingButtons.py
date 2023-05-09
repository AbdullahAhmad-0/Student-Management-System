try:
    from Autocomplete_Combo import AutocompleteCombobox
    from Log_Generator import Log_Generator
    from FormRun import *
    from FormCommon import *
except:
    from Library_Files.Autocomplete_Combo import AutocompleteCombobox
    from Library_Files.Log_Generator import Log_Generator
    from Library_Files.FormRun import *
    from Library_Files.FormCommon import *

try:
    from CallSetting import CallSetting
    from ColorScheme import ColorScheme
except:
    from Library_Files.CallSetting import CallSetting
    from Library_Files.ColorScheme import ColorScheme


class ButtonsFunctions(BeforeInIt, AllSettings):
    def __init__(self):
        BeforeInIt.__init__(self)
        AllSettings.__init__(self)
        super().__init__()

    def status(self, txt, msg=False, show='Info', title=None):
        Log_Generator().addLog(txt)
        try:
            self.lbl_status.config(text=txt)
        except: pass
        if msg:
            if show.lower() == 'info':
                messagebox.showinfo(title, txt, parent=self.root)
            else:
                messagebox.showerror(title, txt, parent=self.root)

    def applyColorScheme(self, save, reopen):
        save()
        needToApply = CallSetting().getCommonSetting(temp=True)[12]

        f = open(f'{self.setting_folder}\\Color Schemes\\{needToApply}', 'r')
        fd = f.read()
        f.close()
        f = open(f'{self.setting_folder}\\Color Scheme', 'w')
        f.write(fd)
        f.close()
        reopen()

    def testdb(self):
        self.dbconfig_db = CallSetting().getDatabaseSetting(temp=True)[1]
        self.dbconfig_host = CallSetting().getDatabaseSetting(temp=True)[2]
        self.dbconfig_user = CallSetting().getDatabaseSetting(temp=True)[3]
        self.dbconfig_pass = CallSetting().getDatabaseSetting(temp=True)[4]
        self.dbconfig_dbname = CallSetting().getDatabaseSetting(temp=True)[5]
        try:
            db_type = self.dbconfig_db

            if db_type == 'sqlite':
                try:
                    self.con = sqlite3.connect(database=self.database)
                    self.cur = self.con.cursor()
                    self.status(f'[{self.mainName}] [Database] Connected with sqlite', True, 'info', 'Successful')
                except Exception as e:
                    self.status(f'[{self.mainName}] [Database Error] {e}\n\nContact With Creator +923150490481', True, 'Error', 'Database Error')

            elif db_type == 'mysql':
                host_ = self.dbconfig_host
                user_ = self.dbconfig_user
                password_ = self.dbconfig_pass

                try:
                    self.con = pymysql.connect(host=host_, user=user_, passwd=password_)
                    self.cur = self.con.cursor()
                    self.status(f'[{self.mainName}] [Database] Login Successfully')
                    try:
                        self.cur.execute(f'use {self.dbdbconfig_dbname}')
                        self.status(f'[{self.mainName}] [Database] Connected with mysql', True, 'info', 'Successful')
                    except Exception as e:
                        self.cur.execute(f'create database {self.dbdbconfig_dbname}')
                        self.cur.execute(f'use {self.dbdbconfig_dbname}')
                        self.status(f'[{self.mainName}] [Database] Created and Connected with mysql')
                except Exception as e:
                    self.status(f'[{self.mainName}] [Database Error] Enter Correct Database Credentials We are not able to Login Database\n\nContact With Creator +923150490481', True, 'Error', 'Database Error')
            else:
                self.status(f'[{self.mainName}] [Database Error] Select Database We Cannot Find Any Database And its Setting\n\nContact With Creator +923150490481', True, 'Error', 'Database Error')
        except Exception as e:
            self.status(f'[{self.mainName}] [Database Error] {e}\n\nContact With Creator +923150490481', True, 'Error', 'Database Error')

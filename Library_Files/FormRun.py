import os

try:
    from CallSetting import CallSetting
    from ColorScheme import ColorScheme
except:
    from Library_Files.CallSetting import CallSetting
    from Library_Files.ColorScheme import ColorScheme


class BeforeInIt:
    current_folder = os.getcwd()
    if os.path.basename(current_folder) == 'Library_Files':
        main_folder = os.path.dirname(current_folder)
    else:
        main_folder = current_folder
    setting_folder = f'{main_folder}\\Setting'
    database_folder = f'{main_folder}\\Database'
    temp_folder = f'{main_folder}\\Temp'
    images_folder = f'{main_folder}\\Images'
    library_folder = f'{main_folder}\\Library_Files'
    generated_folder = f'{main_folder}\\Generated'
    iconPath = f"{images_folder}\\ico.ico"
    default_db = f'{database_folder}\\Ahmad Soft Main DB.asdb'

    colorList = ColorScheme().getColor()
    advanceSetting = CallSetting().getAdvanceSetting()
    commonSetting = CallSetting().getCommonSetting()
    databaseSetting = CallSetting().getDatabaseSetting()
    formSetting = CallSetting().getFormSetting()
    if advanceSetting[4] == 'Default':
        database = default_db
    else:
        database = advanceSetting[4]

    old_mainW = 0
    old_mainH = 0

    def __init__(self):
        self.colorList = ColorScheme().getColor()


def __getFromList__(setting):
    setting = setting.replace('[', '')
    setting = setting.replace(']', '')
    setting = setting.split(',')
    return setting


class AllSettings:
    def __init__(self):
        self.refreshAllSettings()

    def refreshAllSettings(self):
        # Advance Setting
        self.advset_rtf = CallSetting().getAdvanceSetting()[1]
        self.advset_dbb = CallSetting().getAdvanceSetting()[2]
        self.advset_dbe = CallSetting().getAdvanceSetting()[3]
        self.advset_dbl = CallSetting().getAdvanceSetting()[4]

        # Common Setting
        self.cmnset_msgboxAadd = CallSetting().getCommonSetting()[1]
        self.cmnset_Afteradd = CallSetting().getCommonSetting()[2]
        self.cmnset_msgboxAupd = CallSetting().getCommonSetting()[3]
        self.cmnset_Afterupd = CallSetting().getCommonSetting()[4]
        self.cmnset_msgboxAdel = CallSetting().getCommonSetting()[5]
        self.cmnset_Afterdel = CallSetting().getCommonSetting()[6]
        self.cmnset_msgboxAimp = CallSetting().getCommonSetting()[7]
        self.cmnset_msgboxAexp = CallSetting().getCommonSetting()[8]
        self.cmnset_refA = CallSetting().getCommonSetting()[9]
        self.cmnset_refT = CallSetting().getCommonSetting()[10]
        self.cmnset_fullscreen = CallSetting().getCommonSetting()[11]
        self.cmnset_current_cs = CallSetting().getCommonSetting()[12]
        # buttons [13]

        # Database Configuration
        self.dbconfig_db = CallSetting().getDatabaseSetting()[1]
        self.dbconfig_host = CallSetting().getDatabaseSetting()[2]
        self.dbconfig_user = CallSetting().getDatabaseSetting()[3]
        self.dbconfig_pass = CallSetting().getDatabaseSetting()[4]
        self.dbconfig_dbname = CallSetting().getDatabaseSetting()[5]

        # Form Setting
        self.formset_searchFH = CallSetting().getFormSetting()[1]
        self.formset_statusFH = CallSetting().getFormSetting()[2]
        self.formset_btn_detFW = CallSetting().getFormSetting()[3]
        self.formset_btnFH = CallSetting().getFormSetting()[4]
        self.formset_mainFBFW = CallSetting().getFormSetting()[5]
        self.formset_mainFSFH = CallSetting().getFormSetting()[6]
        self.formset_yInF = CallSetting().getFormSetting()[7]
        self.formset_wOfF = CallSetting().getFormSetting()[8]
        self.formset_xOfF = CallSetting().getFormSetting()[9]
        self.formset_idStart = CallSetting().getFormSetting()[10]
        self.formset_mainFHB = CallSetting().getFormSetting()[11]
        self.formset_mainHF = CallSetting().getFormSetting()[12]
        self.formset_mainF = (CallSetting().getFormSetting()[13], CallSetting().getFormSetting()[14])
        self.formset_fieldH = CallSetting().getFormSetting()[15]
        self.formset_resetStatus = CallSetting().getFormSetting()[16]

        # Report Setting
        self.repset_Sauto = CallSetting().getReportSetting()[1]
        self.repset_Sloc = CallSetting().getReportSetting()[2]
        self.repset_Lrep = __getFromList__(CallSetting().getReportSetting()[3])
        self.repset_Prep = __getFromList__(CallSetting().getReportSetting()[4])
        self.repset_Size = CallSetting().getReportSetting()[5]
        self.repset_tm = CallSetting().getReportSetting()[6]
        self.repset_bm = CallSetting().getReportSetting()[7]
        self.repset_lm = CallSetting().getReportSetting()[8]
        self.repset_rm = CallSetting().getReportSetting()[9]
        self.repset_oras = CallSetting().getReportSetting()[10]

        # Card Generator and Cam Setting
        self.cgcmset_cpp = CallSetting().getCardandCamSetting()[1]
        self.cgcmset_rpp = CallSetting().getCardandCamSetting()[2]
        self.cgcmset_out = CallSetting().getCardandCamSetting()[3]
        self.cgcmset_cam = CallSetting().getCardandCamSetting()[4]

    def CallCommonVar(self, height_):
        # common variables
        self.sF_h = int(self.formset_searchFH)  # Search Frame Height
        self.dFsF_y = 20  # Detail Frame And Search Frame Y
        self.dFbFstF_x = 0  # Detail Frame And Button Frame And Status Frame X
        self.stF_h = int(self.formset_statusFH)  # Status Frame Height

        self.dFbF_w = int(self.formset_btn_detFW)  # Detail Frame and Button Frame Width
        self.rF_y = self.dFsF_y + self.sF_h + 1  # Record Frame Y
        self.stF_w = self.mainW  # Status Frame Width
        self.rF_w = self.mainW - self.dFbF_w  # Record Frame Width
        self.rF_h = self.mainH - self.rF_y - self.stF_h - height_ - 1  # Detail Frame and Record Frame Height -1 because we add 1 in stF_y
        self.bF_h = int(self.formset_btnFH)  # Button Frame Height

        self.dF_h = self.mainH - self.dFsF_y - self.bF_h - self.stF_h - height_ - 2
        self.bF_y = self.dFsF_y + self.dF_h + 1
        self.sF_w = self.mainW - self.dFbF_w  # Search Frame Width
        self.rF_x = self.dFbF_w + 1
        self.stF_y = self.rF_y + self.rF_h + 1  # Status Frame Y


class BeforeRun:
    def __init__(self):
        pass


class AfterRun:
    def __init__(self):
        pass

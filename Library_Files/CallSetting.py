import os


class CallSetting:
    setting = ['']

    current_folder = os.getcwd()
    if os.path.basename(current_folder) == 'Library_Files':
        main_folder = os.path.dirname(current_folder)
    else:
        main_folder = current_folder
    setting_folder = f'{main_folder}\\Setting'
    temp_folder = f'{main_folder}\\Temp'

    def getAdvanceSetting(self, temp=False):
        return self.__CommonSetting__("Advance Setting", temp)

    def getCommonSetting(self, temp=False):
        return self.__CommonSetting__("Common Setting", temp)

    def getDatabaseSetting(self, temp=False):
        return self.__CommonSetting__("Database Configurations", temp)

    def getFormSetting(self, temp=False):
        return self.__CommonSetting__("Form Setting", temp)

    def getReportSetting(self, temp=False):
        return self.__CommonSetting__("Report Setting", temp)

    def getCardandCamSetting(self, temp=False):
        return self.__CommonSetting__("Card Generator and Cam Setting", temp)

    def __checkFL__(self, setting, temp):
        nList = []
        for i in setting:
            try:
                if '+' in i:
                    a, b = i.split('+')
                    if temp:
                        f = open(f'{self.temp_folder}\\{a}.fl', 'r')
                    else:
                        f = open(f'{self.setting_folder}\\{a}.fl', 'r')
                    files = f.readlines()
                    f.close()
                    nList.append(files[int(b) - 1].strip('\n'))
                else:
                    nList.append(i)
            except:
                nList.append(i)

        return nList

    def __CommonSetting__(self, name, temp):
        self.setting = [temp]
        if temp:
            colorFile = f'{self.temp_folder}\\{name}'
        else:
            colorFile = f'{self.setting_folder}\\{name}'

        f = open(colorFile, 'r')
        color_set = f.readlines()
        f.close()

        cnt = 0
        for _ in color_set:
            _, a = color_set[cnt].strip('\n').split(':')
            a, *_ = a.split('.')
            self.setting.append(a)
            cnt += 1

        self.setting = self.__checkFL__(self.setting, temp)

        return self.setting


def main():
    a = CallSetting().getCommonSetting()
    print(a)


if __name__ == '__main__':
    main()

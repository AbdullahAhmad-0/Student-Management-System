import os


class ColorScheme:
    colorList = ['']

    current_folder = os.getcwd()
    if os.path.basename(current_folder) == 'Library_Files':
        main_folder = os.path.dirname(current_folder)
    else:
        main_folder = current_folder
    setting_folder = f'{main_folder}\\Setting'

    def getColor(self):
        self.colorList = ['']
        colorFile = f'{self.setting_folder}\\Color Scheme'

        f = open(colorFile, 'r')
        color_set = f.readlines()
        f.close()

        cnt = 0
        for _ in color_set:
            _, a = color_set[cnt].strip('\n').split(':')
            a, *_ = a.split('.')
            self.colorList.append(a)
            cnt += 1

        return self.colorList


def main():
    a = ColorScheme().getColor()
    print(a)


if __name__ == '__main__':
    main()

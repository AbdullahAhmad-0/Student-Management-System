from tkinter import *
from tkinter import ttk, messagebox, filedialog, font, colorchooser
from tkcalendar import Calendar, DateEntry
import os, threading, shutil

try:
    from Autocomplete_Combo import AutocompleteCombobox
    from Log_Generator import Log_Generator
    from ColorScheme import ColorScheme
    from FormRun import *
    from SettingButtons import *
except:
    from Library_Files.Autocomplete_Combo import AutocompleteCombobox
    from Library_Files.Log_Generator import Log_Generator
    from Library_Files.ColorScheme import ColorScheme
    from Library_Files.FormRun import *
    from Library_Files.SettingButtons import *


class Setting(ButtonsFunctions):
    wSize, hSize = 800, 550
    title = "Setting - Student Management System"
    mainName = "Setting"

    def __init__(self, wind, default_setting_selected=None, libFormList=[]) -> None:
        ButtonsFunctions.__init__(self)
        super().__init__()
        self.root = wind
        self.root.title(self.title)
        self.root.iconbitmap(self.iconPath)
        self.root.config(bg=self.colorList[3])

        if self.cmnset_fullscreen == 'True':
            self.root.attributes("-fullscreen", True)
        self.root.state('zoomed')  # zoomed
        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        self.root.minsize(self.wSize, self.hSize)

        # TTk Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", foreground=self.colorList[10], fieldbackground=self.colorList[13], background=self.colorList[9])
        style.configure("Treeview", fieldbackground=self.colorList[17], background=self.colorList[17], foreground=self.colorList[18])
        style.map('Treeview', background=[('selected', self.colorList[19])], foreground=[('selected', self.colorList[20])])

        self.root.update()
        self.mainW = self.root.winfo_width()
        self.mainH = self.root.winfo_height()
        self.CallCommonVar(21)

        # Detail Frame
        self.detailFrame = Frame(self.root, bg=self.colorList[2])
        self.detailFrame.place(x=self.dFbFstF_x, y=self.dF_y, width=self.dFbF_w, height=self.dF_h)

        y_space = int(self.formset_yInF)  # 30 for 20 fields limit 40 for 15 fields limit
        self.dF_ent_w = 490
        self.dF_ent_x = 300

        y_ = 20
        self.settingFile = StringVar()
        settingFrom_list = [f for f in os.listdir(self.setting_folder) if os.path.isfile(os.path.join(self.setting_folder, f)) and not f.endswith('.fl') and not f.endswith('.pn') and not f.endswith('.sv') and f != "Default"]
        settingFrom_list.sort(reverse=True)
        if default_setting_selected != None:
            self.settingFile.set(default_setting_selected)
        else:
            self.settingFile.set(settingFrom_list[-1])
        lbl_set = Label(self.detailFrame, text='Setting', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_set.place(x=10, y=y_)
        cmb_set = AutocompleteCombobox(self.detailFrame, values=settingFrom_list, textvariable=self.settingFile, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_set.set_completion_list(settingFrom_list)
        cmb_set.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_set)
        cmb_set.place(x=self.dF_ent_x - 200, y=y_, width=self.dF_ent_w + 200)
        cmb_set.bind("<<ComboboxSelected>>", self.SelectSetting)

        y_ += y_space
        separator = ttk.Separator(self.detailFrame, orient='horizontal')
        separator.place(x=10, y=y_, width=self.dFbF_w - 20)

        # Button Frame
        self.buttonFrame = Frame(self.root, bg=self.colorList[3])
        self.buttonFrame.place(x=self.dFbFstF_x, y=self.bF_y + 1, width=self.dFbF_w, height=self.bF_h)

        self.bF_btn_w = int(self.dFbF_w/4) + 1
        self.bF_btn_h = self.bF_h
        self.bf_btn_x = 0
        self.bF_btn_y = 0

        btn_add = Button(self.buttonFrame, command=self.Save, justify=LEFT, text='Save', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_add.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        btn_update = Button(self.buttonFrame, command=self.Refresh, justify=LEFT, text='Refresh', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_update.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        btn_delete = Button(self.buttonFrame, command=self.Clear, justify=LEFT, text='Clear', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_delete.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        btn_clear = Button(self.buttonFrame, command=self.SetDefault, justify=LEFT, text='Default', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_clear.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w

        # Status Frame
        self.statusFrame = Frame(self.root, bg=self.colorList[2])
        self.statusFrame.place(x=self.dFbFstF_x, y=self.stF_y + 2, width=self.stF_w, height=self.stF_h)

        self.lbl_status = Label(self.statusFrame, text='Status:', anchor=W, justify=LEFT, font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        self.lbl_status.place(x=0, y=0, width=self.stF_w, height=self.stF_h)

        # After UI Creating
        self.SelectSetting('e')
        self.Refresh()

        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu = Menu(fileMenu, background=self.colorList[2])
        fileMenu.add_separator()
        fileMenu.add_command(label="Save", command=self.Save)
        fileMenu.add_command(label="Refresh", command=self.Refresh)
        fileMenu.add_command(label="Clear", command=self.Clear)
        fileMenu.add_command(label="Reset To Default", command=self.SetDefault)
        fileMenu.add_separator()
        fileMenu.add_command(label="Reset All Settings To Default", command=self.SetAllDefault)
        fileMenu.add_separator()
        fileMenu.add_command(label="Backup Settings", command=self.Backup)
        fileMenu.add_command(label="Restore Settings", command=self.Restore)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=0, command=self.root.destroy)
        menubar.add_command(label="x", underline=0, command=self.root.destroy)
        def minmax():
            self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
            self.root.attributes("-topmost", False)
        menubar.add_command(label="⬜", underline=0, command=lambda: minmax())
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)

        moreMenu = Menu(menubar)
        moreMenu = Menu(moreMenu, background=self.colorList[2])
        moreMenu.add_separator()
        moreMenu.add_command(label="Refresh Common Variable", command=lambda: self.CallCommonVar(1))
        moreMenu.add_separator()
        def rT(s):
            if s == 1:
                self.cmnset_refT = 'True'
            elif s == 0:
                self.cmnset_refT = 'False'
        moreMenu.add_command(label="Enable Refresh Thread", command=lambda: rT(1))
        moreMenu.add_command(label="Disable Refresh Thread", command=lambda: rT(0))
        menubar.add_cascade(label="More", underline=0, menu=moreMenu)

        menubar.add_cascade(label="Refresh", underline=0, command=lambda: self.Refresh_(thread_=0))
        self.RefreshT('1')

    def Save(self, temp=False):
        selectedSet = self.settingFile.get()
        if selectedSet.endswith('.ls'):
            ls = self.listbox_ls.get(0, self.listbox_ls.size())
            if temp:
                f = open(f'{self.temp_folder}\\{selectedSet}', 'w')
            else:
                f = open(f'{self.setting_folder}\\{selectedSet}', 'w')
            ls = [x.strip('\n').rstrip(' ')+"\n" for x in ls]
            ls = [i for i in ls if i]
            f.writelines(ls)

        elif selectedSet.endswith('.pg'):
            self.DATA = []
            self.DATAFORSAVE = []
            f = open(f"{self.setting_folder}\\{selectedSet.replace('.pg', '')}.sv", 'r')
            settings = f.readlines()
            f.close()
            f = open(f"{self.setting_folder}\\{selectedSet.replace('.pg', '')}.pn", 'r')
            pn = f.readlines()
            f.close()
            count = 0
            for set_ in settings:
                id_, data = set_.strip('\n').split(':')
                if self.var_cmbPN.get() == id_:
                    field_ = self.SetField_[count]
                    name__ = data.split('.')
                    for name_ in name__:
                        if field_.startswith("combo"):
                            cmb_d = self.SetVar[count].get()
                            self.DATAFORSAVE.append(cmb_d)

                        elif field_.startswith("font"):
                            font_d = self.SetVar[count].get()
                            self.DATAFORSAVE.append(font_d)

                        elif field_.startswith("text"):
                            if name_.startswith('File+'):
                                name, line = str(name_).split('+')
                                ent_d = f'File+{line}+{self.SetVar[count].get()}'
                            else:
                                ent_d = self.SetVar[count].get()
                            self.DATAFORSAVE.append(ent_d)

                        elif field_.startswith("button"):
                            self.DATAFORSAVE.append('button')

                        elif field_.startswith("color"):
                            ent_d = self.SetVar[count].get()
                            self.DATAFORSAVE.append(ent_d)

                        elif field_.startswith("aofoT"):
                            if name_.startswith('File+'):
                                name, line = str(name_).split('+')
                                ent_d = f'File+{line}+{self.SetVar[count].get()}'
                            else:
                                ent_d = self.SetVar[count].get()
                            self.DATAFORSAVE.append(ent_d)

                        elif field_.startswith("aofiT"):
                            if name_.startswith('File+'):
                                name, line = str(name_).split('+')
                                ent_d = f'File+{line}+{self.SetVar[count].get()}'
                            else:
                                ent_d = self.SetVar[count].get()
                            self.DATAFORSAVE.append(ent_d)

                        elif field_.startswith("no"):
                            ent_d = self.SetVar[count].get()
                            self.DATAFORSAVE.append(ent_d)

                        elif field_.startswith("list"):
                            ls = self.SetFields[count].get(0, self.SetFields[count].size())
                            ls = [x.strip('\n').rstrip(' ') for x in ls]
                            ls = [i for i in ls if i]
                            a = '['
                            for i in ls:
                                a += str(i) + ','
                            a = a.rstrip(',')
                            a += ']'
                            lis_d = a
                            self.DATAFORSAVE.append(lis_d)

                        elif field_.startswith("date"):
                            ent_d = self.SetVar[count].get()
                            self.DATAFORSAVE.append(ent_d)

                        elif field_.startswith("attachment"):
                            pass

                        count += 1

            count = 0
            for set_ in settings:
                id_, data = set_.strip('\n').split(':')
                if self.var_cmbPN.get() == id_:
                    name__ = data.split('.')
                    a = self.DATAFORSAVE
                    name_new = ''
                    c = 0
                    for i in a:
                        if i.startswith('File+'):
                            name, line, data = str(i).split('+')
                            f = open(f'{self.setting_folder}\\File.fl', 'r')
                            fd = f.readlines()
                            f.close()
                            new_fd = []
                            for i in range(len(fd)):
                                if int(i) == int(line) - 1:
                                    new_fd.append(f'{data}')
                                else:
                                    new_fd.append(f'{fd[int(i)]}')
                            if temp:
                                f = open(f'{self.temp_folder}\\File.fl', 'w')
                            else:
                                f = open(f'{self.setting_folder}\\File.fl', 'w')
                            f.writelines(new_fd)
                            f.close()
                            name_new += str(name__[c]) + '.'
                        else:
                            name_new += str(i) + '.'
                        c += 1
                    name_new = name_new.rstrip('.')
                    count += 1
                    self.DATA.append(f"{id_}:{name_new}\n")
    
                    f = open(f"{self.setting_folder}\\{selectedSet.replace('.pg', '')}.sv", 'r')
                    fd = f.readlines()
                    f.close()
                    c = 0
                    s = 0
                    sta = 0
                    for i in fd:
                        if i.startswith(id_):
                            s = c
                            sta = 1
                        c += 1
                    if sta == 0:
                        f = open(f"{self.setting_folder}\\{selectedSet.replace('.pg', '')}.sv", 'a')
                        f.writelines(self.DATA)
                        f.close()
                    elif sta == 1:
                        fd[s] = self.DATA[0]
                        if temp:
                            f = open(f"{self.temp_folder}\\{selectedSet.replace('.pg', '')}.sv", 'w')
                        else:
                            f = open(f"{self.setting_folder}\\{selectedSet.replace('.pg', '')}.sv", 'w')
                        f.writelines(fd)
                        f.close()

        else:
            self.DATA = []
            self.DATAFORSAVE = []
            f = open(f'{self.setting_folder}\\{selectedSet}', 'r')
            settings = f.readlines()
            f.close()
            count = 0
            for set_ in settings:
                id_, data = set_.strip('\n').split(':')
                name_, field_, condition_ = data.split('.')

                if field_.startswith("combo"):
                    cmb_d = self.SetVar[count].get()
                    self.DATAFORSAVE.append(cmb_d)

                elif field_.startswith("font"):
                    font_d = self.SetVar[count].get()
                    self.DATAFORSAVE.append(font_d)

                elif field_.startswith("text"):
                    if name_.startswith('File+'):
                        name, line = str(name_).split('+')
                        ent_d = f'File+{line}+{self.SetVar[count].get()}'
                    else:
                        ent_d = self.SetVar[count].get()
                    self.DATAFORSAVE.append(ent_d)

                elif field_.startswith("button"):
                    self.DATAFORSAVE.append('button')

                elif field_.startswith("color"):
                    ent_d = self.SetVar[count].get()
                    self.DATAFORSAVE.append(ent_d)

                elif field_.startswith("aofoT"):
                    if name_.startswith('File+'):
                        name, line = str(name_).split('+')
                        ent_d = f'File+{line}+{self.SetVar[count].get()}'
                    else:
                        ent_d = self.SetVar[count].get()
                    self.DATAFORSAVE.append(ent_d)

                elif field_.startswith("aofiT"):
                    if name_.startswith('File+'):
                        name, line = str(name_).split('+')
                        ent_d = f'File+{line}+{self.SetVar[count].get()}'
                    else:
                        ent_d = self.SetVar[count].get()
                    self.DATAFORSAVE.append(ent_d)

                elif field_.startswith("no"):
                    ent_d = self.SetVar[count].get()
                    self.DATAFORSAVE.append(ent_d)

                elif field_.startswith("list"):
                    ls = self.SetFields[count].get(0, self.SetFields[count].size())
                    ls = [x.strip('\n').rstrip(' ') for x in ls]
                    ls = [i for i in ls if i]
                    a = '['
                    for i in ls:
                        a += str(i) + ','
                    a = a.rstrip(',')
                    a += ']'
                    lis_d = a
                    self.DATAFORSAVE.append(lis_d)

                elif field_.startswith("date"):
                    ent_d = self.SetVar[count].get()
                    self.DATAFORSAVE.append(ent_d)

                elif field_.startswith("attachment"):
                    pass

                count += 1

            count = 0
            for set_ in settings:
                id_, data = set_.strip('\n').split(':')
                name_, field_, condition_ = data.split('.')
                name_new = self.DATAFORSAVE[count]
                count += 1
                a = '\n'
                if name_.startswith('File+'):
                    name, line, data = str(name_new).split('+')
                    f = open(f'{self.setting_folder}\\File.fl', 'r')
                    fd = f.readlines()
                    f.close()
                    new_fd = []
                    data = data.rstrip('\n')
                    data += '\n'
                    for i in range(len(fd)):
                        if int(i) == int(line) - 1:
                            new_fd.append(f'{data}')
                        else:
                            new_fd.append(f'{fd[int(i)]}')
                    if temp:
                        f = open(f'{self.temp_folder}\\File.fl', 'w')
                    else:
                        f = open(f'{self.setting_folder}\\File.fl', 'w')
                    f.writelines(new_fd)
                    f.close()
                    self.DATA.append(f"{id_}:{name_}.{field_}.{condition_.rstrip(a)}\n")
                else:
                    self.DATA.append(f"{id_}:{name_new}.{field_}.{condition_.rstrip(a)}\n")

            if temp:
                f = open(f'{self.temp_folder}\\{selectedSet}', 'w')
            else:
                f = open(f'{self.setting_folder}\\{selectedSet}', 'w')
            f.writelines(self.DATA)

        self.lbl_status.config(text='Setting Saved: Successfully')

    def Refresh(self):
        self.Refresh_(0)

        selectedSet = self.settingFile.get()
        if selectedSet.endswith('.ls'):
            f = open(f'{self.setting_folder}\\{selectedSet}', 'r')
            ls = f.readlines()
            self.listbox_ls.delete(0, END)
            for ls_ in ls:
                if ls_.strip('\n') != '' and ls_.strip('\t') != '':
                    self.listbox_ls.insert(END, ls_)
            f.close()

        elif selectedSet.endswith('.pg'):
            f = open(f"{self.setting_folder}\\{selectedSet.replace('.pg', '')}.sv", 'r')
            settings = f.readlines()
            f.close()
            for set_ in settings:
                count = 0
                id_, data = set_.strip('\n').split(':')
                if self.var_cmbPN.get() == id_:
                    field_ = self.SetField_[count]
                    name_ = data.split('.')
                    for name__ in name_:
                        if name__.startswith('File+'):
                            name__ = name__.rstrip('\n')
                            name__, line = str(name__).split('+')
                            f = open(f'{self.setting_folder}\\File.fl', 'r')
                            fd = f.readlines()
                            f.close()
                            name__ = fd[int(line) - 1]

                        if field_.startswith("combo"):
                            self.SetVar[count].set(name__)
                            self.SetFields[count].set(name__)

                        elif field_.startswith("font"):
                            self.SetVar[count].set(name__)
                            self.SetFields[count].set(name__)

                        elif field_.startswith("text"):
                            self.SetVar[count].set(name__)

                        elif field_.startswith("button"):
                            pass

                        elif field_.startswith("color"):
                            self.SetVar[count].set(name__)
                            try:
                                self.SetFields[count][1].config(fg=name__)
                            except:
                                pass

                        elif field_.startswith("aofoT"):
                            self.SetVar[count].set(name__)

                        elif field_.startswith("aofiT"):
                            self.SetVar[count].set(name__)

                        elif field_.startswith("no"):
                            self.SetVar[count].set(name__)

                        elif field_.startswith("list"):
                            lis_d = str(name__)
                            lis_d = lis_d.replace("[", '')
                            lis_d = lis_d.replace("]", '')
                            lis_d = lis_d.split(',')

                            self.SetFields[count].delete(0, END)
                            for ls_ in lis_d:
                                if ls_ != '':
                                    self.SetFields[count].insert(END, ls_)

                        elif field_.startswith("date"):
                            self.SetVar[count].set(name__)

                        elif field_.startswith("attachment"):
                            pass

                        count += 1

        else:
            f = open(f'{self.setting_folder}\\{selectedSet}', 'r')
            settings = f.readlines()
            f.close()
            count = 0
            for set_ in settings:
                id_, data = set_.strip('\n').split(':')
                name_, field_, condition_ = data.split('.')

                if name_.startswith('File+'):
                    name_ = name_.rstrip('\n')
                    name_,line = str(name_).split('+')
                    f = open(f'{self.setting_folder}\\File.fl', 'r')
                    fd = f.readlines()
                    f.close()
                    name_ = fd[int(line) - 1]

                if field_.startswith("combo"):
                    self.SetVar[count].set(name_)
                    self.SetFields[count].set(name_)

                elif field_.startswith("font"):
                    self.SetVar[count].set(name_)
                    self.SetFields[count].set(name_)

                elif field_.startswith("text"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("button"):
                    pass

                elif field_.startswith("color"):
                    self.SetVar[count].set(name_)
                    try:
                        self.SetFields[count][1].config(fg=name_)
                    except:
                        pass

                elif field_.startswith("aofoT"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("aofiT"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("no"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("list"):
                    lis_d = str(name_)
                    lis_d = lis_d.replace("[", '')
                    lis_d = lis_d.replace("]", '')
                    lis_d = lis_d.split(',')

                    self.SetFields[count].delete(0, END)
                    for ls_ in lis_d:
                        if ls_ != '':
                            self.SetFields[count].insert(END, ls_)

                elif field_.startswith("date"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("attachment"):
                    pass

                count += 1

    def Clear(self):
        self.Refresh_(0)

        selectedSet = self.settingFile.get()
        if selectedSet.endswith('.ls'):
            f = open(f'{self.setting_folder}\\{selectedSet}', 'r')
            ls = f.readlines()
            self.listbox_ls.delete(0, END)
            for ls_ in ls:
                if ls_.strip('\n') != '' and ls_.strip('\t') != '':
                    self.listbox_ls.insert(END, ls_)
            f.close()

        elif selectedSet.endswith('.pg'):
            f = open(f"{self.setting_folder}\\{selectedSet.replace('.pg', '')}.sv", 'r')
            settings = f.readlines()
            f.close()
            count = 0
            for set_ in settings:
                id_, data = set_.strip('\n').split(':')
                if self.var_cmbPN.get() == id_:
                    field_ = self.SetField_[count]
                    name__ = data.split(',')
                    for name_ in name__:
                        name_ = ''
                        if field_.startswith("combo"):
                            self.SetVar[count].set(name_)

                        elif field_.startswith("font"):
                            self.SetVar[count].set(name_)

                        elif field_.startswith("text"):
                            self.SetVar[count].set(name_)

                        elif field_.startswith("button"):
                            pass

                        elif field_.startswith("color"):
                            self.SetVar[count].set(name_)

                        elif field_.startswith("aofoT"):
                            self.SetVar[count].set(name_)

                        elif field_.startswith("aofiT"):
                            self.SetVar[count].set(name_)

                        elif field_.startswith("no"):
                            self.SetVar[count].set(name_)

                        elif field_.startswith("list"):
                            self.SetFields[count].delete(0, END)

                        elif field_.startswith("date"):
                            self.SetVar[count].set(name_)

                        elif field_.startswith("attachment"):
                            pass

                        count += 1

        else:
            f = open(f'{self.setting_folder}\\{selectedSet}', 'r')
            settings = f.readlines()
            f.close()
            count = 0
            for set_ in settings:
                id_, data = set_.strip('\n').split(':')
                name_, field_, condition_ = data.split('.')
                name_ = ''
                if field_.startswith("combo"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("font"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("text"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("button"):
                    pass

                elif field_.startswith("color"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("aofoT"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("aofiT"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("no"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("list"):
                    self.SetFields[count].delete(0, END)

                elif field_.startswith("date"):
                    self.SetVar[count].set(name_)

                elif field_.startswith("attachment"):
                    pass

                count += 1

    def SetDefault(self):
        selectedSet = self.settingFile.get()

        f = open(f'{self.setting_folder}\\Default\\{selectedSet}', 'r')
        fd = f.read()
        f.close()
        f = open(f'{self.setting_folder}\\{selectedSet}', 'w')
        f.write(fd)
        f.close()

        try:
            self.Refresh()
        except:
            pass

    def SetAllDefault(self):
        lsd = os.listdir(f'{self.setting_folder}')
        lsd = [x for x in lsd if os.path.isfile(os.path.join(self.setting_folder, x))]
        for i in lsd:
            if os.path.exists(f'{self.setting_folder}\\{i}'):
                os.remove(f'{self.setting_folder}\\{i}')

        source_folder = rf"{self.setting_folder}\\Default\\"
        destination_folder = rf"{self.setting_folder}\\"

        # fetch all files
        for file_name in os.listdir(source_folder):
            # construct full file path
            source = source_folder + file_name
            destination = destination_folder + file_name
            # copy only files
            if os.path.isfile(source):
                shutil.copy(source, destination)
        try:
            self.Refresh()
        except:
            pass

    def Backup(self):
        pass

    def Restore(self):
        pass

    def SelectSetting(self, e):
        # Remove All Child Widget From Sub Form
        try:
            for widgets in self.selectSetFrame.winfo_children():
                widgets.destroy()
        except:pass

        # Remove Sub Form
        try:
            self.selectSetFrame.destroy()
        except:pass

        # Clear ListBox
        try:
            self.listbox_ls.delete(0, END)
            self.listbox_ls.destroy()
        except:pass

        # Create Sub Form
        self.selectSetFrame = Frame(self.root, bg=self.colorList[2])
        self.selectSetFrame.place(x=self.dFbFstF_x, y=self.dF_y + 70, width=self.dFbF_w, height=self.dF_h - 70)
        selectedSet = self.settingFile.get()

        if selectedSet.endswith('.ls'):
            var_ls = StringVar()
            y_space = int(self.formset_yInF)  # 30 for 20 fields limit 40 for 15 fields limit

            y_ = 0
            lbl_ls = Label(self.selectSetFrame, text=f'Add {selectedSet.replace(".ls", "")}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
            lbl_ls.place(x=10, y=y_)
            ent_ls = Entry(self.selectSetFrame, textvariable=var_ls, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
            ent_ls.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 100 - 2)

            def Add_ls():
                ls = ent_ls.get()
                if ls != "" and ls.strip('\t') != '':
                    self.listbox_ls.insert(END, ls)
                    ent_ls.delete(0, END)

            def Del_ls():
                try:
                    ls_index = self.listbox_ls.curselection()[0]
                    self.listbox_ls.delete(ls_index)
                except:pass

            btn_ls_add = Button(self.selectSetFrame, command=Add_ls, justify=LEFT, text='Add', font=(self.formset_mainF, 13), bd=1, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
            btn_ls_add.place(x=self.dF_ent_x + self.dF_ent_w - 99, y=y_, width=50, height=self.formset_fieldH)
            btn_ls_del = Button(self.selectSetFrame, command=Del_ls, justify=LEFT, text='Delete', font=(self.formset_mainF, 13), bd=1, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
            btn_ls_del.place(x=self.dF_ent_x + self.dF_ent_w - 49, y=y_, width=50, height=self.formset_fieldH)

            y_ += y_space
            self.listbox_ls = Listbox(self.selectSetFrame, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
            self.listbox_ls.place(x=10, y=y_, width=self.dFbF_w - 40, height=self.dF_h - y_ - 70 - 10)
            scrollbar_ls = Scrollbar(self.selectSetFrame)
            scrollbar_ls.place(x=self.dFbF_w - 30, y=y_, width=20, height=self.dF_h - y_ - 70 - 10)

            self.listbox_ls.config(yscrollcommand=scrollbar_ls.set)
            scrollbar_ls.config(command=self.listbox_ls.yview)

        elif selectedSet.endswith('.pg'):
            self.var_cmbPN = StringVar()
            y_space = int(self.formset_yInF)  # 30 for 20 fields limit 40 for 15 fields limit
            f = open(f"{self.setting_folder}\\{selectedSet.replace('.pg', '')}.pn", 'r')
            cmb__list = f.readlines()
            cmb__list = [x.rstrip('\n') for x in cmb__list]
            f.close()

            y_ = 0
            lbl_ = Label(self.selectSetFrame, text=f'{selectedSet.replace(".pg", "")}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
            lbl_.place(x=10, y=y_)
            cmb_PN = AutocompleteCombobox(self.selectSetFrame, values=cmb__list, textvariable=self.var_cmbPN, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
            cmb_PN.set_completion_list(cmb__list)
            cmb_PN.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_PN)
            cmb_PN.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)
            cmb_PN.current(0)

            y_ += y_space
            separator = ttk.Separator(self.selectSetFrame, orient='horizontal')
            separator.place(x=10, y=y_, width=self.dFbF_w - 20)

            self.selectSetFrame2 = Frame(self.selectSetFrame, bg=self.colorList[2])
            self.selectSetFrame2.place(x=self.dFbFstF_x, y=self.dF_y + 35, width=self.dFbF_w, height=self.dF_h - 105)

            def SelectSetting2(event):
                try:
                    self.selectSetFrame2Demo.destroy()
                except: pass

                self.selectSetFrame2Demo = Frame(self.selectSetFrame2, bg=self.colorList[2])
                self.selectSetFrame2Demo.place(x=0, y=0, width=self.dFbF_w, height=self.dF_h - 105)

                self.canvasRP2 = Canvas(self.selectSetFrame2Demo, bd=0, highlightthickness=0, bg=self.colorList[2], width=300, height=300, scrollregion=(0, 0, 500, 500))
                self.vbarButtonFrame2 = Scrollbar(self.selectSetFrame2Demo, orient=VERTICAL)
                self.vbarButtonFrame2.place(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h - 105 + 24)
                self.vbarButtonFrame2.config(command=self.canvasRP2.yview)
                self.canvasRP2.config(width=300, height=300)
                self.canvasRP2.config(yscrollcommand=self.vbarButtonFrame2.set)
                self.canvasRP2.pack(side=LEFT, expand=True, fill=BOTH)

                self.canvasRP2.bind('<Configure>', lambda e: self.canvasRP2.configure(scrollregion=self.canvasRP2.bbox('all')))
                self.selectSetFrameO2 = Frame(self.canvasRP2, bg=self.colorList[2])
                self.canvasRP2.create_window((0, 0), window=self.selectSetFrameO2, anchor="nw")

                try:
                    for i in self.SetFields:
                        i.destroy()
                except:
                    pass
                try:
                    for i in self.SetFields_:
                        i.destroy()
                except:
                    pass

                self.SetFields = []
                self.SetVar = []
                self.SetField_ = []

                f = open(f"{self.setting_folder}\\{selectedSet}", 'r')
                settings2 = f.readlines()
                f.close()
                count = 0
                y_space = int(self.formset_yInF)  # 30 for 20 fields limit 40 for 15 fields limit
                y_ = -30
                for set_ in settings2:
                    id_, data = set_.strip('\n').split(':')
                    field_, condition_ = data.split('.')

                    if field_.startswith("combo"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("combo")
                        field_ = str(field_)
                        if field_.startswith("comboFIF"):
                            field_ = field_.replace("comboFIF[", '')
                            field_ = field_.replace("]", '')
                            cmb_list = os.listdir(f"{self.setting_folder}\\{field_}")
                        elif field_.startswith("comboF"):
                            field_ = field_.replace("comboF[", '')
                            field_ = field_.replace("]", '')
                            f = open(f"{self.setting_folder}\\{field_}.ls", 'r')
                            cmb_list = f.readlines()
                            cmb_list = [x.rstrip('\\n') for x in cmb_list]
                            f.close()
                        elif field_.startswith("combo"):
                            field_ = field_.replace("combo[", '')
                            field_ = field_.replace("]", '')
                            field_ = field_.split(',')
                            cmb_list = field_

                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        cmb_ = AutocompleteCombobox(frm_, values=cmb_list, textvariable=var_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
                        cmb_.set_completion_list(cmb_list)
                        cmb_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_)
                        cmb_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)
                        cmb_.current(0)
                        self.SetFields.append(cmb_)
                        self.SetVar.append(var_)

                    elif field_.startswith("font"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("font")
                        field_ = list(font.families())

                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        cmb_list = field_
                        cmb_ = AutocompleteCombobox(frm_, values=cmb_list, textvariable=var_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
                        cmb_.set_completion_list(cmb_list)
                        cmb_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_)
                        cmb_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)
                        cmb_.current(0)
                        self.SetFields.append(cmb_)
                        self.SetVar.append(var_)

                    elif field_.startswith("text"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("text")
                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)
                        self.SetFields.append(ent_)
                        self.SetVar.append(var_)

                    elif field_.startswith("button"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("button")
                        field_ = str(field_)
                        field_ = field_.replace("button[", '')
                        field_ = field_.replace("]", '')
                        field_ = field_.split('|')
                        field_ = field_[0:len(field_) - 1]

                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        btnC = len(field_)
                        btnW = self.dF_ent_w / btnC
                        btnX = self.dF_ent_x
                        for i in field_:
                            id_, func = i.split('+')
                            btn_ = Button(frm_, command=lambda: (self.Save(temp=True), exec(f'self.{func}'.replace('sseellff', 'self.'), {'self': self})), justify=LEFT, text=id_, font=self.formset_mainF, bd=1, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                            btn_.place(x=btnX, y=y_, width=btnW - 1, height=self.formset_fieldH)
                            btnX += btnW
                        self.SetFields.append('button')
                        self.SetVar.append('button')

                    elif field_.startswith("color"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("color")
                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 31)

                        def color_(c):
                            color_code = colorchooser.askcolor(parent=self.root, title="Choose color")
                            if color_code[1] != "" and color_code[1] is not None:
                                self.SetVar[c].set(color_code[1])
                                self.SetFields[c][0].update()
                                self.SetFields[c][1].config(fg=color_code[1])

                        btn_ = Button(frm_, command=lambda count=count: color_(count), justify=LEFT, text='🎨', font=('calibri', 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                        btn_.place(x=self.dF_ent_x + self.dF_ent_w - 30, y=y_, width=30, height=self.formset_fieldH)

                        self.SetFields.append([ent_, btn_])
                        self.SetVar.append(var_)

                    elif field_.startswith("aofoT"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("aofoT")
                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 30 - 1)
                        self.SetFields.append(ent_)
                        self.SetVar.append(var_)

                        def aof_(c):
                            folderName = filedialog.askdirectory(title='Select Folder')
                            if folderName != '':
                                self.SetVar[c].set(folderName)
                                self.SetFields[c].update()

                        btn_openFolder = Button(frm_, command=lambda count=count: aof_(count), justify=LEFT, text='1', font=('wingdings', 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                        btn_openFolder.place(x=self.dF_ent_x + self.dF_ent_w - 30, y=y_, width=30, height=self.formset_fieldH)

                    elif field_.startswith("aofiT"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("aofiT")
                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 30 - 1)
                        self.SetFields.append(ent_)
                        self.SetVar.append(var_)

                        def aof_(c):
                            folderName = filedialog.askdirectory(title='Select Folder')
                            if folderName != '':
                                self.SetVar[c].set(folderName)
                                self.SetFields[c].update()

                        btn_openFolder = Button(frm_, command=lambda count=count: aof_(count), justify=LEFT, text='1', font=('wingdings', 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                        btn_openFolder.place(x=self.dF_ent_x + self.dF_ent_w - 30, y=y_, width=30, height=self.formset_fieldH)

                    elif field_.startswith("no"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("no")
                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)
                        self.SetFields.append(ent_)
                        self.SetVar.append(var_)

                        def check_int_(event=None, c=0):
                            try:
                                int(self.SetVar[c].get())
                            except:
                                len1 = len(self.SetVar[c].get())
                                len1 = len1 - 1
                                self.SetVar[c].set(self.SetVar[c].get()[0:len1])
                                try:
                                    int(self.SetVar[c].get())
                                except:
                                    pass

                        ent_.bind("<KeyRelease>", lambda e, count=count: check_int_(e, count))
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)

                    elif field_.startswith("list"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space * 5)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("list")
                        field_ = str(field_)
                        field_ = field_.replace("list[", '')
                        field_ = field_.replace("]", '')
                        if field_ == 'text':
                            var_ = StringVar()
                            y_ = 1
                            lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                            lbl_.place(x=10, y=y_)
                            cmb_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                            cmb_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 100)
                        else:
                            f = open(f"{self.setting_folder}\\{field_}.pn", 'r')
                            cmb_list = f.readlines()
                            cmb_list = [x.rstrip('\n') for x in cmb_list]
                            f.close()
                            var_ = StringVar()
                            y_ = 1
                            lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                            lbl_.place(x=10, y=y_)
                            cmb_list = cmb_list
                            cmb_ = AutocompleteCombobox(frm_, values=cmb_list, textvariable=var_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
                            cmb_.set_completion_list(cmb_list)
                            cmb_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_)
                            cmb_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 100)
                            cmb_.current(0)

                        def Add_(c, cmb):
                            ls = cmb.get()
                            if ls != "" and ls.strip('\t') != '':
                                self.SetFields[c].insert(END, ls)
                                cmb.delete(0, END)

                        def Del_(c):
                            try:
                                ls_index = self.SetFields[c].curselection()[0]
                                self.SetFields[c].delete(ls_index)
                            except:
                                pass

                        btn_ = Button(frm_, command=lambda count=count, cmb_=cmb_: Add_(count, cmb_), justify=LEFT, text='Add', font=(self.formset_mainF, 13), bd=1, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                        btn_.place(x=self.dF_ent_x + self.dF_ent_w - 99, y=y_, width=50, height=self.formset_fieldH)
                        btn_ = Button(frm_, command=lambda count=count: Del_(count), justify=LEFT, text='Delete', font=(self.formset_mainF, 13), bd=1, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                        btn_.place(x=self.dF_ent_x + self.dF_ent_w - 49, y=y_, width=50, height=self.formset_fieldH)

                        var_ = StringVar()
                        y_ += y_space
                        listbox_ = Listbox(frm_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        listbox_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 10, height=55 + (y_space * 2))
                        scrollbar_ = Scrollbar(frm_)
                        scrollbar_.place(x=self.dF_ent_x + self.dF_ent_w - 10, y=y_, width=10, height=55 + (y_space * 2))
                        listbox_.config(yscrollcommand=scrollbar_.set)
                        scrollbar_.config(command=listbox_.yview)
                        self.SetFields.append(listbox_)
                        self.SetVar.append(var_)
                        y_ += y_space
                        y_ += y_space
                        y_ += y_space

                    elif field_.startswith("date"):
                        frm_ = Frame(self.selectSetFrameO2, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                        frm_.pack(fill=BOTH, expand=True)

                        self.SetField_.append("date")
                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        ent_ = DateEntry(frm_, textvariable=var_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12], justify=CENTER, date_pattern='dd-mm-y')
                        ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 10)
                        self.SetFields.append(ent_)
                        self.SetVar.append(var_)

                        def cls_(c):
                            self.SetVar[c].set("")
                            self.SetFields[c].update()

                        btn_ = Button(frm_, command=lambda count=count: cls_(count), justify=LEFT, text='-', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                        btn_.place(x=self.dF_ent_x + self.dF_ent_w - 10, y=y_, width=10, height=self.formset_fieldH)

                    elif field_.startswith("attachment"):
                        pass

                    count += 1
                self.Refresh()
            cmb_PN.bind("<<ComboboxSelected>>", SelectSetting2)
            SelectSetting2('e')

        else:
            self.canvasRP = Canvas(self.selectSetFrame, bd=0, highlightthickness=0, bg=self.colorList[2], width=300, height=300, scrollregion=(0, 0, 500, 500))
            self.vbarButtonFrame = Scrollbar(self.selectSetFrame, orient=VERTICAL)
            self.vbarButtonFrame.place(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h - 70 + 24)
            self.vbarButtonFrame.config(command=self.canvasRP.yview)
            self.canvasRP.config(width=300, height=300)
            self.canvasRP.config(yscrollcommand=self.vbarButtonFrame.set)
            self.canvasRP.pack(side=LEFT, expand=True, fill=BOTH)

            self.canvasRP.bind('<Configure>', lambda e: self.canvasRP.configure(scrollregion=self.canvasRP.bbox('all')))
            self.selectSetFrameO = Frame(self.canvasRP, bg=self.colorList[2])
            self.canvasRP.create_window((0, 0), window=self.selectSetFrameO, anchor="nw")

            try:
                for i in self.SetFields:
                    i.destroy()
            except: pass

            self.SetFields = []
            self.SetVar = []

            f = open(f'{self.setting_folder}\\{selectedSet}', 'r')
            settings = f.readlines()
            f.close()
            count = 0
            y_space = int(self.formset_yInF)  # 30 for 20 fields limit 40 for 15 fields limit
            for set_ in settings:
                id_, data = set_.strip('\n').split(':')
                name_, field_, condition_ = data.split('.')

                if field_.startswith("combo"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                    frm_.pack(fill=BOTH, expand=True)

                    field_ = str(field_)
                    if field_.startswith("comboFIF"):
                        field_ = field_.replace("comboFIF[", '')
                        field_ = field_.replace("]", '')
                        cmb_list = os.listdir(f"{self.setting_folder}\\{field_}")
                    elif field_.startswith("comboF"):
                        field_ = field_.replace("comboF[", '')
                        field_ = field_.replace("]", '')
                        f = open(f"{self.setting_folder}\\{field_}.ls", 'r')
                        cmb_list = f.readlines()
                        cmb_list = [x.rstrip('\\n') for x in cmb_list]
                        f.close()
                    elif field_.startswith("combo"):
                        field_ = field_.replace("combo[", '')
                        field_ = field_.replace("]", '')
                        field_ = field_.split(',')
                        cmb_list = field_

                    var_ = StringVar()
                    y_ = 1
                    lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    lbl_.place(x=10, y=y_)
                    cmb_ = AutocompleteCombobox(frm_, values=cmb_list, textvariable=var_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
                    cmb_.set_completion_list(cmb_list)
                    cmb_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_)
                    cmb_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)
                    cmb_.current(0)

                    self.SetFields.append(cmb_)
                    self.SetVar.append(var_)

                elif field_.startswith("font"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                    frm_.pack(fill=BOTH, expand=True)

                    field_ = list(font.families())

                    var_ = StringVar()
                    y_ = 1
                    lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    lbl_.place(x=10, y=y_)
                    cmb_list = field_
                    cmb_ = AutocompleteCombobox(frm_, values=cmb_list, textvariable=var_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
                    cmb_.set_completion_list(cmb_list)
                    cmb_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_)
                    cmb_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)
                    cmb_.current(0)

                    self.SetFields.append(cmb_)
                    self.SetVar.append(var_)

                elif field_.startswith("text"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                    frm_.pack(fill=BOTH, expand=True)
                    
                    var_ = StringVar()
                    y_ = 1
                    lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    lbl_.place(x=10, y=y_)
                    ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)
                    self.SetFields.append(ent_)
                    self.SetVar.append(var_)

                elif field_.startswith("button"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                    frm_.pack(fill=BOTH, expand=True)

                    field_ = str(field_)
                    field_ = field_.replace("button[", '')
                    field_ = field_.replace("]", '')
                    field_ = field_.split('|')
                    field_ = field_[0:len(field_) - 1]

                    y_ = 1
                    lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    lbl_.place(x=10, y=y_)
                    btnC = len(field_)
                    btnW = self.dF_ent_w / btnC
                    btnX = self.dF_ent_x
                    for i in field_:
                        id_, func = i.split('+')
                        btn_ = Button(frm_, command=lambda: (self.Save(temp=True), exec(f'self.{func}'.replace('sseellff', 'self.'), {'self': self})), justify=LEFT, text=id_, font=self.formset_mainF, bd=1, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                        btn_.place(x=btnX, y=y_, width=btnW - 1, height=self.formset_fieldH)
                        btnX += btnW
                    self.SetFields.append('button')
                    self.SetVar.append('button')

                elif field_.startswith("color"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                    frm_.pack(fill=BOTH, expand=True)

                    var_ = StringVar()
                    y_ = 1
                    lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    lbl_.place(x=10, y=y_)
                    ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 31)

                    def color_(c):
                        color_code = colorchooser.askcolor(parent=self.root, title="Choose color")
                        if color_code[1] != "" and color_code[1] is not None:
                            self.SetVar[c].set(color_code[1])
                            self.SetFields[c][0].update()
                            self.SetFields[c][1].config(fg=color_code[1])

                    btn_ = Button(frm_, command=lambda count=count: color_(count), justify=LEFT, text='🎨', font=('calibri', 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                    btn_.place(x=self.dF_ent_x + self.dF_ent_w - 30, y=y_, width=30, height=self.formset_fieldH)

                    self.SetFields.append([ent_, btn_])
                    self.SetVar.append(var_)

                elif field_.startswith("aofoT"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                    frm_.pack(fill=BOTH, expand=True)
                    
                    var_ = StringVar()
                    y_ = 1
                    lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    lbl_.place(x=10, y=y_)
                    ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 30 - 1)
                    self.SetFields.append(ent_)
                    self.SetVar.append(var_)
                    def aof_(c):
                        folderName = filedialog.askdirectory(title='Select Folder')
                        if folderName != '':
                            self.SetVar[c].set(folderName)
                            self.SetFields[c].update()
                    btn_openFolder = Button(frm_, command=lambda count=count: aof_(count), justify=LEFT, text='1', font=('wingdings', 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                    btn_openFolder.place(x=self.dF_ent_x + self.dF_ent_w-30, y=y_, width=30, height=self.formset_fieldH)

                elif field_.startswith("aofiT"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                    frm_.pack(fill=BOTH, expand=True)
                    
                    var_ = StringVar()
                    y_ = 1
                    lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    lbl_.place(x=10, y=y_)
                    ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 30 - 1)
                    self.SetFields.append(ent_)
                    self.SetVar.append(var_)
                    def aof_(c):
                        folderName = filedialog.askopenfilename(title='Select File')
                        if folderName != '':
                            self.SetVar[c].set(folderName)
                            self.SetFields[c].update()
                    btn_openFolder = Button(frm_, command=lambda count=count: aof_(count), justify=LEFT, text='1', font=('wingdings', 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                    btn_openFolder.place(x=self.dF_ent_x + self.dF_ent_w-30, y=y_, width=30, height=self.formset_fieldH)

                elif field_.startswith("no"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                    frm_.pack(fill=BOTH, expand=True)

                    var_ = StringVar()
                    y_ = 1
                    lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    lbl_.place(x=10, y=y_)
                    ent_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w)
                    self.SetFields.append(ent_)
                    self.SetVar.append(var_)

                    def check_int_(event=None, c=0):
                        try:
                            int(self.SetVar[c].get())
                        except:
                            len1 = len(self.SetVar[c].get())
                            len1 = len1 - 1
                            self.SetVar[c].set(self.SetVar[c].get()[0:len1])
                            try:
                                int(self.SetVar[c].get())
                            except:
                                pass
                    ent_.bind("<KeyRelease>", lambda e, count=count: check_int_(e, count))

                elif field_.startswith("list"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space * 5)
                    frm_.pack(fill=BOTH, expand=True)

                    field_ = str(field_)
                    field_ = field_.replace("list[", '')
                    field_ = field_.replace("]", '')
                    if field_ == 'text':
                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        cmb_ = Entry(frm_, border=0, textvariable=var_, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        cmb_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 100)
                    else:
                        f = open(f"{self.setting_folder}\\{field_}.pn", 'r')
                        cmb_list = f.readlines()
                        cmb_list = [x.rstrip('\n') for x in cmb_list]
                        f.close()
                        var_ = StringVar()
                        y_ = 1
                        lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                        lbl_.place(x=10, y=y_)
                        cmb_list = cmb_list
                        cmb_ = AutocompleteCombobox(frm_, values=cmb_list, textvariable=var_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
                        cmb_.set_completion_list(cmb_list)
                        cmb_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_)
                        cmb_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 100)
                        cmb_.current(0)

                    def Add_(c, cmb):
                        ls = cmb.get()
                        if ls != "" and ls.strip('\t') != '':
                            self.SetFields[c].insert(END, ls)
                            cmb.delete(0, END)
                    def Del_(c):
                        try:
                            ls_index = self.SetFields[c].curselection()[0]
                            self.SetFields[c].delete(ls_index)
                        except:pass
                    btn_ = Button(frm_, command=lambda count=count, cmb_=cmb_: Add_(count, cmb_), justify=LEFT, text='Add', font=(self.formset_mainF, 13), bd=1, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                    btn_.place(x=self.dF_ent_x + self.dF_ent_w - 99, y=y_, width=50, height=self.formset_fieldH)
                    btn_ = Button(frm_, command=lambda count=count: Del_(count), justify=LEFT, text='Delete', font=(self.formset_mainF, 13), bd=1, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                    btn_.place(x=self.dF_ent_x + self.dF_ent_w - 49, y=y_, width=50, height=self.formset_fieldH)

                    var_ = StringVar()
                    y_ += y_space
                    listbox_ = Listbox(frm_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    listbox_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 10, height=55 + (y_space * 2))
                    scrollbar_ = Scrollbar(frm_)
                    scrollbar_.place(x=self.dF_ent_x + self.dF_ent_w - 10, y=y_, width=10, height=55 + (y_space * 2))
                    listbox_.config(yscrollcommand=scrollbar_.set)
                    scrollbar_.config(command=listbox_.yview)
                    self.SetFields.append(listbox_)
                    self.SetVar.append(var_)
                    y_ += y_space
                    y_ += y_space
                    y_ += y_space

                elif field_.startswith("date"):
                    frm_ = Frame(self.selectSetFrameO, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
                    frm_.pack(fill=BOTH, expand=True)

                    var_ = StringVar()
                    y_ = 1
                    lbl_ = Label(frm_, text=f'{id_}', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
                    lbl_.place(x=10, y=y_)
                    ent_ = DateEntry(frm_, textvariable=var_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12], justify=CENTER, date_pattern='dd-mm-y')
                    ent_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 10)
                    self.SetFields.append(ent_)
                    self.SetVar.append(var_)
                    def cls_(c):
                        self.SetVar[c].set("")
                        self.SetFields[c].update()
                    btn_ = Button(frm_, command=lambda count=count: cls_(count), justify=LEFT, text='-', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                    btn_.place(x=self.dF_ent_x + self.dF_ent_w - 10, y=y_, width=10, height=self.formset_fieldH)

                elif field_.startswith("attachment"):
                    pass

                count += 1

        self.Refresh()

    def CallCommonVar(self, height_):
        # Frames Variables
        self.dFbFstF_x = 0
        self.dF_y = 1
        self.dFbF_w = 800
        self.bF_h = 30
        self.stF_h = 20
        self.dF_h = self.mainH - self.dF_y - self.bF_h - self.stF_h - height_ - 2
        self.bF_y = self.dF_y + self.dF_h
        self.stF_y = self.bF_y + self.bF_h
        self.stF_w = self.mainW

    def RefreshT(self, thread_):
        if thread_ == '1':
            x = threading.Thread(target=self.Refresh_, args=(1,))
            x.start()
        elif thread_ == '0':
            Log_Generator().addLog(f'[{self.mainName}] [Refresh] Thread Stopped')

    def Refresh_(self, thread_):
        self.root.update()
        self.mainW = self.root.winfo_width()
        self.mainH = self.root.winfo_height()

        if self.old_mainW != self.mainW or self.old_mainH != self.mainH:
            self.old_mainW = self.mainW
            self.old_mainH = self.mainH

            if thread_ == 0:
                Log_Generator().addLog(f'[{self.mainName}] [After Refresh]\t[Root Width] {self.mainW}, [Root Height] {self.mainH}')
                self.CallCommonVar(1)

            if thread_ == 1:
                self.CallCommonVar(1)

            self.buttonFrame.place_forget()
            self.buttonFrame.place_configure(x=self.dFbFstF_x, y=self.bF_y + 1, width=self.dFbF_w, height=self.bF_h)

            # Detail Frame
            self.detailFrame.place_forget()
            self.detailFrame.place_configure(x=self.dFbFstF_x, y=self.dF_y, width=self.dFbF_w, height=self.dF_h)

            try:
                self.selectSetFrame.place_forget()
                self.selectSetFrame.place_configure(x=self.dFbFstF_x, y=self.dF_y + 70, width=self.dFbF_w, height=self.dF_h - 70)

                self.vbarButtonFrame.place_forget()
                self.vbarButtonFrame.place(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h - 70 + 24)
            except: pass

            try:
                self.selectSetFrame2.place_forget()
                self.selectSetFrame2.place(x=self.dFbFstF_x, y=self.dF_y + 35, width=self.dFbF_w, height=self.dF_h - 105)
            except: pass

            try:
                self.selectSetFrame2Demo.place_forget()
                self.selectSetFrame2Demo.place_configure(x=0, y=0, width=self.dFbF_w, height=self.dF_h - 105)

                self.vbarButtonFrame2.place_forget()
                self.vbarButtonFrame2.place_configure(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h - 105 + 24)
            except: pass

            # Status Frame
            self.statusFrame.place_forget()
            self.statusFrame.place(x=self.dFbFstF_x, y=self.stF_y + 2, width=self.stF_w, height=self.stF_h)
            self.lbl_status.place_forget()
            self.lbl_status.place_configure(x=0, y=0, width=self.stF_w, height=self.stF_h)

        if thread_ == 1:
            if self.cmnset_refT == 'True':
                self.root.after(int(self.cmnset_refA), lambda: self.RefreshT('1'))
            elif self.cmnset_refT == 'False':
                self.root.after(int(self.cmnset_refA), lambda: self.RefreshT('0'))
        try:
            self.lbl_status.config(text='')
        except:
            pass

    def Reopen(self):
        selectedSet = self.settingFile.get()
        self.root.destroy()
        root = Toplevel()
        Setting(root,default_setting_selected=selectedSet)


if __name__ == '__main__':
    root = Tk()
    obj = Setting(root)
    root.mainloop()
    Log_Generator().closeLog()

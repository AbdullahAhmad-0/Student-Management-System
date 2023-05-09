from tkinter import *
from tkinter import ttk, messagebox
import threading
# import pymysql, sqlite3
import re, os

# import webbrowser  # For Opening Links

list_of_libFiles = os.listdir('Library_Files')
list_of_libFiles = [x for x in list_of_libFiles if x.endswith('_frm.py')]
list_of_libFiles.sort(reverse=True)

for i in list_of_libFiles:
    x = f"from Library_Files.{i.replace('.py','')} import {i.replace('_frm.py', '')}"
    exec(x)

from Library_Files.Top_Func import Func
from Library_Files.Log_Generator import Log_Generator
from Library_Files.FormRun import *


class Main(BeforeInIt, AllSettings, Func):
    wSize, hSize = 700, 550
    title = "Student Management System"
    mainName = title

    def __init__(self, wind) -> None:
        BeforeInIt.__init__(self)
        AllSettings.__init__(self)
        super().__init__()
        if Log_Generator().findLog():
            Log_Generator().startLog()
        else:
            Log_Generator().createLog()

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

        # Call Functions
        self.CallCommonVar(1)

        f = open(f'{self.library_folder}\\Top Func', 'r')
        top_func = f.readlines()
        f.close()

        method_list = [method for method in dir(Func) if method.startswith('__') is False]

        self.bf_btnt_x = 0
        self.bF_btnt_y = 0
        symbols = {"self": self, "Func": Func}
        for i in range(len(top_func)):
            btn_text_, btn_w_ = top_func[i].strip('\n').split('.')
            btn_w_ = int(btn_w_)

            btn_add = Button(self.root, command=eval(f'lambda: Func.{method_list[i]}(self)', symbols), justify=LEFT, text=btn_text_, font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
            btn_add.place(x=self.bf_btnt_x + 1, y=self.bF_btnt_y, width=btn_w_, height=19)
            self.bf_btnt_x += btn_w_ + 1

        # Detail Frame
        self.buttonFrameDemo = Frame(self.root, bg=self.colorList[3])
        self.buttonFrameDemo.place(x=self.dFbFstF_x, y=self.dFsF_y, width=self.dFbF_w, height=self.dF_h)

        self.canvasRP = Canvas(self.buttonFrameDemo, bd=0, highlightthickness=0, bg=self.colorList[3], width=300, height=300, scrollregion=(0, 0, 500, 500))
        self.vbarButtonFrame = Scrollbar(self.buttonFrameDemo, orient=VERTICAL)
        self.vbarButtonFrame.place(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h + 24)
        self.vbarButtonFrame.config(command=self.canvasRP.yview)
        self.canvasRP.config(width=300, height=300)
        self.canvasRP.config(yscrollcommand=self.vbarButtonFrame.set)
        self.canvasRP.pack(side=LEFT, expand=True, fill=BOTH)

        self.canvasRP.bind('<Configure>', lambda e: self.canvasRP.configure(scrollregion=self.canvasRP.bbox('all')))
        self.buttonFrame = Frame(self.canvasRP, bg=self.colorList[3])
        self.canvasRP.create_window((0, 0), window=self.buttonFrame, anchor="nw")

        self.Open_Main()

        # Record Frame
        self.detailFrame = Frame(self.root, bg=self.colorList[2])
        self.detailFrame.place(x=self.rF_x, y=self.rF_y, width=self.rF_w, height=self.rF_h)

        # Status Frame
        self.statusFrame = Frame(self.root, bg=self.colorList[2])
        self.statusFrame.place(x=self.dFbFstF_x, y=self.stF_y, width=self.stF_w, height=self.stF_h)

        self.lbl_status = Label(self.statusFrame, text='Status:', anchor=W, justify=LEFT, font=(self.formset_mainF[0], 13), bg=self.colorList[2], fg=self.colorList[4], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        self.lbl_status.place(x=0, y=0, width=self.stF_w, height=self.stF_h)

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        fileMenu = Menu(self.menubar)
        fileMenu = Menu(fileMenu, background=self.colorList[2])
        fileMenu.add_separator()

        def rT(s):
            if s == 1:
                self.cmnset_refT = 'True'
            elif s == 0:
                self.cmnset_refT = 'False'

        fileMenu.add_command(label="Enable Refresh Thread", command=lambda: rT(1))
        fileMenu.add_command(label="Disable Refresh Thread", command=lambda: rT(0))
        fileMenu.add_separator()
        def close_root():
            r = messagebox.askyesno('Quit', 'Are you sure you want to exit')
            if r:
                self.root.destroy()
        fileMenu.add_command(label="Exit", underline=0, command=close_root)
        self.menubar.add_command(label="x", underline=0, command=close_root)
        def minmax():
            self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
            self.root.attributes("-topmost", False)
        self.menubar.add_command(label="⬜", underline=0, command=lambda: minmax())
        self.menubar.add_cascade(label="File", underline=0, menu=fileMenu)

        self.Menu()
        self.menubar.add_cascade(label="Refresh", underline=0, command=lambda: self.Refresh(thread_=0))
        self.RefreshT('1')
        self.list_libForm = self.libFormList()

    def libFormList(self):
        f = open(f'Forms', 'r')
        fread = f.read()
        f.close()
        names = fread.split('\n')
        forms = []
        for name in names:
            # match form names that follow the pattern '[name]' or '[name].[subname]'
            if "." in name:
                matches = re.findall(r'\[(.*?)\]', name)
                for match in matches:
                    # extract the form name(s)
                    form_names = [name.strip() for name in match.split(',') if name is not None]
                    forms.extend(form_names)
            else:
                forms.append(name)

        func = []
        for i in forms:
            btn_cls = f'{i}'.replace(' ', '')
            try:
                func.append(globals()[btn_cls])
            except:
                func.append('ERROR')
        func_dict = dict(zip(forms, func))

        return func_dict

    def Menu(self):
        f = open(f'Forms', 'r')
        self.forms_ = f.readlines()
        f.close()

        formsMenu = Menu(self.menubar)
        formsMenu = Menu(formsMenu, background=self.colorList[2])
        formsMenu.add_separator()
        for i in self.forms_:
            btn_ = i.strip('\n')
            try:
                _ = btn_.split('.')  # For Checking Purpose
                if len(_) == 1: raise EXCEPTION  # For Checking Purpose
                self.Open_menu('0', _, 0)
            except:
                formsMenu.add_command(label=btn_, underline=0, command=lambda btn_=btn_: self.Open_menu('1', btn_, 0))
        self.menubar.add_cascade(label="Forms", underline=0, menu=formsMenu)

    def Open_menu(self, single, btn_, sta):
        if single == '1':
            btn_frm = f'{btn_}_frm'.replace(' ', '')
            btn_cls = f'{btn_}'.replace(' ', '')
            try:
                obj_toplevel = Toplevel(root)
                globals()[btn_cls](obj_toplevel, libFormList=self.list_libForm)
                Log_Generator().addLog(f"[Open Form] {btn_frm}")
            except:
                messagebox.showerror("Error", f"Error While Finding The {btn_} Form")
                Log_Generator().addLog(f"[Error] While Finding The {btn_} Form")

        elif single == '0':
            btn_t = btn_[0]
            if sta == 0:
                self.btnMenu = Menu(self.menubar)
                self.btnMenu = Menu(self.btnMenu, background=self.colorList[2])
                self.btnMenu.add_separator()

            btn_ = '.'.join([str(x) for x in btn_[1:]])
            btn_ = btn_[1:-1]
            leave = re.findall(r'\[.*?\]', btn_)
            result = ''
            paren = 0
            for ch in btn_:
                if ch == '[':
                    paren = paren + 1
                elif (ch == ']') and paren:
                    paren = paren - 1
                elif not paren:
                    result += ch

            btn_ = result.split(',')
            result = []
            cnt = 0

            for i in btn_:
                if i.endswith('.'):
                    result.append(f'{i}{leave[cnt]}')
                    cnt += 1
                else:
                    result.append(i)
            btn_ = result

            if sta == 1:
                nBtnMenu = Menu(self.menubar)
                nBtnMenu = Menu(self.btnMenu, background=self.colorList[2])
                nBtnMenu.add_separator()
                self.btnMenu.add_cascade(label=btn_t, underline=0, menu=nBtnMenu)

            for i in btn_:
                btn_ = i.strip('\n')
                try:
                    _ = btn_.split('.')  # For Checking Purpose
                    if len(_) == 1: raise EXCEPTION  # For Checking Purpose
                    self.Open_menu('0', _, 1)
                except:
                    if sta == 0:
                        self.btnMenu.add_command(label=btn_, underline=0, command=lambda btn_=btn_: self.Open_menu('1', btn_, 0))
                    if sta == 1:
                        nBtnMenu.add_command(label=btn_, underline=0, command=lambda btn_=btn_: self.Open_menu('1', btn_, 0))

            if sta == 0:
                self.menubar.add_cascade(label=btn_t, underline=0, menu=self.btnMenu)

    def Open_frm(self, single, btn_, sta):
        if single == '1':
            btn_frm = f'{btn_}_frm'.replace(' ', '')
            btn_cls = f'{btn_}'.replace(' ', '')
            try:
                obj_toplevel = Toplevel(root)
                globals()[btn_cls](obj_toplevel, libFormList=self.list_libForm)
                Log_Generator().addLog(f"[Open Form] {btn_frm}")
            except Exception as e:
                messagebox.showerror("Error", f"Error While Finding The {btn_} Form {e}")
                Log_Generator().addLog(f"[Error] While Finding The {btn_} Form")

        elif single == '0':
            btn_t = btn_[0]
            btn_ = '.'.join([str(x) for x in btn_[1:]])
            btn_ = btn_[1:-1]
            leave = re.findall(r'\[.*?\]', btn_)
            result = ''
            paren = 0
            for ch in btn_:
                if ch == '[':
                    paren = paren + 1
                elif (ch == ']') and paren:
                    paren = paren - 1
                elif not paren:
                    result += ch

            btn_ = result.split(',')
            result = []
            cnt = 0
            for i in btn_:
                if i.endswith('.'):
                    result.append(f'{i}{leave[cnt]}')
                    cnt += 1
                else:
                    result.append(i)
            btn_ = result
            try:
                self.buttonFrame1Demo.destroy()
            except:
                pass

            self.buttonFrame1Demo = Frame(self.root, bg=self.colorList[3])
            self.buttonFrame1Demo.place(x=self.dFbFstF_x, y=self.dFsF_y, width=self.dFbF_w, height=self.dF_h)

            self.canvasRP1 = Canvas(self.buttonFrame1Demo, bd=0, highlightthickness=0, bg=self.colorList[3], width=300, height=300, scrollregion=(0, 0, 500, 500))
            self.vbarButtonFrame1 = Scrollbar(self.buttonFrame1Demo, orient=VERTICAL)
            self.vbarButtonFrame1.place(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h + 24 - int(self.formset_mainFHB))
            self.vbarButtonFrame1.config(command=self.canvasRP1.yview)
            self.canvasRP1.config(width=300, height=300)
            self.canvasRP1.config(yscrollcommand=self.vbarButtonFrame1.set)
            self.canvasRP1.pack(side=LEFT, expand=True, fill=BOTH)

            self.canvasRP1.bind('<Configure>', lambda e: self.canvasRP1.configure(scrollregion=self.canvasRP1.bbox('all')))
            self.buttonFrame1 = Frame(self.canvasRP1, bg=self.colorList[3])
            self.canvasRP1.create_window((0, 0), window=self.buttonFrame1, anchor="nw")

            w_btn = int(self.dFbF_w)
            y_btn = -31
            h_btn = int(self.formset_mainFHB)
            self.btn_back = Button(self.buttonFrame1Demo, command=lambda: self.Back(), justify=LEFT, text='Back To Main', font=('goudy old style', 15), relief=GROOVE, bd=2, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
            self.btn_back.place(x=0, y=self.dF_h - h_btn, width=w_btn, height=h_btn)
            y_btn += h_btn + 1

            for i in btn_:
                btn_ = i.strip('\n')
                try:
                    _ = btn_.split('.')  # For Checking Purpose
                    if len(_) == 1: raise EXCEPTION  # For Checking Purpose

                    btn_addFrame = Frame(self.buttonFrame1, bg=self.colorList[3], width=w_btn - 10, height=h_btn)
                    btn_add = Button(btn_addFrame, command=lambda _=_: self.Open_frm('0', _, 1), justify=LEFT, text=_[0], font=('goudy old style', 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                    btn_add.place(x=0, y=1, width=w_btn, height=h_btn)
                    btn_addFrame.pack(fill=BOTH, expand=True)
                except:
                    btn_addFrame = Frame(self.buttonFrame1, bg=self.colorList[3], width=w_btn - 10, height=h_btn)
                    btn_add = Button(btn_addFrame, command=lambda btn_=btn_: self.Open_frm('1', btn_, 1), justify=LEFT, text=btn_, font=('goudy old style', 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                    btn_add.place(x=0, y=1, width=w_btn, height=h_btn)
                    btn_addFrame.pack(fill=BOTH, expand=True)

    def Open_Main(self):
        f = open(f'Forms', 'r')
        self.forms = f.readlines()
        f.close()

        w_btn = int(self.dFbF_w)
        h_btn = int(self.formset_mainFHB)

        for i in self.forms:
            btn_ = i.strip('\n')
            try:
                _ = btn_.split('.')  # For Checking Purpose
                if len(_) == 1: raise EXCEPTION  # For Checking Purpose

                btn_addFrame = Frame(self.buttonFrame, bg=self.colorList[3], width=w_btn - 10, height=h_btn)
                btn_add = Button(btn_addFrame, command=lambda _=_: self.Open_frm('0', _, 1), justify=LEFT, text=_[0], font=('goudy old style', 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                btn_add.place(x=0, y=1, width=w_btn, height=h_btn)
                btn_addFrame.pack(fill=BOTH, expand=True)
            except:
                btn_addFrame = Frame(self.buttonFrame, bg=self.colorList[3], width=w_btn - 10, height=h_btn)
                btn_add = Button(btn_addFrame, command=lambda btn_=btn_: self.Open_frm('1', btn_, 1), justify=LEFT, text=btn_, font=('goudy old style', 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
                btn_add.place(x=0, y=1, width=w_btn, height=h_btn)
                btn_addFrame.pack(fill=BOTH, expand=True)

    def Back(self):
        self.buttonFrame1Demo.destroy()
        self.buttonFrame.destroy()
        # self.buttonFrame = Frame(bg=self.colorList[3])
        # self.buttonFrame.place(x=self.dFbFstF_x, y=self.dFsF_y, width=self.dFbF_w, height=self.dF_h)
        self.buttonFrame = Frame(self.canvasRP, bg=self.colorList[3])
        self.canvasRP.create_window((0, 0), window=self.buttonFrame, anchor="nw")
        self.btn_back.destroy()
        self.Open_Main()

    def CallCommonVar(self, height_):
        # common variables
        self.dFsF_y = 20  # Detail Frame And Search Frame Y
        self.dFbFstF_x = 0  # Detail Frame And Button Frame And Status Frame X
        self.stF_h = int(self.formset_mainFSFH)  # Status Frame Height

        self.dFbF_w = int(self.formset_mainFBFW)
        self.rF_y = self.dFsF_y  # Record Frame Y
        self.stF_w = self.mainW  # Status Frame Width
        self.rF_w = self.mainW - self.dFbF_w  # Record Frame Width
        self.rF_h = self.mainH - self.rF_y - self.stF_h - height_ - 1  # Detail Frame and Record Frame Height -1 because we add 1 in stF_y

        self.dF_h = self.mainH - self.dFsF_y - self.stF_h - height_ - 1
        self.bF_y = self.dFsF_y + self.dF_h + 1
        self.rF_x = self.dFbF_w + 1
        self.stF_y = self.rF_y + self.rF_h + 1  # Status Frame Y

    def RefreshT(self, thread_):
        if thread_ == '1':
            x = threading.Thread(target=self.Refresh, args=(1,))
            x.start()
        elif thread_ == '0':
            Log_Generator().addLog(f'[{self.mainName}] [Refresh] Thread Stopped')

    def Refresh(self, thread_):
        self.root.update()
        self.mainW = self.root.winfo_width()
        self.mainH = self.root.winfo_height()

        if self.old_mainW != self.mainW or self.old_mainH != self.mainH:
            self.old_mainW = self.mainW
            self.old_mainH = self.mainH

            if thread_ == 0:
                Log_Generator().addLog(f'[{self.mainName}] [After Refresh]\t[Root Width] {self.mainW}, [Root Height] {self.mainH}')
            self.CallCommonVar(1)

            self.buttonFrameDemo.place_forget()
            self.buttonFrameDemo.place_configure(x=self.dFbFstF_x, y=self.dFsF_y, width=self.dFbF_w, height=self.dF_h)
            self.vbarButtonFrame.place_forget()
            self.vbarButtonFrame.place_configure(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h + 24)

            try:
                self.buttonFrame1Demo.place_forget()
                self.buttonFrame1Demo.place_configure(x=self.dFbFstF_x, y=self.dFsF_y, width=self.dFbF_w, height=self.dF_h)
                self.vbarButtonFrame1.place_forget()
                self.vbarButtonFrame1.place_configure(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h + 24 - int(self.formset_mainFHB))
            except: pass

            self.detailFrame.place_forget()
            self.detailFrame.place_configure(x=self.rF_x, y=self.rF_y, width=self.rF_w, height=self.rF_h)
            try:
                self.btn_back.place_configure(x=0, y=self.dF_h - int(self.formset_mainFHB), width=self.dFbF_w, height=int(self.formset_mainFHB))
            except:
                pass

            self.statusFrame.place_forget()
            self.statusFrame.place(x=self.dFbFstF_x, y=self.stF_y, width=self.stF_w, height=self.stF_h)
            self.lbl_status.place_forget()
            self.lbl_status.place_configure(x=0, y=0, width=self.stF_w, height=self.stF_h)

        if thread_ == 1:
            if self.cmnset_refT == 'True':
                self.root.after(int(self.cmnset_refA), lambda: self.RefreshT('1'))
            elif self.cmnset_refT == 'False':
                self.root.after(int(self.cmnset_refA), lambda: self.RefreshT('0'))


if __name__ == '__main__':
    root = Tk()
    obj = Main(root)
    root.mainloop()
    Log_Generator().closeLog()

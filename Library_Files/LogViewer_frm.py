import os
from tkinter import *
from tkinter import ttk

try:
    from Autocomplete_Combo import AutocompleteCombobox
    from FormRun import *
except:
    from Library_Files.Autocomplete_Combo import AutocompleteCombobox
    from Library_Files.FormRun import *


class LogViewer(BeforeInIt, AllSettings):
    wSize, hSize = 700, 550

    mainName = "Log Viewer"
    title = mainName

    def __init__(self, wind, libFormList=[]) -> None:
        BeforeInIt.__init__(self)
        AllSettings.__init__(self)
        super().__init__()
        self.root = wind
        self.root.title(self.title)
        self.root.iconbitmap(self.iconPath)
        self.root.config(bg=self.colorList[2])

        if self.cmnset_fullscreen == 'True':
            self.root.attributes("-fullscreen", True)

        self.root.state('zoomed')  # zoomed
        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        self.root.minsize(self.wSize, self.hSize)

        self.mainW = self.root.winfo_width()
        self.mainH = self.root.winfo_height()

        # TTk Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", foreground=self.colorList[10], fieldbackground=self.colorList[13], background=self.colorList[9])

        # -==== title =====- #
        Label(self.root, text=f'{self.mainName}', font=(self.formset_mainHF, 20, 'bold'), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=10, width=self.mainW-20, height=40)

        # ==== content ==== #
        self.logFile_type = StringVar()
        logFrom_list = os.listdir(self.temp_folder)
        logFrom_list = [x for x in logFrom_list if x.endswith('.txt')]
        logFrom_list.sort(reverse=True)
        self.logFile_type.set(logFrom_list[0])
        Label(self.root, text='Log File', font=(self.formset_mainF, 15), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=55)
        cmb_log = AutocompleteCombobox(self.root, values=logFrom_list, textvariable=self.logFile_type, font=(self.formset_mainF, 15), background=self.colorList[9], foreground=self.colorList[10])
        cmb_log.set_completion_list_sorted(logFrom_list)
        cmb_log.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_log)
        cmb_log.place(x=210, y=55, width=self.mainW - 220)
        cmb_log.bind("<<ComboboxSelected>>", self.selectFile)

        txt_Frame = Frame(self.root, bg=self.colorList[2])
        txt_Frame.pack(padx=10, pady=(90,10), fill=BOTH, expand=True)
        scroll_x = Scrollbar(txt_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(txt_Frame, orient=VERTICAL)
        self.txt_import = Text(txt_Frame, font=(self.formset_mainF, 15), wrap=NONE, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12], xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_x.config(command=self.txt_import.xview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.txt_import.yview)
        self.txt_import.pack(fill=BOTH, expand=1)

        self.selectFile('e')

        btn_ = Button(self.root, command=self.root.destroy, justify=LEFT, text='x', font=('calibri', 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_.place(x=0, y=0, width=30, height=25)
    
    def selectFile(self, e):
        self.txt_import.delete('1.0', END)
        f = open(f'{self.temp_folder}\\{self.logFile_type.get()}', 'r')
        self.txt_import.insert(END, f.read())
        f.close()
    

if __name__ == '__main__':
    root = Tk()
    obj = LogViewer(root)
    root.mainloop()

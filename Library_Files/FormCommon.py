from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkcalendar import Calendar, DateEntry
import re, os, random, time, pandas, csv, threading
import pymysql, sqlite3
from reportlab.lib import colors as abcdef
from reportlab.lib import pagesizes  # For creating reports
from reportlab.lib.units import mm, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle  # For creating reports
from reportlab.lib.styles import getSampleStyleSheet  # For creating reports
from datetime import datetime, timedelta
import textwrap
import webbrowser  # For Opening Links
# import openpyxl # for creating the excel report xlsx format

try:
    from Autocomplete_Combo import AutocompleteCombobox
    from Log_Generator import Log_Generator
    from Top_Func import Func
except:
    from Library_Files.Autocomplete_Combo import AutocompleteCombobox
    from Library_Files.Log_Generator import Log_Generator
    from Library_Files.Top_Func import Func


class CommonFunction:
    def CommonCall(self, topButton=True, detailsPanel=True):
        self.root.title(self.title)
        self.root.iconbitmap(self.iconPath)
        self.root.config(bg=self.colorList[3])

        if self.cmnset_fullscreen == 'True':
            self.root.attributes("-fullscreen", True)
        self.root.state('zoomed')  # zoomed
        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        self.root.minsize(self.wSize, self.hSize)
        self.root.attributes("-topmost", False)

        # Enable Database
        self.EnableDb()

        # TTk Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", foreground=self.colorList[10], fieldbackground=self.colorList[13], background=self.colorList[9])
        style.configure("Treeview", fieldbackground=self.colorList[17], background=self.colorList[17], foreground=self.colorList[18])
        style.map('Treeview', background=[('selected', self.colorList[19])], foreground=[('selected', self.colorList[20])])

        self.root.update()
        self.mainW = self.root.winfo_width()
        self.mainH = self.root.winfo_height()

        self.Variables()

        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        # Call Functions
        self.CallCommonVar(1)

        if topButton:
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

        if detailsPanel:
            # Detail Frame
            self.detailFrameDemo = Frame(self.root, bg=self.colorList[2])
            self.detailFrameDemo.place(x=self.dFbFstF_x, y=self.dFsF_y, width=self.dFbF_w, height=self.dF_h)

            self.canvasRP = Canvas(self.detailFrameDemo, bd=0, highlightthickness=0, bg=self.colorList[2], width=300, height=300, scrollregion=(0, 0, 500, 500))
            self.vbarDetailFrame = Scrollbar(self.detailFrameDemo, orient=VERTICAL)
            self.vbarDetailFrame.place(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h + 24)
            self.vbarDetailFrame.config(command=self.canvasRP.yview)
            self.canvasRP.config(width=300, height=300)
            self.canvasRP.config(yscrollcommand=self.vbarDetailFrame.set)
            self.canvasRP.pack(side=LEFT, expand=True, fill=BOTH)

            self.canvasRP.bind('<Configure>', lambda e: self.canvasRP.configure(scrollregion=self.canvasRP.bbox('all')))
            self.detailFrame = Frame(self.canvasRP, bg=self.colorList[2])
            self.canvasRP.create_window((0, 0), window=self.detailFrame, anchor="nw")

    def CommonCall2(self, searchHead=None):
        # Button Frame
        self.buttonFrame = Frame(self.root, bg=self.colorList[3])
        self.buttonFrame.place(x=self.dFbFstF_x, y=self.bF_y, width=self.dFbF_w, height=self.bF_h)

        self.acessableBtns, acessableBtns_cnt = self.accessableButtons()
        self.bF_btn_w = int(self.dFbF_w / (acessableBtns_cnt + 1)) + 1
        self.bF_btn_h = self.bF_h
        self.bf_btn_x = 0
        self.bF_btn_y = 0

        if self.acessableBtns[0] == 'True':
            btn_add = Button(self.buttonFrame, command=self.Add, justify=LEFT, text='Add', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
            btn_add.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
            self.bf_btn_x += self.bF_btn_w
            self.root.bind('<Return>', self._Add)

        if self.acessableBtns[1] == 'True':
            btn_update = Button(self.buttonFrame, command=self.Update, justify=LEFT, text='Update', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
            btn_update.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
            self.bf_btn_x += self.bF_btn_w
            self.root.bind('<Control-u>', self._Update)

        if self.acessableBtns[2] == 'True':
            btn_delete = Button(self.buttonFrame, command=self.Delete, justify=LEFT, text='Delete', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
            btn_delete.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
            self.bf_btn_x += self.bF_btn_w
            # self.root.bind('<Delete>', self.Delete)

        btn_clear = Button(self.buttonFrame, command=self.Clear, justify=LEFT, text='Clear', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_clear.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        self.root.bind('<Control-BackSpace>', self._Clear)

        if self.acessableBtns[3] == 'True':
            btn_import = Button(self.buttonFrame, command=self.Import, justify=LEFT, text='Import', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
            btn_import.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
            self.bf_btn_x += self.bF_btn_w
            self.root.bind('<Control-i>', self._Import)
            self.root.bind('<Prior>', self._Import)

        if self.acessableBtns[4] == 'True':
            btn_export = Button(self.buttonFrame, command=self.Export, justify=LEFT, text='Export', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
            btn_export.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
            self.bf_btn_x += self.bF_btn_w
            self.root.bind('<Control-e>', self._Export)
            self.root.bind('<Next>', self._Export)

        # Search Frame
        self.searchFrame = Frame(self.root, bg=self.colorList[2])
        self.searchFrame.place(x=self.dFbF_w + 1, y=self.dFsF_y, width=self.sF_w, height=self.sF_h)
        
        if searchHead == None:
            cmb_search_list = self.__list__('head')
        else:
            cmb_search_list = self.__list__('head') + searchHead
        cmb_search = AutocompleteCombobox(self.searchFrame, values=cmb_search_list, textvariable=self.var_search_by, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_search.set_completion_list(cmb_search_list)
        cmb_search.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_search)
        cmb_search.place(x=10, y=10, width=150, height=self.sF_h - 20)
        cmb_search.set('Select')

        self.txt_search = Entry(self.searchFrame, textvariable=self.var_search_txt, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        self.txt_search.place(x=162, y=10, height=self.sF_h - 20, width=self.sF_w - 150 - 20 - 2)
        self.txt_search.bind("<KeyRelease>", self.Search)

    def CommonCall3(self):
        # Status Frame
        self.statusFrame = Frame(self.root, bg=self.colorList[2])
        self.statusFrame.place(x=self.dFbFstF_x, y=self.stF_y, width=self.stF_w, height=self.stF_h)

        self.lbl_status = Label(self.statusFrame, text='Status:', anchor=W, justify=LEFT, font=(self.formset_mainF[0], 13), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        self.lbl_status.place(x=0, y=0, width=self.stF_w, height=self.stF_h)

        # After UI Creating
        self.Table.bind("<ButtonRelease-1>", self.Get_Data)
        self.Show()

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        fileMenu = Menu(self.menubar)
        fileMenu = Menu(fileMenu, background=self.colorList[2])
        if self.acessableBtns[4] == 'True':
            fileMenu.add_separator()
            fileMenu.add_command(label="Save To PDF", command=self.export_pdf)
            fileMenu.add_command(label="Save To Excel(CSV)", command=self.export_csv)
            fileMenu.add_command(label="Save To Excel(XLSX)", command=self.export_excel)
            fileMenu.add_command(label="Save To HTML", command=self.export_html)
            fileMenu.add_command(label="Save To TXT", command=self.export_txt)
            fileMenu.add_command(label="Copy To Clipboard", command=self.export_clip)
        if self.acessableBtns[3] == 'True':
            fileMenu.add_separator()
            fileMenu.add_command(label="Import From CSV", command=lambda: self.import_csv(self.__listTotxt__(self.__list__('head'))))
        fileMenu.add_separator()
        fileMenu.add_command(label="Remove All Records", command=self.delete_Table)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=0, command=self.root.destroy)
        self.menubar.add_command(label="x", underline=0, command=self.root.destroy)
        def minmax():
            self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
            self.root.attributes("-topmost", False)
        self.menubar.add_command(label="⬜", underline=0, command=lambda: minmax())
        self.menubar.add_cascade(label="File", underline=0, menu=fileMenu)

        moreMenu = Menu(self.menubar)
        moreMenu = Menu(moreMenu, background=self.colorList[2])
        moreMenu.add_separator()
        moreMenu.add_command(label="Refresh ID", command=self.RefreshId)
        moreMenu.add_command(label="Refresh Common Variable", command=lambda: self.CallCommonVar(1))
        moreMenu.add_separator()
        moreMenu.add_command(label="Enable Database", command=self.EnableDb)
        moreMenu.add_command(label="Disable Database", command=self.DisableDb)
        moreMenu.add_separator()

        def rT(s):
            if s == 1:
                self.cmnset_refT = 'True'
            elif s == 0:
                self.cmnset_refT = 'False'

        moreMenu.add_command(label="Enable Refresh Thread", command=lambda: rT(1))
        moreMenu.add_command(label="Disable Refresh Thread", command=lambda: rT(0))
        self.menubar.add_cascade(label="More", underline=0, menu=moreMenu)
        self.menubar.add_cascade(label="Refresh", underline=0, command=lambda: self.Refresh(thread_=0, force=True))

        self.Clear()
        self.CallReportSet()
        self.RefreshT('1')
        self.ResetlblStaT('1')
        self.Refresh(0, True)

    def Add(self):
        """
        Args:
            # list_var: List Of Variables
            # list_cvar: List Of [Validations Variables, Field Name]
            # bq: Query Before Update Not Required
            # aq: Query After Update Not Required
        Returns:
            bool: Whether the record was added successfully or not
        """

        list_cvar = self.__list__('cvar')
        list_var = self.__list__('var')
        bq = self.__bq__('add')
        aq = self.__aq__('add')

        lval = self.__getListVar__(list_var)
        try:
            Validations = False
            for i in list_cvar:
                if i[0].get() == '':
                    if self.cmnset_msgboxAadd == 'True':
                        self.status(f'[{self.mainName}] [Add Error] {i[1]} IS REQUIRED', True, 'Error', 'Add Error')
                    else:
                        self.status(f'[{self.mainName}] [Add Error] {i[1]} IS REQUIRED')
                    Validations = True
                    break

            if not Validations:
                self.cur.execute(f"select * from {self.mainName.replace(' ', '_')} where id='" + lval[0] + "'")
                row = self.cur.fetchone()
                if row is not None:
                    self.status(f'[{self.mainName}] [Add Error] This ID is Already Assigned, Try New One', True, 'Error', 'Add Error')
                else:
                    a = '?,' * len(lval)
                    a = a.rstrip(',')

                    if bq is not None:
                        self.cur.execute(bq)
                    self.cur.execute(f"insert into {self.mainName.replace(' ', '_')} VALUES ({a})", lval)
                    if aq is not None:
                        self.cur.execute(aq)

                    self.con.commit()
                    if self.cmnset_msgboxAadd == 'True':
                        r = messagebox.askyesno('Success', f'{self.mainName} Record {lval[0]} Added Successfully\nAre You Want To Clear The Field', parent=self.root)
                        if r:
                            self.Clear()
                        else:
                            self.Show()
                    elif self.cmnset_msgboxAadd == 'False':
                        if self.cmnset_Afteradd == 'Clear Record':
                            self.Clear()
                        else:
                            self.Show()

                self.status(f'[{self.mainName}] [Add Record] Record With ID {lval[0]} Added Successfully')
                return True
        except Exception as ex:
            self.status(f'[{self.mainName}] [Add Error] Record With ID {lval[0]} Add Failed: {ex}', True, 'Error', 'Add Error')
            return False

    def Update(self):
        """
        Args:
            # list_shn: List Of Field Short Name
            # list_var:  List Of Variables
            # list_cvar: List Of [Validations Variables, Field Name]
            # bq: Query Before Update Not Required
            # aq: Query After Update Not Required
        Returns:
            Succeed or Not: Boolean
        """

        list_shn = self.__list__('shn')
        list_cvar = self.__list__('cvar')
        list_var = self.__list__('var')
        bq = self.__bq__('update')
        aq = self.__aq__('update')

        lval = self.__getListVar__(list_var)
        try:
            Validations = False
            for i in list_cvar:
                if i[0].get() == '':
                    if self.cmnset_msgboxAadd == 'True':
                        self.status(f'[{self.mainName}] [Update Error] {i[1]} IS REQUIRED', True, 'Error', 'Update Error')
                    else:
                        self.status(f'[{self.mainName}] [Update Error] {i[1]} IS REQUIRED')
                    Validations = True
                    break

            if not Validations:
                self.cur.execute(f"select * from {self.mainName.replace(' ', '_')} where id='" + lval[0] + "'")
                row = self.cur.fetchone()
                if row == None:
                    self.status(f'[{self.mainName}] [Update Error] Invalid Record ID, Select The Correct One', True, 'Error', 'Update Error')
                else:
                    lshn = ''
                    for i in list_shn:
                        lshn += i + '=?, '
                    lshn = lshn.rstrip(', ')
                    lval.append(lval[0])

                    if bq is not None:
                        self.cur.execute(bq)
                    self.cur.execute(f"update {self.mainName.replace(' ', '_')} set {lshn} where id=?", lval)
                    if aq is not None:
                        self.cur.execute(aq)
                    self.con.commit()

                    if self.cmnset_msgboxAupd == 'True':
                        r = messagebox.askyesno('Success', f'{self.mainName} Record {lval[0]} Updated Successfully\nAre You Want To Clear The Field', parent=self.root)
                        if r:
                            self.Clear()
                        else:
                            self.Show()
                    elif self.cmnset_msgboxAupd == 'False':
                        if self.cmnset_Afterupd == 'Clear Record':
                            self.Clear()
                        else:
                            self.Show()

                self.status(f'[{self.mainName}] [Update Record] Record With ID {lval[0]} Updated Successfully')
                return True
        except Exception as ex:
            self.status(f"[{self.mainName}] [Update Error] Record With ID {lval[0]} Updation Failed: {ex}", True, 'Error', 'Update Error')
            return False

    def Delete(self):
        """
        Args:
            # id_var: ID Variable
            # bq: Query Before Update Not Required
            # aq: Query After Update Not Required
        Returns:

        """
        bq = self.__bq__('delete')
        aq = self.__aq__('delete')
        try:
            if self.var_id.get() == '':
                self.status(f"[{self.mainName}] [Delete Error] First Select The Record That You Want To Delete From Treeview", True, 'Error', 'Delete Error')
            else:
                self.cur.execute(f"select * from {self.mainName.replace(' ', '_')} where id='" + self.var_id.get() + "'")
                row = self.cur.fetchone()
                if row == None:
                    self.status(f"[{self.mainName}] [Delete Error] Select The Correct Record, Invalid {self.mainName} Record", True, 'Error', 'Delete Error')
                else:
                    if self.cmnset_msgboxAdel == 'True':
                        op = messagebox.askyesno('Confirm', f'Do you really want to delete Record {self.var_id.get()}', parent=self.root)
                        if op:
                            if bq is not None:
                                self.cur.execute(bq)
                            self.cur.execute(f"delete from {self.mainName.replace(' ', '_')} where id='" + self.var_id.get() + "'")
                            if aq is not None:
                                self.cur.execute(aq)
                            self.con.commit()

                            r = messagebox.askyesno('Success', f'{self.mainName} Record {self.var_id.get()} Deleted Successfully\nAre You Want To Clear The Field', parent=self.root)
                            if r:
                                self.Clear()
                            else:
                                self.Show()
                    else:
                        if bq is not None:
                            self.cur.execute(bq)
                        self.cur.execute(f"delete from {self.mainName.replace(' ', '_')} where id='" + self.var_id.get() + "'")
                        if aq is not None:
                            self.cur.execute(aq)
                        self.con.commit()

                        if self.cmnset_Afterdel == 'Clear Record':
                            self.Clear()
                        else:
                            self.Show()

                    self.status(f'[{self.mainName}] [Delete Record] Record With ID {self.var_id.get()} Deleted Successfully')
                    return True
        except Exception as ex:
            self.status(f'[{self.mainName}] [Delete Error] Record With ID {self.var_id.get()} Deletion Failed: {ex}', True, 'Error', 'Delete Error')

    def Clear(self):
        list_var = self.__list__('var')
        self.Refresh(0)
        self.Show()
        try:
            list_var += self.__list__('extra_clear')
        except:
            pass
        for i in list_var:
            i.set('')

        self.RefreshId()
        self.var_search_by.set('Select')
        self.var_search_txt.set('')
        self.status(f"[{self.mainName}] [Clear] All Fields And Refresh Interface Successfully")

    def Search(self, e):
        try:
            if self.var_search_by.get() == 'Select':
                self.status(f"[{self.mainName}] [Search] Select Search By option", True, 'Error', 'Error')
            else:
                shn = self.__list__('shn')
                head = self.__list__('head')
                for i in range(len(head)):
                    if head[i] == self.var_search_by.get():
                        search_by = shn[i]
                        break
                self.cur.execute(f"select * from {self.mainName.replace(' ', '_')} where " + search_by + " LIKE '%" + self.var_search_txt.get() + "%'")
                rows = self.cur.fetchall()
                try:
                    rows.sort(key=lambda x: eval(self.sortKey))
                except:
                    pass
                if len(rows) != 0:
                    self.lbl_status.config(text='')
                    self.Table.delete(*self.Table.get_children())
                    for row in rows:
                        self.Table.insert('', END, values=row)
                    self.status(f"[{self.mainName}] [Search] {len(rows)} Record Found")
                else:
                    if self.var_search_txt.get() == '':
                        pass
                    else:
                        self.Table.delete(*self.Table.get_children())
                        self.status(f"[{self.mainName}] [Search] No Record Found")
        except Exception as ex:
            self.status(f"[{self.mainName}] [Search] We Found Error: {ex}", True, 'Error', 'Error')

    def Show(self):
        try:
            self.cur.execute(f"select * from {self.mainName.replace(' ', '_')}")
            rows = self.cur.fetchall()
            self.Table.delete(*self.Table.get_children())
            try:
                rows.sort(key=lambda x: eval(self.sortKey))
            except:
                pass
            for row in rows:
                self.Table.insert('', END, values=row)

            self.status(f"[{self.mainName}] [Fetch] Record Successfully")
        except Exception as ex:
            self.status(f"[{self.mainName}] [Fetch] We Found Error: {ex}", True, 'Error', 'Error')

    def RefreshId(self):
        try:
            self.cur.execute(f"select id from {self.mainName.replace(' ', '_')}")
            self.con.commit()
            row = self.cur.fetchall()
            for i in row:
                for i in i:
                    pass
            self.var_id.set(i + 1)
        except:
            self.var_id.set(int(self.formset_idStart))
        Log_Generator().addLog(f'[{self.mainName}] [ID Refresh] Successfully')

    def Export(self):
        self.tp_export = Toplevel()
        self.tp_export.geometry("420x280+220+140")
        self.tp_export.title(self.title)
        self.tp_export.resizable(0, 0)
        self.tp_export.config(bg=self.colorList[2])
        self.tp_export.focus_force()
        self.tp_export.iconbitmap(self.iconPath)

        # -==== title =====- #
        Label(self.tp_export, text='EXPORT', font=(self.formset_mainHF, 20, 'bold'), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=10, width=400, height=40)

        # # ==== content ==== #
        expFile_type = StringVar()
        expFrom_list = ['Clipboard', 'Excel(CSV)', 'Excel(XLSX)', 'HTML', 'PDF', 'TXT']
        Label(self.tp_export, text='EXPORT INTO', font=(self.formset_mainF, 15), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=55)
        cmb_expFrom = AutocompleteCombobox(self.tp_export, values=expFrom_list, textvariable=expFile_type, font=(self.formset_mainF, 15), background=self.colorList[9], foreground=self.colorList[10])
        cmb_expFrom.set_completion_list(expFrom_list)
        cmb_expFrom.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_expFrom)
        cmb_expFrom.place(x=150, y=55, width=260)
        cmb_expFrom.current(4)

        def checkPDF(e):
            if expFile_type.get() == 'PDF':
                check_sz('e')
            else:
                self.tp_export.geometry("420x170+220+140")

        cmb_expFrom.bind("<<ComboboxSelected>>", checkPDF)

        Label(self.tp_export, text='Save Automatically', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=90)
        lst_repset_Sauto = ['True', 'False']
        self._sa = StringVar()
        self.tp_export.focus_force()
        self._sa.set(self.repset_Sauto)
        cmb_repset_Sauto = AutocompleteCombobox(self.tp_export, values=lst_repset_Sauto, textvariable=self._sa, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_repset_Sauto.set_completion_list(lst_repset_Sauto)
        cmb_repset_Sauto.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_repset_Sauto)
        cmb_repset_Sauto.place(x=150, y=90, width=260)

        self.var_repsetorn = StringVar()
        Label(self.tp_export, text='Orientation', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=170)
        lst_repsetorn = ['Landscape', 'Portrait']
        cmb_repsetorn = AutocompleteCombobox(self.tp_export, values=lst_repsetorn, textvariable=self.var_repsetorn, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_repsetorn.set_completion_list(lst_repsetorn)
        cmb_repsetorn.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_repsetorn)
        cmb_repsetorn.place(x=150, y=170, width=260)
        if self.repset_Lrep:
            self.var_repsetorn.set('Landscape')
        else:
            self.var_repsetorn.set('Portrait')

        Label(self.tp_export, text='Report Size', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=200)
        self.var_repset_Size = StringVar()
        self.var_repset_Size.set(self.repset_Size)
        lst_repset_Size = ['A4', 'Multiple']
        cmb_repset_Size = AutocompleteCombobox(self.tp_export, values=lst_repset_Size, textvariable=self.var_repset_Size, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_repset_Size.set_completion_list(lst_repset_Size)
        cmb_repset_Size.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_repset_Size)
        cmb_repset_Size.place(x=150, y=200, width=260)

        def check_sz(e):
            if self.var_repset_Size.get() == 'A4':
                self.tp_export.geometry("420x230+220+140")
            else:
                self.tp_export.geometry("420x280+220+140")

        cmb_repset_Size.bind("<<ComboboxSelected>>", check_sz)
        checkPDF('e')
        check_sz('e')

        self.var_pgrepset_u = StringVar()
        self.var_pgrepset_u.set(self.pgrepset_u)
        Label(self.tp_export, text='Unit/Width/Height', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=230)
        lst_pgrepset_u = ['mm', 'inch']
        cmb_pgrepset_u = AutocompleteCombobox(self.tp_export, values=lst_pgrepset_u, textvariable=self.var_pgrepset_u, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_pgrepset_u.set_completion_list(lst_pgrepset_u)
        cmb_pgrepset_u.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_pgrepset_u)
        cmb_pgrepset_u.place(x=150, y=230, width=(260 / 3) - 1)
        self.var_pgrepset_w = StringVar()
        self.var_pgrepset_w.set(self.pgrepset_w)
        txt_pgrepset_w = Entry(self.tp_export, textvariable=self.var_pgrepset_w, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        txt_pgrepset_w.place(x=150 + (260 / 3), y=230, width=(260 / 3) - 1)
        self.var_pgrepset_h = StringVar()
        self.var_pgrepset_h.set(self.pgrepset_h)
        txt_pgrepset_h = Entry(self.tp_export, textvariable=self.var_pgrepset_h, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        txt_pgrepset_h.place(x=150 + ((260 / 3) * 2), y=230, width=(260 / 3) - 1)

        def save():
            if expFile_type.get() == 'Clipboard':
                self.export_clip(self.tp_export)
            elif expFile_type.get() == 'Excel(CSV)':
                self.export_csv(self.tp_export)
            elif expFile_type.get() == 'Excel(XLSX)':
                self.export_excel(self.tp_export)
            elif expFile_type.get() == 'HTML':
                self.export_html(self.tp_export)
            elif expFile_type.get() == 'PDF':
                self.export_pdf(self.tp_export)
            elif expFile_type.get() == 'TXT':
                self.export_txt(self.tp_export)

        self.var_ename = StringVar()
        txt_name = Entry(self.tp_export, textvariable=self.var_ename, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        txt_name.place(x=10, y=125, width=280, height=35)

        Entry(self.tp_export, border=0, font=self.formset_mainF, disabledbackground=self.colorList[9], state=DISABLED, disabledforeground=self.colorList[10]).place(x=290, y=125, width=120, height=35)
        Button(self.tp_export, text='Export', command=save, justify=LEFT, font=(self.formset_mainF, 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6]).place(x=295, y=130, width=110, height=25)

    def getPath(self, fFormat, tp):
        path = ''

        def _sa(sta):
            nonlocal path
            if sta == 'a':  # Check For Save Automatically
                path_ = f'{self.repset_Sloc}\\Report'
                try:
                    os.mkdir(path_)
                except:
                    pass
                now = datetime.now()
                date_time = now.strftime("%d-%m-%Y, %H %M %S")
                path = f'{path_}\\{self.mainName} Report {date_time}.{fFormat}'
            else:  # Check For Save Manually
                if tp is not None:
                    path = filedialog.asksaveasfilename(title=f"SAVE REPORT IN {fFormat.swapcase()} FORMAT", defaultextension=f".{fFormat}", parent=tp)
                else:
                    path = filedialog.asksaveasfilename(title=f"SAVE REPORT IN {fFormat.swapcase()} FORMAT", defaultextension=f".{fFormat}", parent=self.root)

        try:
            if self._sa.get() == 'True':
                _sa('a')  # Check For Save Automatically
            elif self._sa.get() == 'False':
                _sa('m')  # Check For Save Manually
        except:
            if self.repset_Sauto == 'True':
                _sa('a')  # Check For Save Automatically
            elif self.repset_Sauto == 'False':
                _sa('m')  # Check For Save Manually

        return path

    def export_pdf(self, tp=None):
        def find_repsize(sta):
            # Check For Report Size
            try:
                rep_a4(sta, self.var_repset_Size.get())
            except:
                rep_a4(sta, self.repset_Size)

        def rep_a4(sta, sz='A4'):
            if sta == 'P':
                if sz == 'Multiple':
                    try:
                        if self.var_pgrepset_u.get() == 'mm':
                            self.PAGESIZE = pagesizes.portrait(((int(self.var_pgrepset_w.get()) * mm, int(self.var_pgrepset_h.get()) * mm)))
                        elif self.var_pgrepset_u.get() == 'inch':
                            self.PAGESIZE = pagesizes.portrait(((int(self.var_pgrepset_w.get()) * inch, int(self.var_pgrepset_h.get()) * inch)))
                    except:
                        if self.pgrepset_u == 'mm':
                            self.PAGESIZE = pagesizes.portrait(((int(self.pgrepset_w) * mm, int(self.pgrepset_h) * mm)))
                        elif self.pgrepset_u == 'inch':
                            self.PAGESIZE = pagesizes.portrait(((int(self.pgrepset_w) * inch, int(self.pgrepset_h) * inch)))
                else:
                    self.PAGESIZE = pagesizes.portrait(pagesizes.A4)
            elif sta == 'L':
                if sz == 'Multiple':
                    try:
                        if self.var_pgrepset_u.get() == 'mm':
                            self.PAGESIZE = pagesizes.landscape(((int(self.var_pgrepset_w.get()) * mm, int(self.var_pgrepset_h.get()) * mm)))
                        elif self.var_pgrepset_u.get() == 'inch':
                            self.PAGESIZE = pagesizes.landscape(((int(self.var_pgrepset_w.get()) * inch, int(self.var_pgrepset_h.get()) * inch)))
                    except:
                        if self.pgrepset_u == 'mm':
                            self.PAGESIZE = pagesizes.landscape(((int(self.pgrepset_w) * mm, int(self.pgrepset_h) * mm)))
                        elif self.pgrepset_u == 'inch':
                            self.PAGESIZE = pagesizes.landscape(((int(self.pgrepset_w) * inch, int(self.pgrepset_h) * inch)))
                else:
                    self.PAGESIZE = pagesizes.landscape(pagesizes.A4)

        # Check For Report Orientation
        try:
            if self.var_repsetorn.get() == 'Landscape':
                find_repsize('L')
            elif self.var_repsetorn.get() == 'Portrait':
                find_repsize('P')
        except:
            if self.repset_Lrep:
                find_repsize('L')
            else:
                find_repsize('P')

        path = self.getPath('pdf', tp)
        pdf = SimpleDocTemplate(path, pagesize=self.PAGESIZE, topMargin=float(int(self.repset_tm)), bottomMargin=float(int(self.repset_bm)), leftMargin=float(int(self.repset_lm)), rightMargin=float(int(self.repset_rm)))

        styles = getSampleStyleSheet()
        try:
            ename = self.var_ename.get()
            if ename != "":
                header = Paragraph(f"{ename}", styles['Heading1'])
            else:
                header = Paragraph(f"{self.title}", styles['Heading1'])
        except:
            header = Paragraph(f"{self.title}", styles['Heading1'])

        flow_obj = [header]
        count, headings, expList = self.Export_def()
        wrapped_expList = []
        for row in expList:
            wrapped_row = []
            for i, cell in enumerate(row):
                if self.split_pdf_rep:
                    try:
                        e = True
                        for j, split in self.split_pdf_rep.items():
                            if i == j:
                                try:
                                    wrapped_cell = "\n".join(textwrap.wrap(str(cell), width=int(split)))
                                except:
                                    wrapped_cell = "\n".join(str(cell).split(split))
                                e = False
                                break
                            else: e = True
                        if e:
                            raise Exception()
                    except Exception as e:
                        if self.split_pdf_rep_auto:
                            wrapped_cell = "\n".join(textwrap.wrap(str(cell), width=self.split_pdf_rep_auto_len))  # Wrap text to 20 characters
                        else:
                            wrapped_cell = cell
                else:
                    if self.split_pdf_rep_auto:
                        wrapped_cell = "\n".join(textwrap.wrap(str(cell), width=self.split_pdf_rep_auto_len))  # Wrap text to 20 characters
                    else:
                        wrapped_cell = cell
                wrapped_row.append(wrapped_cell)
            wrapped_expList.append(wrapped_row)
        t = Table([headings] + wrapped_expList, hAlign='LEFT', repeatRows=1)
        tstyle = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, abcdef.springgreen),
            ('LINEBELOW', (0, 0), (-1, 0), 2, abcdef.springgreen),
            ('BACKGROUND', (0, 0), (-1, 0), abcdef.springgreen),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('WORDWRAP', (0, 0), (-1, -1), 1),
        ])

        t.setStyle(tstyle)
        flow_obj.append(t)
        footer = Paragraph("Total Records: " + str(count), styles['Heading2'])
        flow_obj.append(footer)
        pdf.build(flow_obj)
        self.msglog(count, path, tp)

    def export_csv(self, tp=None):
        path = self.getPath('csv', tp)
        count, headings, expList = self.Export_def()
        df = pandas.DataFrame(expList, columns=headings)
        paths = r'{}'.format(path)
        df.to_csv(paths, index=False)
        self.msglog(count, path, tp)

    def export_excel(self, tp=None):
        path = self.getPath('xlsx', tp)
        count, headings, expList = self.Export_def()
        df = pandas.DataFrame(expList, columns=headings)
        paths = r'{}'.format(path)
        df.to_excel(paths, index=False)
        self.msglog(count, path, tp)

    def export_html(self, tp=None):
        path = self.getPath('html', tp)
        count, headings, expList = self.Export_def()
        df = pandas.DataFrame(expList, columns=headings)
        paths = r'{}'.format(path)
        df.to_html(paths, index=False)
        self.msglog(count, path, tp)

    def export_txt(self, tp=None):
        path = self.getPath('txt', tp)
        count, headings, expList = self.Export_def()
        df = pandas.DataFrame(expList, columns=headings)
        a = df.to_string(index=False)
        paths = r'{}'.format(path)
        f = open(paths, 'w')
        f.write(a)
        f.close()
        self.msglog(count, path, tp)

    def export_clip(self, tp=None):
        count, headings, expList = self.Export_def()
        df = pandas.DataFrame(expList, columns=headings)
        df.to_clipboard(index=False)
        self.msglog(count, tp=tp, exp='Copied', path=False, open_file=False)

    def Import(self):
        self.tp_import = Toplevel()
        self.tp_import.geometry("1020x325+220+140")
        self.tp_import.title(self.title)
        self.tp_import.resizable(0, 0)
        self.tp_import.config(bg=self.colorList[2])
        self.tp_import.focus_force()
        self.tp_import.iconbitmap(self.iconPath)

        # -==== title =====- #
        Label(self.tp_import, text='IMPORT', font=(self.formset_mainHF, 20, 'bold'), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=10, width=1000, height=40)

        # ==== content ==== #
        impFile_type = StringVar()
        impFrom_list = ['Excel(CSV)']
        Label(self.tp_import, text='IMPORT FROM', font=(self.formset_mainF, 15), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).place(x=10, y=55)
        cmb_impFrom = AutocompleteCombobox(self.tp_import, values=impFrom_list, textvariable=impFile_type, font=(self.formset_mainF, 15), background=self.colorList[9], foreground=self.colorList[10])
        cmb_impFrom.set_completion_list(impFrom_list)
        cmb_impFrom.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_impFrom)
        cmb_impFrom.place(x=155, y=55, width=855)
        cmb_impFrom.current(0)

        txt_Frame = Frame(self.tp_import, bg=self.colorList[3])
        txt_Frame.place(x=10, y=90, width=1000, height=175)

        list_head = self.__list__('headA')
        txt_head = self.__listTotxt__(list_head)
        scroll_y2 = Scrollbar(txt_Frame, orient=VERTICAL)
        txt_import = Text(txt_Frame, font=(self.formset_mainF, 15), bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12], yscrollcommand=scroll_y2.set)
        scroll_y2.pack(side=RIGHT, fill=Y)
        scroll_y2.config(command=txt_import.yview)
        txt_import.pack(fill=BOTH, expand=1)
        txt_import.insert(END, f"Are You Sure You Want To Import CSV File\nDon't Worry It's Not Delete Your Previous Data\nMake Sure Your First Row (Header) Is Empty Or With Column Names\nMake Sure Your First Column Is A Sr No Or Empty\nThe Program Not Copy First Row And First Column\nMake Sure Your Column Are Sorted According To\n{txt_head}")

        def save():
            if impFile_type.get() == 'Excel(CSV)':
                self.import_csv(txt_head, tp=self.tp_import)

        Entry(self.tp_import, border=0, font=self.formset_mainF, disabledbackground=self.colorList[9], state=DISABLED, disabledforeground=self.colorList[10]).place(x=590, y=270, width=149, height=35)
        Button(self.tp_import, text='Open Layout', command=lambda: self.open_layout(txt_head), justify=LEFT, font=(self.formset_mainF, 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6]).place(x=595, y=275, width=139, height=25)

        Entry(self.tp_import, border=0, font=self.formset_mainF, disabledbackground=self.colorList[9], state=DISABLED, disabledforeground=self.colorList[10]).place(x=740, y=270, width=149, height=35)
        Button(self.tp_import, text='Import Saved', command=lambda: self.import_layout(txt_head, self.tp_import), justify=LEFT, font=(self.formset_mainF, 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6]).place(x=745, y=275, width=139, height=25)

        Entry(self.tp_import, border=0, font=self.formset_mainF, disabledbackground=self.colorList[9], state=DISABLED, disabledforeground=self.colorList[10]).place(x=890, y=270, width=120, height=35)
        Button(self.tp_import, text='Import', command=save, justify=LEFT, font=(self.formset_mainF, 15), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6]).place(x=895, y=275, width=110, height=25)

    def open_layout(self, list_head):
        path = f"{self.temp_folder}\\ImportTemp.csv"
        # try:
        #     f = open(path, 'r')
        #     d = f.read()
        #     f.close()
        #
        #     if len(d) < 1:
        #         f = open(path, 'w')
        #         f.write(list_head)
        #         f.close()
        # except:
        f = open(path, 'w')
        f.write(list_head)
        f.close()
        os.startfile(path)

    def import_layout(self, txt_head, tp=None):
        path = f"{self.temp_folder}\\ImportTemp.csv"
        imp = self.import_csv(txt_head, path, tp)

        if imp:
            f = open(path, 'w')
            f.write('')
            f.close()

    def import_csv(self, txt_head, path=None, tp=None):
        if tp is None:
            tp == self.root

        def _imp():
            try:
                if path is None:
                    ff = filedialog.askopenfilename(parent=tp, title='Open CSV File', filetypes=(('CSV File', '*.csv'), ('All Files', '*.*')))
                else:
                    ff = path
                a_file = open(ff)
                rows = csv.reader(a_file)
                next(rows, None)
                rows = list(rows)
                try:
                    self.cur.execute(f"select id from {self.mainName.replace(' ', '_')}")
                    self.con.commit()
                    row = self.cur.fetchall()
                    for i in row:
                        for i in i:
                            pass
                    id_count = i + 1
                except:
                    id_count = int(self.formset_idStart)
                for i in rows:
                    a = ''
                    for j in range(len(i) - 1):
                        a += f",'{i[j + 1]}'"
                    self.cur.execute(f"insert into {self.mainName.replace(' ', '_')} values('" + str(id_count) + "'" + a + ")")
                    id_count += 1
                    self.con.commit()
                txt_success = f"[{self.mainName}] [Import Successful] {len(rows)} Records Found And Imported To Database Successfully"
                self.lbl_status.config(text=txt_success)
                Log_Generator().addLog(txt_success)
                self.Show()
                return True
            except Exception as ex:
                txt_error = f"[{self.mainName}] [Import Error] While Importing Record We Found Error: {ex}"
                self.lbl_status.config(text=txt_error)
                Log_Generator().addLog(txt_error)
                messagebox.showerror('[Import Error]', txt_error, parent=self.root)
                return False

        if self.cmnset_msgboxAimp == 'False':
            return _imp()
        else:
            msg = messagebox.askyesno('Are You Sure', "Are You Sure You Want To Import CSV File\nDon't Worry It's Not Delete Your Previous Data", parent=tp)
            if msg:
                messagebox.showinfo('Read Me', f"Make Sure Your First Row (Header) Is Empty Or With Column Names\nMake Sure Your First Column Is A Sr No Or Empty\nThe Program Not Copy First Row And First Column\nMake Sure Your Column Are Sorted According To\n{txt_head}", parent=tp)
                return _imp()

    def CallReportSet(self):
        self.repset_Lrep = self.getRepSetting(self.repset_Lrep)
        self.repset_Prep = self.getRepSetting(self.repset_Prep)
        f = open(f'{self.setting_folder}\\Pages Setting Report.sv', 'r')
        report_set = f.readlines()
        f.close()
        self.pgrepset_w, self.pgrepset_h, self.pgrepset_u = 210, 297, mm
        for i in report_set:
            mn, pgrepset_ = i.strip('\n').split(':')
            if mn == self.mainName:
                self.pgrepset_w, self.pgrepset_h,self.pgrepset_u = pgrepset_.split('.')

    def RefreshT(self, thread_):
        if thread_ == '1':
            x = threading.Thread(target=self.Refresh, args=(1,))
            x.start()
        elif thread_ == '0':
            Log_Generator().addLog(f'[{self.mainName}] [Refresh] Thread Stopped')

    def Refresh(self, thread_, force=False):
        try:
            self.root.update()
            self.mainW = self.root.winfo_width()
            self.mainH = self.root.winfo_height()
            if force:
                self.old_mainW = 0
                self.old_mainH = 0

            if self.old_mainW != self.mainW or self.old_mainH != self.mainH:
                self.old_mainW = self.mainW
                self.old_mainH = self.mainH

                if thread_ == 0:
                    self.RefreshId()
                    Log_Generator().addLog(f'[{self.mainName}] [After Refresh]\t[Root Width] {self.mainW}, [Root Height] {self.mainH}')

                self.CallCommonVar(1)

                self.detailFrameDemo.place_forget()
                self.detailFrameDemo.place_configure(x=self.dFbFstF_x, y=self.dFsF_y, width=self.dFbF_w, height=self.dF_h)

                self.vbarDetailFrame.place_forget()
                self.vbarDetailFrame.place(x=self.dFbF_w - 10, y=-12, width=10, height=self.dF_h + 24)

                self.buttonFrame.place_forget()
                self.buttonFrame.place(x=self.dFbFstF_x, y=self.bF_y, width=self.dFbF_w, height=self.bF_h)

                self.searchFrame.place_forget()
                self.searchFrame.place(x=self.dFbF_w + 1, y=self.dFsF_y, width=self.sF_w, height=self.sF_h)

                self.recordFrame.place_forget()
                self.recordFrame.place(x=self.rF_x, y=self.rF_y, width=self.rF_w, height=self.rF_h)

                self.statusFrame.place_forget()
                self.statusFrame.place(x=self.dFbFstF_x, y=self.stF_y, width=self.stF_w, height=self.stF_h)

                self.txt_search.place_forget()
                self.txt_search.place_configure(x=162, y=10, height=self.sF_h - 20, width=self.sF_w - 150 - 20 - 2)

                self.lbl_status.place_forget()
                self.lbl_status.place_configure(x=0, y=0, width=self.stF_w, height=self.stF_h)

            if thread_ == 1:
                if self.cmnset_refT == 'True':
                    self.root.after(int(self.cmnset_refA), lambda: self.RefreshT('1'))
                elif self.cmnset_refT == 'False':
                    self.root.after(int(self.cmnset_refA), lambda: self.RefreshT('0'))
        except:
            pass

    def ResetlblStaT(self, thread_):
        if thread_ == '1':
            x = threading.Thread(target=self.ResetlblSta, args=(1,))
            x.start()

    def ResetlblSta(self, thread_):
        try:
            self.lbl_status.config(text='')
            if thread_ == 1:
                if self.formset_resetStatus == 'True':
                    self.root.after(3000, lambda: self.ResetlblStaT('1'))
        except:
            pass

    def EnableDb(self):
        try:
            db_type = self.dbconfig_db

            if db_type == 'sqlite':
                try:
                    self.con = sqlite3.connect(database=self.database)
                    self.cur = self.con.cursor()
                    self.status(f'[{self.mainName}] [Database] Connected with sqlite')

                    try:
                        self.StarterDb()
                        self.status(f'[{self.mainName}] [Database] Enabled')
                    except Exception as e:
                        self.status(f'[{self.mainName}] [Database Error] {e}')

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
                        self.status(f'[{self.mainName}] [Database] Connected with mysql')
                    except Exception as e:
                        self.cur.execute(f'create database {self.dbdbconfig_dbname}')
                        self.cur.execute(f'use {self.dbdbconfig_dbname}')
                        self.status(f'[{self.mainName}] [Database] Created and Connected with mysql')

                    try:
                        self.StarterDb('mysql')
                        self.status(f'[{self.mainName}] [Database] Enabled')
                    except Exception as e:
                        self.status(f'[{self.mainName}] [Database Error] {e}')
                except Exception as e:
                    self.status(f'[{self.mainName}] [Database Error] Enter Correct Database Credentials We are not able to Login Database\n\nContact With Creator +923150490481', True, 'Error', 'Database Error')
                    # Call DB Settings
            else:
                self.status(f'[{self.mainName}] [Database Error] Select Database We Cannot Find Any Database And its Setting\n\nContact With Creator +923150490481', True, 'Error', 'Database Error')
                # Call DB Settings
        except Exception as e:
            self.status(f'[{self.mainName}] [Database Error] {e}\n\nContact With Creator +923150490481', True, 'Error', 'Database Error')

    def DisableDb(self):
        try:
            self.cur.close()
            self.con.close()
            self.status(f"[{self.mainName}] [Database] Database Disabled Successfully")
        except Exception as ex:
            self.status(f"[{self.mainName}] [Database] Database Already Closed Error: {ex}", True, 'Error', 'Database Error')

    def delete_Table(self):
        permission = True
        if permission:
            r = messagebox.askyesno('Are You Sure', "Are You Sure You Want To Remove All Data Of This Form\tDon't Worry It Does Not Remove All Forms", parent=self.root)
            if r:
                try:
                    self.cur.execute(f"Drop Table {self.mainName.replace(' ', '_')}")
                    self.con.commit()
                    r_ = messagebox.askyesno('Success', f"All Data Were Removed From {self.mainName} Table\tAre You Want To Recreate Empty {self.mainName} Table Again", parent=self.root)
                    if r_:
                        self.EnableDb()
                        self.Clear()
                except Exception as e:
                    self.status(f'Not Found Table\t{e}')
        else:
            messagebox.askyesno('Need Permission', f"You Don't Have enough Permission to Delete All Data From {self.mainName}", parent=self.root)

    def accessableButtons(self):
        #           Add Update Delete Import Export
        buttons = ['True', 'True', 'True', 'True', 'True']
        cnt = 0
        for i in buttons:
            if i == 'True':
                cnt += 1
        return buttons, cnt

    def msglog(self, cnt, pth=None, tp=None, exp='Exported', path=True, open_file=True):
        if path:
            txt_success = f'[{self.mainName}] [Export] {cnt} Record Found And {exp} At {pth} Successfully'
        else:
            txt_success = f'[{self.mainName}] [Export] {cnt} Record Found And {exp} Successfully'

        if self.cmnset_msgboxAexp == 'True':
            if tp is not None:
                messagebox.showinfo('[Export Successfully]', txt_success, parent=tp)
            else:
                messagebox.showinfo('[Export Successfully]', txt_success, parent=self.root)

        self.lbl_status.config(text=txt_success)
        Log_Generator().addLog(txt_success)

        if open_file:
            if self.repset_oras == 'True':
                os.startfile(pth)

    def status(self, txt, msg=False, show='Info', title=None):
        Log_Generator().addLog(txt)
        try:
            self.lbl_status.config(text=txt)
        except: pass
        if msg:
            if show == 'Info':
                messagebox.showinfo(title, txt, parent=self.root)
            elif show == 'Warning':
                messagebox.showwarning(title, txt, parent=self.root)
            else:
                messagebox.showerror(title, txt, parent=self.root)

    def convertToNo(self, e, var):
        o = var.get()
        if o != '':
            n = ''
            for i in o:
                try:
                    n += str(int(i))
                except:
                    pass
        else:
            n = '0'
        var.set(n)

    def GetNumber(self, var):
        try:
            n = int(var.get())
        except:
            n = 0
        return n

    @staticmethod
    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    @staticmethod
    def __getListVar__(lvar):
        lval = []
        for i in lvar:
            lval.append(i.get())
        return lval

    def getRepSetting(self, setting):
        setting_ = False
        for i in setting:
            if i == self.mainName:
                setting_ = True
                break
        return setting_

    def __listTotxt__(self, list, sep=', '):
        txt = ''
        for i in list: txt += i + sep
        return txt.rstrip(sep)

    @staticmethod
    def list_nd_Add(lis, var, outVar):
        ls = var.get().replace(', ', '')
        p = True
        for i in range(lis.size()):
            if ls != lis.get(i):
                p = False
            else:
                p = True
                break

        if not p:
            if ls != "" and ls.strip('\t') != '':
                lis.insert(END, ls)
                var.set('')

        items = ''
        for i in range(lis.size()):
            items+= lis.get(i) + ', '
        items = items.strip(', ')
        outVar.set(items)

    @staticmethod
    def list_ndc_Add(lis, var, outVar, cmbVal, cmb):
        ls = var.get().replace(', ', '')
        p = True
        for i in range(lis.size()):
            if ls != lis.get(i):
                p = False
            else:
                p = True
                break

        if not p:
            if ls != "" and ls.strip('\t') != '':
                lis.insert(END, ls)

        items = ''
        itemsL = []
        for i in range(lis.size()):
            itemsL.append(lis.get(i))
            items += lis.get(i) + ', '
        items = items.strip(', ')
        outVar.set(items)

        cmb.set("")
        var.set("")
        cmb.delete(cmb.get())
        without_bracket = []
        fetch = [item for item in cmbVal if item not in itemsL]
        for i in fetch:
            without_bracket.append(str(i))
        without_bracket = list(dict.fromkeys(without_bracket))
        without_bracket.sort()
        cmb.config(values=without_bracket)
        cmb.set_completion_list(without_bracket)

    @staticmethod
    def list_Add(lis, var, outVar):
        ls = var.get().replace(', ', '')
        if ls != "" and ls.strip('\t') != '':
            lis.insert(END, ls)
            var.set('')

        items = ''
        for i in range(lis.size()):
            items+= lis.get(i) + ', '
        items = items.strip(', ')
        outVar.set(items)

    @staticmethod
    def list_ndc_Del(lis, outVar, var, cmbVal, cmb):
        try:
            ls_index = lis.curselection()[0]
            lis.delete(ls_index)

            items = ''
            itemsL = []
            for i in range(lis.size()):
                items += lis.get(i) + ', '
                itemsL.append(lis.get(i))
            items = items.strip(', ')
            outVar.set(items)

            cmb.set("")
            var.set("")
            cmb.delete(cmb.get())
            without_bracket = []
            fetch = [item for item in cmbVal if item not in itemsL]
            for i in fetch:
                without_bracket.append(str(i))
            without_bracket = list(dict.fromkeys(without_bracket))
            without_bracket.sort()
            cmb.config(values=without_bracket)
            cmb.set_completion_list(without_bracket)
        except:
            pass

    @staticmethod
    def list_Del(lis, outVar):
        try:
            ls_index = lis.curselection()[0]
            lis.delete(ls_index)

            items = ''
            for i in range(lis.size()):
                items += lis.get(i) + ', '
            items = items.strip(', ')
            outVar.set(items)
        except:
            pass

    @staticmethod
    def bindList(lis, var, outVar):
        var.set('')
        items = outVar.get()
        items = items.split(', ')
        lis.delete(0, END)
        for i in items:
            lis.insert(END, i)

    @staticmethod
    def bindList_ndc(lis, var, outVar, cmbVal, cmb, split=None):
        var.set('')
        items = outVar.get()
        items = items.split(', ')
        lis.delete(0, END)
        for i in items:
            lis.insert(END, i)
        itemsL = []
        for i in range(lis.size()):
            itemsL.append(lis.get(i))
            items += lis.get(i) + ', '

        if split == None:
            cmb.set("")
            var.set("")
            cmb.delete(cmb.get())
            without_bracket = []
            fetch = [item for item in cmbVal if item not in itemsL]
            for i in fetch:
                without_bracket.append(str(i))
            without_bracket = list(dict.fromkeys(without_bracket))
            without_bracket.sort()
            cmb.config(values=without_bracket)
            cmb.set_completion_list(without_bracket)
        else:
            cmb.set("")
            var.set("")
            cmb.delete(cmb.get())
            without_bracket = []
            fetch = []
            if len(itemsL) != 0 and itemsL != ['']:
                for i in cmbVal:
                    a = False
                    for j in itemsL:
                        try:
                            j, _ = j.split(split)
                            if i == j:
                                a = False
                                break
                            elif i != j:
                                a = True
                        except:
                            pass
                    if a:
                         fetch.append(i)
            else:
                fetch = cmbVal

            for i in fetch:
                without_bracket.append(str(i))
            without_bracket = list(dict.fromkeys(without_bracket))
            without_bracket.sort()
            cmb.config(values=without_bracket)
            cmb.set_completion_list(without_bracket)

    def removeDuplicatesTreeview(self, tree):
        items = tree.get_children()
        unique_items = set()
        duplicates = []

        for item in items:
            values = tuple(tree.item(item)['values'])  # Convert list to tuple
            if values not in unique_items:
                unique_items.add(values)
            else:
                duplicates.append(item)

        for duplicate in duplicates:
            tree.delete(duplicate)

    def getFormsName(self):
        list_of_libFiles = os.listdir(self.library_folder)
        list_of_Forms = [x for x in list_of_libFiles if x.endswith('_frm.py')]
        list_of_Forms.sort(reverse=True)

        names_of_forms = []
        # Iterate over each name and modify it as required
        for name in list_of_Forms:
            # Remove the "_frm.py" suffix and replace underscores with spaces
            s = name.replace('_frm.py', '').replace('_', ' ')
            # Split the string with spaces if the next letter is capital
            modified_s = s[0]
            for i in range(1, len(s)):
                if s[i].isupper() and s[i - 1] != ' ':
                    modified_s += ' '
                modified_s += s[i]
            names_of_forms.append(modified_s)
        return names_of_forms

    def getFuncList(self):
        return ['Add', 'Update', 'Delete', 'Import', 'Export', 'Delete All']

    def open_libForm(self, name):
        obj_toplevel = Toplevel(self.root)
        self.libFormList[name](obj_toplevel, libFormList=self.libFormList)

    def get_combo_list(self, query, cmb, var, set_none=[], addAnotherValue=[]):
        try:
            self.cur.execute(query)
            for i in set_none:
                i[0].set("")
                i[1].set("")
                i[0].delete(i[0].get())
            cmb.set("")
            var.set("")
            cmb.delete(cmb.get())
            fetch = self.cur.fetchall()
            without_bracket = []
            for i in fetch:
                without_bracket.append(str(i[0]))
                try:without_bracket.extend(addAnotherValue)
                except:pass
                without_bracket = list(dict.fromkeys(without_bracket))
                without_bracket.sort()
                cmb.config(values=without_bracket)
                cmb.set_completion_list(without_bracket)
            self.con.commit()
        except Exception as e:
            messagebox.showerror('Error', e, parent=self.root)

    def set_combo_text(self, query, var, cmb, var_list, call=False):
        def set_(query, var, var_list):
            try:
                self.cur.execute(query.replace('{var}', var.get()))
                fetch = self.cur.fetchall()
                self.con.commit()
                for c, i in enumerate(var_list):
                    i.set(fetch[0][c])
            except Exception as e:
                self.status(f"[{self.mainName}] [Combobox Select Error] We Found Error: {e}", True, 'Error', 'Combobox Select Error')
        if call:
            set_(query, var, var_list)
        else:
            cmb.bind('<<ComboboxSelected>>', lambda _: set_(query, var, var_list))

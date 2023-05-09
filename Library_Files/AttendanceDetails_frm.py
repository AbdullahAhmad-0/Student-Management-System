try:
    from Autocomplete_Combo import AutocompleteCombobox
    from Log_Generator import Log_Generator
    from Top_Func import Func
    from ColorScheme import ColorScheme
    from FormRun import *
    from FormCommon import *
except:
    from Library_Files.Autocomplete_Combo import AutocompleteCombobox
    from Library_Files.Log_Generator import Log_Generator
    from Library_Files.Top_Func import Func
    from Library_Files.ColorScheme import ColorScheme
    from Library_Files.FormRun import *
    from Library_Files.FormCommon import *


class AttendanceDetails(BeforeInIt, AllSettings, CommonFunction):
    wSize, hSize = 800, 550
    title = "Attendance Details - Student Management System"
    mainName = "Attendance Details"

    def __init__(self, wind, libFormList=[]) -> None:
        BeforeInIt.__init__(self)
        AllSettings.__init__(self)
        super().__init__()
        self.root = wind
        self.sortKey = 'x[0]'
        self.split_pdf_rep = {}
        self.split_pdf_rep_auto = True
        self.split_pdf_rep_auto_len = 15
        self.CommonCall()
        self.libFormList = libFormList

        y_space = int(self.formset_yInF)  # 30 for 20 fields limit 40 for 15 fields limit
        self.dF_ent_w = int(self.formset_wOfF)
        self.dF_ent_x = int(self.formset_xOfF)

        frm_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=20)
        frm_.pack(fill=BOTH, expand=True)

        frm_id = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_id.pack(fill=BOTH, expand=True)
        lbl_id = Label(frm_id, text='ID', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_id.place(x=10, y=1)
        ent_id = Entry(frm_id, textvariable=self.var_id, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, border=0, font=self.formset_mainF)
        ent_id.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_date_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_date_.pack(fill=BOTH, expand=True)
        lbl_date_ = Label(frm_date_, text='Date', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_date_.place(x=10, y=1)
        ent_date_ = DateEntry(frm_date_, textvariable=self.var_date_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12], justify=CENTER, date_pattern='dd-mm-y')
        ent_date_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w - 10, height=self.formset_fieldH)
        def cls_date_():
            self.var_date_.set("")
            ent_date_.update()
        btn_date_ = Button(frm_date_, command=cls_date_, justify=LEFT, text='-', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_date_.place(x=self.dF_ent_x + self.dF_ent_w - 10, y=1, width=10, height=self.formset_fieldH)

        frm_time_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_time_.pack(fill=BOTH, expand=True)
        lbl_time_ = Label(frm_time_, text='Time', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_time_.place(x=10, y=1)
        ent_time_ = Entry(frm_time_, textvariable=self.var_time_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_time_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_status_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_status_.pack(fill=BOTH, expand=True)
        lbl_status_ = Label(frm_status_, text='Status', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_status_.place(x=10, y=1)
        cmb_status__list = ['In', 'Out']
        cmb_status_ = AutocompleteCombobox(frm_status_, values=cmb_status__list, textvariable=self.var_status_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_status_.set_completion_list(cmb_status__list)
        cmb_status_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_status_)
        cmb_status_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)
        cmb_status_.current(0)

        frm_sroll_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_sroll_.pack(fill=BOTH, expand=True)
        lbl_sroll_ = Label(frm_sroll_, text='Student Roll Number', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_sroll_.place(x=10, y=1)
        cmb_sroll__list = ['']
        cmb_sroll_ = AutocompleteCombobox(frm_sroll_, values=cmb_sroll__list, textvariable=self.var_sroll_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_sroll_.set_completion_list(cmb_sroll__list)
        cmb_sroll_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_sroll_)
        cmb_sroll_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w - 21, height=self.formset_fieldH)
        btn_sroll_ = Button(frm_sroll_, command=lambda: self.get_combo_list("select sroll_ from Student_Form", cmb_sroll_, self.var_sroll_), justify=LEFT, text='🔃', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_sroll_.place(x=self.dF_ent_x + self.dF_ent_w - 21, y=1, width=10, height=self.formset_fieldH)
        btn_sroll_ = Button(frm_sroll_, command=lambda: self.open_libForm('Student Form'), justify=LEFT, text='+', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_sroll_.place(x=self.dF_ent_x + self.dF_ent_w - 10, y=1, width=10, height=self.formset_fieldH)
        self.get_combo_list("select sroll_ from Student_Form", cmb_sroll_, self.var_sroll_)
        self.set_combo_text("select name_,technology_,class_,shift_ from Student_Form where sroll_='{var}'", self.var_sroll_, cmb_sroll_, [self.var_student_, self.var_technology_, self.var_class_, self.var_shift_])
        cmb_sroll_.current(0)

        frm_student_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_student_.pack(fill=BOTH, expand=True)
        lbl_student_ = Label(frm_student_, text='Student Name', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_student_.place(x=10, y=1)
        ent_student_ = Entry(frm_student_, textvariable=self.var_student_, border=0, font=self.formset_mainF, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_student_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_technology_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_technology_.pack(fill=BOTH, expand=True)
        lbl_technology_ = Label(frm_technology_, text='Technology', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_technology_.place(x=10, y=1)
        ent_technology_ = Entry(frm_technology_, textvariable=self.var_technology_, border=0, font=self.formset_mainF, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_technology_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_class_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_class_.pack(fill=BOTH, expand=True)
        lbl_class_ = Label(frm_class_, text='Class', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_class_.place(x=10, y=1)
        ent_class_ = Entry(frm_class_, textvariable=self.var_class_, border=0, font=self.formset_mainF, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_class_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_shift_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_shift_.pack(fill=BOTH, expand=True)
        lbl_shift_ = Label(frm_shift_, text='Shift', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_shift_.place(x=10, y=1)
        ent_shift_ = Entry(frm_shift_, textvariable=self.var_shift_, border=0, font=self.formset_mainF, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_shift_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        self.CommonCall2()

        # Record Frame
        self.recordFrame = Frame(self.root, bg=self.colorList[2])
        self.recordFrame.place(x=self.rF_x, y=self.rF_y, width=self.rF_w, height=self.rF_h)

        scroll_y = Scrollbar(self.recordFrame, orient=VERTICAL)
        scroll_x = Scrollbar(self.recordFrame, orient=HORIZONTAL)

        self.Table = ttk.Treeview(self.recordFrame, columns=['id', 'date_', 'time_', 'status_', 'sroll_', 'student_', 'technology_', 'class_', 'shift_'], yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.Table.yview)
        scroll_x.config(command=self.Table.xview)
        self.Table.heading('id', text='ID')
        self.Table.heading('date_', text='Date')
        self.Table.heading('time_', text='Time')
        self.Table.heading('status_', text='Status')
        self.Table.heading('sroll_', text='Student Roll Number')
        self.Table.heading('student_', text='Student Name')
        self.Table.heading('technology_', text='Technology')
        self.Table.heading('class_', text='Class')
        self.Table.heading('shift_', text='Shift')
        self.Table["show"] = "headings"
        self.Table.column('id', width=50)
        self.Table.column('date_', width=100)
        self.Table.column('time_', width=100)
        self.Table.column('status_', width=100)
        self.Table.column('sroll_', width=100)
        self.Table.column('student_', width=100)
        self.Table.column('technology_', width=100)
        self.Table.column('class_', width=100)
        self.Table.column('shift_', width=100)
        self.Table.pack(fill=BOTH, expand=True)

        self.CommonCall3()

    def _Add(self, e): self.Add()
    def _Update(self, e): self.Update()
    def _Delete(self, e): self.Delete()
    def _Clear(self, e): self.Clear()
    def _Import(self, e): self.Import()
    def _Export(self, e): self.Export()

    def Variables(self):
        # Variables
        self.var_id = StringVar()  # id serial Number
        self.var_date_ = StringVar()  # Date
        self.var_time_ = StringVar()  # Time
        self.var_status_ = StringVar()  # Status
        self.var_sroll_ = StringVar()  # Student Roll Number
        self.var_student_ = StringVar()  # Student Name
        self.var_technology_ = StringVar()  # Technology
        self.var_class_ = StringVar()  # Class
        self.var_shift_ = StringVar()  # Shift

    def Export_def(self):
        gg = self.Table.get_children()
        id = []
        date_ = []
        time_ = []
        status_ = []
        sroll_ = []
        student_ = []
        technology_ = []
        class_ = []
        shift_ = []
        count = 0
        for i in gg:
            content = self.Table.item(i)
            pp = content['values']
            count += 1
            id.append(str(count))
            date_.append(pp[1])
            time_.append(pp[2])
            status_.append(pp[3])
            sroll_.append(pp[4])
            student_.append(pp[5])
            technology_.append(pp[6])
            class_.append(pp[7])
            shift_.append(pp[8])

        headings = self.__list__('head')
        expList = list(zip(id, date_, time_, status_, sroll_, student_, technology_, class_, shift_))
        Log_Generator().addLog(f'[Export] {count} Record Found')
        return count, headings, expList

    def Get_Data(self, e):
        try:
            f = self.Table.focus()
            content = (self.Table.item(f))
            row = content['values']
            self.var_id.set(row[0])
            self.var_date_.set(row[1])
            self.var_time_.set(row[2])
            self.var_status_.set(row[3])
            self.var_sroll_.set(row[4])
            self.var_student_.set(row[5])
            self.var_technology_.set(row[6])
            self.var_class_.set(row[7])
            self.var_shift_.set(row[8])

            self.status(f'[{self.mainName}] [Get Data] Record {self.var_id.get()} Selected Successfully')
        except Exception as ex:
            self.status(f'[{self.mainName}] [Get Data] Error: {ex}')
            pass

    def StarterDb(self, db='sqlite'):
        if db == 'sqlite':
            self.cur.execute('''CREATE TABLE IF NOT EXISTS "''' + self.mainName.replace(' ', '_') + '''" (
                "id"	INTEGER NOT NULL UNIQUE,
                "date_"	TEXT,
                "time_"	TEXT,
                "status_"	TEXT,
                "sroll_"	TEXT,
                "student_"	TEXT,
                "technology_"	TEXT,
                "class_"	TEXT,
                "shift_"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT))''')
            self.con.commit()
        else:
            self.cur.execute(
                '''CREATE TABLE IF NOT EXISTS ''' + self.mainName.replace(' ', '_') + ''' (
                id SERIAL NOT NULL AUTO_INCREMENT
                , date_ TEXT NOT NULL
                , time_ TEXT NOT NULL
                , status_ TEXT NOT NULL
                , sroll_ TEXT NOT NULL
                , student_ TEXT NOT NULL
                , technology_ TEXT NOT NULL
                , class_ TEXT NOT NULL
                , shift_ TEXT NOT NULL )''')
            self.con.commit()

    def __list__(self, fetch):
        list_var = [self.var_id, self.var_date_, self.var_time_, self.var_status_, self.var_sroll_, self.var_student_, self.var_technology_, self.var_class_, self.var_shift_]
        list_shn = ['id', 'date_', 'time_', 'status_', 'sroll_', 'student_', 'technology_', 'class_', 'shift_']
        list_cvar = [[self.var_id, 'ID'], [self.var_date_, 'Date'], [self.var_time_, 'Time'], [self.var_status_, 'Status'], [self.var_sroll_, 'Student Roll Number'], [self.var_student_, 'Student Name'], [self.var_technology_, 'Technology'], [self.var_class_, 'Class'], [self.var_shift_, 'Shift']]
        list_head = ['ID', 'Date', 'Time', 'Status', 'Student Roll Number', 'Student Name', 'Technology', 'Class', 'Shift']
        list_headA = ['ID', 'Date', 'Time', 'Status', 'Student Roll Number', 'Student Name', 'Technology', 'Class', 'Shift']

        if fetch == 'var':
            return list_var
        elif fetch == 'cvar':
            return list_cvar
        elif fetch == 'shn':
            return list_shn
        elif fetch == 'head':
            return list_head
        elif fetch == 'headA':
            return list_headA

    def __bq__(self, q):
        if q == 'add':
            query = None
            return query
        elif q == 'update':
            query = None
            return query
        elif q == 'delete':
            query = None
            return query

    def __aq__(self, q):
        if q == 'add':
            query = None
            return query
        elif q == 'update':
            query = None
            return query
        elif q == 'delete':
            query = None
            return query


if __name__ == '__main__':
    root = Tk()
    obj = AttendanceDetails(root)
    root.mainloop()
    Log_Generator().closeLog()

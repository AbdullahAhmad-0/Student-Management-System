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


class Classes(BeforeInIt, AllSettings, CommonFunction):
    wSize, hSize = 800, 550
    title = "Classes - Student Management System"
    mainName = "Classes"

    def __init__(self, wind, libFormList=[]) -> None:
        BeforeInIt.__init__(self)
        AllSettings.__init__(self)
        super().__init__()
        self.root = wind
        self.sortKey = '(x[1], x[2])'
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

        frm_technology_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_technology_.pack(fill=BOTH, expand=True)
        lbl_technology_ = Label(frm_technology_, text='Technology', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_technology_.place(x=10, y=1)
        ent_technology_ = Entry(frm_technology_, textvariable=self.var_technology_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_technology_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_class_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_class_.pack(fill=BOTH, expand=True)
        lbl_class_ = Label(frm_class_, text='Class Name', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_class_.place(x=10, y=1)
        ent_class_ = Entry(frm_class_, textvariable=self.var_class_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_class_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_shift_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_shift_.pack(fill=BOTH, expand=True)
        lbl_shift_ = Label(frm_shift_, text='Shift', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_shift_.place(x=10, y=1)
        ent_shift_ = Entry(frm_shift_, textvariable=self.var_shift_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_shift_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_det_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_det_.pack(fill=BOTH, expand=True)
        lbl_det_ = Label(frm_det_, text='Details', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_det_.place(x=10, y=1)
        ent_det_ = Entry(frm_det_, textvariable=self.var_det_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_det_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        self.CommonCall2()

        # Record Frame
        self.recordFrame = Frame(self.root, bg=self.colorList[2])
        self.recordFrame.place(x=self.rF_x, y=self.rF_y, width=self.rF_w, height=self.rF_h)

        scroll_y = Scrollbar(self.recordFrame, orient=VERTICAL)
        scroll_x = Scrollbar(self.recordFrame, orient=HORIZONTAL)

        self.Table = ttk.Treeview(self.recordFrame, columns=['id', 'technology_', 'class_', 'shift_', 'det_'], yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.Table.yview)
        scroll_x.config(command=self.Table.xview)
        self.Table.heading('id', text='ID')
        self.Table.heading('technology_', text='Technology')
        self.Table.heading('class_', text='Class Name')
        self.Table.heading('shift_', text='Shift')
        self.Table.heading('det_', text='Details')
        self.Table["show"] = "headings"
        self.Table.column('id', width=50)
        self.Table.column('technology_', width=100)
        self.Table.column('class_', width=100)
        self.Table.column('shift_', width=100)
        self.Table.column('det_', width=250)
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
        self.var_technology_ = StringVar()  # Technology
        self.var_class_ = StringVar()  # Class Name
        self.var_shift_ = StringVar()  # Shift
        self.var_det_ = StringVar()  # Details

    def Export_def(self):
        gg = self.Table.get_children()
        id = []
        technology_ = []
        class_ = []
        shift_ = []
        det_ = []
        count = 0
        for i in gg:
            content = self.Table.item(i)
            pp = content['values']
            count += 1
            id.append(str(count))
            technology_.append(pp[1])
            class_.append(pp[2])
            shift_.append(pp[3])
            det_.append(pp[4])

        headings = self.__list__('head')
        expList = list(zip(id, technology_, class_, shift_, det_))
        Log_Generator().addLog(f'[Export] {count} Record Found')
        return count, headings, expList

    def Get_Data(self, e):
        try:
            f = self.Table.focus()
            content = (self.Table.item(f))
            row = content['values']
            self.var_id.set(row[0])
            self.var_technology_.set(row[1])
            self.var_class_.set(row[2])
            self.var_shift_.set(row[3])
            self.var_det_.set(row[4])

            self.status(f'[{self.mainName}] [Get Data] Record {self.var_id.get()} Selected Successfully')
        except Exception as ex:
            self.status(f'[{self.mainName}] [Get Data] Error: {ex}')
            pass

    def StarterDb(self, db='sqlite'):
        if db == 'sqlite':
            self.cur.execute('''CREATE TABLE IF NOT EXISTS "''' + self.mainName.replace(' ', '_') + '''" (
                "id"	INTEGER NOT NULL UNIQUE,
                "technology_"	TEXT,
                "class_"	TEXT,
                "shift_"	TEXT,
                "det_"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT))''')
            self.con.commit()
        else:
            self.cur.execute(
                '''CREATE TABLE IF NOT EXISTS ''' + self.mainName.replace(' ', '_') + ''' (
                id SERIAL NOT NULL AUTO_INCREMENT
                , technology_ TEXT NOT NULL
                , class_ TEXT NOT NULL
                , shift_ TEXT NOT NULL
                , det_ TEXT NOT NULL )''')
            self.con.commit()

    def __list__(self, fetch):
        list_var = [self.var_id, self.var_technology_, self.var_class_, self.var_shift_, self.var_det_]
        list_shn = ['id', 'technology_', 'class_', 'shift_', 'det_']
        list_cvar = [[self.var_id, 'ID'], [self.var_technology_, 'Technology'], [self.var_class_, 'Class Name'], [self.var_shift_, 'Shift']]
        list_head = ['ID', 'Technology', 'Class Name', 'Shift', 'Details']
        list_headA = ['ID', 'Technology', 'Class Name', 'Shift', 'Details']

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
    obj = Classes(root)
    root.mainloop()
    Log_Generator().closeLog()

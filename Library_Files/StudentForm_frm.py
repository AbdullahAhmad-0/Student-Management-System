import cv2
from pyzbar import pyzbar
import barcode
from barcode.writer import ImageWriter

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


class StudentForm(BeforeInIt, AllSettings, CommonFunction):
    wSize, hSize = 800, 550
    title = "Student Form - Student Management System"
    mainName = "Student Form"

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

        frm_note_1 = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=20)
        frm_note_1.pack(fill=BOTH, expand=True)
        lbl_note_1 = Label(frm_note_1, text='Note: Enter Roll No In This Format: "Class-Year-RollNo"', font=(self.formset_mainF, 10), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_note_1.place(x=10, y=1)

        frm_sroll_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_sroll_.pack(fill=BOTH, expand=True)
        lbl_sroll_ = Label(frm_sroll_, text='Roll No', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_sroll_.place(x=10, y=1)
        ent_sroll_ = Entry(frm_sroll_, textvariable=self.var_sroll_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_sroll_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_name_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_name_.pack(fill=BOTH, expand=True)
        lbl_name_ = Label(frm_name_, text='Student Name', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_name_.place(x=10, y=1)
        ent_name_ = Entry(frm_name_, textvariable=self.var_name_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_name_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_fname_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_fname_.pack(fill=BOTH, expand=True)
        lbl_fname_ = Label(frm_fname_, text='Father Name', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_fname_.place(x=10, y=1)
        ent_fname_ = Entry(frm_fname_, textvariable=self.var_fname_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_fname_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_phone_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_phone_.pack(fill=BOTH, expand=True)
        lbl_phone_ = Label(frm_phone_, text='Phone Number', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_phone_.place(x=10, y=1)
        ent_phone_ = Entry(frm_phone_, textvariable=self.var_phone_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_phone_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)

        frm_code_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_code_.pack(fill=BOTH, expand=True)
        lbl_code_ = Label(frm_code_, text='Code', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_code_.place(x=10, y=1)
        ent_code_ = Entry(frm_code_, textvariable=self.var_code_, border=0, font=self.formset_mainF, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_code_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w - 21, height=self.formset_fieldH)
        btn_code_ = Button(frm_code_, command=self.generateBarcode, justify=LEFT, text='💭', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_code_.place(x=self.dF_ent_x + self.dF_ent_w - 20, y=1, width=20, height=self.formset_fieldH)

        frm_technology_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_technology_.pack(fill=BOTH, expand=True)
        lbl_technology_ = Label(frm_technology_, text='Technology', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_technology_.place(x=10, y=1)
        cmb_technology__list = ['']
        cmb_technology_ = AutocompleteCombobox(frm_technology_, values=cmb_technology__list, textvariable=self.var_technology_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_technology_.set_completion_list(cmb_technology__list)
        cmb_technology_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_technology_)
        cmb_technology_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w - 21, height=self.formset_fieldH)
        btn_technology_ = Button(frm_technology_, command=lambda: self.get_combo_list("select technology_ from Classes", cmb_technology_, self.var_technology_), justify=LEFT, text='🔃', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_technology_.place(x=self.dF_ent_x + self.dF_ent_w - 21, y=1, width=10, height=self.formset_fieldH)
        btn_technology_ = Button(frm_technology_, command=lambda: self.open_libForm('Classes'), justify=LEFT, text='+', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_technology_.place(x=self.dF_ent_x + self.dF_ent_w - 10, y=1, width=10, height=self.formset_fieldH)
        self.get_combo_list("select technology_ from Classes", cmb_technology_, self.var_technology_)

        frm_class_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_class_.pack(fill=BOTH, expand=True)
        lbl_class_ = Label(frm_class_, text='Class', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_class_.place(x=10, y=1)
        cmb_class__list = ['']
        cmb_class_ = AutocompleteCombobox(frm_class_, values=cmb_class__list, textvariable=self.var_class_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_class_.set_completion_list(cmb_class__list)
        cmb_class_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_class_)
        cmb_class_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)
        def _technology_(e):technology_()
        def technology_():
            try:
                self.cur.execute(f"select class_ from Classes where technology_='" + self.var_technology_.get() + "'")
                cmb_class_.set("")
                self.var_class_.set("")
                cmb_class_.delete(cmb_class_.get())
                cmb_shift_.set("")
                self.var_shift_.set("")
                fetch = self.cur.fetchall()
                without_bracket = []
                for i in fetch:
                    without_bracket.append(str(i[0]))
                    without_bracket = list(dict.fromkeys(without_bracket))
                    without_bracket.sort()
                    cmb_class_.config(values=without_bracket)
                    cmb_class__list = without_bracket
                    cmb_class_.set_completion_list(cmb_class__list)
                self.con.commit()
            except Exception as e:
                Log_Generator().addLog(f'[Combobox Error] {e}')
                self.lbl_status.config(text=f'[Combobox Error] {e}')
        cmb_technology_.bind('<<ComboboxSelected>>', _technology_)

        frm_shift_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_shift_.pack(fill=BOTH, expand=True)
        lbl_shift_ = Label(frm_shift_, text='Shift', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_shift_.place(x=10, y=1)
        cmb_shift__list = ['']
        cmb_shift_ = AutocompleteCombobox(frm_shift_, values=cmb_shift__list, textvariable=self.var_shift_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_shift_.set_completion_list(cmb_shift__list)
        cmb_shift_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_shift_)
        cmb_shift_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)
        cmb_shift_.current(0)
        def _class_(e):class_()
        def class_():
            try:
                self.cur.execute(f"select shift_ from Classes where technology_='" + self.var_technology_.get() + "' and class_='" + self.var_class_.get() + "'")
                cmb_shift_.set("")
                self.var_shift_.set("")
                cmb_shift_.delete(cmb_shift_.get())
                fetch = self.cur.fetchall()
                without_bracket = []
                for i in fetch:
                    without_bracket.append(str(i[0]))
                    without_bracket = list(dict.fromkeys(without_bracket))
                    without_bracket.sort()
                    cmb_shift_.config(values=without_bracket)
                    cmb_shift__list = without_bracket
                    cmb_shift_.set_completion_list(cmb_shift__list)
                self.con.commit()
            except Exception as e:
                Log_Generator().addLog(f'[Combobox Error] {e}')
                self.lbl_status.config(text=f'[Combobox Error] {e}')
        cmb_class_.bind('<<ComboboxSelected>>', _class_)

        self.CommonCall2()

        # Record Frame
        self.recordFrame = Frame(self.root, bg=self.colorList[2])
        self.recordFrame.place(x=self.rF_x, y=self.rF_y, width=self.rF_w, height=self.rF_h)

        scroll_y = Scrollbar(self.recordFrame, orient=VERTICAL)
        scroll_x = Scrollbar(self.recordFrame, orient=HORIZONTAL)

        self.Table = ttk.Treeview(self.recordFrame, columns=['id', 'sroll_', 'name_', 'fname_', 'phone_', 'code_', 'technology_', 'class_', 'shift_'], yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.Table.yview)
        scroll_x.config(command=self.Table.xview)
        self.Table.heading('id', text='ID')
        self.Table.heading('sroll_', text='Roll No')
        self.Table.heading('name_', text='Student Name')
        self.Table.heading('fname_', text='Father Name')
        self.Table.heading('phone_', text='Phone Number')
        self.Table.heading('code_', text='Code')
        self.Table.heading('technology_', text='Technology')
        self.Table.heading('class_', text='Class')
        self.Table.heading('shift_', text='Shift')
        self.Table["show"] = "headings"
        self.Table.column('id', width=50)
        self.Table.column('sroll_', width=100)
        self.Table.column('name_', width=100)
        self.Table.column('fname_', width=100)
        self.Table.column('phone_', width=100)
        self.Table.column('code_', width=100)
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

    def generateBarcode(self):
        number = str(int(datetime.now().strftime("%S%d%m%Y%H%M")))[:13]
        ean = barcode.get('ean13', number, writer=ImageWriter())
        ean.save(f'{self.images_folder}\\TEMP_BARCODE')

        image = cv2.imread(f'{self.images_folder}\\TEMP_BARCODE.png')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        barcodes = pyzbar.decode(gray)
        if len(barcodes) > 0:
            barcode_ = barcodes[0]
            barcode_data = barcode_.data.decode("utf-8")
            self.var_code_.set(barcode_data)
        else:
            self.var_code_.set('ERROR WHILE GENERATING')

    # Example usage
    code = '1234567890123'  # 13-digit code
    filename = 'ean13_barcode.png'  # Output filename


    def Variables(self):
        # Variables
        self.var_id = StringVar()  # id serial Number
        self.var_sroll_ = StringVar()  # Roll No
        self.var_name_ = StringVar()  # Student Name
        self.var_fname_ = StringVar()  # Father Name
        self.var_phone_ = StringVar()  # Phone Number
        self.var_code_ = StringVar()  # Code
        self.var_technology_ = StringVar()  # Class
        self.var_class_ = StringVar()  # Class
        self.var_shift_ = StringVar()  # Shift

    def Export_def(self):
        gg = self.Table.get_children()
        id = []
        sroll_ = []
        name_ = []
        fname_ = []
        phone_ = []
        code_ = []
        technology_ = []
        class_ = []
        shift_ = []
        count = 0
        for i in gg:
            content = self.Table.item(i)
            pp = content['values']
            count += 1
            id.append(str(count))
            sroll_.append(pp[1])
            name_.append(pp[2])
            fname_.append(pp[3])
            phone_.append(pp[4])
            code_.append(pp[5])
            technology_.append(pp[6])
            class_.append(pp[7])
            shift_.append(pp[8])

        headings = self.__list__('head')
        expList = list(zip(id, sroll_, name_, fname_, phone_, code_, technology_, class_, shift_))
        Log_Generator().addLog(f'[Export] {count} Record Found')
        return count, headings, expList

    def Get_Data(self, e):
        try:
            f = self.Table.focus()
            content = (self.Table.item(f))
            row = content['values']
            self.var_id.set(row[0])
            self.var_sroll_.set(row[1])
            self.var_name_.set(row[2])
            self.var_fname_.set(row[3])
            self.var_phone_.set(row[4])
            self.var_code_.set(row[5])
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
                "sroll_"	TEXT,
                "name_"	TEXT,
                "fname_"	TEXT,
                "phone_"	TEXT,
                "code_"	TEXT,
                "technology_"	TEXT,
                "class_"	TEXT,
                "shift_"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT))''')
            self.con.commit()
        else:
            self.cur.execute(
                '''CREATE TABLE IF NOT EXISTS ''' + self.mainName.replace(' ', '_') + ''' (
                id SERIAL NOT NULL AUTO_INCREMENT
                , sroll_ TEXT NOT NULL
                , name_ TEXT NOT NULL
                , fname_ TEXT NOT NULL
                , phone_ TEXT NOT NULL
                , code_ TEXT NOT NULL
                , technology_ TEXT NOT NULL
                , class_ TEXT NOT NULL
                , shift_ TEXT NOT NULL )''')
            self.con.commit()

    def __list__(self, fetch):
        list_var = [self.var_id, self.var_sroll_, self.var_name_, self.var_fname_, self.var_phone_, self.var_code_, self.var_technology_, self.var_class_, self.var_shift_]
        list_shn = ['id', 'sroll_', 'name_', 'fname_', 'phone_', 'code_', 'technology_', 'class_', 'shift_']
        list_cvar = [[self.var_id, 'ID'], [self.var_sroll_, 'Roll No'], [self.var_name_, 'Student Name'], [self.var_fname_, 'Father Name'], [self.var_technology_, 'Technology'], [self.var_class_, 'Class'], [self.var_shift_, 'Shift']]
        list_head = ['ID', 'Roll No', 'Student Name', 'Father Name', 'Phone Number', 'Code', 'technology_', 'Class', 'Shift']
        list_headA = ['ID', 'Roll No', 'Student Name', 'Father Name', 'Phone Number', 'Code', 'technology_', 'Class', 'Shift']

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
    obj = StudentForm(root)
    root.mainloop()
    Log_Generator().closeLog()

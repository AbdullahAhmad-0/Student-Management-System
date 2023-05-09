from PIL import Image as ImagePIL, ImageDraw, ImageFont
from barcode import EAN13
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


class CardGenerator(BeforeInIt, AllSettings, CommonFunction):
    wSize, hSize = 800, 550
    title = "Card Generator - Student Management System"
    mainName = "Card Generator"

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

        frm_generate_ = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space)
        frm_generate_.pack(fill=BOTH, expand=True)
        lbl_generate_ = Label(frm_generate_, text='Generate', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_generate_.place(x=10, y=1)
        cmb_generate__list = ['Single Student', 'Multiple Student']
        cmb_generate_ = AutocompleteCombobox(frm_generate_, values=cmb_generate__list, textvariable=self.var_generate_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_generate_.set_completion_list(cmb_generate__list)
        cmb_generate_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_generate_)
        cmb_generate_.place(x=self.dF_ent_x, y=1, width=self.dF_ent_w, height=self.formset_fieldH)
        cmb_generate_.current(0)

        self.frm_single = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space * 6)
        y_ = 1
        lbl_sroll_ = Label(self.frm_single, text='Student Roll Number', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_sroll_.place(x=10, y=y_)
        cmb_sroll__list = ['']
        cmb_sroll_ = AutocompleteCombobox(self.frm_single, values=cmb_sroll__list, textvariable=self.var_sroll_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_sroll_.set_completion_list(cmb_sroll__list)
        cmb_sroll_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_sroll_)
        cmb_sroll_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 21, height=self.formset_fieldH)
        btn_sroll_ = Button(self.frm_single, command=lambda: self.get_combo_list("select sroll_ from Student_Form", cmb_sroll_, self.var_sroll_), justify=LEFT, text='🔃', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_sroll_.place(x=self.dF_ent_x + self.dF_ent_w - 21, y=y_, width=10, height=self.formset_fieldH)
        btn_sroll_ = Button(self.frm_single, command=lambda: self.open_libForm('Student Form'), justify=LEFT, text='+', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_sroll_.place(x=self.dF_ent_x + self.dF_ent_w - 10, y=y_, width=10, height=self.formset_fieldH)
        self.get_combo_list("select sroll_ from Student_Form", cmb_sroll_, self.var_sroll_)
        self.set_combo_text("select name_,technology_,class_,shift_,code_ from Student_Form where sroll_='{var}'", self.var_sroll_, cmb_sroll_, [self.var_name_, self.var_technology_, self.var_class_, self.var_shift_, self.var_code_])
        cmb_sroll_.current(0)

        y_ += y_space
        lbl_student_ = Label(self.frm_single, text='Student Name', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_student_.place(x=10, y=y_)
        ent_student_ = Entry(self.frm_single, textvariable=self.var_name_, border=0, font=self.formset_mainF, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_student_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w, height=self.formset_fieldH)

        y_ += y_space
        lbl_technology_ = Label(self.frm_single, text='Technology', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_technology_.place(x=10, y=y_)
        ent_technology_ = Entry(self.frm_single, textvariable=self.var_technology_, border=0, font=self.formset_mainF, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_technology_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w, height=self.formset_fieldH)

        y_ += y_space
        lbl_class_ = Label(self.frm_single, text='Class', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_class_.place(x=10, y=y_)
        ent_class_ = Entry(self.frm_single, textvariable=self.var_class_, border=0, font=self.formset_mainF, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_class_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w, height=self.formset_fieldH)

        y_ += y_space
        lbl_shift_ = Label(self.frm_single, text='Shift', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_shift_.place(x=10, y=y_)
        ent_shift_ = Entry(self.frm_single, textvariable=self.var_shift_, border=0, font=self.formset_mainF, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_shift_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w, height=self.formset_fieldH)

        y_ += y_space
        lbl_code_ = Label(self.frm_single, text='Code', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_code_.place(x=10, y=y_)
        ent_code_ = Entry(self.frm_single, textvariable=self.var_code_, border=0, font=self.formset_mainF, disabledbackground=self.colorList[14], disabledforeground=self.colorList[15], state=DISABLED, bg=self.colorList[9], fg=self.colorList[10], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        ent_code_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w, height=self.formset_fieldH)

        self.frm_multiple = Frame(self.detailFrame, bg=self.colorList[2], width=self.dFbF_w - 10, height=y_space * 3)
        y_ = 1
        lbl_technology_ = Label(self.frm_multiple, text='Technology', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_technology_.place(x=10, y=y_)
        cmb_technology__list = ['']
        cmb_technology_ = AutocompleteCombobox(self.frm_multiple, values=cmb_technology__list, textvariable=self.var_technology_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_technology_.set_completion_list(cmb_technology__list)
        cmb_technology_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_technology_)
        cmb_technology_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w - 21, height=self.formset_fieldH)
        btn_technology_ = Button(self.frm_multiple, command=lambda: self.get_combo_list("select technology_ from Classes", cmb_technology_, self.var_technology_), justify=LEFT, text='🔃', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_technology_.place(x=self.dF_ent_x + self.dF_ent_w - 21, y=y_, width=10, height=self.formset_fieldH)
        btn_technology_ = Button(self.frm_multiple, command=lambda: self.open_libForm('Classes'), justify=LEFT, text='+', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_technology_.place(x=self.dF_ent_x + self.dF_ent_w - 10, y=y_, width=10, height=self.formset_fieldH)
        self.get_combo_list("select technology_ from Classes", cmb_technology_, self.var_technology_,addAnotherValue=['All'])

        y_ += y_space
        lbl_class_ = Label(self.frm_multiple, text='Class', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_class_.place(x=10, y=y_)
        cmb_class__list = ['']
        cmb_class_ = AutocompleteCombobox(self.frm_multiple, values=cmb_class__list, textvariable=self.var_class_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_class_.set_completion_list(cmb_class__list)
        cmb_class_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_class_)
        cmb_class_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w, height=self.formset_fieldH)

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
                    cmb_class_.config(values=without_bracket + ['All'])
                    cmb_class__list = without_bracket
                    cmb_class_.set_completion_list(cmb_class__list + ['All'])
                self.con.commit()
            except Exception as e:
                Log_Generator().addLog(f'[Combobox Error] {e}')
                self.lbl_status.config(text=f'[Combobox Error] {e}')
        cmb_technology_.bind('<<ComboboxSelected>>', _technology_)

        y_ += y_space
        lbl_shift_ = Label(self.frm_multiple, text='Shift', font=self.formset_mainF, bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        lbl_shift_.place(x=10, y=y_)
        cmb_shift__list = ['']
        cmb_shift_ = AutocompleteCombobox(self.frm_multiple, values=cmb_shift__list, textvariable=self.var_shift_, font=self.formset_mainF, background=self.colorList[9], foreground=self.colorList[10])
        cmb_shift_.set_completion_list(cmb_shift__list)
        cmb_shift_.tk.eval(f'[ttk::combobox::PopdownWindow %s].f.l configure -background {self.colorList[13]}' % cmb_shift_)
        cmb_shift_.place(x=self.dF_ent_x, y=y_, width=self.dF_ent_w, height=self.formset_fieldH)
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
                    cmb_shift_.config(values=without_bracket + ['All'])
                    cmb_shift__list = without_bracket
                    cmb_shift_.set_completion_list(cmb_shift__list + ['All'])
                self.con.commit()
            except Exception as e:
                Log_Generator().addLog(f'[Combobox Error] {e}')
                self.lbl_status.config(text=f'[Combobox Error] {e}')
        cmb_class_.bind('<<ComboboxSelected>>', _class_)

        def single_student():
            try:self.frm_single.pack_forget()
            except:pass
            try:self.frm_multiple.pack_forget()
            except:pass
            self.frm_single.pack(fill=BOTH, expand=True)

        def multiple_student():
            try:self.frm_single.pack_forget()
            except:pass
            try:self.frm_multiple.pack_forget()
            except:pass
            self.frm_multiple.pack(fill=BOTH, expand=True)

        def _generate_(e):
            if self.var_generate_.get() == 'Single Student':
                single_student()
            if self.var_generate_.get() == 'Multiple Student':
                multiple_student()
        cmb_generate_.bind('<<ComboboxSelected>>', _generate_)
        _generate_('')

        # Button Frame
        self.buttonFrame = Frame(self.root, bg=self.colorList[3])
        self.buttonFrame.place(x=self.dFbFstF_x, y=self.bF_y, width=self.dFbF_w, height=self.bF_h)

        self.acessableBtns, acessableBtns_cnt = self.accessableButtons()
        self.bF_btn_w = int(self.dFbF_w / (acessableBtns_cnt + 1)) + 1
        self.bF_btn_h = self.bF_h
        self.bf_btn_x = 0
        self.bF_btn_y = 0

        btn_add = Button(self.buttonFrame, command=self.AddToList, justify=LEFT, text='Add', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_add.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        self.root.bind('<Return>', self._Add)

        btn_generate = Button(self.buttonFrame, command=self.Generate, justify=LEFT, text='Generate', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_generate.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        self.root.bind('<Control-g>', self._Generate)

        btn_delete = Button(self.buttonFrame, command=self.DeleteFromList, justify=LEFT, text='Delete', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_delete.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        self.root.bind('<Delete>', self.Delete)

        btn_clear = Button(self.buttonFrame, command=self.Clear, justify=LEFT, text='Clear', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_clear.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        self.root.bind('<Control-BackSpace>', self._Clear)

        btn_import = Button(self.buttonFrame, command=self.Import, justify=LEFT, text='Import', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_import.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        self.root.bind('<Control-i>', self._Import)
        self.root.bind('<Prior>', self._Import)

        btn_export = Button(self.buttonFrame, command=self.Export, justify=LEFT, text='Export', font=(self.formset_mainF, 13), bd=0, cursor='hand2', bg=self.colorList[5], activeforeground=self.colorList[22], activebackground=self.colorList[21], fg=self.colorList[6])
        btn_export.place(x=self.bf_btn_x + 1, y=self.bF_btn_y, width=self.bF_btn_w - 1, height=self.bF_btn_h)
        self.bf_btn_x += self.bF_btn_w
        self.root.bind('<Control-e>', self._Export)
        self.root.bind('<Next>', self._Export)

        # Search Frame
        self.searchFrame = Frame(self.root, bg=self.colorList[2])
        self.searchFrame.place(x=self.dFbF_w + 1, y=self.dFsF_y, width=self.sF_w, height=self.sF_h)

        Label(self.searchFrame, text='Student Names', font=(self.formset_mainHF, 20, 'bold'), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12]).pack(fill=BOTH, expand=True)

        # Record Frame
        self.recordFrame = Frame(self.root, bg=self.colorList[2])
        self.recordFrame.place(x=self.rF_x, y=self.rF_y, width=self.rF_w, height=self.rF_h)

        scroll_y = Scrollbar(self.recordFrame, orient=VERTICAL)
        scroll_x = Scrollbar(self.recordFrame, orient=HORIZONTAL)

        self.Table = ttk.Treeview(self.recordFrame, columns=['sroll_', 'name_', 'code_', 'technology_', 'class_', 'shift_'], yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.Table.yview)
        scroll_x.config(command=self.Table.xview)
        self.Table.heading('sroll_', text='Roll No')
        self.Table.heading('name_', text='Student Name')
        self.Table.heading('code_', text='Code')
        self.Table.heading('technology_', text='Technology')
        self.Table.heading('class_', text='Class')
        self.Table.heading('shift_', text='Shift')
        self.Table["show"] = "headings"
        self.Table.column('sroll_', width=100)
        self.Table.column('name_', width=100)
        self.Table.column('code_', width=100)
        self.Table.column('technology_', width=100)
        self.Table.column('class_', width=100)
        self.Table.column('shift_', width=100)
        self.Table.pack(fill=BOTH, expand=True)
        # Bind the delete event to the TreeView widget
        self.Table.bind('<Delete>', lambda event: self.DeleteFromList())

        self.CommonCall3()

    def _Add(self, e): self.AddToList()
    def _Generate(self, e): self.Generate()
    def _Delete(self, e): self.DeleteFromList()
    def _Clear(self, e): self.Clear()
    def _Import(self, e): self.Import()
    def _Export(self, e): self.Export()

    def generate_image_grid(self, row_count, column_count, folder_name):
        try:
            # Set the image size for each grid cell
            cell_width = 1011
            cell_height = 586

            # Get the list of image filenames from the 'IMAGES' folder
            image_folder = self.generated_folder
            image_filenames = os.listdir(image_folder)

            # Calculate the total number of images and pages
            image_count = len(image_filenames)
            page_count = (image_count - 1) // (row_count * column_count) + 1

            for page in range(page_count):
                # Create a new blank image for the current page
                grid_image = ImagePIL.new('RGB', (column_count * cell_width, row_count * cell_height))

                for i in range(row_count):
                    for j in range(column_count):
                        # Calculate the index of the current image
                        index = page * (row_count * column_count) + i * column_count + j

                        if index < image_count:
                            # Load the image and resize it to fit the cell size
                            image_filename = os.path.join(image_folder, image_filenames[index])
                            image = ImagePIL.open(image_filename)
                            image = image.resize((cell_width, cell_height))

                            # Paste the image into the grid at the current cell position
                            grid_image.paste(image, (j * cell_width, i * cell_height))

                # Save the grid image
                grid_image.save(f"{folder_name}/grid_page_{page+1}.png")
            self.status(f"[{self.mainName}] [Card Generating] Card Saved Successfully")
        except Exception as ex:
            self.status(f"[{self.mainName}] [Card Generating] We Found Error: {ex}", True, 'Error', 'Error')

    def Generate(self):
        try:
            self.remove_files_from_folder(self.generated_folder)
        except Exception as e: self.status(f'[{self.mainName}] [Remove Temp Cards] Error: {e}')

        def generate_barcode(code):
            try:
                barcode = EAN13(code, writer=ImageWriter())
                barcode_image = barcode.render()
                self.status(f"[{self.mainName}] [Card Generating] Barcode Generated On Card Successfully")
                return barcode_image
            except Exception as ex:
                self.status(f"[{self.mainName}] [Card Generating] We Found Error: {ex}", True, 'Error', 'Error')

        def add_text_to_image(image_path, output_path, fields=[]):
            # Open the image using Pillow
            image = ImagePIL.open(image_path)

            # Create a drawing object
            draw = ImageDraw.Draw(image)

            # Define the font size and font type
            font_size = 30
            font = ImageFont.truetype("arial", font_size)  # Replace "path_to_font.ttf" with the actual path to your font file

            # Define the position where the text will be drawn
            text1_position = (220, 370 - 10)
            text2_position = (220, 412 - 10)
            text3_position = (220, 453 - 10)
            text4_position = (220, 498 - 10)
            text5_position = (220, 540 - 10)

            # Define the color of the text (optional)
            text_color = (0, 0, 0)  # Black color

            # Add the text to the image
            draw.text(text1_position, str(fields[0]), font=font, fill=text_color)
            draw.text(text2_position, str(fields[1]), font=font, fill=text_color)
            draw.text(text3_position, str(fields[4]), font=font, fill=text_color)
            draw.text(text4_position, str(fields[5]), font=font, fill=text_color)
            draw.text(text5_position, str(fields[3]), font=font, fill=text_color)

            # Generate the barcode image
            barcode_image = generate_barcode(str(fields[2]))

            # Resize the barcode image to fit the original image
            barcode_image = barcode_image.resize((200, 100))

            # Calculate the position to place the barcode on the original image
            # x = 609
            # y = 358

            # Paste the barcode image onto the original image
            image.paste(barcode_image, (660, 340))

            # Save the modified image
            image.save(output_path)
            self.status(f"[{self.mainName}] [Card Generating] Card Designed Successfully")

        image_path = f"{self.images_folder}\Card Design.png"  # Replace "path_to_image.jpg" with the actual path to your image file

        items = self.Table.get_children()  # Get all items in the TreeView
        rows = []
        for item in items:
            text = self.Table.item(item)['values']  # Get the text of the item
            rows.append(text)  # Add the text to the data list
        success = 0
        fail = 0
        for sr, row in enumerate(rows):
            try:
                output_path = f"{self.generated_folder}\{sr}.png"  # Replace "output_image.jpg" with the desired output image path
                add_text_to_image(image_path, output_path, row)
                success += 1
            except: fail += 1
        folderName = filedialog.askdirectory(title='Select Folder Where To Paste', parent=self.root)
        self.generate_image_grid(int(self.cgcmset_rpp), int(self.cgcmset_cpp), folderName)
        self.status(f"[{self.mainName}] [Card Generating] Card Designed Successfully   Total Cards: {success + fail}  Successful: {success}  Error: {fail}")
        messagebox.showinfo('', f'Card Generated\nTotal Cards: {success + fail}\nSuccessful Generated: {success}\nError: {fail}', parent=self.root)

    @staticmethod
    def remove_files_from_folder(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def AddToList(self):
        if self.var_generate_.get() == 'Single Student':
            if self.var_sroll_.get() != '':
                self.Table.insert('', END, values=[self.var_sroll_.get(), self.var_name_.get(), self.var_code_.get(), self.var_technology_.get(), self.var_class_.get(), self.var_shift_.get()])
                self.Clear()
                self.removeDuplicatesTreeview(self.Table)
        elif self.var_generate_.get() == 'Multiple Student':
            fields = [['technology_', self.var_technology_.get()], ['class_', self.var_class_.get()], ['shift_', self.var_shift_.get()]]

            q_ = 'where'
            for i in fields:
                if i[1] != 'All' and i[1].strip() != '':
                    q_ += f" {i[0]} = '{i[1]}' and"
            q_ = q_.strip('').strip('and').strip('')
            if q_ != 'where':
                q = f'select sroll_,name_,code_,technology_,class_,shift_ from Student_Form {q_}'
            else:
                q = f'select sroll_,name_,code_,technology_,class_,shift_ from Student_Form'

            try:
                self.cur.execute(q)
                rows = self.cur.fetchall()
                try:
                    rows.sort(key=lambda x: eval(self.sortKey))
                except:
                    pass
                for row in rows:
                    self.Table.insert('', END, values=row)
                self.removeDuplicatesTreeview(self.Table)

                self.status(f"[{self.mainName}] [Fetch] Record Successfully")
            except Exception as ex:
                self.status(f"[{self.mainName}] [Fetch] We Found Error: {ex}", True, 'Error', 'Error')

    def DeleteFromList(self):
        selected_item = self.Table.selection()  # Get the selected item
        if selected_item:
            item_text = self.Table.item(selected_item)['text']  # Get the text of the selected item
            self.Table.delete(selected_item)  # Remove the item from the treeview

    def Variables(self):
        # Variables
        self.var_id = StringVar()  # id serial Number
        self.var_generate_ = StringVar()  # Generate
        self.var_sroll_ = StringVar()  # Roll No
        self.var_name_ = StringVar()  # Student Name
        self.var_code_ = StringVar()  # Code
        self.var_technology_ = StringVar()  # Technology
        self.var_class_ = StringVar()  # Class
        self.var_shift_ = StringVar()  # Shift

    def Export_def(self):
        gg = self.Table.get_children()
        id = []
        sroll_ = []
        name_ = []
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
            code_.append(pp[3])
            technology_.append(pp[4])
            class_.append(pp[5])
            shift_.append(pp[6])

        headings = self.__list__('head')
        expList = list(zip(id, sroll_, sroll_, name_, code_, technology_, class_, shift_))
        Log_Generator().addLog(f'[Export] {count} Record Found')
        return count, headings, expList

    def Show(self):
        pass

    def Get_Data(self, e):
        try:
            f = self.Table.focus()
            content = (self.Table.item(f))
            row = content['values']
            self.var_id.set(row[0])

            self.status(f'[{self.mainName}] [Get Data] Record {self.var_id.get()} Selected Successfully')
        except Exception as ex:
            self.status(f'[{self.mainName}] [Get Data] Error: {ex}')
            pass

    def StarterDb(self, db='sqlite'):
        pass

    def __list__(self, fetch):
        list_var = [self.var_id, self.var_sroll_, self.var_sroll_, self.var_name_, self.var_code_, self.var_technology_, self.var_class_, self.var_shift_]
        list_shn = ['id', 'sroll_', 'sroll_', 'name_', 'code_', 'technology_', 'class_', 'shift_']
        list_cvar = [[self.var_id, 'ID'], [self.var_sroll_, 'Generate'], [self.var_sroll_, 'Roll No'], [self.var_name_, 'Student Name'], [self.var_technology_, 'Technology'], [self.var_class_, 'Class'], [self.var_shift_, 'Shift']]
        list_head = ['ID', 'Generate', 'Roll No', 'Student Name', 'Code', 'Technology', 'Class', 'Shift']
        list_headA = ['ID', 'Generate', 'Roll No', 'Student Name', 'Code', 'Technology', 'Class', 'Shift']

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
        return None

    def __aq__(self, q):
        return None


if __name__ == '__main__':
    root = Tk()
    obj = CardGenerator(root)
    root.mainloop()
    Log_Generator().closeLog()

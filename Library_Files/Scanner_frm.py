import cv2
import pyzbar.pyzbar as pyzbar
from PIL import Image as ImagePIL, ImageTk
from playsound import playsound

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


class Scanner(BeforeInIt, AllSettings, CommonFunction):
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
        self.CommonCall(False, False)
        self.libFormList = libFormList

        # create the video capture object
        try:
            self.cgcmset_cam = int(self.cgcmset_cam)
        except:
            pass
        self.captureCV2 = cv2.VideoCapture(self.cgcmset_cam.strip())

        # create the video display
        self.videoCanvas = Label(self.root)
        self.videoCanvas.pack(padx=10, pady=10)

        # create the data display
        self.labelStatus = Label(self.root, font=("Courier", 24))
        self.labelStatus.pack(padx=10, pady=10)

        # create the barcode display
        self.labelStatus2 = Label(self.root, font=("Courier", 14))
        self.labelStatus2.place(x=0, y=0)

        # start the video update loop
        self.update_video()

        self.acessableBtns, _ = self.accessableButtons()
        self.CommonCall3()

    def Variables(self):
        # Variables
        self.var_id = StringVar()  # id serial Number

    def CommonCall3(self):
        # Status Frame
        self.statusFrame = Frame(self.root, bg=self.colorList[2])
        self.statusFrame.place(x=self.dFbFstF_x, y=self.stF_y, width=self.stF_w, height=self.stF_h)

        self.lbl_status = Label(self.statusFrame, text='Status:', anchor=W, justify=LEFT, font=(self.formset_mainF[0], 13), bg=self.colorList[7], fg=self.colorList[8], highlightbackground=self.colorList[11], highlightthickness=2, highlightcolor=self.colorList[12])
        self.lbl_status.place(x=0, y=0, width=self.stF_w, height=self.stF_h)

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        fileMenu = Menu(self.menubar)
        fileMenu = Menu(fileMenu, background=self.colorList[2])
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

    def read_barcodes(self, frame):
        # convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # use the pyzbar library to detect barcodes in the frame
        barcodes = pyzbar.decode(gray)

        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the barcode data
            barcode_data = barcode.data.decode("utf-8")

            # draw a rectangle around the barcode
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.labelStatus2.config(text=f'BarCode: {barcode_data}')

            # display the barcode data in the tkinter window
            self.cur.execute(f'select sroll_,name_,technology_,class_,shift_ from Student_Form where code_="{barcode_data}"')
            fetch = self.cur.fetchall()
            try:
                if len(fetch) != 0 or fetch[0][0] != '':
                    current_date = datetime.now().strftime('%d-%m-%Y')
                    self.cur.execute(f'select date_,time_,status_,sroll_ from Attendance_Details where sroll_="{fetch[0][0]}" and date_="{current_date}" ORDER BY id DESC LIMIT 1')
                    fetch2 = self.cur.fetchone()

                    # Refresh ID
                    try:
                        self.cur.execute(f"select id from Attendance_Details")
                        self.con.commit()
                        row = self.cur.fetchall()
                        for i in row:
                            for i in i:
                                pass
                        _id = i + 1
                    except:_id = int(self.formset_idStart)

                    if fetch2 is not None:
                        checkTime, diffTime = self.check_time_difference(fetch2[0], fetch2[1], True)
                        if not checkTime:
                            if fetch2[2] == 'Out':
                                checkTime = True
                            else:
                                if diffTime < timedelta(seconds=5):
                                    pass
                                else:
                                    self.labelStatus.config(text=f"Error 165: Already Added Before {diffTime}\n")
                                    self.errorMusic()
                        elif checkTime:
                            if fetch2[2] == 'In':
                                new_status = 'Out'
                            elif fetch2[2] == 'Out':
                                new_status = 'In'
                            current_date = datetime.now().strftime('%d-%m-%Y')
                            current_time = datetime.now().strftime('%H:%M:%S')
                            self.cur.execute(f"insert into Attendance_Details VALUES (?,?,?,?,?,?,?,?,?)",
                                             [_id, current_date, current_time, new_status, fetch[0][0], fetch[0][1], fetch[0][2], fetch[0][3], fetch[0][4]])
                            self.con.commit()
                            self.labelStatus.config(text=f'Attendance Marked {new_status}: {fetch[0][0]}\nCode: {barcode_data}')
                            self.successMusic()
                        else:
                            self.labelStatus.config(text=f'Error 170: Not Allowed To Exit From Collage')
                            self.errorMusic()
                    else:
                        new_status = 'In'
                        current_date = datetime.now().strftime('%d-%m-%Y')
                        current_time = datetime.now().strftime('%H:%M:%S')
                        self.cur.execute(f"insert into Attendance_Details VALUES (?,?,?,?,?,?,?,?,?)",
                                         [_id, current_date, current_time, new_status, fetch[0][0], fetch[0][1], fetch[0][2], fetch[0][3], fetch[0][4]])
                        self.con.commit()
                        self.labelStatus.config(text=f'Attendance Marked {new_status}: {fetch[0][0]}\nCode: {barcode_data}')
                        self.successMusic()
                else:
                    self.labelStatus.config(text=f'Error 191: Invalid Code No Record Found')
                    self.errorMusic()
            except Exception as e:
                self.labelStatus.config(text=f'Error 194: Invalid Code No Record Found\n{e}')
                self.errorMusic()

        # return the frame
        return frame

    def successMusic(self):
        threading.Thread(target=self.successMusic_).start()

    def successMusic_(self):
        try:playsound(f'{self.images_folder}/success.mp3')
        except:pass

    def errorMusic(self):
        threading.Thread(target=self.errorMusic_).start()

    def errorMusic_(self):
        try:playsound(f'{self.images_folder}/error.mp3')
        except:pass

    def update_video(self):
        # read a frame from the video stream
        ret, frame = self.captureCV2.read()

        if ret:
            # detect and read barcodes in the frame
            frame = self.read_barcodes(frame)

            # convert the frame to tkinter format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImagePIL.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)

            # update the video display
            self.videoCanvas.config(image=img)
            self.videoCanvas.image = img

        # schedule the next update
        self.root.after(10, self.update_video)

    def check_time_difference(self, date_str, time_str, det=None):
        # Get the current date and time
        current_datetime = datetime.now()

        # Parse the given date and time strings
        given_date = datetime.strptime(date_str, '%d-%m-%Y')
        given_time = datetime.strptime(time_str, '%H:%M:%S')

        # Combine the given date and time into a single datetime object
        given_datetime = given_date.replace(hour=given_time.hour, minute=given_time.minute, second=given_time.second)

        # Calculate the time difference
        time_diff = current_datetime - given_datetime

        # Check if the time difference is at least 1 hour
        if time_diff >= timedelta(hours=1):
            if det is not None:
                return True, time_diff
        else:
            if det is not None:
                return False, time_diff

    def Export_def(self):
        pass

    def Show(self):
        pass

    def Get_Data(self, e):
        pass

    def StarterDb(self, db='sqlite'):
        pass

    def __list__(self, fetch):
        return []

    def __bq__(self, q):
        return None

    def __aq__(self, q):
        return None


if __name__ == '__main__':
    root = Tk()
    obj = Scanner(root)
    root.mainloop()
    Log_Generator().closeLog()

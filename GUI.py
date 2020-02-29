from tkinter import *
from tkinter import messagebox


class Paint:
    def __init__(self, parent):
        self.parent = parent
        self.pixel = 20
        self.pencil_width = 20
        self.train_directory = 'Boolean_train'
        self.figures = []
        self.pixels = []
        self.matrix = []

        self.cnv = Canvas(self.parent, width=500, height=500)
        self.cnv.pack(side=LEFT)
        # Left toolbar_frame nearby canvas
        toolbar_frame = Frame(self.parent, bg='lightgrey', width=200, height=500)
        toolbar_frame.pack(side=RIGHT, fill=Y)
        # mini instructions for hotkeys
        label_hotkey = Label(toolbar_frame, text='R - delete all\n'
                                                 'E - show all figures(c)\n'
                                                 'Q - kill app\n'
                                                 'D - show matrix(c)\n'
                                                 'G - draw grid\n'
                                                 'F - convert img\n'
                                                 'TAB - confirm fs', bg='lightgrey', font=('Ubuntu', 15), justify=LEFT)
        label_hotkey.grid(row=0, columnspan=2)

        # frame which contains 'font' and entry for font
        frame_label = Frame(toolbar_frame)
        frame_label.grid(row=1, columnspan=2, pady=10)

        font_label = Label(frame_label, text='Font:', bg='lightgrey')
        font_label.grid(row=0, column=0)
        self.font_entry = Entry(frame_label)
        self.font_entry.grid(row=0, column=1, ipadx=15)
        self.font_entry.insert(0, self.pencil_width)

        # button toolbar sorted by rows
        btn_upper_font = Button(toolbar_frame, text='+', command=self.upper_font)
        btn_upper_font.grid(row=2, column=0, sticky='we', padx=5, pady=5)
        btn_lower_font = Button(toolbar_frame, text='-', command=self.lower_font)
        btn_lower_font.grid(row=2, column=1, sticky='we', padx=5, pady=5)

        btn_convert_img = Button(toolbar_frame, text='Convert', command=self.converting_func)
        btn_convert_img.grid(row=3, column=0, sticky=EW, padx=5, pady=5)
        btn_delete_img = Button(toolbar_frame, text=' Delete ', command=self.del_func)
        btn_delete_img.grid(row=3, column=1, sticky=EW, padx=5, pady=5)

        btn_recognise = Button(toolbar_frame, text='Recognise', command=print(2))  # need to do this func
        btn_recognise.grid(row=4, column=0, sticky=EW, padx=5, pady=5)
        btn_add_train = Button(toolbar_frame, text='Add train', command=self.add_train_func)  # need to update this
        btn_add_train.grid(row=4, column=1, sticky=EW, padx=5, pady=5)

        self.btn_mode_boolean = Button(toolbar_frame, text='Boolean mode', command=lambda: self.change_mode(True))
        self.btn_mode_boolean.configure(bg='lightblue')
        self.btn_mode_boolean.grid(row=5, column=0, sticky=EW, padx=5, pady=5)
        self.btn_mode_numbers = Button(toolbar_frame, text='Number mode', command=lambda: self.change_mode(False))
        self.btn_mode_numbers.grid(row=5, column=1, sticky=EW, padx=5, pady=5)

        btn_exit = Button(toolbar_frame, text='Exit', command=self.parent.destroy)
        btn_exit.grid(row=6, column=0, sticky=EW, padx=5, pady=5)

        self.font_entry.bind('<FocusOut>', self.change_font_entry)
        self.parent.bind('<r>', self.del_all)
        self.parent.bind('<e>', lambda event: print(self.figures))
        self.parent.bind('<q>', lambda event: self.parent.destroy())
        self.parent.bind('<d>', lambda event: print(self.matrix))
        self.parent.bind('<g>', self.draw_grid)
        self.parent.bind('<f>', self.fill_pixels)
        self.cnv.bind('<B1-Motion>', self.draw)

    def change_mode(self, mode):
        if mode:
            self.btn_mode_numbers.configure(bg='#F0F0F0')
            self.btn_mode_boolean.configure(bg='lightblue')
            self.train_directory = 'Boolean_train'
        else:
            self.btn_mode_boolean.configure(bg='#F0F0F0')
            self.btn_mode_numbers.configure(bg='lightblue')
            self.train_directory = 'Number_train'

    def add_train_func(self):
        save_form = Toplevel()
        save_form.resizable(False, False)
        save_form.title('Save new train data')

        ask_save_frame = Frame(save_form)
        ask_save_frame.grid(columnspan=2, pady=5, padx=5)
        ask_save_label = Label(ask_save_frame, text='What number was written?')
        ask_save_label.grid()
        ask_save_entry = Entry(ask_save_frame, width=5, justify=CENTER)
        ask_save_entry.grid(row=0, column=1)

        ask_save_btn_ok = Button(save_form, text='Ok', width=10)
        ask_save_btn_ok.grid(row=2, column=0, pady=5)
        ask_save_btn_cancel = Button(save_form, text='Cancel', width=10, command=save_form.destroy)
        ask_save_btn_cancel.grid(row=2, column=1, pady=5)
        # only GUI need to add func for save

    def del_func(self):
        self.del_all('this is useless, just ignore')

    def converting_func(self):
        self.fill_pixels('this is useless, just ignore')
        self.draw_grid('this is useless, just ignore')

    def change_font_entry(self, event):
        try:
            self.pencil_width = int(self.font_entry.get())
        except ValueError:
            messagebox.showerror(title='Error', message='You should enter the valid number')

    def upper_font(self):
        self.pencil_width += 4
        self.font_entry.delete(0, END)
        self.font_entry.insert(0, self.pencil_width)

    def lower_font(self):
        self.pencil_width -= 4
        self.font_entry.delete(0, END)
        self.font_entry.insert(0, self.pencil_width)

    def debug(self, event):
        for elem in self.figures:
            print(elem)

    def draw(self, event):
        self.figures.append((event.x + self.pencil_width,
                             event.y + self.pencil_width,
                             event.x - self.pencil_width,
                             event.y - self.pencil_width))

        self.cnv.create_oval(event.x + self.pencil_width,
                             event.y + self.pencil_width,
                             event.x - self.pencil_width,
                             event.y - self.pencil_width,
                             fill='black')
        objects = self.cnv.find_overlapping(0, 0, 10, 10)
        print(objects)

    def del_all(self, event):
        self.cnv.delete(ALL)
        self.matrix = []
        self.figures = []

    def draw_grid(self, event):
        for i in range(0, 500, self.pixel):
            self.cnv.create_line(i, 0, i, 500, width=1, fill='grey')
            self.cnv.create_line(0, i, 500, i, width=1, fill='grey')

    def fill_pixels(self, event):
        for pixel_x in range(0, 500, self.pixel):
            for pixel_y in range(0, 500, self.pixel):
                if self.cnv.find_overlapping(pixel_x + 1, pixel_y + 1, pixel_x + 19, pixel_y + 19):
                    self.cnv.create_rectangle(pixel_x, pixel_y, pixel_x + 19, pixel_y + 19, fill='blue')
                    self.matrix.append(1)
                else:
                    self.matrix.append(0)


root = Tk()
root.geometry('700x500')
root.resizable(False, False)
Paint(root)

root.mainloop()

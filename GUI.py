from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from Neural_Network import sigm
import numpy as np
import time
import pickle


class AppGUI:
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
        btn_upper_font = Button(toolbar_frame, text='+', command=self.upper_font_func)
        btn_upper_font.grid(row=2, column=0, sticky='we', padx=5, pady=5)
        btn_lower_font = Button(toolbar_frame, text='-', command=self.lower_font_func)
        btn_lower_font.grid(row=2, column=1, sticky='we', padx=5, pady=5)

        btn_convert_img = Button(toolbar_frame, text='Convert', command=self.converting_func)
        btn_convert_img.grid(row=3, column=0, sticky=EW, padx=5, pady=5)
        btn_delete_img = Button(toolbar_frame, text=' Delete ', command=self.del_func)
        btn_delete_img.grid(row=3, column=1, sticky=EW, padx=5, pady=5)

        btn_recognise = Button(toolbar_frame, text='Recognise',
                               command=lambda: AppGUI.recognise_func(self.matrix, self.prediction_label))  # TODO: need to do this func
        btn_recognise.grid(row=4, column=0, sticky=EW, padx=5, pady=5)
        btn_add_train = Button(toolbar_frame, text='Add train', command=self.add_train_func)
        btn_add_train.grid(row=4, column=1, sticky=EW, padx=5, pady=5)

        btn_recognise = Button(toolbar_frame, text='Open file', command=self.open_matrix)
        btn_recognise.grid(row=5, column=0, sticky=EW, padx=5, pady=5)
        btn_nn_control = Button(toolbar_frame, text='Open NN',
                                command=self.open_nn_control_func)  # TODO:need to update this
        btn_nn_control.grid(row=5, column=1, sticky=EW, padx=5, pady=5)

        self.btn_mode_boolean = Button(toolbar_frame, text='Boolean mode', command=lambda: self.change_mode_func(True))
        self.btn_mode_boolean.configure(bg='lightblue')
        self.btn_mode_boolean.grid(row=6, column=0, sticky=EW, padx=5, pady=5)
        self.btn_mode_numbers = Button(toolbar_frame, text='Number mode',
                                       command=lambda: self.change_mode_func(False))  # TODO: Number mode doesnt work
        self.btn_mode_numbers.grid(row=6, column=1, sticky=EW, padx=5, pady=5)

        self.prediction_label = Label(toolbar_frame, font=('Ubuntu', 15))
        self.prediction_label.grid(row=7, columnspan=2, sticky=EW, padx=5, pady=5)

        btn_recognise = Button(toolbar_frame, text='True', command=lambda: self.add_train_after_prediction(True))
        btn_recognise.grid(row=8, column=0, sticky=EW, padx=5, pady=5)
        btn_nn_control = Button(toolbar_frame, text='False', command=lambda: self.add_train_after_prediction(False))
        btn_nn_control.grid(row=8, column=1, sticky=EW, padx=5, pady=5)

        btn_exit = Button(toolbar_frame, text='Exit', command=self.parent.destroy)
        btn_exit.grid(row=9, column=0, sticky=EW, padx=5, pady=5)
        btn_auto_recog = Button(toolbar_frame, text='Auto-Recognise', command=self.auto_recognise_func)
        btn_auto_recog.grid(row=9, column=1, sticky=EW, padx=5, pady=5)

        # all binds
        self.font_entry.bind('<FocusOut>', self.change_font_entry_func)
        self.parent.bind('<r>', self.del_all)
        self.parent.bind('<e>', lambda event: print(self.figures))
        self.parent.bind('<q>', lambda event: self.parent.destroy())
        self.parent.bind('<d>', lambda event: print(self.matrix))
        self.parent.bind('<g>', self.draw_grid)
        self.parent.bind('<f>', self.fill_pixels)
        self.cnv.bind('<B1-Motion>', self.draw)

    def auto_recognise_func(self):
        self.converting_func()
        AppGUI.recognise_func(self.matrix, self.prediction_label)

    def add_train_after_prediction(self, pos):
        prediction = self.prediction_label['text']
        if pos:
            pos = bool(eval(prediction))
            self.save_train(boolean=pos, windowed=False)
        else:
            pos = bool(eval(prediction) - 1)
            self.save_train(boolean=pos, windowed=False)

    @staticmethod
    def recognise_func(data, label):
        f = open('weights.goose', 'rb')
        synaptic_weight = pickle.load(f)
        f.close()
        output = sigm(np.dot(data, synaptic_weight))
        if output > 0.5:
            label.configure(text='True')
        else:
            label.configure(text='False')

    def open_nn_control_func(self):
        nn_control = Toplevel(self.parent)
        # nn_control.resizable(False, False)

    def change_mode_func(self, mode):
        if mode:
            self.btn_mode_numbers.configure(bg='#F0F0F0')
            self.btn_mode_boolean.configure(bg='lightblue')
            self.train_directory = 'Boolean_train'
        else:
            self.btn_mode_boolean.configure(bg='#F0F0F0')
            self.btn_mode_numbers.configure(bg='lightblue')
            self.train_directory = 'Number_train'

    def open_matrix(self):
        step = -1
        file_name = filedialog.askopenfilename()
        file = open(file_name, 'rb')
        self.matrix = pickle.load(file)
        file.close()
        self.draw_grid('this is useless, just ignore')  # TODO: delete all like this-do not forget to delete this later
        for pixel_y in range(0, 500, self.pixel):
            for pixel_x in range(0, 500, self.pixel):
                step += 1
                if self.matrix[step]:
                    self.cnv.create_rectangle(pixel_x, pixel_y, pixel_x + 19, pixel_y + 19, fill='blue')

    def add_train_func(self):
        self.save_form = Toplevel()
        self.save_form.geometry('+200+200')
        self.save_form.wm_attributes('-topmost', 1)
        self.save_form.resizable(False, False)
        self.save_form.title('Save new train data')

        ask_save_frame = Frame(self.save_form)
        ask_save_frame.grid(columnspan=2, pady=5, padx=5)
        ask_save_label = Label(ask_save_frame)
        ask_save_label.grid()
        if self.train_directory == 'Number_train':
            ask_save_entry = Entry(ask_save_frame, width=5, justify=CENTER)
            ask_save_entry.grid(row=0, column=1)
            ask_save_label.configure(text='What number was written?')

            ask_save_btn_ok = Button(self.save_form, text='Ok', width=10,
                                     command=lambda: self.save_train(ask_save_entry))
            ask_save_btn_ok.grid(row=2, column=0, pady=5)
            ask_save_btn_cancel = Button(self.save_form, text='Cancel', width=10, command=self.save_form.destroy)
            ask_save_btn_cancel.grid(row=2, column=1, pady=5)

        if self.train_directory == 'Boolean_train':
            ask_save_label.configure(text='What symbol was writen?')

            ask_save_btn_ok = Button(self.save_form, text='True', width=10,
                                     command=lambda: self.save_train(boolean=True))
            ask_save_btn_ok.grid(row=2, column=0, pady=5, padx=5)
            ask_save_btn_ok = Button(self.save_form, text='False', width=10,
                                     command=lambda: self.save_train(boolean=False))
            ask_save_btn_ok.grid(row=2, column=1, pady=5, padx=5)

        # only GUI need to add func for save

    def save_train(self, entry=None, boolean=None, windowed=True):
        # TODO: prohibit adding more than one character and add red glow for letters
        #   https://www.cyberforum.ru/python-beginners/thread1196795.html
        file_time = int(time.time())

        if self.train_directory == 'Boolean_train':
            file = open(f'{self.train_directory}/{boolean}_{file_time}.goose', 'wb')
            pickle.dump(self.matrix, file)
            file.close()
            if windowed:
                self.save_form.destroy()

        elif self.train_directory == 'Number_train':
            data = entry.get()
            try:
                data = int(data)
            except ValueError:
                messagebox.showerror('Error', 'You should enter the number type')
                return None
            file = open(f'{self.train_directory}\{data}_{file_time}.goose', 'wb')
            pickle.dump(self.matrix, file)
            file.close()
            self.save_form.destroy()

    def del_func(self):
        self.del_all('this is useless, just ignore')  # do not forget to delete this later

    def converting_func(self):
        self.fill_pixels('this is useless, just ignore')  # do not forget to delete this later
        self.draw_grid('this is useless, just ignore')  # do not forget to delete this later

    def change_font_entry_func(self, event):
        try:
            self.pencil_width = int(self.font_entry.get())
        except ValueError:
            messagebox.showerror(title='Error', message='You should enter the valid number')

    def upper_font_func(self):
        self.pencil_width += 4
        self.font_entry.delete(0, END)
        self.font_entry.insert(0, self.pencil_width)

    def lower_font_func(self):
        self.pencil_width -= 4
        self.font_entry.delete(0, END)
        self.font_entry.insert(0, self.pencil_width)

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
        self.prediction_label.configure(text='')

    def draw_grid(self, event):
        for i in range(0, 500, self.pixel):
            self.cnv.create_line(i, 0, i, 500, width=1, fill='grey')
            self.cnv.create_line(0, i, 500, i, width=1, fill='grey')

    def fill_pixels(self, event):
        for pixel_y in range(0, 500, self.pixel):
            for pixel_x in range(0, 500, self.pixel):
                if self.cnv.find_overlapping(pixel_x + 1, pixel_y + 1, pixel_x + 19, pixel_y + 19):
                    self.cnv.create_rectangle(pixel_x, pixel_y, pixel_x + 19, pixel_y + 19, fill='blue')
                    self.matrix.append(1)
                else:
                    self.matrix.append(0)


if __name__ == '__main__':
    root = Tk()
    root.geometry('700x500+200+200')
    root.resizable(False, False)

    AppGUI(root)

    root.mainloop()

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser
from pathlib import Path
#from ctypes import windll  # it's for fixing blurry windows ui
import variables


def read_config():
    global BACKGROUND_COLOR, FOREGROUND_COLOR, FONT_NAME, FONT_SIZE
    file = open('config', 'r')
    settings_list = file.readlines()
    print(settings_list)
    BACKGROUND_COLOR = settings_list[0].split('=')[1][:-1]
    FOREGROUND_COLOR = settings_list[1].split('=')[1][:-1]
    FONT_NAME = settings_list[2].split('=')[1][:-1]
    FONT_SIZE = int(settings_list[3].split('=')[1])
    file.close()

def update_config():
    global BACKGROUND_COLOR, FOREGROUND_COLOR, FONT_NAME, FONT_SIZE

    lines = open('config', 'r').readlines()
    lines[0] = 'BACKGROUND_COLOR=' + BACKGROUND_COLOR + '\n'
    out = open('config', 'w')
    out.writelines(lines)
    out.close()

    lines = open('config', 'r').readlines()
    lines[1] = 'FOREGROUND_COLOR=' + FOREGROUND_COLOR + '\n'
    out = open('config', 'w')
    out.writelines(lines)
    out.close()

    lines = open('config', 'r').readlines()
    lines[2] = 'FONT_NAME=' + FONT_NAME + '\n'
    out = open('config', 'w')
    out.writelines(lines)
    out.close()

    lines = open('config', 'r').readlines()
    lines[3] = 'FONT_SIZE=' + str(FONT_SIZE) + '\n'
    out = open('config', 'w')
    out.writelines(lines)
    out.close()

def open_file():
    global is_file_open, file_path, file_name
    file_path = filedialog.askopenfilename(initialdir='C:',
                                           title='Open File',
                                           filetypes=(('.txt', '*.txt'),
                                                      ('.py', '*.py'),
                                                      ('All Files', '*.*')))
    if file_path == '': return
    file = open(file_path, 'r')
    file_name = Path(file_path).name
    window.title(file_name)
    text.delete('1.0', END)
    text.insert(END, str(file.read()))
    file.close()
    is_file_open = True


def save_file():
    global file_name
    file = filedialog.asksaveasfile(defaultextension='.txt',
                                    title='Save File',
                                    initialdir="/<file_name>",
                                    filetypes=[
                                        ('Text File', '.txt'),
                                        ('HTML', '.html'),
                                        ('Python File', '.py')
                                    ], initialfile=file_name)
    if file is None:
        return
    file_content = text.get(1.0, END)
    file.write(file_content)
    file.close()


def cut():
    text.event_generate("<<Cut>>")


def copy():
    text.event_generate("<<Copy>>")


def paste():
    text.event_generate("<<Paste>>")


def change_font():
    global FONT_SIZE, FONT_NAME
    font_window = Toplevel()

    font_name_label = Label(font_window, text='Font')
    font_name_label.grid(column=0, row=0)

    variable = StringVar(font_window)
    variable.set(FONT_NAME)
    variable = StringVar()
    variable.set(FONT_NAME)

    font_choice = OptionMenu(font_window, variable, *variables.fonts)
    font_choice.grid(column=1, row=0, sticky=W)

    font_size_label = Label(font_window, text='Font Size')
    font_size_label.grid(column=0, row=1)

    font_size_entry = Entry(font_window, width=10)
    font_size_entry.insert(0, FONT_SIZE)
    font_size_entry.grid(column=1, row=1)

    FONT_NAME = variable.get()
    FONT_SIZE = font_size_entry.get()

    font_submit_button = Button(font_window, text='Submit',
                                command=lambda: font_submit(variable.get(), int(font_size_entry.get())))
    font_submit_button.grid(column=0, row=2, columnspan=2)

    font_window.mainloop()


def font_submit(name, size):
    global FONT_SIZE, FONT_NAME
    FONT_SIZE = size
    FONT_NAME = name
    update_config()
    text['font'] = (name, size)


def change_bg():
    color_hex = colorchooser.askcolor()[1]
    window.config(bg=color_hex)
    text['bg'] = color_hex

    lines = open('config', 'r').readlines()
    lines[0] = 'BACKGROUND_COLOR=' + color_hex + '\n'
    out = open('config', 'w')
    out.writelines(lines)
    out.close()


def change_fg():
    color_hex = colorchooser.askcolor()[1]
    text['fg'] = color_hex

    lines = open('config', 'r').readlines()
    lines[1] = 'FOREGROUND_COLOR=' + color_hex + '\n'
    out = open('config', 'w')
    out.writelines(lines)
    out.close()


def about():
    messagebox.showinfo(title='About Notepad',
                        message='Author of this application is Matin Huseynzade\n' +
                                'github: chillmetin')


#windll.shcore.SetProcessDpiAwareness(1)  # fix for blurry windows 10 scaling

# OPEN FILE VARIABLES
is_file_open = False
BACKGROUND_COLOR = 'yellow'
FOREGROUND_COLOR = 'blue'
FONT_NAME = 'Calibri'
FONT_SIZE = 12

file_path = ''
file_name = ''
read_config()

window = Tk()  # main screen
window.title('Untitled')
icon = PhotoImage(file='icon.png')
window.iconphoto(True, icon)
window.geometry('1280x720')

### MAIN SCREEN
text = Text(window, bg=BACKGROUND_COLOR,
            fg=FOREGROUND_COLOR,
            font=(FONT_NAME, FONT_SIZE),
            )
text.pack(expand=True, fill='both')

### MENU BAR
menubar = Menu(window)
window.config(menu=menubar)

# File cascade
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open...', command=open_file, compound='left')
file_menu.add_command(label='Save', command=save_file, compound='left')
file_menu.add_separator()
file_menu.add_command(label='Exit', command=quit)

# Edit cascade
edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Cut', command=cut, accelerator='Ctrl+X')
edit_menu.add_command(label='Copy', command=copy, accelerator='Ctrl+C')
edit_menu.add_command(label='Paste', command=paste, accelerator='Ctrl+V')

# View cascade
view_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='View', menu=view_menu)
view_menu.add_command(label='Font', command=change_font)
view_menu.add_command(label='Change Background', command=change_bg)
view_menu.add_command(label='Change Foreground', command=change_fg)

# About cascade
about_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='About', menu=about_menu)
about_menu.add_command(label='About Notepad', command=about)

window.mainloop()

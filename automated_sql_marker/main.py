import os.path
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import sys

from marker import mark_script
# venv\Script\deactivate
# interpreter\Scripts\activate
# Open a file dialog to allow a file to be selected
# update the combo box showing all files in that folder
# Also updates the variable marking_script_file_name to include the filename of the marking script
def select_files():
    filetypes = (
        ('SQL script files', '*.sql'),
        ('Text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilenames(title='Open files', initialdir='/', filetypes=filetypes)

    if filename:
        message_box1.config(state='normal')
        message_box1.delete('1.0', 'end')
        message_box1.insert('1.0', filename[0])
        message_box1.config(state='disabled')

        files_in_folder = get_file_names(str(os.path.dirname(filename[0])))

        global current_directory
        current_directory = os.path.dirname(filename[0])

        choice_var.set(files_in_folder[0])
        file_selection_box['values'] = files_in_folder
        file_selection_box.update()

        global marking_script_file_name
        marking_script_file_name = filename[0]

# Open a file browser to select a specific directory
# currently not used as default to folder selected by above function
def select_directory():
    filepath = fd.askdirectory(title='Open files', initialdir='/')
    showinfo(title='Selected Directory', message=filepath)


# return a list containing all file names in a current folder with a .sql extension
def get_file_names(current_directory):
    files = []
    for filename in os.listdir(current_directory):
        if os.path.isfile(os.path.join(current_directory, filename)):
            if filename.endswith('.sql'):
                files.append(filename)
    if not files:
        files.append("No files in this folder")
    return files


# taken from https://stackoverflow.com/questions/12351786/how-to-redirect-print-statements-to-tkinter-text-widget
# used to redirect text output to a text box
def redirector(input_str):
    output_box.insert('end', input_str)


# just a test for now
# eventually want it to display the contents of the chosen file (file_to_display) in the output_box
def display_file_contents(file_to_display, clear=True, full_path=True):
    # print("combo box selection")
    if clear:
        output_box.delete("1.0", "end")
    if full_path:
        full_file_name = file_to_display
    else:
        full_file_name = os.path.join(current_directory, file_to_display)
    if os.path.isfile(full_file_name):
        f = open(full_file_name, "r")
        file_contents = f.read()
        print(file_contents)
        f.close()
    else:
        print("Invalid file name:", full_file_name)

def call_marker_script(cur_dir, ms_file_name, ss_file_name, detail_selected=True):
    output_box.delete("1.0", "end")
    mark_script(cur_dir, ms_file_name, ss_file_name, detail_selected)

def main():
    # Global variables used throughout
    # better to create a class structure as it's starting to get messy
    global marking_script_file_name  # name of marking script file selected
    global message_box1  # message box showing above file name once selected by user
    global choice_var  # variable which stores list of .sql files in the selected folder
    global file_selection_box  # the combo box which allows a file to be selected for processing
    global output_box  # box where all output will be redirected
    global current_directory # the currently selected directory
    global output_box # the box for output from the application

    current_directory = r"c:\\"

    files_in_folder = get_file_names(r'c:\\')
    marking_script_file_name = 'No file selected'

    root = tk.Tk()
    root.geometry('1020x680')
    root.resizable(False, False)
    root.title("SQL Marking Tool")
    my_frame = ttk.Frame(root)

    message = tk.Label(my_frame, text="Welcome to the SQL Automated Marking System!", foreground="blue" )
    message.grid(row=0, column=1, columnspan=3)

    # button to open file dialog to choose marking sample file
    button1 = tk.Button(my_frame, text="Select Marking Sample Script", command=lambda: select_files())
    button1.grid(row=1, column=0)

    # Message box to show name of file selected
    message_box1 = tk.Text(my_frame, height=1, width=100, )
    message_box1.insert('1.0', marking_script_file_name)
    message_box1.config(state='disabled')
    message_box1.grid(row=1, column=1, columnspan=4, sticky="W")

    message2 = tk.Label(my_frame, text="Select Student Script to mark:")
    message2.grid(row=2, column=0, sticky="W")

    # Creating a combo box which will contain all the .sql files in the selected folder
    choices = files_in_folder
    choice_var = tk.StringVar()
    choice_var.set(choices[0])
    # fileSelectionBox = tk.OptionMenu(root, choiceVar, *choices)
    # edited out as using a combo box rather than a file selection box
    file_selection_box = ttk.Combobox(my_frame, textvariable=choice_var, values=choices)
    file_selection_box.grid(row=2, column=1, columnspan=2, sticky='W')

    # A button to display the marking script
    # not sure why script_file_name is 'No file selected' after I have selected a file
    # think the same variable is being used for both the marking and student script - oops!
    # need to put all the file details in a class, me thinks
    # and maybe the form too
    markscr_btn = tk.Button(my_frame, text="Display Mark Script", command=lambda: display_file_contents(marking_script_file_name, full_path=True))
    markscr_btn.grid(row=2, column=2, sticky='E')

    # A button to display the student's script
    studscr_btn = tk.Button(my_frame, text="Display Student Script", command=lambda: display_file_contents(file_selection_box.get(), full_path=False))
    studscr_btn.grid(row=2, column=3)

    # A button which should eventually call the marking process
    # but at the moment it won't display in the correct column - want it directly next to the above combo box
    # Inspiration - maybe I need multiple frames!!!
    process_btn = tk.Button(my_frame, text="Mark Script", command=lambda: call_marker_script(current_directory, marking_script_file_name, file_selection_box.get(), detail_selected.get()))
    process_btn.grid(row=2, column=4, sticky='W')

    # A check box which will allow us to select whether to display detail
    # i.e. the trees, when running the marking script
    detail_selected = tk.BooleanVar()
    detail_check_box = tk.Checkbutton(my_frame, text="Show_Detail", variable=detail_selected, command=lambda: print(detail_selected.get()))
    detail_check_box.grid(row=3, column=4, sticky="w")

    # creating an output box which will show all the results, and adds a horizontal and vertical scroll bar
    output_box = tk.Text(my_frame, height=30, width=120, wrap='none')
    ys = ttk.Scrollbar(my_frame, orient='vertical', command=output_box.yview)
    xs = ttk.Scrollbar(my_frame, orient='horizontal', command=output_box.xview)
    output_box['yscrollcommand'] = ys.set
    output_box['xscrollcommand'] = xs.set
    output_box.grid(row=4, column=0, columnspan=5)
    xs.grid(column=0, columnspan=6, row=5, sticky='we')
    ys.grid(column=6, row=4, sticky='ns')

    exit_btn = tk.Button(my_frame, text=' Exit! ', foreground="red", command=lambda: quit())
    exit_btn.grid(row=6, column=2, columnspan=2)

    my_frame.grid_columnconfigure(0, weight=1)
    my_frame.grid_rowconfigure(0, weight=1)

    # redirect stdout to the redirector function
    sys.stdout.write = redirector  # whenever sys.stdout.write is called, redirector is called.

    print("So does this get put in me message box")
    print("Or this?")

    my_frame.grid(padx=30, pady=30)

    root.mainloop()


if __name__ == '__main__':
    main()

from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image
import xml_parser as xmlparser
import hmod_parser as hmodparser

root = Tk()
root.title('SBML2HYB')
root.geometry("1000x800")

# Vertical (y) Scroll Bar
top_frame = Frame(root, pady=10)
mid_frame = Frame(root, pady=10)
bot_frame = Frame(root, pady=10)

top_frame.pack()
bot_frame.pack()

mid_frame.pack()

canvas = Canvas(top_frame, width=350, height=100)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("sbml2hyb_logo.png").resize((330, 80), Image.ANTIALIAS))
canvas.create_image(20, 20, anchor=NW, image=img)

# top_title_label = Label(top_frame, pady=20, text="SBML <-> HMOD converter")
# top_title_label.config(font=(50))
# top_title_label.pack()

# top_label = Label(top_frame, pady=10, text="Choose an SBML file to export to hmod\n"
#                                            "or\n"
#                                            "Choose an hmod file to export to SBML")
# top_label.config(font=(10))
#
# top_label.pack()

pos1 = Label(bot_frame, pady=10, text='Choose an SBML file to export to hmod           OR', borderwidth=1)
pos1.config(font=(50))
pos1.grid(row=0, column=0)

pos2 = Label(bot_frame, pady=10, text='          Choose an hmod file to export to SBML', borderwidth=1)
pos2.config(font=(50))
pos2.grid(row=0, column=1)


save_label = Label(top_frame, text="File Saved!")

my_text = Text(mid_frame, wrap=NONE, height=50, width=150)

scroll_y = Scrollbar(mid_frame, orient="vertical", command=my_text.yview)
scroll_x = Scrollbar(mid_frame, orient="horizontal", command=my_text.xview)



def open_xml_file():
    top_frame.filename = filedialog.askopenfilename(title="Select A File",
                                                    filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    if top_frame.filename is None or top_frame.filename == '':
        return
    try:
        res = xmlparser.main(top_frame.filename)
    except Exception as e:
        print(e)
        res = "An unexpected error as occurred"

    my_text.delete('1.0', END)
    save_label.config(text="")
    my_text.insert(INSERT, res)

    scroll_y.pack(side="right", expand=True, fill="y")
    scroll_x.pack(side="bottom", expand=True, fill="x")

    my_text.configure(yscrollcommand=scroll_y.set)
    my_text.configure(xscrollcommand=scroll_x.set)
    my_btn_export.grid(row=1, column=3)

    my_text.pack(side="left")


def open_hmod_file():
    top_frame.filename = filedialog.askopenfilename(title="Select A File",
                                                    filetypes=(("hmod files", "*.hmod"), ("all files", "*.*")))
    if top_frame.filename is None or top_frame.filename == '':
        return
    try:
        res = hmodparser.main(top_frame.filename)
    except Exception as e:
        print(e)
        res = "An unexpected error as occurred"

    my_text.delete('1.0', END)
    save_label.config(text="")
    my_text.insert(INSERT, res)

    scroll_y.pack(side="right", expand=True, fill="y")
    scroll_x.pack(side="bottom", expand=True, fill="x")

    my_text.configure(yscrollcommand=scroll_y.set)
    my_text.configure(xscrollcommand=scroll_x.set)
    my_btn_export.grid(row=1, column=3)

    my_text.pack(side="left")


def save_file():
    text2save = my_text.get("1.0", END)
    if "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" in text2save:
        f = filedialog.asksaveasfile(mode='w', defaultextension=".xml")
    else:
        f = filedialog.asksaveasfile(mode='w', defaultextension=".hmod")
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return

    f.write(text2save)
    f.close()
    save_label.config(text="File Saved!")
    save_label.pack(side="bottom")


my_btn_export = Button(bot_frame, text="Export file", command=save_file)
my_btn_xml = Button(bot_frame, padx=10, text="Translate SBML File", command=open_xml_file)
my_btn_hmod = Button(bot_frame, padx=10, text="Translate HMOD File", command=open_hmod_file)

my_btn_xml.grid(row=1, column=0)

my_btn_hmod.grid(row=1, column=1)

# my_btn_export.grid(row=1, column=2)

# # my_btn.grid(row=0, column=0)
# my_btn_xml.pack(side="left")
# my_btn_hmod.pack(side="left")

root.mainloop()

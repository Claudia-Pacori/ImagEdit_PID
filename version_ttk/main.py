import ttkbootstrap as ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab
import os


# defining global variables
LF_WIDTH = 250
RF_WIDTH = 700
HEIGHT = 500
file_path = ""
temp_path = "temp.png"
temp_filter = "temp_filter.png"
pen_size = 3
pen_color = "black"


def get_temp(withFilter=False):
    if withFilter:
        image = Image.open(temp_filter)
    else:
        image = Image.open(temp_path)
    image_aspect_ratio = image.size[1] / float(image.size[0])
    if image_aspect_ratio > 1:
        # vertical image
        new_height = int((HEIGHT))
        new_width = int((new_height / image_aspect_ratio))
    else:
        # horizontal image
        new_width = int((RF_WIDTH))
        new_height = int((new_width * image_aspect_ratio))
    image = image.resize((new_width, new_height), Image.LANCZOS)
    image = ImageTk.PhotoImage(image)
    return image


# function to open the image file
def add_image():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Open Image File",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")],
    )
    if file_path:
        global image
        image = Image.open(file_path)
        image.save(temp_path)
        image = get_temp()
        canvas.create_image(RF_WIDTH / 2, HEIGHT / 2, image=image)
    if os.path.exists(temp_filter):
        os.remove(temp_filter)


def flip_image():
    try:
        global image
        image = Image.open(temp_path).transpose(Image.FLIP_LEFT_RIGHT)
        image.save(temp_path)
        if os.path.exists(temp_filter):
            image = Image.open(temp_filter).transpose(Image.FLIP_LEFT_RIGHT)
            image.save(temp_filter)
            image = get_temp(withFilter=True)
        else:
            image = get_temp()
        # convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        canvas.create_image(RF_WIDTH / 2, HEIGHT / 2, image=image)

    except:
        showerror(title="Flip Image Error", message="Please select an image to flip!")


# global variable for tracking rotation angle
def rotate_image():
    try:
        global image
        # open the image and rotate it
        image = Image.open(temp_path).rotate(90, expand=True)
        image.save(temp_path)
        if os.path.exists(temp_filter):
            image = Image.open(temp_filter).rotate(90, expand=True)
            image.save(temp_filter)
            image = get_temp(withFilter=True)
        else:
            image = get_temp()
        # convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        canvas.create_image(RF_WIDTH / 2, HEIGHT / 2, image=image)

    except:
        showerror(
            title="Rotate Image Error", message="Please select an image to rotate!"
        )

def restore_image():
    try:
        global image, file_path
        image = Image.open(file_path)
        image.save(temp_path)
        image = get_temp()
        # convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        canvas.create_image(RF_WIDTH / 2, HEIGHT / 2, image=image)
        if os.path.exists(temp_filter):
            os.remove(temp_filter)
    except:
        showerror(
            title="Restore Image Error", message="Please select an image to restore!"
        )

def save_image():
    global file_path

    if file_path:
        # open file dialog to select save location and file type
        if os.path.exists(temp_filter):
            image = Image.open(temp_filter)
        else:
            image = Image.open(temp_path)
        file_path_save = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path_save:
            if askyesno(title="Save Image", message="Do you want to save this image?"):
                # save the image to a file
                image.save(file_path_save)

# function for applying filters to the opened image file
def apply_filter(filter):
    global image
    try:
        image = Image.open(temp_path)
        image.save(temp_filter)
        image = Image.open(temp_filter)
        # apply the filter to the original image
        if filter == "Black and White":
            image = ImageOps.grayscale(image)

        elif filter == "Blur":
            image = image.filter(ImageFilter.BLUR)

        elif filter == "Sharpen":
            image = image.filter(ImageFilter.SHARPEN)

        elif filter == "Smooth":
            image = image.filter(ImageFilter.SMOOTH)

        elif filter == "Emboss":
            image = image.filter(ImageFilter.EMBOSS)

        elif filter == "Detail":
            image = image.filter(ImageFilter.DETAIL)

        elif filter == "Edge Enhance":
            image = image.filter(ImageFilter.EDGE_ENHANCE)

        elif filter == "Contour":
            image = image.filter(ImageFilter.CONTOUR)

        image.save(temp_filter)
        image = get_temp(withFilter=True)
        # convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        canvas.create_image(RF_WIDTH / 2, HEIGHT / 2, image=image)

    except:
        showerror(title="Error", message="Please select an image first!")

if os.path.exists(temp_path):
    os.remove(temp_path)
if os.path.exists(temp_filter):
    os.remove(temp_filter)

root = ttk.Window(themename="cosmo")
root.title("Image Editor")
root.geometry(f"{LF_WIDTH + RF_WIDTH + 10}x{HEIGHT + 10}")
root.resizable(0, 0)
icon = ttk.PhotoImage(file="icon.png")
root.iconphoto(False, icon)

# the left frame to contain the 4 buttons
left_frame = ttk.Frame(root, width=LF_WIDTH, relief="solid", border=1)
left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# the right canvas for displaying the image
canvas = ttk.Canvas(root, width=RF_WIDTH, relief="solid", border=1)
canvas.pack(fill="both", expand=True, padx=5, pady=5)

# label
filter_label = ttk.Label(left_frame, text="Select Filter:", background="white")
filter_label.grid(row=0, column=0, padx=10, pady=5)

# a list of filters
image_filters = [
    "Contour",
    "Black and White",
    "Blur",
    "Detail",
    "Emboss",
    "Edge Enhance",
    "Sharpen",
    "Smooth",
]

# combobox for the filters
filter_combobox = ttk.Combobox(left_frame, values=image_filters, width=15)
filter_combobox.grid(row=0, column=1, padx=10, pady=5)

# binding the apply_filter function to the combobox
filter_combobox.bind(
    "<<ComboboxSelected>>", lambda event: apply_filter(filter_combobox.get())
)

options = ["add", "flip", "rotate", "save", "restore"]
options_label = [
    "Open Image",
    "Flip Image",
    "Rotate Image",
    "Save Image",
    "Restore Image"
]

button_icon = [None] * 6
for i in range(len(options)):
    button_icon[i] = ttk.PhotoImage(file=options[i] + ".png").subsample(12, 12)
    image_button = ttk.Button(
        left_frame,
        image=button_icon[i],
        bootstyle="light",
        command=eval(options[i] + "_image"),
    )
    button_label = ttk.Label(left_frame, text=options_label[i], background="white")

    image_button.grid(row=i + 1, column=0, padx=10, pady=5)
    button_label.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")

root.mainloop()

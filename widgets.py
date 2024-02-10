import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import *


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(parent)
        self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.import_func = import_func

        ctk.CTkButton(self, text="Open Image", command=self.open_dialog).pack(
            expand=True
        )

    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_func(path)


class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(
            parent,
            background=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.bind("<Configure>", resize_image)


class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            parent,
            text="Close",
            text_color=WHITE,
            fg_color="transparent",
            width=40,
            height=40,
            corner_radius=0,
            hover_color=CLOSE_RED,
            command=close_func,
        )
        self.place(relx=0.9, rely=0.1, anchor="ne")

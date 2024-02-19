import customtkinter as ctk
from tkinter import Canvas
from settings_ import *
from menu_ import *


class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, rowspan=3, column=0, sticky="nsew", pady=10, padx=10)

        self.add("Menu")
        self.add("Efectos")
        self.add("Exportar")

        self.menu_funcs = {
            "OpenImage": parent.import_image,
            "ExportImage": parent.export_image,
            "LastUsedGroup": parent.last_used_group,
        }
        self.effect_vars = parent.effect_vars
        self.last_group = parent.last_group

        MenuFrame(self, self.tab("Menu"))
        EffectsFrame(self, self.tab("Efectos"))
        ExportFrame(self, self.tab("Exportar"))


class ImageInput(Canvas):
    def __init__(self, parent):
        super().__init__(
            parent,
            background=FRAME_COLOR,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


class ImageOutput(Canvas):
    def __init__(self, parent):
        super().__init__(
            parent,
            # background=BACKGROUND_COLOR,
            background=FRAME_COLOR,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)


class VideoProgressBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BACKGROUND_COLOR)
        self.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        for i in range(6):
            self.columnconfigure(i, weight=1, uniform="a")
            if i == 4:
                self.columnconfigure(i, weight=7, uniform="a")

        self.play = ctk.CTkButton(self, text="Play", state="disabled")
        self.play.grid(row=0, column=0, padx=5)

        self.pause = ctk.CTkButton(self, text="Pause", state="disabled")
        self.pause.grid(row=0, column=1, padx=5)

        self.stop = ctk.CTkButton(self, text="Stop", state="disabled")
        self.stop.grid(row=0, column=2, padx=5)

        self.current_time = ctk.CTkLabel(self, text="00:00", state="disabled")
        self.current_time.grid(row=0, column=3, padx=5)

        self.progress = ctk.CTkSlider(self, fg_color=SLIDER_BG, state="disabled")
        self.progress.grid(row=0, column=4, padx=5, sticky="ew")

        self.total_time = ctk.CTkLabel(self, text="00:00", state="disabled")
        self.total_time.grid(row=0, column=5, padx=5)

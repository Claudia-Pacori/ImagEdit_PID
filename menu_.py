import customtkinter as ctk
from panels_ import *


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, frame):
        super().__init__(frame, fg_color="transparent")
        self.pack(expand=True, fill="both", padx=5, pady=10)

        OpenImageButton(self, parent.menu_funcs["OpenImage"])
        OpenVideoButton(self)
        OpenWebcamButton(self)


class EffectsFrame(ctk.CTkFrame):
    def __init__(self, parent, frame):
        super().__init__(frame, fg_color="transparent")
        self.pack(expand=True, fill="both", padx=5, pady=10)
        self.last_used_group = parent.menu_funcs["LastUsedGroup"]

        SliderGroupPanel(
            self,
            "Aclarar",
            (parent.effect_vars["gamma"], "Alpha", 0.00, 1.00),
        )
        SliderGroupPanel(
            self,
            "Bordes",
            (parent.effect_vars["kernel"], "Kernel", 3, 9),
            (parent.effect_vars["sigma"], "Sigma", 0.00, 1.00),
        )
        SliderGroupPanel(
            self,
            "Rotación",
            (parent.effect_vars["roll"], "Roll", -180.00, 180.00),
            (parent.effect_vars["pitch"], "Pitch", -180.00, 180.00),
            (parent.effect_vars["yaw"], "Yaw", -180.00, 180.00),
        )
        RadioButtonGroupPanel(
            self,
            parent.effect_vars["option"],
            "Dilatación",
            "Erosión",
        )
        RestoreButton(self, parent.effect_vars, parent.last_group)


class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, frame):
        super().__init__(frame, fg_color="transparent")
        self.pack(expand=True, fill="both")

        self.name_string = ctk.StringVar()
        self.file_string = ctk.StringVar(value="jpg")
        self.path_string = ctk.StringVar()

        FileNamePanel(self, self.name_string, self.file_string)
        FilePathPanel(self, self.path_string)
        SaveButton(
            self,
            parent.menu_funcs["ExportImage"],
            self.name_string,
            self.file_string,
            self.path_string,
        )

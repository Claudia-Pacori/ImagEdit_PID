import customtkinter as ctk

from panels_ import (
    FileNamePanel,
    FilePathPanel,
    OpenImageButton,
    OpenVideoButton,
    OpenWebcamButton,
    RadioButtonGroupPanel,
    RestoreButton,
    SaveButton,
    SliderGroupPanel,
)


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, frame):
        super().__init__(frame, fg_color="transparent")
        self.pack(expand=True, fill="both", padx=5, pady=10)

        OpenImageButton(self, parent.menu_funcs["OpenImage"])
        OpenVideoButton(self, parent.menu_funcs["OpenVideo"])
        OpenWebcamButton(self, parent.menu_funcs["OpenWebcam"])


class EffectsFrame(ctk.CTkFrame):
    def __init__(self, parent, frame):
        super().__init__(frame, fg_color="transparent")
        self.pack(expand=True, fill="both", padx=5, pady=10)
        self.last_group = parent.last_group

        SliderGroupPanel(
            self,
            "Aclarar",
            (parent.effect_vars["gamma"], "Alpha", 0.00, 1.00),
        )
        SliderGroupPanel(
            self,
            "Bordes",
            (parent.effect_vars["sigma"], "Sigma", 0.00, 1.00),
            (parent.effect_vars["low_th"], "Low", 0, 255),
            (parent.effect_vars["high_th"], "High", 0, 255),
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
        RestoreButton(self, parent.effect_vars)


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

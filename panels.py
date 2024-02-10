import customtkinter as ctk
from settings import *
from tkinter import filedialog


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=DARK_GRAY)
        self.pack(fill="x", pady=4, ipady=8)


class SliderPanel(Panel):
    def __init__(self, parent, text, variable, min_value, max_value):
        super().__init__(parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.variable = variable
        self.variable.trace_add("write", self.update_text)

        ctk.CTkLabel(self, text=text).grid(row=0, column=0, sticky="w", padx=5)
        self.num_label = ctk.CTkLabel(self, text=variable.get())
        self.num_label.grid(row=0, column=1, sticky="e", padx=5)
        ctk.CTkSlider(
            self,
            fg_color=SLIDER_BG,
            variable=self.variable,
            from_=min_value,
            to=max_value,
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5,
        )

    def update_text(self, *args):
        self.num_label.configure(text=f"{round(self.variable.get(), 2)}")


class SegmentedPanel(Panel):
    def __init__(self, parent, text, variable, options):
        super().__init__(parent)

        ctk.CTkLabel(self, text=text).pack()
        ctk.CTkSegmentedButton(self, values=options, variable=variable).pack(
            expand=True, fill="both", padx=5, pady=5
        )


class SwitchPanel(Panel):
    def __init__(self, parent, *args):
        super().__init__(parent)

        for var, text in args:
            switch = ctk.CTkSwitch(
                self, text=text, variable=var, button_color=BLUE, fg_color=SLIDER_BG
            )
            switch.pack(side="left", expand=True, fill="both", padx=5, pady=5)


class DropDownPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, variable, options):
        super().__init__(
            parent,
            values=options,
            fg_color=DARK_GRAY,
            button_color=DROPDOWN_MAIN_COLOR,
            button_hover_color=DROPDOWN_HOVER_COLOR,
            dropdown_fg_color=DROPDOWN_MENU_COLOR,
            variable=variable,
        )
        self.pack(fill="x", padx=5, pady=5)


class RevertButton(ctk.CTkButton):
    def __init__(self, parent, *args):
        super().__init__(
            parent,
            text="Revert",
            command=self.revert,
        )
        self.pack(side="bottom", pady=10)
        self.args = args

    def revert(self):
        for var, default in self.args:
            var.set(default)


class FileNamePanel(Panel):
    def __init__(self, parent, name_string, file_string):
        super().__init__(parent)

        self.name_string = name_string
        self.name_string.trace_add("write", self.update_output)
        self.file_string = file_string

        ctk.CTkEntry(self, textvariable=self.name_string).pack(
            fill="x", padx=20, pady=5
        )
        frame = ctk.CTkFrame(self, fg_color="transparent")
        jpg_check = ctk.CTkCheckBox(
            frame,
            text="JPG",
            variable=self.file_string,
            onvalue="jpg",
            offvalue="png",
            command=lambda: self.click("jpg"),
        )
        jpg_check.pack(side="left", fill="x", expand=True)
        png_check = ctk.CTkCheckBox(
            frame,
            text="PNG",
            variable=self.file_string,
            onvalue="png",
            offvalue="jpg",
            command=lambda: self.click("png"),
        )
        png_check.pack(side="left", fill="x", expand=True)
        frame.pack(fill="x", padx=20, pady=5, expand=True)

        self.output = ctk.CTkLabel(self, text="")
        self.output.pack()

    def click(self, value):
        self.file_string.set(value)
        self.update_output()

    def update_output(self, *args):
        if self.name_string.get():
            text = self.name_string.get().replace(" ", "_")
            self.output.configure(text=f"{text}.{self.file_string.get()}")


class FilePathPanel(Panel):
    def __init__(self, parent, path_string):
        super().__init__(parent)
        self.path_string = path_string

        ctk.CTkButton(self, text="Open Explorer", command=self.open_file_dialog).pack(
            pady=5
        )
        ctk.CTkEntry(self, textvariable=self.path_string).pack(
            fill="both", padx=5, pady=5, expand=True
        )

    def open_file_dialog(self):
        self.path_string.set(filedialog.askdirectory())


class SaveButton(ctk.CTkButton):
    def __init__(self, parent, export_image, name_string, file_string, path_string):
        super().__init__(
            parent,
            text="Save",
            command=self.save,
        )
        self.pack(side="bottom", pady=10)
        self.export_image = export_image
        self.name_string = name_string
        self.file_string = file_string
        self.path_string = path_string

    def save(self):
        self.export_image(
            self.name_string.get(),
            self.file_string.get(),
            self.path_string.get(),
        )

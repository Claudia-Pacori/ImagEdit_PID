from tkinter import filedialog

import customtkinter as ctk

from settings_ import DARK_GRAY, DEFAULT_VALUES, SLIDER_BG


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=DARK_GRAY)
        self.pack(fill="x", pady=4, ipady=4, side="top")


class OpenImageButton(ctk.CTkButton):
    def __init__(self, parent, import_func):
        super().__init__(parent, text="Abrir Imagen", command=self.open_dialog)
        self.pack(fill="x", padx=5, pady=5)
        self.import_func = import_func

    def open_dialog(self):
        path = filedialog.askopenfile(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if path:
            path = path.name
            self.import_func(path)


class OpenVideoButton(ctk.CTkButton):
    def __init__(self, parent, import_func):
        super().__init__(parent, text="Abrir Video", command=self.open_dialog)
        self.pack(fill="x", padx=5, pady=5)
        self.import_func = import_func

    def open_dialog(self):
        path = filedialog.askopenfile(
            filetypes=[("Video files", "*.mp4 *.avi *.flv *.mov")]
        )
        if path:
            path = path.name
            self.import_func(path)


class OpenWebcamButton(ctk.CTkButton):
    def __init__(self, parent, import_func=None):
        super().__init__(parent, text="Abrir Webcam", command=import_func)
        self.pack(fill="x", padx=5, pady=5)


class RestoreButton(ctk.CTkButton):
    def __init__(self, parent, effect_vars):
        super().__init__(parent, text="Restaurar", command=self.revert)
        self.pack(fill="x", padx=5, pady=5)
        self.last_group = parent.last_group
        self.effect_vars = effect_vars

    def revert(self):
        self.last_group.set("None")
        for name, var in self.effect_vars.items():
            var.set(DEFAULT_VALUES[name])


class SliderGroupPanel(Panel):
    def __init__(self, parent, groupLabel, *args):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)

        topLabel = ctk.CTkLabel(self, text=groupLabel)
        topLabel.grid(row=0, column=0, columnspan=3, sticky="w", padx=5)
        topLabel.cget("font").configure(size=20)

        self.variables, self.num_labels = [None] * len(args), [None] * len(args)
        self.last_group = parent.last_group

        for i, (var, name, min_, max_) in enumerate(args):
            self.rowconfigure(i + 1, weight=1)
            self.variables[i] = var
            var.trace_add("write", self.update_text)

            ctk.CTkLabel(self, text=name, width=65, anchor="w").grid(
                row=i + 1, column=0, sticky="w", padx=5
            )

            ctk.CTkSlider(
                self,
                fg_color=SLIDER_BG,
                variable=var,
                from_=min_,
                to=max_,
                number_of_steps=100 if max_ == 1 else max_ - min_,
                command=lambda *args: self.set_group(groupLabel),
            ).grid(row=i + 1, column=1, sticky="ew", padx=5)

            self.num_labels[i] = ctk.CTkLabel(self, text=var.get(), width=65)
            self.num_labels[i].grid(row=i + 1, column=2, sticky="e", padx=5)

    def set_group(self, groupLabel, *args):
        self.last_group.set(groupLabel)

    def update_text(self, name, index, mode):
        for var, num_label in zip(self.variables, self.num_labels):
            if var._name == name:
                num_label.configure(text=f"{round(var.get(), 2):6.2f}")


class RadioButtonGroupPanel(Panel):
    def __init__(self, parent, var, *args):
        super().__init__(parent)
        self.last_group = parent.last_group

        for i, text in enumerate(args):
            self.rowconfigure(i, weight=1)
            radioButton = ctk.CTkRadioButton(
                self,
                text=text,
                variable=var,
                value=text,
                command=self.set_group,
            )
            radioButton.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            radioButton.cget("font").configure(size=20)

    def set_group(self):
        self.last_group.set("Adicional")


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
        frame.pack(fill="x", padx=20, pady=5, expand=True)

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

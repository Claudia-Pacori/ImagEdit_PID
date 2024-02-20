import customtkinter as ctk
from widgets_ import *
from PIL import Image, ImageTk
import scripts.aclarar as aclarar
import scripts.bordes as bordes
import scripts.dilatacion as dilatacion
import scripts.erosion as erosion
import scripts.rotacion as rotacion
import numpy as np


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.geometry("1024x768")
        self.title("Imagedit - Image Editor")
        self.resizable(False, False)
        self.init_parameters()

        self.rowconfigure(0, weight=5, uniform="a")
        self.rowconfigure(1, weight=5, uniform="a")
        self.rowconfigure(2, weight=1, uniform="a")
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=5, uniform="a")

        self.menu = Menu(self)
        self.image_input = ImageInput(self)
        self.image_output = ImageOutput(self)
        self.video_progress_bar = VideoProgressBar(self)

        self.mainloop()

    def init_parameters(self):
        self.last_group = "None"

        self.effect_vars = {
            "gamma": ctk.DoubleVar(value=DEFAULT_VALUES["gamma"]),
            "kernel": ctk.IntVar(value=DEFAULT_VALUES["kernel"]),
            "sigma": ctk.DoubleVar(value=DEFAULT_VALUES["sigma"]),
            "roll": ctk.DoubleVar(value=DEFAULT_VALUES["roll"]),
            "pitch": ctk.DoubleVar(value=DEFAULT_VALUES["pitch"]),
            "yaw": ctk.DoubleVar(value=DEFAULT_VALUES["yaw"]),
            "option": ctk.StringVar(value=DEFAULT_VALUES["option"]),
        }

        for var in self.effect_vars.values():
            var.trace_add("write", self.manipulate_image)

    def manipulate_image(self, *args):
        try:
            self.image_np = self.original_np.copy()
            self.image_bw_np = self.original_bw_np.copy()

            match self.last_group:
                case "Aclarar":
                    self.image_np = aclarar.apply_homomorphic_filter(
                        image=self.image_bw_np, alpha=self.effect_vars["gamma"].get()
                    )
                case "Bordes":
                    self.image_np = bordes.gaussian_highpass_filter(
                        image=self.image_bw_np,
                        kernel_size=self.effect_vars["kernel"].get(),
                        sigma=self.effect_vars["sigma"].get(),
                    )
                case "Rotación":
                    self.image_np = rotacion.rotate_image(
                        image=self.image_np,
                        angle_roll=self.effect_vars["roll"].get(),
                        angle_pitch=self.effect_vars["pitch"].get(),
                        angle_yaw=self.effect_vars["yaw"].get(),
                    )
                case "Adicional":
                    self.image_bw_np = self.original_bw_np.copy()
                    if self.effect_vars["option"].get() == "Dilatación":
                        self.image_np = dilatacion.dilate_image(self.image_bw_np)
                    elif self.effect_vars["option"].get() == "Erosión":
                        self.image_np = erosion.erode_image(self.image_bw_np)
                    else:
                        self.image_np = self.original_np.copy()
                case _:
                    self.image_np = self.original_np.copy()

            if len(self.image_np.shape) == 3 and self.image_np.shape[2] == 4:
                self.image_np = self.image_np[:, :, :3]

            self.image = Image.fromarray(self.image_np)
            self.place_image(self.image_output, self.image)

        except Exception as e:
            pass

    def last_used_group(self, group):
        self.last_group = group

    def import_image(self, path):
        self.original = Image.open(path)
        self.original_np = np.array(self.original)
        self.original_bw = self.original.convert("L")
        self.original_bw_np = np.array(self.original_bw)
        self.image = self.original.copy()
        self.image_ratio = self.original.width / self.original.height
        self.resize_image(self.image_input, self.original)
        self.resize_image(self.image_output, self.image)

    def resize_image(self, frame, image):
        canvas_width = frame.winfo_width()
        canvas_height = frame.winfo_height()
        canvas_ratio = canvas_width / canvas_height

        if canvas_ratio > self.image_ratio:
            image_width = int(canvas_height * self.image_ratio)
            image_height = canvas_height
        else:
            image_width = canvas_width
            image_height = int(canvas_width / self.image_ratio)

        self.canvas_image = (canvas_width, canvas_height, image_width, image_height)

        self.place_image(frame, image)

    def place_image(self, frame, image):
        frame.delete("all")

        canvas_width, canvas_height, image_width, image_height = self.canvas_image

        resized_image = image.resize((image_width, image_height))
        image_tk = ImageTk.PhotoImage(resized_image)
        frame.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=image_tk,
        )

        if frame == self.image_input:
            self.image_tk_in = image_tk
        else:
            self.image_tk_out = image_tk

    def export_image(self, path, name, file):
        export_string = f"{file}/{path}.{name}"
        self.image.save(export_string)


if __name__ == "__main__":
    App()

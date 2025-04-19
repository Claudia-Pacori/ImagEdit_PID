from tkinter import Canvas

import customtkinter as ctk

from menu_ import EffectsFrame, ExportFrame, MenuFrame
from settings_ import BACKGROUND_COLOR, FRAME_COLOR, SLIDER_BG


class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, rowspan=3, column=0, sticky="nsew", pady=10, padx=10)

        self.add("Menu")
        self.add("Efectos")
        self.add("Exportar")

        self.menu_funcs = {
            "OpenImage": parent.import_image,
            "OpenVideo": parent.import_video,
            "OpenWebcam": parent.import_webcam,
            "ExportImage": parent.export_image,
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
        self.current_frame = parent.current_frame
        self.video_status = parent.video_status
        self.slider_update = parent.slider_update

        for i in range(5):
            self.columnconfigure(i, weight=1, uniform="a")
            if i == 3:
                self.columnconfigure(i, weight=7, uniform="a")

        self.play_pause = ctk.CTkButton(
            self, text="Play", state="disabled", command=self.play_pause_video
        )
        self.play_pause.grid(row=0, column=0, padx=5)

        self.stop = ctk.CTkButton(
            self, text="Stop", state="disabled", command=self.stop_video
        )
        self.stop.grid(row=0, column=1, padx=5)

        self.current_time = ctk.CTkLabel(self, text="00:00", state="disabled")
        self.current_time.grid(row=0, column=2, padx=5)

        self.progress = ctk.CTkSlider(
            self, fg_color=SLIDER_BG, command=self.update_current_time, state="disabled"
        )
        self.progress.grid(row=0, column=3, padx=5, sticky="ew")
        self.progress.set(0)

        self.total_time = ctk.CTkLabel(self, text="00:00", state="disabled")
        self.total_time.grid(row=0, column=4, padx=5)

    def initialize_bar(self, total_frames, frame_rate):
        self.play_pause.configure(state="normal")
        self.stop.configure(state="normal")
        self.current_time.configure(state="normal")
        self.progress.configure(state="normal")
        self.total_time.configure(state="normal")

        self.var = self.current_frame
        self.var.trace_add("write", self.update_current_time)

        self.total_frames = total_frames
        self.frame_rate = frame_rate
        self.progress.configure(
            to=total_frames, number_of_steps=total_frames, variable=self.var
        )
        self.total_time.configure(
            text=f"{total_frames // frame_rate // 60:02}:{total_frames // frame_rate % 60:02}"
        )

        self.progress.bind("<ButtonRelease-1>", self.slider_update)

    def disable(self):
        self.play_pause.configure(state="disabled")
        self.stop.configure(state="disabled")
        self.current_time.configure(state="disabled")
        self.progress.configure(state="disabled")
        self.total_time.configure(state="disabled")

    def update_current_time(self, *args):
        current_frame = self.var.get()
        frame_rate = self.frame_rate
        self.current_time.configure(
            text=f"{current_frame // frame_rate // 60:02}:{current_frame // frame_rate % 60:02}"
        )

    def play_pause_video(self):
        if self.play_pause.cget("text") == "Play":
            self.play_pause.configure(text="Pause")
            self.video_status.set("Playing")
        else:
            self.play_pause.configure(text="Play")
            self.video_status.set("Paused")

    def stop_video(self):
        self.play_pause.configure(text="Play")
        self.video_status.set("Stopped")

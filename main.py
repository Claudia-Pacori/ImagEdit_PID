import customtkinter as ctk
from widgets_ import *
from PIL import Image, ImageTk
import scripts.aclarar as aclarar
import scripts.bordes as bordes
import scripts.dilatacion as dilatacion
import scripts.erosion as erosion
import scripts.rotacion as rotacion
from threading import Thread, active_count, main_thread, current_thread
from time import sleep, perf_counter


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        window_height = self.winfo_screenheight()
        window_width = self.winfo_screenwidth()
        window_size = f"{int(0.5*window_width)}x{int(0.5*window_height)}"
        print(window_size)
        self.geometry(window_size)
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
        self.cap = None
        self.image_tk = [None, None]
        self.last_group = ctk.StringVar(value="None")

        self.video_status = ctk.StringVar(value="Paused")
        self.video_status.trace_add("write", self.status_video)

        self.current_frame = ctk.IntVar(value=0)

        self.effect_vars = {
            "gamma": ctk.DoubleVar(value=DEFAULT_VALUES["gamma"]),
            "sigma": ctk.DoubleVar(value=DEFAULT_VALUES["sigma"]),
            "low_th": ctk.DoubleVar(value=DEFAULT_VALUES["low_th"]),
            "high_th": ctk.DoubleVar(value=DEFAULT_VALUES["high_th"]),
            "roll": ctk.DoubleVar(value=DEFAULT_VALUES["roll"]),
            "pitch": ctk.DoubleVar(value=DEFAULT_VALUES["pitch"]),
            "yaw": ctk.DoubleVar(value=DEFAULT_VALUES["yaw"]),
            "option": ctk.StringVar(value=DEFAULT_VALUES["option"]),
        }

        for var in self.effect_vars.values():
            var.trace_add("write", self.manipulate_image_thread)

    def manipulate_image_thread(self, *args):
        if self.type_imported == "image":
            if hasattr(self, 'image_thread') and self.image_thread.is_alive():
                return
            self.image_thread = Thread(target=self.manipulate_image, daemon=True)
            self.image_thread.start()

    def manipulate_image(self, *args):
        try:
            self.image = self.original.copy()
            self.image_bw = self.original_bw.copy()

            match self.last_group.get():
                case "Aclarar":
                    self.image = aclarar.apply_homomorphic_filter(
                        image=self.image, alpha=self.effect_vars["gamma"].get()
                    )
                case "Bordes":
                    self.image = bordes.canny_edge_detection(
                        image=self.image_bw,
                        sigma=self.effect_vars["sigma"].get(),
                        low_threshold=self.effect_vars["low_th"].get(),
                        high_threshold=self.effect_vars["high_th"].get(),
                    )
                case "Rotación":
                    self.image = rotacion.rotate_image(
                        image=self.image,
                        angle_roll=self.effect_vars["roll"].get(),
                        angle_pitch=self.effect_vars["pitch"].get(),
                        angle_yaw=self.effect_vars["yaw"].get(),
                    )
                case "Adicional":
                    if self.effect_vars["option"].get() == "Dilatación":
                        self.image = dilatacion.dilate_image(self.image_bw)
                    elif self.effect_vars["option"].get() == "Erosión":
                        self.image = erosion.erode_image(self.image_bw)
                    else:
                        self.image = self.original.copy()
                case _:
                    self.place_image(self.image_output, self.original)
                    return

            self.place_image(self.image_output, self.image)

        except Exception as e:
            pass

    def import_image(self, path):
        self.image_input.delete("all")
        self.image_output.delete("all")

        if self.cap is not None:
            self.cap.release()

        self.video_progress_bar.disable()

        self.type_imported = "image"
        image_original = cv2.imread(path, cv2.IMREAD_COLOR)
        self.original = cv2.cvtColor(image_original, cv2.COLOR_BGR2RGB)
        self.original_bw = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)

        self.image = self.original.copy()

        height = self.original.shape[0]
        width = self.original.shape[1]
        self.image_ratio = width / height

        self.resize_image(self.image_input, self.original)
        self.resize_image(self.image_output, self.image)

    def import_webcam(self):
        self.image_input.delete("all")
        self.image_output.delete("all")
        self.type_imported = "webcam"
        self.time_frame = 1 / 30

        if self.cap is not None:
            self.cap.release()

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", 0)

        self.video_progress_bar.disable()

        videoWidth = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        videoHeight = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.image_ratio = videoWidth / videoHeight

        ret, frame = self.cap.read()
        if ret:
            self.original = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.original_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            self.image = self.original.copy()

            self.resize_image(self.image_input, self.original)
            self.resize_image(self.image_output, self.image)

        self.webcam_thread = Thread(target=self.webcam_update, daemon=True)
        self.webcam_thread.start()

        self.webcam_output_thread = Thread(target=self.webcam_output_update, daemon=True)
        self.webcam_output_thread.start()

    def webcam_update(self, *args):
        while self.cap.isOpened() and self.type_imported == "webcam":
            ret, frame = self.cap.read()
            if ret:
                t1 = perf_counter()
                self.original = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.original_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                self.place_image(self.image_input, self.original)
                t2 = perf_counter()
                while t2 - t1 < self.time_frame:
                    t2 = perf_counter()

    def webcam_output_update(self, *args):
        while self.cap.isOpened() and self.type_imported == "webcam":
            self.manipulate_image()

    def import_video(self, path: str):
        self.image_input.delete("all")
        self.image_output.delete("all")
        self.type_imported = "video"
        self.current_frame.set(0)

        if self.cap is not None:
            self.cap.release()

        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", path)

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_rate = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.time_frame = 1 / self.frame_rate

        videoWidth = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        videoHeight = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.image_ratio = videoWidth / videoHeight

        self.video_progress_bar.initialize_bar(self.total_frames, self.frame_rate)

        ret, frame = self.cap.read()
        if ret:
            self.original = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.original_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.image = self.original.copy()

            self.resize_image(self.image_input, self.original)
            self.resize_image(self.image_output, self.image)

    def slider_update(self, *args):
        if self.cap is not None and self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame.get())

    def status_video(self, *args):
        if self.video_status.get() == "Playing":
            self.video_thread = Thread(target=self.video_update, daemon=True)
            self.output_thread = Thread(target=self.output_update, daemon=True)
            print("Video thread started...")
            self.video_thread.start()
            self.output_thread.start()

    def video_update(self, *args):
        while self.video_status.get() == "Playing":
            t1 = perf_counter()
            self.current_frame.set(self.current_frame.get() + 1)
            if self.current_frame.get() >= self.total_frames:
                self.current_frame.set(0)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.update_video_frame()
            t2 = perf_counter()
            while t2 - t1 < self.time_frame:
                t2 = perf_counter()
        if self.video_status.get() == "Stopped":
            self.current_frame.set(0)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.update_video_frame()

    def output_update(self, *args):
        while self.video_status.get() == "Playing":
            self.manipulate_image()
        if self.video_status.get() == "Stopped":
            self.manipulate_image()

    def update_video_frame(self, *args):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.original = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.original_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.place_image(self.image_input, self.original)

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
        canvas_width, canvas_height, image_width, image_height = self.canvas_image

        i = 0 if frame == self.image_input else 1

        resized_image = cv2.resize(image, (image_width, image_height))
        self.image_tk[i] = ImageTk.PhotoImage(Image.fromarray(resized_image))
        frame.delete("all")
        frame.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.image_tk[i],
        )

    def export_image(self, path, name, file):
        export_string = f"{file}/{path}.{name}"
        cv2.imwrite(export_string, self.image)

if __name__ == "__main__":
    App()

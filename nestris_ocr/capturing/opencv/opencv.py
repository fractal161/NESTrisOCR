import cv2
from multiprocessing import Lock
from multiprocessing.pool import ThreadPool

from PIL import Image
import time
import platform
from typing import Tuple

from nestris_ocr.capturing.base import AbstractCapture
from nestris_ocr.utils import xywh_to_ltrb
from nestris_ocr.types import XYWHBox


class OpenCVCapture(AbstractCapture):
    def __init__(self, source_id: str, xywh_box: XYWHBox) -> None:
        super().__init__(source_id, xywh_box)
        print("Initializing capture device")
        if platform.system() == "Windows":
            self.cap = cv2.VideoCapture(int(source_id), cv2.CAP_DSHOW)
            # todo: call benchmark_setup and cache result in config?
        else:
            self.cap = cv2.VideoCapture(int(source_id))
        self.cv2_retval = None
        self.cv2_image = None
        self.image_ts = None

        self.started = False
        self.read_lock = Lock()
        self.start()

    def benchmark_startup(self, source_id):
        times = []
        WINDOWS_BACKENDS = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_VFW]
        for backend in WINDOWS_BACKENDS:
            timer = time.time()
            try:
                cap = cv2.VideoCapture(int(source_id), backend)
                cap.release()
            except:  # noqa  E722
                times.append(10, backend)
            else:
                times.append((time.time() - timer, backend))
        times.sort(key=lambda x: x[0])
        print(times[0])

    def get_image(self, rgb: bool = False) -> Tuple[float, Image.Image]:
        if not self.cv2_retval:
            raise Exception("Faulty capturing device")

        with self.read_lock:
            cv2_image = self.cv2_image.copy()
            image_ts = self.image_ts

        if rgb:
            cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(cv2_image).crop(xywh_to_ltrb(self.xywh_box))

        return image_ts, image

    def start(self):
        if self.started:
            print("[!] Threaded video capturing has already been started.")
            return None
        self.started = True
        self.pool = ThreadPool(processes=1)
        self.pool.apply_async(self.update)

    def update(self):
        while self.started:
            cv2_retval, cv2_image = self.cap.read()
            with self.read_lock:
                self.cv2_retval = cv2_retval
                self.cv2_image = cv2_image
                self.image_ts = time.time()

    def stop(self):
        self.started = False

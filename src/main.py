import logging
import platform
import threading
import tkinter as tk
from tkinter import ttk

from src.ui.body import BodyTelegramBot
from src.ui.header import Header
from src.utils.logger import ConsoleUi, logger


class TelegramAccountCreator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        logging.basicConfig(level=logging.INFO)
        self.rowconfigure([1, 2], weight=1)  # type: ignore
        self.columnconfigure(0, weight=1, uniform="fred")
        self.resizable(False, False)
        self.geometry("800x550")
        self._current_running_tab = None
        style_cbox = ttk.Style()
        style_cbox.map("BW.TCombobox", fieldbackground=[("readonly", "white")])
        current_os = platform.system().lower()
        if current_os == "linux":
            icon = tk.PhotoImage(file="src/icons/linux/telegram.png")
            self.call("wm", "iconphoto", self._w, icon)  # type: ignore
        elif platform.system().lower() == "windows":
            self.iconbitmap(default=f"src/icons/{current_os}/telegram.ico")
        else:
            print("Not recognized platform. No icon will be set.")
            raise Exception("Not recognized platform.")

        self.title("Telegram Auto Account")
        self.header = Header(parent=self)
        self.header.grid(row=0, column=0, sticky="w")

        self.ui_body = BodyTelegramBot(self)
        self.ui_body.grid(row=1, column=0, sticky="nsew")

        self.header.btn_run.configure(command=self.run)
        self.header.btn_pause.configure(command=self.pause)
        self.header.btn_stop.configure(command=self.stop)

        console = ConsoleUi(self)
        console.grid(row=2, column=0, sticky="nsew")
        logger.info("App starting")

    def run(self):

        if not self._current_running_tab:
            self._current_running_tab = self.ui_body
            self._current_running_tab.run()
            if self._current_running_tab.frame_thread:
                threading.Thread(
                    target=self.reset_status_after_complete, args=[self._current_running_tab.frame_thread]
                ).start()
            else:
                self._current_running_tab = None
                return

            self.header.btn_run["state"] = "disabled"
            self.header.btn_pause["state"] = "normal"
            self.header.btn_stop["state"] = "enabled"
            self.change_status_of_frame(tk.DISABLED)
            self.header.btn_run["text"] = "Resume"
        else:
            self._current_running_tab.run()

    def pause(self):
        if self._current_running_tab:
            self.header.btn_run["state"] = "normal"
            self.header.btn_pause["state"] = "disabled"
            self.header.btn_stop["state"] = "disabled"
            self._current_running_tab.pause()

    def stop(self):
        if self._current_running_tab:
            self._current_running_tab.stop()

    def reset_status_after_complete(self, thread: threading.Thread):
        thread.join()
        self.header.btn_run["state"] = "normal"
        self.header.btn_pause["state"] = "disabled"
        self.header.btn_stop["state"] = "disabled"
        self.change_status_of_frame(tk.NORMAL)
        self._current_running_tab = None
        self.header.btn_run["text"] = "Run"

    @property
    def get_current_running_tab(self):
        return self._current_running_tab

    def change_status_of_frame(self, state):
        for child in self._current_running_tab.winfo_children():  # type: ignore
            child.configure(state=state)  # type: ignore


def main():
    nft_app = TelegramAccountCreator()
    nft_app.mainloop()


if __name__ == "__main__":
    nft_app = TelegramAccountCreator()
    nft_app.mainloop()
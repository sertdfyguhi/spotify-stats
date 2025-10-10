from reader import ListeningHistoryReader
import dearpygui.dearpygui as dpg
from windows import WINDOWS

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

dpg.create_context()
dpg.create_viewport(title="Spotify Stats", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

reader = None

with dpg.font_registry():
    dpg.add_font("font/SFMono-Regular.otf", 14, tag="default_font")
    dpg.add_font("font/SFMono-Bold.otf", 14, tag="bold_font")

with dpg.window(show=False) as main_window:
    with dpg.menu_bar():
        current_window = list(WINDOWS.keys())[0]

        def change_window_callback(window):
            global current_window

            if window != current_window:
                dpg.hide_item(current_window + "_window")

                if dpg.does_item_exist(window + "_window"):
                    dpg.show_item(window + "_window")
                else:
                    WINDOWS[window](reader, main_window)

                current_window = window

        for window in WINDOWS:
            dpg.add_button(label=window, tag=window, callback=change_window_callback)

dpg.set_primary_window(main_window, True)


def load_folder_callback():
    global reader

    dpg.configure_item("load_button", label="Loading...")

    reader = ListeningHistoryReader(dpg.get_value("folder_path"))
    WINDOWS[current_window](reader, main_window)

    dpg.show_item(main_window)
    dpg.hide_item("importer_window")
    dpg.hide_item("file_dialog")


def file_dialog_callback(sender, app_data):
    dpg.set_value("folder_path", app_data["file_path_name"])


dpg.add_file_dialog(
    directory_selector=True,
    callback=file_dialog_callback,
    tag="file_dialog",
    width=700,
    height=400,
    show=False,
)

with dpg.window(
    label="Importer",
    tag="importer_window",
    width=WINDOW_WIDTH / 2,
    height=WINDOW_HEIGHT / 2,
    pos=(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4),
):
    with dpg.group(horizontal=True):
        dpg.add_input_text(width=WINDOW_WIDTH / 5, tag="folder_path")
        dpg.add_button(
            label="Find Directory", callback=lambda: dpg.show_item("file_dialog")
        )

    dpg.add_button(label="Load Data", callback=load_folder_callback, tag="load_button")

dpg.bind_font("default_font")

if __name__ == "__main__":
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

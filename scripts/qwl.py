import webbrowser
import urllib.parse
import keyboard
import sys
import time
from threading import Event

try:
    import tkinter as tk
except ImportError:
    print("tkinter is needed. Install python3-tk if you use Linux.")
    sys.exit(1)


BASE_URL_TEMPLATE = "https://www.google.com/search?q={query}"
BASE_URL_PREFIX = "https://www.google.com/search?q="

HOTKEY_OPEN = "ctrl+alt+space"
HOTKEY_QUIT = "ctrl+alt+q"

WINDOW_TITLE = "Quick Web Launcher"
PLACEHOLDER = "Input text..."
WIDTH_PX = 520
PADDING = 12


def build_url(query: str) -> str:
    encoded = urllib.parse.quote_plus(query.strip())
    #encoded = query

    if "{query}" in BASE_URL_TEMPLATE:
        return BASE_URL_TEMPLATE.format(query=encoded)
    
    if not (BASE_URL_PREFIX.startswith("http://") or BASE_URL_PREFIX.startswith("https://")):
        prefix = "https://" + BASE_URL_PREFIX
    else:
        prefix = BASE_URL_PREFIX
    
    return prefix + encoded


def open_input_window() -> None:
    root = tk.Tk()
    root.title(WINDOW_TITLE)

    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = int((screen_w - WIDTH_PX) / 2)
    y = int(screen_h * 0.28)
    root.geometry(f"{WIDTH_PX}x120+{x}+{y}")

    try:
        root.attributes("-topmost", True)
    except Exception:
        pass

    frame = tk.Frame(root, padx=PADDING, pady=PADDING)
    frame.pack(fill="both", expand=True)

    label = tk.Label(frame, text="Input text -> Enter / Cancel -> Esc", anchor="w")
    label.pack(fill="x")

    var = tk.StringVar()
    entry = tk.Entry(frame, textvariable=var, font=("Consolas, Calibri", 14))
    entry.pack(fill="x", pady=(6, 0))
    entry.focus_set()

    entry.insert(0, PLACEHOLDER)

    def on_focus_in(_):
        if entry.get() == PLACEHOLDER:
            entry.delete(0, "end")
    
    def on_focus_out(_):
        if not entry.get():
            entry.insert(0, PLACEHOLDER)
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    def submit(_event=None):
        text = entry.get().strip()
        if not text or text == PLACEHOLDER:
            root.destroy()
            return
        url = build_url(text)

        webbrowser.open_new_tab(url)
        root.destroy()
    
    def cancel(_event=None):
        root.destroy()
    
    root.bind("<Return>", submit)
    root.bind("<Escape>", cancel)

    root.mainloop()


def main():
    print(f"[Quick Web Launcher] is being executed.")
    print(f" - To open the text box: {HOTKEY_OPEN}")
    print(f" - To quit: {HOTKEY_QUIT}")
    print(f" - Current template: {BASE_URL_TEMPLATE!r}")
    stop_event = Event()

    def open_cb():
        triggers.append(time.time())
    
    def quit_cb():
        stop_event.set()

    global triggers
    triggers = []

    keyboard.add_hotkey(HOTKEY_OPEN, open_cb)
    keyboard.add_hotkey(HOTKEY_QUIT, quit_cb)

    try:
        while not stop_event.is_set():
            if triggers:
                _ = triggers.pop(0)
                open_input_window()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.clear_all_hotkeys()
        print("[Quick Web Launcher] has been terminated.")



if __name__ == "__main__":
    main()

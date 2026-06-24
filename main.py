import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import pyttsx3

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# ==========================
# Text To Speech
# ==========================

engine = pyttsx3.init()

# ==========================
# Main Window
# ==========================

root = tk.Tk()
root.title("AI Language Translator")
root.geometry("900x700")
root.configure(bg="#EAF4FF")

dark_mode = False

# ==========================
# Functions
# ==========================

def translate_text():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Warning",
            "Please enter some text."
        )
        return

    try:
        translated = GoogleTranslator(
            source=source_lang.get(),
            target=target_lang.get()
        ).translate(text)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)

        # Romanized Hindi

        roman_text.delete("1.0", tk.END)

        if target_lang.get() == "hindi":
            try:
                roman = transliterate(
                    translated,
                    sanscript.DEVANAGARI,
                    sanscript.HK
                )

                roman_text.insert(
                    tk.END,
                    roman.lower()
                )

            except:
                roman_text.insert(
                    tk.END,
                    "Romanization unavailable"
                )

        else:
            roman_text.insert(
                tk.END,
                "Available only for Hindi translations."
            )

    except Exception as e:
        messagebox.showerror(
            "Translation Error",
            str(e)
        )


def swap_languages():

    src = source_lang.get()
    tgt = target_lang.get()

    source_lang.set(tgt)
    target_lang.set(src)


def copy_translation():

    text = output_text.get(
        "1.0",
        tk.END
    ).strip()

    root.clipboard_clear()
    root.clipboard_append(text)

    messagebox.showinfo(
        "Copied",
        "Translation copied!"
    )


def speak_translation():

    text = output_text.get(
        "1.0",
        tk.END
    ).strip()

    if text:
        engine.say(text)
        engine.runAndWait()


def toggle_theme():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        bg = "#1E1E1E"
        fg = "white"
        box = "#2D2D2D"

        root.configure(bg=bg)

        title_label.configure(
            bg=bg,
            fg="#64B5F6"
        )

        for label in labels:
            label.configure(
                bg=bg,
                fg=fg
            )

        input_text.configure(
            bg=box,
            fg="white",
            insertbackground="white"
        )

        output_text.configure(
            bg=box,
            fg="white",
            insertbackground="white"
        )

        roman_text.configure(
            bg=box,
            fg="white",
            insertbackground="white"
        )

        button_frame.configure(bg=bg)
        lang_frame.configure(bg=bg)

    else:

        bg = "#EAF4FF"

        root.configure(bg=bg)

        title_label.configure(
            bg=bg,
            fg="#1565C0"
        )

        for label in labels:
            label.configure(
                bg=bg,
                fg="black"
            )

        input_text.configure(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        output_text.configure(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        roman_text.configure(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        button_frame.configure(bg=bg)
        lang_frame.configure(bg=bg)

# ==========================
# Title
# ==========================

title_label = tk.Label(
    root,
    text="🌍 AI Language Translator",
    font=("Arial", 24, "bold"),
    bg="#EAF4FF",
    fg="#1565C0"
)

title_label.pack(
    pady=15
)

# ==========================
# Input
# ==========================

label_input = tk.Label(
    root,
    text="Enter Text",
    font=("Arial", 12, "bold"),
    bg="#EAF4FF"
)

label_input.pack()

input_text = tk.Text(
    root,
    height=7,
    font=("Arial", 12),
    bd=2,
    relief="groove"
)

input_text.pack(
    fill="x",
    padx=20,
    pady=10
)

# ==========================
# Languages
# ==========================

lang_frame = tk.Frame(
    root,
    bg="#EAF4FF"
)

lang_frame.pack(
    pady=10
)

languages = sorted(
    GoogleTranslator().get_supported_languages()
)

label_source = tk.Label(
    lang_frame,
    text="Source Language",
    bg="#EAF4FF"
)

label_source.grid(
    row=0,
    column=0,
    padx=25
)

label_target = tk.Label(
    lang_frame,
    text="Target Language",
    bg="#EAF4FF"
)

label_target.grid(
    row=0,
    column=1,
    padx=25
)

source_lang = ttk.Combobox(
    lang_frame,
    values=languages,
    width=25
)

source_lang.set("english")

source_lang.grid(
    row=1,
    column=0,
    padx=25
)

target_lang = ttk.Combobox(
    lang_frame,
    values=languages,
    width=25
)

target_lang.set("hindi")

target_lang.grid(
    row=1,
    column=1,
    padx=25
)

# ==========================
# Buttons
# ==========================

button_frame = tk.Frame(
    root,
    bg="#EAF4FF"
)

button_frame.pack(
    pady=15
)

tk.Button(
    button_frame,
    text="🚀 Translate",
    bg="#4CAF50",
    fg="white",
    width=14,
    command=translate_text
).grid(
    row=0,
    column=0,
    padx=5
)

tk.Button(
    button_frame,
    text="🔄 Swap",
    bg="#2196F3",
    fg="white",
    width=12,
    command=swap_languages
).grid(
    row=0,
    column=1,
    padx=5
)

tk.Button(
    button_frame,
    text="📋 Copy",
    bg="#FF9800",
    fg="white",
    width=12,
    command=copy_translation
).grid(
    row=0,
    column=2,
    padx=5
)

tk.Button(
    button_frame,
    text="🔊 Speak",
    bg="#009688",
    fg="white",
    width=12,
    command=speak_translation
).grid(
    row=0,
    column=3,
    padx=5
)

tk.Button(
    button_frame,
    text="🌙 Dark Mode",
    bg="#673AB7",
    fg="white",
    width=14,
    command=toggle_theme
).grid(
    row=0,
    column=4,
    padx=5
)

# ==========================
# Translation Output
# ==========================

label_output = tk.Label(
    root,
    text="Translation",
    font=("Arial", 12, "bold"),
    bg="#EAF4FF"
)

label_output.pack(
    pady=(10, 0)
)

output_text = tk.Text(
    root,
    height=7,
    font=("Noto Sans Devanagari", 14),
    bd=2,
    relief="groove"
)

output_text.pack(
    fill="x",
    padx=20,
    pady=10
)

# ==========================
# Romanized Text
# ==========================

label_roman = tk.Label(
    root,
    text="Romanized Hindi",
    font=("Arial", 12, "bold"),
    bg="#EAF4FF"
)

label_roman.pack(
    pady=(10, 0)
)

roman_text = tk.Text(
    root,
    height=4,
    font=("Arial", 12),
    bd=2,
    relief="groove"
)

roman_text.pack(
    fill="x",
    padx=20,
    pady=10
)

# ==========================
# Footer
# ==========================

footer = tk.Label(
    root,
    text="Made with Python 🐍 + Tkinter",
    bg="#EAF4FF",
    fg="gray"
)

footer.pack(
    pady=10
)

labels = [
    label_input,
    label_source,
    label_target,
    label_output,
    label_roman,
    footer
]

root.mainloop()
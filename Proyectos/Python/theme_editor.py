import tkinter as tk
from tkinter import ttk, colorchooser

def edit_ui_elements(bot):
    """Ventana para editar colores y textos de la interfaz."""
    edit_window = tk.Toplevel(bot.window)
    edit_window.title("Edit UI Elements")
    edit_window.geometry("500x600")
    theme = bot.themes[bot.current_theme]
    edit_window.configure(bg=theme["window_bg"])

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), background=theme["window_bg"], foreground=theme["label_fg"])
    style.configure("TButton", font=("Apple Color Emoji", 11) if "Apple Color Emoji" in font.families() else ("Arial Unicode MS", 11), padding=8, foreground=theme["button_fg"], background=theme["button_bg"])
    style.map("TButton", background=[("active", theme["button_bg"])], foreground=[("active", theme["button_fg"])])

    title_label = ttk.Label(edit_window, text="Edit UI Elements", style="TLabel")
    title_label.pack(pady=10)

    theme_label = ttk.Label(edit_window, text="Select Theme:", style="TLabel")
    theme_label.pack(pady=5)
    theme_combo = ttk.Combobox(edit_window, values=list(bot.themes.keys()), state="readonly")
    theme_combo.set(bot.current_theme)
    theme_combo.pack(pady=5)

    elements = ["window_bg", "frame_bg", "label_fg", "button_bg", "button_fg", "text_bg", "text_fg", "highlight"]
    color_entries = {}
    color_buttons = {}
    color_display = {}

    frame = ttk.Frame(edit_window)
    frame.pack(pady=10, fill="x", padx=20)

    def update_color_elements():
        selected_theme = theme_combo.get()
        for element in elements:
            color = bot.themes[selected_theme][element]
            color_entries[element].delete(0, tk.END)
            color_entries[element].insert(0, color)
            color_buttons[element].configure(bg=color)
            color_display[element].configure(bg=color)

    for element in elements:
        elem_frame = ttk.Frame(frame)
        elem_frame.pack(fill="x", pady=5)
        ttk.Label(elem_frame, text=f"{element}:", style="TLabel").pack(side=tk.LEFT, padx=5)
        
        color_display[element] = tk.Label(elem_frame, width=3, height=1, bg=bot.themes[theme_combo.get()][element], relief="ridge")
        color_display[element].pack(side=tk.LEFT, padx=5)

        color_entries[element] = ttk.Entry(elem_frame)
        color_entries[element].insert(0, bot.themes[theme_combo.get()][element])
        color_entries[element].pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        color_buttons[element] = tk.Button(elem_frame, text="Pick", command=lambda el=element: pick_color(el))
        color_buttons[element].pack(side=tk.LEFT, padx=5)

    def pick_color(element):
        color = colorchooser.askcolor(title=f"Choose color for {element}")[1]
        if color:
            color_entries[element].delete(0, tk.END)
            color_entries[element].insert(0, color)
            color_buttons[element].configure(bg=color)
            color_display[element].configure(bg=color)

    theme_combo.bind("<<ComboboxSelected>>", lambda event: update_color_elements())

    def save_changes():
        try:
            selected_theme = theme_combo.get()
            for element in elements:
                bot.themes[selected_theme][element] = color_entries[element].get()
            bot.apply_theme(selected_theme)
            with open("themes.json", "w") as f:
                json.dump(bot.themes, f, indent=4)
            bot.log(f"UI elements for theme {selected_theme} updated and saved.")
            edit_window.destroy()
        except Exception as e:
            bot.log(f"Error saving UI elements: {str(e)}", "error")

    button_frame = ttk.Frame(edit_window)
    button_frame.pack(pady=20)
    ttk.Button(button_frame, text="Save", command=save_changes).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=10)

    update_color_elements()

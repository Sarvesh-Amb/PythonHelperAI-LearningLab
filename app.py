import tkinter as tk
from tkinter import ttk, messagebox

from curriculum import load_chapters, get_chapter_by_id
from model_manager import get_provider_status, choose_model


class TutorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PythonHelperAI Learning Lab")
        self.geometry("1100x720")
        self.minsize(900, 620)

        self.chapters = load_chapters()
        self.current_chapter_id = 1 if self.chapters else None
        self.provider_var = tk.StringVar(value="auto")
        self.model_var = tk.StringVar(value="gemma3:1b")

        self.build_ui()
        self.show_current_chapter()
        self.refresh_status()

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        root = ttk.Frame(self, padding=12)
        root.grid(row=0, column=0, sticky="nsew")
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        title = ttk.Label(root, text="PythonHelperAI Learning Lab", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        left_panel = ttk.LabelFrame(root, text="Setup")
        left_panel.grid(row=1, column=0, sticky="ns", padx=(0, 12), pady=(0, 12))
        left_panel.columnconfigure(0, weight=1)

        ttk.Label(left_panel, text="Provider").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        provider_combo = ttk.Combobox(left_panel, textvariable=self.provider_var, values=["auto", "local", "cloud"], state="readonly")
        provider_combo.grid(row=1, column=0, padx=10, sticky="ew", pady=(0, 8))

        ttk.Label(left_panel, text="Model").grid(row=2, column=0, sticky="w", padx=10, pady=(0, 5))
        model_combo = ttk.Combobox(left_panel, textvariable=self.model_var, values=["gemma3:1b", "gemma3:2b", "gemma3:4b", "qwen2.5-coder:3b", "gpt-4o-mini"], state="readonly")
        model_combo.grid(row=3, column=0, padx=10, sticky="ew", pady=(0, 8))

        ttk.Button(left_panel, text="Refresh status", command=self.refresh_status).grid(row=4, column=0, padx=10, sticky="ew", pady=(0, 8))
        ttk.Button(left_panel, text="Use selected model", command=self.use_selected_model).grid(row=5, column=0, padx=10, sticky="ew", pady=(0, 8))

        main_panel = ttk.LabelFrame(root, text="Current chapter")
        main_panel.grid(row=1, column=1, sticky="nsew")
        main_panel.columnconfigure(0, weight=1)
        main_panel.rowconfigure(2, weight=1)

        self.chapter_title = ttk.Label(main_panel, text="", font=("Segoe UI", 12, "bold"))
        self.chapter_title.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 6))

        self.chapter_overview = tk.Text(main_panel, wrap="word", height=16, state="disabled")
        self.chapter_overview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.exercise_list = tk.Listbox(main_panel, height=8)
        self.exercise_list.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        nav = ttk.Frame(root)
        nav.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(4, 0))
        nav.columnconfigure(0, weight=1)
        nav.columnconfigure(1, weight=1)

        ttk.Button(nav, text="Previous", command=self.previous_chapter).grid(row=0, column=0, sticky="w")
        ttk.Button(nav, text="Next", command=self.next_chapter).grid(row=0, column=1, sticky="e")

        self.status_box = ttk.LabelFrame(root, text="Status")
        self.status_box.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(12, 0))
        self.status_text = tk.Text(self.status_box, wrap="word", height=8, state="disabled")
        self.status_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def refresh_status(self):
        status = get_provider_status()
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", tk.END)
        self.status_text.insert("1.0", status)
        self.status_text.configure(state="disabled")

    def use_selected_model(self):
        provider = self.provider_var.get()
        model = self.model_var.get()
        chosen = choose_model(provider, model)
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", tk.END)
        self.status_text.insert("1.0", f"Selected provider: {provider}\nSelected model: {model}\nEffective model: {chosen}")
        self.status_text.configure(state="disabled")

    def show_current_chapter(self):
        if not self.chapters:
            self.chapter_title.config(text="No chapters available")
            return
        chapter = get_chapter_by_id(self.chapters, self.current_chapter_id)
        if chapter is None:
            chapter = self.chapters[0]
            self.current_chapter_id = chapter["id"]

        self.chapter_title.config(text=f"Chapter {chapter['id']}: {chapter['title']}")
        self.chapter_overview.configure(state="normal")
        self.chapter_overview.delete("1.0", tk.END)
        self.chapter_overview.insert("1.0", chapter.get("overview", ""))
        self.chapter_overview.configure(state="disabled")

        self.exercise_list.delete(0, tk.END)
        for idx, exercise in enumerate(chapter.get("exercises", []), start=1):
            self.exercise_list.insert(tk.END, f"{idx}. {exercise}")

    def previous_chapter(self):
        if not self.chapters:
            return
        current_index = next((i for i, chapter in enumerate(self.chapters) if chapter["id"] == self.current_chapter_id), 0)
        if current_index > 0:
            self.current_chapter_id = self.chapters[current_index - 1]["id"]
            self.show_current_chapter()

    def next_chapter(self):
        if not self.chapters:
            return
        current_index = next((i for i, chapter in enumerate(self.chapters) if chapter["id"] == self.current_chapter_id), 0)
        if current_index < len(self.chapters) - 1:
            self.current_chapter_id = self.chapters[current_index + 1]["id"]
            self.show_current_chapter()


if __name__ == "__main__":
    app = TutorApp()
    app.mainloop()

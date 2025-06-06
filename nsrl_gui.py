import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Iterable, List

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:  # pragma: no cover - drag and drop optional
    TkinterDnD = tk  # type: ignore[attr-defined]
    DND_FILES = "DND_Files"

def extract_hashes(db_paths: Iterable[str], output_path: str, hash_type: str) -> None:
    """Extract hashes from one or more NSRL databases into ``output_path``."""

    def column_for_hash(cur) -> str:
        cur.execute("PRAGMA table_info(NSRLFile)")
        for _cid, name, *_rest in cur.fetchall():
            if name.lower().replace("-", "") == hash_type.lower():
                return name
        raise ValueError(f"{hash_type} column not found in NSRLFile table")

    with open(output_path, "w") as outfile:
        for db_path in db_paths:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            column = column_for_hash(cur)
            query = f'SELECT "{column}" FROM NSRLFile'
            for row in cur.execute(query):
                value = row[0]
                if value:
                    outfile.write(str(value).strip() + "\n")
            conn.close()

class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("NSRL Hash Extractor")
        self.geometry("400x200")
        self.db_paths: List[str] = []
        self.hash_type = tk.StringVar(value="md5")

        self.drop_label = tk.Label(
            self,
            text="Drag and drop NSRL database (.db) files here",
            relief="ridge",
            width=40,
            height=5,
        )
        self.drop_label.pack(pady=10)
        try:
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind('<<Drop>>', self.handle_drop)
        except Exception:
            # Drag and drop not available; fall back to button
            browse_button = tk.Button(self, text="Browse", command=self.browse_files)
            browse_button.pack()

        md5_radio = tk.Radiobutton(self, text="MD5", variable=self.hash_type, value="md5")
        sha1_radio = tk.Radiobutton(self, text="SHA1", variable=self.hash_type, value="sha1")
        md5_radio.pack()
        sha1_radio.pack()

        export_button = tk.Button(self, text="Export Hashes", command=self.export_hashes)
        export_button.pack(pady=10)

    def handle_drop(self, event):
        paths = self.tk.splitlist(event.data)
        self.set_db_paths(list(paths))

    def browse_files(self):
        paths = filedialog.askopenfilenames(
            filetypes=[("DB files", "*.db"), ("All files", "*.*")]
        )
        if paths:
            self.set_db_paths(list(paths))

    def set_db_paths(self, paths):
        self.db_paths = paths
        if len(paths) == 1:
            label = paths[0]
        else:
            label = f"{len(paths)} files selected"
        self.drop_label.config(text=label)

    def export_hashes(self):
        if not self.db_paths:
            messagebox.showerror("Error", "No database selected")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not output_path:
            return
        try:
            extract_hashes(self.db_paths, output_path, self.hash_type.get())
            messagebox.showinfo("Success", f"Hashes saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = Application()
    app.mainloop()

import customtkinter as ctk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import os
import sys
from pdf2docx import Converter
from tkinter import messagebox, filedialog, simpledialog

class LitePDFReader(ctk.CTk):
    def __init__(self, file_to_open=None):
        super().__init__()
        self.title("LitePDF Ultra Pro - Liyas Syarifudin, S.Pd.I, M.Pd")
        self.geometry("1300x900")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # State
        self.pdf_doc = None
        self.file_path = None
        self.current_page = 0
        self.zoom_level = 1.3
        self.mode = "view" # view, edit, sign
        self.tk_img = None

        # --- Ribbon UI ---
        self.ribbon = ctk.CTkTabview(self, height=150)
        self.ribbon.pack(side="top", fill="x", padx=10, pady=5)
        
        self.tab_view = self.ribbon.add("Tampilan & Navigasi")
        self.tab_edit = self.ribbon.add("Edit & Tanda Tangan")
        self.tab_conv = self.ribbon.add("Konversi")

        self.setup_ribbon()

        # --- Workspace ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#A0A0A0")
        self.scroll_frame.pack(fill="both", expand=True)
        self.canvas = ctk.CTkCanvas(self.scroll_frame, bg="white", highlightthickness=1)
        self.canvas.pack(pady=20)
        
        # Events
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_draw)

        if file_to_open: self.load_pdf(file_to_open)

    def setup_ribbon(self):
        # Tab 1: Navigasi (Fungsi Utama Membaca)
        f_nav = ctk.CTkFrame(self.tab_view, fg_color="transparent")
        f_nav.pack(side="left", padx=10)
        ctk.CTkButton(f_nav, text="Buka PDF", command=self.open_pdf, width=100).pack(side="left", padx=5)
        ctk.CTkButton(f_nav, text="◀", command=self.prev_page, width=40).pack(side="left", padx=2)
        self.lbl_page = ctk.CTkLabel(f_nav, text="0 / 0", font=("Arial", 14, "bold"))
        self.lbl_page.pack(side="left", padx=10)
        ctk.CTkButton(f_nav, text="▶", command=self.next_page, width=40).pack(side="left", padx=2)
        
        ctk.CTkLabel(self.tab_view, text="Zoom:").pack(side="left", padx=(20, 5))
        self.zoom_slider = ctk.CTkSlider(self.tab_view, from_=0.5, to=2.5, command=self.update_zoom, width=150)
        self.zoom_slider.set(self.zoom_level)
        self.zoom_slider.pack(side="left", padx=5)

        # Tab 2: Edit (Fungsi Tambahan Tanpa Merusak Struktur)
        self.btn_edit = ctk.CTkButton(self.tab_edit, text="Mode Edit Teks", command=lambda: self.set_mode("edit"), fg_color="gray")
        self.btn_edit.pack(side="left", padx=5)
        self.btn_sign = ctk.CTkButton(self.tab_edit, text="Tanda Tangan", command=lambda: self.set_mode("sign"), fg_color="gray")
        self.btn_sign.pack(side="left", padx=5)
        ctk.CTkButton(self.tab_edit, text="Simpan Langsung", command=self.save_incremental, fg_color="#217346").pack(side="left", padx=5)

        # Tab 3: Konversi
        ctk.CTkButton(self.tab_conv, text="Export ke Word (.docx)", command=self.to_word).pack(pady=10)

    def set_mode(self, mode):
        self.mode = mode if self.mode != mode else "view"
        color_e = "#0078D4" if self.mode == "edit" else "gray"
        color_s = "#0078D4" if self.mode == "sign" else "gray"
        self.btn_edit.configure(fg_color=color_e)
        self.btn_sign.configure(fg_color=color_s)
        self.canvas.configure(cursor="ibeam" if self.mode == "edit" else "pencil" if self.mode == "sign" else "")

    def load_pdf(self, path):
        self.file_path = path
        self.pdf_doc = fitz.open(path)
        self.current_page = 0
        self.render_page()

    def render_page(self):
        if not self.pdf_doc: return
        page = self.pdf_doc.load_page(self.current_page)
        pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom_level, self.zoom_level))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.config(width=pix.width, height=pix.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.lbl_page.configure(text=f"{self.current_page + 1} / {len(self.pdf_doc)}")

    def handle_click(self, event):
        if self.mode == "edit" and self.pdf_doc:
            pdf_x, pdf_y = event.x / self.zoom_level, event.y / self.zoom_level
            page = self.pdf_doc[self.current_page]
            for b in page.get_text("dict")["blocks"]:
                if "lines" in b:
                    for l in b["lines"]:
                        for s in l["spans"]:
                            r = fitz.Rect(s["bbox"])
                            if r.contains(fitz.Point(pdf_x, pdf_y)):
                                new_t = simpledialog.askstring("Edit", "Ubah Kalimat:", initialvalue=s["text"])
                                if new_t:
                                    page.add_redact_annot(r, fill=(1,1,1))
                                    page.apply_redactions()
                                    page.insert_text((r.x0, r.y1-2), new_t, fontsize=s["size"])
                                    self.render_page()
                                return

    def handle_draw(self, event):
        if self.mode == "sign":
            self.canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill="black")

    def save_incremental(self):
        if self.pdf_doc:
            try:
                self.pdf_doc.saveIncremental()
                messagebox.showinfo("Sukses", "Perubahan disimpan!")
            except:
                self.pdf_doc.save(self.file_path + ".tmp")
                self.pdf_doc.close()
                os.replace(self.file_path + ".tmp", self.file_path)
                self.pdf_doc = fitz.open(self.file_path)
                messagebox.showinfo("Sukses", "File diperbarui!")

    def open_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path: self.load_pdf(path)

    def prev_page(self):
        if self.pdf_doc and self.current_page > 0:
            self.current_page -= 1; self.render_page()

    def next_page(self):
        if self.pdf_doc and self.current_page < len(self.pdf_doc)-1:
            self.current_page += 1; self.render_page()

    def update_zoom(self, v):
        self.zoom_level = float(v)
        if self.pdf_doc: self.render_page()

    def to_word(self):
        if self.file_path:
            out = filedialog.asksaveasfilename(defaultextension=".docx")
            if out:
                cv = Converter(self.file_path); cv.convert(out); cv.close()
                messagebox.showinfo("Sukses", "Konversi Selesai!")

if __name__ == "__main__":
    app = LitePDFReader(sys.argv[1] if len(sys.argv) > 1 else None)
    app.mainloop()
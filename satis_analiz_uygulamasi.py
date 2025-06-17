import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fpdf import FPDF

class SatisAnalizUygulamasi:
    def __init__(self, master):
        self.master = master
        master.title("Satış Analizi")
        master.geometry("800x600")

        self.frame = tk.Frame(master)
        self.frame.pack()

        self.btn_yukle = tk.Button(self.frame, text="Excel Dosyası Yükle", command=self.dosya_yukle)
        self.btn_yukle.pack(pady=10)

        self.analiz_sonucu = tk.Text(master, height=5, width=80)
        self.analiz_sonucu.pack()

        self.btn_rapor = tk.Button(master, text="PDF Rapor Oluştur", command=self.pdf_olustur)
        self.btn_rapor.pack(pady=10)

        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.df = None

    def dosya_yukle(self):
        dosya_yolu = filedialog.askopenfilename(filetypes=[("Excel dosyaları", "*.xlsx")])
        if dosya_yolu:
            try:
                self.df = pd.read_excel(dosya_yolu)
                self.df["Toplam"] = self.df["Adet"] * self.df["Fiyat"]
                self.analiz_yap()
                self.grafik_goster()
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya okunamadı:\n{e}")

    def analiz_yap(self):
        toplam_ciro = self.df["Toplam"].sum()
        en_cok_satan = self.df.groupby("Ürün")["Adet"].sum().idxmax()

        sonuc = f"Toplam Ciro: {toplam_ciro:.2f} TL\n"
        sonuc += f"En Çok Satan Ürün: {en_cok_satan}\n"

        self.analiz_sonucu.delete(1.0, tk.END)
        self.analiz_sonucu.insert(tk.END, sonuc)

    def grafik_goster(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, axs = plt.subplots(1, 2, figsize=(12, 4))

        gunluk = self.df.groupby("Tarih")["Toplam"].sum()
        gunluk.plot(ax=axs[0], marker='o', title="Günlük Satış Grafiği")
        axs[0].set_ylabel("TL")

        kategori = self.df.groupby("Kategori")["Toplam"].sum()
        kategori.plot(kind="pie", ax=axs[1], autopct='%1.1f%%', title="Kategori Dağılımı")
        axs[1].set_ylabel("")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def pdf_olustur(self):
        if self.df is None:
            messagebox.showwarning("Uyarı", "Önce bir Excel dosyası yükleyin.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Satış Analizi Raporu", ln=True, align='C')

        toplam_ciro = self.df["Toplam"].sum()
        en_cok_satan = self.df.groupby("Ürün")["Adet"].sum().idxmax()

        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Toplam Ciro: {toplam_ciro:.2f} TL", ln=True)
        pdf.cell(200, 10, txt=f"En Çok Satan Ürün: {en_cok_satan}", ln=True)

        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Dosyası", "*.pdf")])
        if dosya_yolu:
            pdf.output(dosya_yolu)
            messagebox.showinfo("Başarılı", f"PDF raporu kaydedildi:\n{dosya_yolu}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SatisAnalizUygulamasi(root)
    root.mainloop()

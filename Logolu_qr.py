import io
import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import pyqrcode
from PIL import Image

# DEĞİŞKENLER

fg_color = "#000000"
bg_color = "#FFFFFF"
secili_logo_yolu = None

# RENK FONKSİYONLARI

def get_kontrast_renk(hex_color):
    """Arka plan rengine göre siyah veya beyaz yazı seçer."""
    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    return "white" if luminance < 0.5 else "black"


def renk_sec(tip):
    """Ön plan veya arka plan rengini seçer."""
    global fg_color, bg_color

    renk_kodu = colorchooser.askcolor(
        title=f"{tip} Rengi Seç"
    )

    if renk_kodu[1]:
        if tip == "Ön Plan":
            fg_color = renk_kodu[1]

            lbl_fg_color.config(
                bg=fg_color,
                fg=get_kontrast_renk(fg_color)
            )

        else:
            bg_color = renk_kodu[1]

            lbl_bg_color.config(
                bg=bg_color,
                fg=get_kontrast_renk(bg_color)
            )

# LOGO FONKSİYONLARI

def logo_secimi_degisti():
    """Logo checkbox'ı işaretlendiğinde logo seçme ekranını açar."""
    global secili_logo_yolu

    if logo_secim_var.get():
        yol = filedialog.askopenfilename(
            title="Logo Seçin",
            filetypes=[
                ("PNG Dosyaları", "*.png"),
                ("JPEG Dosyaları", "*.jpg"),
                ("JPEG Dosyaları", "*.jpeg")
            ]
        )

        if yol:
            secili_logo_yolu = yol

            durum_etiketi.config(
                text=f"Logo seçildi: {os.path.basename(yol)}"
            )

        else:
            # Kullanıcı dosya seçmeden pencereyi kapattı
            logo_secim_var.set(False)
            secili_logo_yolu = None

            durum_etiketi.config(
                text="Logo seçilmedi."
            )

    else:
        secili_logo_yolu = None

        durum_etiketi.config(
            text=""
        )

# QR KODU OLUŞTURMA

def create_qr_code():
    """Girilen URL ile QR kodu oluşturur."""

    url = url_girdi.get().strip()

    # URL kontrolü
    if not url:
        messagebox.showwarning(
            "Eksik Bilgi",
            "Lütfen bir URL girin."
        )
        return

    # Dosya kayıt yeri
    dosya_yolu = filedialog.asksaveasfilename(
        title="QR Kodunu Kaydet",
        defaultextension=".png",
        filetypes=[
            ("PNG Dosyaları", "*.png")
        ]
    )

    if not dosya_yolu:
        durum_etiketi.config(
            text="Kaydetme iptal edildi."
        )
        return

    try:

        # QR KODU OLUŞTUR

        qr = pyqrcode.create(
            url,
            error="H"
        )

        # QR kodunu bellekte oluştur
        with io.BytesIO() as buffer:

            qr.png(
                buffer,
                scale=10,
                module_color=fg_color,
                background=bg_color
            )

            buffer.seek(0)

            qr_image = Image.open(buffer).convert("RGBA")

            # LOGO EKLE

            if logo_secim_var.get() and secili_logo_yolu:

                logo = Image.open(
                    secili_logo_yolu
                ).convert("RGBA")

                qr_w, qr_h = qr_image.size

                # Logo QR'ın yaklaşık %20'si
                logo_boyut = qr_w // 5

                logo = logo.resize(
                    (logo_boyut, logo_boyut),
                    Image.Resampling.LANCZOS
                )

                # Logo için merkez konumu
                pos_x = (qr_w - logo_boyut) // 2
                pos_y = (qr_h - logo_boyut) // 2

                qr_image.paste(
                    logo,
                    (pos_x, pos_y),
                    logo
                )

            # KAYDET

            qr_image.save(
                dosya_yolu,
                "PNG"
            )

        durum_etiketi.config(
            text="QR kodu başarıyla oluşturuldu!"
        )

        messagebox.showinfo(
            "Başarılı",
            "QR kodu başarıyla oluşturuldu ve kaydedildi."
        )

    except Exception as hata:

        durum_etiketi.config(
            text="QR kodu oluşturulurken hata oluştu."
        )

        messagebox.showerror(
            "Hata",
            f"QR kodu oluşturulamadı:\n\n{hata}"
        )


# TKINTER ARAYÜZÜ

uygulama_penceresi = tk.Tk()

uygulama_penceresi.title(
    "Gelişmiş QR Kod Oluşturucusu"
)

uygulama_penceresi.resizable(
    False,
    False
)


# URL

etiket = tk.Label(
    uygulama_penceresi,
    text="URL'yi girin:"
)

url_girdi = tk.Entry(
    uygulama_penceresi,
    width=40
)


# ÖN PLAN RENGİ

lbl_fg_color = tk.Label(
    uygulama_penceresi,
    text="Ön Plan Rengi",
    bg=fg_color,
    fg=get_kontrast_renk(fg_color),
    relief="raised",
    bd=2,
    padx=10,
    pady=5,
    cursor="hand2"
)

lbl_fg_color.bind(
    "<Button-1>",
    lambda event: renk_sec("Ön Plan")
)

# ARKA PLAN RENGİ

lbl_bg_color = tk.Label(
    uygulama_penceresi,
    text="Arka Plan Rengi",
    bg=bg_color,
    fg=get_kontrast_renk(bg_color),
    relief="raised",
    bd=2,
    padx=10,
    pady=5,
    cursor="hand2"
)

lbl_bg_color.bind(
    "<Button-1>",
    lambda event: renk_sec("Arka Plan")
)

# LOGO CHECKBOX

logo_secim_var = tk.BooleanVar(
    value=False
)

logo_checkbox = tk.Checkbutton(
    uygulama_penceresi,
    text="Ortasına logo ekle",
    variable=logo_secim_var,
    command=logo_secimi_degisti
)

# QR BUTONU

qr_kodu_olustur_butonu = tk.Button(
    uygulama_penceresi,
    text="QR Kodunu Oluştur",
    bg="#4CAF50",
    fg="white",
    command=create_qr_code
)

# DURUM ETİKETİ

durum_etiketi = tk.Label(
    uygulama_penceresi,
    text=""
)

# GRID YERLEŞİMİ

etiket.grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

url_girdi.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)

lbl_fg_color.grid(
    row=1,
    column=0,
    padx=10,
    pady=5,
    sticky="ew"
)

lbl_bg_color.grid(
    row=1,
    column=1,
    padx=10,
    pady=5,
    sticky="ew"
)

logo_checkbox.grid(
    row=2,
    column=0,
    columnspan=2,
    padx=10,
    pady=5
)

qr_kodu_olustur_butonu.grid(
    row=3,
    column=0,
    columnspan=2,
    padx=10,
    pady=10,
    sticky="ew"
)

durum_etiketi.grid(
    row=4,
    column=0,
    columnspan=2,
    padx=10,
    pady=10
)

uygulama_penceresi.mainloop()
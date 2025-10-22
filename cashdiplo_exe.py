# -*- coding: utf-8 -*-
"""
Demo GUI Vusion – 3 llamadas API independientes (Tkinter)
Versión adaptada para Windows

Cambios principales:
- Compatibilidad con certificados SSL en Windows.
- Uso de ruta dinámica para el logo (independiente del sistema).
- Título: "CASHDIPLO"
- Rectángulos de salida API más pequeños.
"""

import json
import urllib.request
import ssl
import os
import tkinter as tk
from tkinter import ttk, messagebox
import sys

# =========================
# CONFIG — AJUSTA AQUÍ
# =========================
VUSION_REGION = "https://api-eu.vusion.io"

# --- Endpoints y storeIds ---
VCLOUD_STORE_ID = "cashdiplo_es.lab"      # <-- pon aquí tu storeId
VLINKPRO_STORE_ID = "cashdiplo_es.lab"

# --- Keys ---
OCPI_KEY_VCLOUD = "406dc6bb7d9d4e618dbf063381c1c3ee"
OCPI_KEY_VLINKPRO = "a9a3d22da6f042b9b4b7efe912aeb901"

# --- Ruta del logo (PNG) ---
# En Windows, el ejecutable se ejecuta desde otro directorio,
# así que usamos la ruta absoluta relativa al script.
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(BASE_DIR, "cash.png")

# --- Headers comunes ---
def base_headers(subscription_key: str):
    return {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

# --- Parte fija del body (según tu API) ---
BASE_ITEM_FIELDS_PRICE = {}
BASE_ITEM_FIELDS_PROMO = {}

# =========================
# FUNCIONES HTTP
# =========================
def do_post(url: str, headers: dict, payload: dict):
    """Ejecuta POST y devuelve (status_code, body_text)."""
    data_str = json.dumps(payload)
    req = urllib.request.Request(url, headers=headers, data=data_str.encode("utf-8"))
    req.get_method = lambda: "POST"

    # ✅ En Windows usamos el almacén de certificados del sistema
    ctx = ssl.create_default_context()

    with urllib.request.urlopen(req, context=ctx) as resp:
        code = resp.getcode()
        body = resp.read().decode("utf-8", errors="replace")
    return code, body

# =========================
# GUI
# =========================
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Ventana ---
        self.title("Demo - Cashdiplo")
        self.geometry("900x560")
        self.resizable(True, True)

        # --- Cabecera con logo ---
        header = ttk.Frame(self, padding=(16, 12, 16, 0))
        header.pack(fill="x", side="top")

        self.logo_img = None
        if os.path.exists(LOGO_PATH):
            try:
                img = tk.PhotoImage(file=LOGO_PATH)
                self.logo_img = img.subsample(2, 2)
            except Exception:
                try:
                    self.logo_img = tk.PhotoImage(file=LOGO_PATH)
                except Exception:
                    self.logo_img = None

        if self.logo_img is not None:
            ttk.Label(header, image=self.logo_img).pack(anchor="w")
        else:
            ttk.Label(header, text="CASHDIPLO", font=("TkDefaultFont", 16, "bold")).pack(anchor="w")

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=16, pady=(8, 8))

        # --- Notebook ---
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=0, pady=(0, 8))

        # ==========================================================
        # Tab 1: Cambiar precio
        # ==========================================================
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="1) Cambiar precio (items)")

        self.id_var_1 = tk.StringVar()
        self.price_var = tk.StringVar()

        frm1 = ttk.Frame(tab1, padding=16)
        frm1.pack(fill="both", expand=True)

        ttk.Label(frm1, text="Product ID (entre comillas en el body):").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm1, textvariable=self.id_var_1, width=40).grid(row=0, column=1, sticky="we", padx=8)

        ttk.Label(frm1, text="Price (numérico, sin comillas):").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(frm1, textvariable=self.price_var, width=20).grid(row=1, column=1, sticky="w", padx=8, pady=(8, 0))

        ttk.Button(frm1, text="Enviar", command=self.send_change_price).grid(row=2, column=0, columnspan=2, pady=12)

        self.out1 = tk.Text(frm1, height=8)  # más pequeño
        self.out1.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(8, 0))
        frm1.rowconfigure(3, weight=1)
        frm1.columnconfigure(1, weight=1)

        # ==========================================================
        # Tab 2: Refresh displays
        # ==========================================================
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="2) Refresh displays")

        self.label_ids_var = tk.StringVar()

        frm2 = ttk.Frame(tab2, padding=16)
        frm2.pack(fill="both", expand=True)

        ttk.Label(frm2, text="Label IDs (coma-separados):").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm2, textvariable=self.label_ids_var).grid(row=0, column=1, sticky="we", padx=8)

        ttk.Button(frm2, text="Refrescar", command=self.send_refresh).grid(row=1, column=0, columnspan=2, pady=12)

        self.out2 = tk.Text(frm2, height=8)
        self.out2.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(8, 0))
        frm2.rowconfigure(2, weight=1)
        frm2.columnconfigure(1, weight=1)

        # ==========================================================
        # Tab 3: Cambiar inPromotion
        # ==========================================================
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="3) Cambiar inPromotion (items)")

        self.id_var_3 = tk.StringVar()
        self.promo_var = tk.StringVar(value="True")

        frm3 = ttk.Frame(tab3, padding=16)
        frm3.pack(fill="both", expand=True)

        ttk.Label(frm3, text="Product ID (entre comillas en el body):").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm3, textvariable=self.id_var_3, width=40).grid(row=0, column=1, sticky="we", padx=8)

        ttk.Label(frm3, text="inPromotion:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        rb_frame = ttk.Frame(frm3)
        rb_frame.grid(row=1, column=1, sticky="w", padx=8, pady=(8, 0))
        ttk.Radiobutton(rb_frame, text="Yes (True)", value="True", variable=self.promo_var).pack(side="left")
        ttk.Radiobutton(rb_frame, text="No (False)", value="False", variable=self.promo_var).pack(side="left")

        ttk.Button(frm3, text="Enviar", command=self.send_change_promo).grid(row=2, column=0, columnspan=2, pady=12)

        self.out3 = tk.Text(frm3, height=8)
        self.out3.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(8, 0))
        frm3.rowconfigure(3, weight=1)
        frm3.columnconfigure(1, weight=1)

    # ---------- Handlers ----------
    def send_change_price(self):
        pid = self.id_var_1.get().strip()
        price_txt = self.price_var.get().strip()

        if not pid or not price_txt:
            messagebox.showerror("Error", "Introduce Product ID y precio.")
            return

        try:
            price = float(price_txt) if "." in price_txt else int(price_txt)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser numérico.")
            return

        url = f"{VUSION_REGION}/vcloud/v1/stores/{VCLOUD_STORE_ID}/items"
        headers = base_headers(OCPI_KEY_VCLOUD)
        payload = [{"id": pid, "price": price, **BASE_ITEM_FIELDS_PRICE}]
        self._post_and_print(url, headers, payload, self.out1)

    def send_refresh(self):
        raw = self.label_ids_var.get().strip()
        if not raw:
            messagebox.showerror("Error", "Introduce al menos un labelId.")
            return
        label_ids = [x.strip() for x in raw.split(",") if x.strip()]
        url = f"{VUSION_REGION}/vlink-pro/v1/stores/{VLINKPRO_STORE_ID}/labels/displays/refresh"
        headers = base_headers(OCPI_KEY_VLINKPRO)
        payload = {"labelIds": label_ids}
        self._post_and_print(url, headers, payload, self.out2)

    def send_change_promo(self):
        pid = self.id_var_3.get().strip()
        if not pid:
            messagebox.showerror("Error", "Introduce el Product ID.")
            return

        promo_bool = self.promo_var.get() == "True"
        url = f"{VUSION_REGION}/vcloud/v1/stores/{VCLOUD_STORE_ID}/items"
        headers = base_headers(OCPI_KEY_VCLOUD)
        payload = [{"id": pid, "inPromotion": promo_bool, **BASE_ITEM_FIELDS_PROMO}]
        self._post_and_print(url, headers, payload, self.out3)

    # ---------- Utilidad ----------
    def _post_and_print(self, url, headers, payload, out_widget: tk.Text):
        out_widget.delete("1.0", tk.END)
        out_widget.insert(tk.END, f"URL: {url}\nHEADERS:\n{json.dumps(headers, indent=2)}\n")
        out_widget.insert(tk.END, f"BODY:\n{json.dumps(payload, indent=2, ensure_ascii=False)}\n\n")

        try:
            code, body = do_post(url, headers, payload)
            out_widget.insert(tk.END, f"STATUS: {code}\nRESPONSE:\n{body}\n")
        except Exception as e:
            out_widget.insert(tk.END, f"ERROR:\n{e}\n")
            messagebox.showerror("Error en la llamada", str(e))

if __name__ == "__main__":
    App().mainloop()

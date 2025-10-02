import customtkinter as ctk
from PIL import Image
import json
import time
import random
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

INTERVALO = 3000

class App(ctk.CTk):
    def exportar_json_a_excel(self):
        import pandas as pd
        import tkinter.filedialog as fd
        if not hasattr(self, 'historial_json') or not self.historial_json:
            self.log_event("No hay historial de datos para exportar.")
            return
        df = pd.DataFrame(self.historial_json)
        ruta = fd.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Guardar historial de datos.json")
        if not ruta:
            self.log_event("Exportación cancelada por el usuario.")
            return
        try:
            df.to_excel(ruta, index=False)
            self.log_event(f"Excel guardado en: {ruta}")
        except Exception as e:
            self.log_event(f"Error guardando Excel: {e}")
    def __init__(self):
        super().__init__()
        self.title("Datacenter Dashboard")
        self.geometry('1280x720')

        # Historial de cambios de datos.json
        self.historial_json = []
        self._ultimo_snapshot_json = None

        #Inicializo tiempo activo:
        self.start_time = time.time()
        self.last_limits = {}      
        #Inicializar limites por defecto de temperatura, disco, ruido, iluminación:
        self.limites = {
            "temp": 80,
            "disk": 80,
            "ruido": 80,
            "iluminacion": 80,
        }

        # Crear historial para graficar evolución
        self.historial = {
            "temp": [],
            "disk": [],
            "ruido": [],
            "iluminacion": [],
        }

        # Crear Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Añadir pestañas
        self.tabview.add("General")
        self.tabview.add("Seguridad y Logs")
        self.tabview.add("Configuración")

#------------------- SEGURIDAD Y LOGS ------------------------------------
        security_tab = self.tabview.tab("Seguridad y Logs")
        security_tab.columnconfigure(1, weight=1)
        security_tab.rowconfigure(1, weight=1)

        security_label = ctk.CTkLabel(security_tab, text='Seguridad y logs')
        for i in range(3):
            security_label.columnconfigure(i, weight=1)
        for i in range(3):
            security_label.rowconfigure(i, weight=1)
        security_label.grid(row=0, column=0, sticky='nsew')

        xls_img = ctk.CTkImage(light_image=Image.open(r'assets/xls.png'), size=(64, 64))
        generate_excel_btn = ctk.CTkButton(security_label, text="Generar excel", image=xls_img, corner_radius=24, compound="top", command=self.exportar_json_a_excel)
        generate_excel_btn.grid(row=0, column=0, sticky='nsew')
#------------------- GENERAL ---------------------------------------------
        general_tab = self.tabview.tab("General")
        for i in range(8):
            general_tab.columnconfigure(i, weight=1)
        for i in range(6):
            general_tab.rowconfigure(i, weight=1)
        
        graph_label = ctk.CTkLabel(general_tab, text='Gráfico y semaforo')
        graph_label.grid(row=0, column=0, rowspan=6, columnspan=3, sticky='nsew')
        graph_label.columnconfigure(0, weight=1)
        graph_label.rowconfigure(0, weight=1)
        graph_label.rowconfigure(1, weight=1)
        
        self.graph_resumelabel = ctk.CTkLabel(graph_label, text='Grafico de categoría seleccionada', bg_color='red')
        self.graph_resumelabel.grid(row=0, column=0, sticky='nsew')

        #Semaforo
        self.status_ok_img = ctk.CTkImage(light_image=Image.open(r"assets/sign-check-icon_34365.png"), size=(256, 256))
        self.status_warning_img = ctk.CTkImage(light_image=Image.open(r"assets/sign-warning-icon_34355.png"), size=(256, 256))
        self.status_fatal_img = ctk.CTkImage(light_image=Image.open(r"assets/sign-error-icon_34362.png"), size=(256, 256))

        self.status_label = ctk.CTkLabel(graph_label, text="", image=self.status_ok_img)
        self.status_label.grid(row=1, column=0, sticky='nsew')

        # ------------------------------- INFORMACION -----------------------------
        information_label = ctk.CTkLabel(general_tab)
        information_label.grid(row=0, column=5, rowspan=6, columnspan=3, sticky='nsew')
        for i in range(6):
            information_label.rowconfigure(i, weight=1)
        for i in range(2):
            information_label.columnconfigure(i, weight=1)

        self.wakeup_time = ctk.CTkEntry(information_label, font=("Arial", 36), justify="center")
        self.wakeup_time.insert(0, "Tiempo activo: 0s")
        self.wakeup_time.configure(state="readonly")
        self.wakeup_time.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.history_box = ctk.CTkTextbox(information_label, font=("Arial", 16))
        self.history_box.insert("end", "Historial de eventos:\n")
        self.history_box.configure(state="disabled")
        self.history_box.grid(row=1, column=0, rowspan=5, columnspan=2, sticky='nsew')

        # ------------------------------- BOTONES -------------------------------
        temp_img = ctk.CTkImage(light_image=Image.open(r'assets/temp_img.png'), size=(64, 64))
        disk_img = ctk.CTkImage(light_image=Image.open(r'assets/disk_img.png'), size=(64, 64))
        ruido_img = ctk.CTkImage(light_image=Image.open(r'assets/audio.png'), size=(64, 64))
        iluminacion_img = ctk.CTkImage(light_image=Image.open(r'assets/iluminacion.png'), size=(64, 64))
        fire_alarm_img = ctk.CTkImage(light_image=Image.open(r"assets/fuego.png"), size=(64, 64))
        self.puerta_abierta_img = ctk.CTkImage(light_image=Image.open(r"assets/internet_locked_padlock_password_secure_security_unlock_icon_127083.png"), size=(64, 64))
        self.puerta_cerrada_img = ctk.CTkImage(light_image=Image.open(r"assets/internet_lock_locked_padlock_password_secure_security_icon_127078.png"), size=(64, 64))

        buttons_label = ctk.CTkLabel(general_tab)
        buttons_label.grid(row=0, column=3, rowspan=8, columnspan=2, sticky='nsew')

        for i in range(4):
            buttons_label.rowconfigure(i, weight=1)
        for i in range(2):
            buttons_label.columnconfigure(i, weight=1)
        
        #Creo y ubico botones
        self.botones = {
            "temp": ctk.CTkButton(buttons_label, text='Temp', image=temp_img, corner_radius=24, compound="top"),
            "disk": ctk.CTkButton(buttons_label, text='Disco', image=disk_img, corner_radius=24, compound="top"),
            "ruido": ctk.CTkButton(buttons_label, text='Ruido', image=ruido_img, corner_radius=24, compound="top"),
            "iluminacion": ctk.CTkButton(buttons_label, text='Iluminación', image=iluminacion_img, corner_radius=24, compound="top"),
        }

        self.botones["temp"].grid(row=0, column=0, sticky='nsew', padx=10, pady=30)
        self.botones["disk"].grid(row=0, column=1, sticky='nsew', padx=10, pady=30)
        self.botones["ruido"].grid(row=1, column=0, sticky='nsew', padx=10, pady=30)
        self.botones["iluminacion"].grid(row=1, column=1, sticky='nsew', padx=10, pady=30)

        # Botón alarma de incendio
        self.alarma_incendio_btn = ctk.CTkButton(
            buttons_label,
            text="Alarma: OFF",
            fg_color="green",
            corner_radius=24,
            image=fire_alarm_img,
            compound="top"
        )
        self.alarma_incendio_btn.grid(row=2, column=1, sticky='nsew', padx=10, pady=30)

        # Botón estado de puerta (inicialmente cerrada)
        self.puerta_estado_btn = ctk.CTkButton(
            buttons_label,
            text="Puerta: Cerrada",
            fg_color="green",
            corner_radius=24,
            image=self.puerta_cerrada_img,
            compound="top"
        )
        self.puerta_estado_btn.grid(row=2, column=0, sticky='nsew', padx=10, pady=30)

#-------------- CONFIGURACION ----------------------------------------------

        config_tab = self.tabview.tab("Configuración")
        for i in range(1):
            config_tab.columnconfigure(i, weight=1)
        for i in range(6):
            config_tab.rowconfigure(i, weight=1)

        # Variables para límites configurables
        self.max_temp_var = ctk.StringVar(value=str(self.limites["temp"]))
        self.max_disk_var = ctk.StringVar(value=str(self.limites["disk"]))
        self.max_ruido_var = ctk.StringVar(value=str(self.limites["ruido"]))
        self.max_iluminacion_var = ctk.StringVar(value=str(self.limites["iluminacion"]))

        ctk.CTkLabel(config_tab, text="Máx. Temp (°C):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(config_tab, textvariable=self.max_temp_var).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(config_tab, text="Máx. Disco (%):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(config_tab, textvariable=self.max_disk_var).grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkLabel(config_tab, text="Máx. Ruido:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(config_tab, textvariable=self.max_ruido_var).grid(row=2, column=1, padx=10, pady=5)
        ctk.CTkLabel(config_tab, text="Máx. Iluminación:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(config_tab, textvariable=self.max_iluminacion_var).grid(row=3, column=1, padx=10, pady=5)

        # Variables para detectar cambios de estado
        self.last_puerta_estado = None
        self.last_alarma_incendio = None

        # Iniciar actualización periódica
        self.actualizar_datos()

        #------------------- ACTUALIZACIÓN ----------------------------------------
    def log_event(self, texto):
        """Agregar evento al historial"""
        self.history_box.configure(state="normal")
        self.history_box.insert("end", f"- {texto}\n")
        self.history_box.see("end")
        self.history_box.configure(state="disabled")
    

    def actualizar_datos(self):
        """Lee datos del JSON y actualiza los botones y el gráfico con historial"""
        try:
            with open("datos.json", "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            mensaje = datos.get("mensaje", {})

            # Guardar snapshot de datos.json y hora en historial_json solo si cambió
            snapshot = json.dumps(datos, ensure_ascii=False, sort_keys=True)
            if snapshot != self._ultimo_snapshot_json:
                try:
                    hora_mod = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime("datos.json")))
                except Exception as e:
                    hora_mod = "Error: " + str(e)
                self.historial_json.append({
                    "datos": snapshot,
                    "hora_actualizacion": hora_mod
                })
                self._ultimo_snapshot_json = snapshot

            def safe_int(val, default=0):
                try:
                    return int(val)
                except (TypeError, ValueError):
                    return default

            # Validaciones de rango
            temperatura = safe_int(mensaje.get("temp", None))
            if temperatura is None or temperatura < 0 or temperatura > 140:
                temperatura = None

            disk = safe_int(mensaje.get("disco", None))
            if disk is None or disk < 0 or disk > 100:
                disk = None

            ruido = safe_int(mensaje.get("ruido", None))
            if ruido is None or ruido < 0 or ruido > 140:
                ruido = None

            iluminacion = safe_int(mensaje.get("ilum", None))
            if iluminacion is None or iluminacion < 0 or iluminacion > 100:
                iluminacion = None

            fuego = safe_int(mensaje.get("fuego", None))
            if fuego not in (0, 1):
                alarma_incendio = None
            else:
                alarma_incendio = bool(fuego)

            puerta = safe_int(mensaje.get("puerta", None))
            if puerta not in (0, 1):
                puerta_estado = None
            else:
                puerta_estado = "abierta" if puerta == 1 else "cerrada"

            # Registrar eventos de cambio de estado
            if self.last_puerta_estado != puerta_estado and puerta_estado is not None:
                if puerta_estado == "abierta":
                    self.log_event("Puerta abierta")
                elif puerta_estado == "cerrada":
                    self.log_event("Puerta cerrada")
                self.last_puerta_estado = puerta_estado

            if self.last_alarma_incendio != alarma_incendio and alarma_incendio is not None:
                if alarma_incendio:
                    self.log_event("Alarma de incendio ACTIVADA")
                else:
                    self.log_event("Alarma de incendio DESACTIVADA")
                self.last_alarma_incendio = alarma_incendio

        except Exception as e:
            print("Error leyendo JSON:", e)
            temperatura = disk = ruido = iluminacion = None
            alarma_incendio = None
            puerta_estado = None

        valores = {
            "temp": temperatura if temperatura is not None else "null",
            "disk": disk if disk is not None else "null",
            "ruido": ruido if ruido is not None else "null",
            "iluminacion": iluminacion if iluminacion is not None else "null",
        }

        # Guardar valores en historial (máximo 50 puntos)
        for key in self.historial:
            self.historial[key].append(valores[key] if valores[key] != "null" else 0)
            if len(self.historial[key]) > 50:
                self.historial[key].pop(0)

        # Actualizar grafico
        for widget in self.graph_resumelabel.winfo_children():
            widget.destroy()  # limpiar gráfico anterior

        x = list(range(1, len(self.historial["temp"]) + 1))
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, self.historial["temp"], label="Temperatura", color="red")
        ax.plot(x, self.historial["disk"], label="Disco", color="gray")
        ax.plot(x, self.historial["ruido"], label="Ruido", color="blue")
        ax.plot(x, self.historial["iluminacion"], label="Iluminación", color="yellow")
        ax.set_title("Gráfico histórico")
        ax.set_ylabel("Valores")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_resumelabel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Actualizo límites desde configuración
        self.limites["temp"] = int(self.max_temp_var.get())
        self.limites["disk"] = int(self.max_disk_var.get())
        self.limites["ruido"] = int(self.max_ruido_var.get())
        self.limites["iluminacion"] = int(self.max_iluminacion_var.get())

        # Actualizar botones con colores y textos
        self.botones["temp"].configure(
            text=f"Temp: {valores['temp']}°C" if valores['temp'] != "null" else "Temp: null",
            fg_color="red" if valores["temp"] != "null" and valores["temp"] > self.limites["temp"] else "green"
        )
        self.botones["disk"].configure(
            text=f"Disco: {valores['disk']}%" if valores['disk'] != "null" else "Disco: null",
            fg_color="red" if valores["disk"] != "null" and valores["disk"] > self.limites["disk"] else "green"
        )
        self.botones["ruido"].configure(
            text=f"Ruido: {valores['ruido']}" if valores['ruido'] != "null" else "Ruido: null",
            fg_color="red" if valores["ruido"] != "null" and valores["ruido"] > self.limites["ruido"] else "green"
        )
        self.botones["iluminacion"].configure(
            text=f"Iluminación: {valores['iluminacion']}" if valores['iluminacion'] != "null" else "Iluminación: null",
            fg_color="red" if valores["iluminacion"] != "null" and valores["iluminacion"] > self.limites["iluminacion"] else "green"
        )

        # Contar botones en rojo
        rojos = sum(1 for b in self.botones.values() if b.cget("fg_color") == "red")

        # Actualizar imagen del semáforo
        if alarma_incendio is None:
            self.status_label.configure(image=self.status_fatal_img)
        elif alarma_incendio:
            self.status_label.configure(image=self.status_fatal_img)
        elif rojos == 0:
            self.status_label.configure(image=self.status_ok_img)
        elif rojos <= 2:
            self.status_label.configure(image=self.status_warning_img)
        else:
            self.status_label.configure(image=self.status_fatal_img)

        # Actualizar tiempo activo
        tiempo_activo = int(time.time() - self.start_time)
        self.wakeup_time.configure(state="normal")
        self.wakeup_time.delete(0, "end")
        self.wakeup_time.insert(0, f"Tiempo activo: {tiempo_activo}s")
        self.wakeup_time.configure(state="readonly")

        # Actualizar botón de alarma de incendio
        if alarma_incendio is None:
            self.alarma_incendio_btn.configure(text="Alarma: null", fg_color="gray")
        elif alarma_incendio:
            self.alarma_incendio_btn.configure(text="Alarma: ON", fg_color="red")
        else:
            self.alarma_incendio_btn.configure(text="Alarma: OFF", fg_color="green")

        # Actualizar botón de puerta
        if puerta_estado is None:
            self.puerta_estado_btn.configure(text="Puerta: null", fg_color="gray", image=self.puerta_cerrada_img)
        elif puerta_estado == "abierta":
            self.puerta_estado_btn.configure(text="Puerta: Abierta", fg_color="red", image=self.puerta_abierta_img)
        else:
            self.puerta_estado_btn.configure(text="Puerta: Cerrada", fg_color="green", image=self.puerta_cerrada_img)

        # Repetir actualización solo una vez
        self.after(INTERVALO, self.actualizar_datos)


if __name__ == "__main__":
    app = App()
    app.mainloop()
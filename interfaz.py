import customtkinter as ctk
import serial
import threading
import time

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Rango ideal de temperatura por animal
animales = {
    "Tortuga": (25, 30),
    "Serpiente": (28, 32),
    "Conejo": (18, 25),
    "Iguana": (29, 35),
    "Hamster": (20, 26),
}

class ControlTemperaturaApp(ctk.CTk):
    def _init_(self):
        super()._init_()

        self.title("Control de Temperatura para Hábitats")
        self.geometry("500x400")

        self.serial_port = None
        self.lectura_serial = True

        # Elementos de GUI
        self.label_titulo = ctk.CTkLabel(self, text="Sistema de Monitoreo Ambiental", font=("Arial", 20))
        self.label_titulo.pack(pady=10)

        self.selector_animal = ctk.CTkComboBox(self, values=list(animales.keys()), command=self.actualizar_rango)
        self.selector_animal.pack(pady=10)
        self.selector_animal.set("Tortuga")

        self.label_rango = ctk.CTkLabel(self, text="Rango ideal: 25-30 °C", font=("Arial", 14))
        self.label_rango.pack()

        self.label_temp = ctk.CTkLabel(self, text="Temperatura actual: -- °C", font=("Arial", 16))
        self.label_temp.pack(pady=10)

        self.label_estado_led = ctk.CTkLabel(self, text="LED: --", font=("Arial", 14))
        self.label_estado_led.pack()

        self.boton_conectar = ctk.CTkButton(self, text="Conectar", command=self.conectar_serial)
        self.boton_conectar.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def actualizar_rango(self, value):
        minimo, maximo = animales[value]
        self.label_rango.configure(text=f"Rango ideal: {minimo}-{maximo} °C")

    def conectar_serial(self):
        try:
            # Cambia COM3 por el puerto real de tu Arduino
            self.serial_port = serial.Serial('COM3', 9600, timeout=1)
            self.label_estado_led.configure(text="Conectado al puerto COM3")
            thread = threading.Thread(target=self.leer_datos_serial)
            thread.start()
        except Exception as e:
            self.label_estado_led.configure(text=f"Error: {e}")

    def leer_datos_serial(self):
        while self.lectura_serial:
            if self.serial_port and self.serial_port.in_waiting:
                linea = self.serial_port.readline().decode('utf-8').strip()
                if "Temperatura:" in linea:
                    temp = float(linea.split(":")[1].replace("°C", "").strip())
                    self.label_temp.configure(text=f"Temperatura actual: {temp:.2f} °C")
                    # Comprobar si el LED está encendido
                    animal = self.selector_animal.get()
                    min_temp, max_temp = animales[animal]
                    if temp < min_temp:
                        estado = "Encendido"
                    else:
                        estado = "Apagado"
                    self.label_estado_led.configure(text=f"LED: {estado}")
            time.sleep(1)

    def on_closing(self):
        self.lectura_serial = False
        if self.serial_port:
            self.serial_port.close()
        self.destroy()


if _name_ == "_main_":
    app = ControlTemperaturaApp()
    app.mainloop()

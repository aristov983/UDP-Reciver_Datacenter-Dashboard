# UDP-Reciver_Datacenter-Dashboard
Este es un proyecto creado en el marco de la materia microprocesadores de la Universidad Católica del Uruguay. Este proyecto recibe datos mediante UDP, los almacena en un .json y muestra la información en una interfaz gráfica utilizando CustomTkinter

# Instalación
Este programa funciona unicamente en Windows 10/11, no se asegura su funcionamiento en otro sistema operativo
## 🚀 Instalación

1. **Instalar Python 3.13**  
   En Windows descarguelo desde la [página oficial de Python](https://www.python.org/downloads/).

---

2. **Clonar el repositorio**  

   ```bash
   git clone https://github.com/aristov983/UDP-Reciver_Datacenter-Dashboard.git
   cd UDP-Reciver_Datacenter-Dashboard
   ```

---

3. **(Opcional) Crear y activar un entorno virtual**  

   ```bash
   python -m venv venv
   .\venv\Scripts\activate     # En Windows
   ```

---

4. **Instalar dependencias**  

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Uso

1. Iniciá la interfaz gráfica:  

   ```bash
   python frontend.py
   ```

2. En otra terminal, ejecutá el receptor UDP:  

   ```bash
   python receiver_udp_01.py
   ```

3. El receptor guardará los mensajes en **`datos.json`**, el cual será leído constantemente por la interfaz para actualizar los datos en tiempo real.


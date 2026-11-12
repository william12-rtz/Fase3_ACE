# Simulador de Circuitos CD — ACE

Interfaz gráfica de la Fase 3, desarrollada con CustomTkinter y Matplotlib.
Incluye parámetros editables, validación, tarjetas de resultados, tabla
comparativa y gráficas de voltaje y potencia.

## Requisitos

- Python 3.10 o posterior
- Tkinter (incluido normalmente con Python para Windows)

## Instalación y ejecución

Clone el repositorio y entre en la carpeta del proyecto:

```powershell
git clone https://github.com/william12-rtz/Fase3_ACE.git
cd Fase3_ACE
```

Cree un entorno virtual, instale las dependencias y ejecute la aplicación:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Si PowerShell impide activar el entorno virtual, puede ejecutar el proyecto
directamente con:

```powershell
python -m pip install -r requirements.txt
python app.py
```

## Uso

1. Revise o modifique los parámetros precargados.
2. Pulse **Ejecutar Simulación / Calcular**.
3. Consulte los resultados y la tabla de error porcentual.
4. Pulse **Mostrar Gráfica** para abrir la visualización.

## Alcance

Esta entrega implementa el frontend solicitado. Como no se proporcionaron la
topología ni las ecuaciones del circuito, el módulo de simulación valida los
parámetros ingresados y devuelve los resultados de referencia de la Fase 1.
`core/simulator.py` aísla esta lógica para poder sustituirla por el solucionador
eléctrico definitivo sin modificar la interfaz.

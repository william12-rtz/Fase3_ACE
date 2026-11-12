"""Ventana secundaria para las gráficas de resultados."""

from tkinter import messagebox

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from core.models import SimulationResults


class ChartWindow(ctk.CTkToplevel):
    """Presenta voltajes y potencia en ejes independientes."""

    def __init__(self, master: ctk.CTk, results: SimulationResults) -> None:
        super().__init__(master)
        self.title("Gráficas de resultados - Simulador CD")
        self.geometry("820x580")
        self.minsize(700, 500)
        self.transient(master)

        try:
            self._build_chart(results)
        except Exception as exc:  # pragma: no cover - protección de la GUI
            self.destroy()
            messagebox.showerror(
                "No se pudo crear la gráfica",
                f"Matplotlib produjo un error:\n{exc}",
                parent=master,
            )

    def _build_chart(self, results: SimulationResults) -> None:
        figure = Figure(figsize=(8, 5), dpi=100, layout="constrained")
        figure.patch.set_facecolor("#f4f7fb")

        voltage_axis, power_axis = figure.subplots(1, 2)
        voltage_names = ["Nodo A", "Nodo B", "Fuente\ndependiente"]
        voltage_values = [
            results.node_a_voltage,
            results.node_b_voltage,
            results.dependent_voltage,
        ]
        bars = voltage_axis.bar(
            voltage_names,
            voltage_values,
            color=["#2563eb", "#0ea5e9", "#6366f1"],
            width=0.62,
        )
        voltage_axis.set_title("Niveles de tensión")
        voltage_axis.set_ylabel("Voltaje (V)")
        voltage_axis.set_ylim(0, max(voltage_values) * 1.25)
        voltage_axis.grid(axis="y", alpha=0.25)
        voltage_axis.bar_label(bars, fmt="%.2f V", padding=4)

        power_bars = power_axis.bar(
            ["R2 (5 Ω)"],
            [results.r2_power],
            color=["#f59e0b"],
            width=0.45,
        )
        power_axis.set_title("Potencia disipada")
        power_axis.set_ylabel("Potencia (W)")
        power_axis.set_ylim(0, results.r2_power * 1.35)
        power_axis.grid(axis="y", alpha=0.25)
        power_axis.bar_label(power_bars, fmt="%.2f W", padding=4)

        figure.suptitle("Resumen gráfico del circuito CD", fontsize=15, weight="bold")

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=(12, 0))

        toolbar_frame = ctk.CTkFrame(self, fg_color="transparent")
        toolbar_frame.pack(fill="x", padx=12, pady=(0, 8))
        NavigationToolbar2Tk(canvas, toolbar_frame).update()

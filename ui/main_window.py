"""Ventana principal de la aplicación."""

from tkinter import messagebox, ttk

import customtkinter as ctk

from core.models import CircuitParameters, REFERENCE_RESULTS, SimulationResults
from core.simulator import ValidationError, parse_parameters, percentage_error, run_simulation
from ui.chart_window import ChartWindow


INPUT_DEFINITIONS = (
    ("voltage_source", "Fuente de voltaje V1", "V"),
    ("r1", "Resistor R1", "Ω"),
    ("r4", "Resistor R4", "Ω"),
    ("r2", "Resistor R2 (control iφ)", "Ω"),
    ("r5", "Resistor R5", "Ω"),
    ("r3", "Resistor R3", "Ω"),
    ("dependent_gain", "Ganancia fuente dependiente", "× iφ"),
)

RESULT_DEFINITIONS = (
    ("node_a_voltage", "Voltaje en Nodo A", "V"),
    ("node_b_voltage", "Voltaje en Nodo B", "V"),
    ("control_current", "Corriente de control iφ", "A"),
    ("dependent_voltage", "Fuente dependiente", "V"),
    ("r2_power", "Potencia disipada R2", "W"),
)


class MainWindow(ctk.CTk):
    """Interfaz moderna del simulador de corriente directa."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Simulador de Circuitos CD - Análisis de Circuitos Eléctricos (ACE)")
        self.geometry("900x650")
        self.minsize(860, 620)
        self._center_window(900, 650)

        self.entries: dict[str, ctk.CTkEntry] = {}
        self.result_values: dict[str, ctk.CTkLabel] = {}
        self.current_results: SimulationResults | None = None
        self.chart_window: ChartWindow | None = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._configure_table_style()
        self._build_input_panel()
        self._build_results_panel()

    def _center_window(self, width: int, height: int) -> None:
        self.update_idletasks()
        x = max((self.winfo_screenwidth() - width) // 2, 0)
        y = max((self.winfo_screenheight() - height) // 2, 0)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_input_panel(self) -> None:
        sidebar = ctk.CTkFrame(self, width=275, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            sidebar,
            text="ACE",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=("#1d4ed8", "#60a5fa"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(22, 0))
        ctk.CTkLabel(
            sidebar,
            text="Parámetros del circuito",
            font=ctk.CTkFont(size=17, weight="bold"),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(2, 16))

        defaults = CircuitParameters()
        for row, (field_name, label, unit) in enumerate(INPUT_DEFINITIONS, start=2):
            group = ctk.CTkFrame(sidebar, fg_color="transparent")
            group.grid(row=row, column=0, sticky="ew", padx=24, pady=4)
            group.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(group, text=label, anchor="w", font=ctk.CTkFont(size=12)).grid(
                row=0, column=0, columnspan=2, sticky="ew"
            )
            entry = ctk.CTkEntry(group, height=30)
            entry.insert(0, f"{getattr(defaults, field_name):g}")
            entry.grid(row=1, column=0, sticky="ew", pady=(2, 0))
            ctk.CTkLabel(group, text=unit, width=35).grid(row=1, column=1, padx=(6, 0))
            self.entries[field_name] = entry

        ctk.CTkButton(
            sidebar,
            text="Ejecutar Simulación / Calcular",
            height=44,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._calculate,
        ).grid(row=9, column=0, sticky="ew", padx=24, pady=(18, 8))

        self.status_label = ctk.CTkLabel(
            sidebar,
            text="Listo para simular",
            text_color=("gray35", "gray70"),
            font=ctk.CTkFont(size=11),
        )
        self.status_label.grid(row=10, column=0, padx=24, pady=(0, 12))

    def _build_results_panel(self) -> None:
        content = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        content.grid(row=0, column=1, sticky="nsew", padx=20, pady=14)
        content.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            content,
            text="Simulador de Circuitos CD",
            font=ctk.CTkFont(size=25, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="ew")
        ctk.CTkLabel(
            content,
            text="Análisis de Circuitos Eléctricos · Fase 3",
            text_color=("gray40", "gray65"),
            anchor="w",
        ).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 14))

        for index, (field_name, title, unit) in enumerate(RESULT_DEFINITIONS):
            row, column = divmod(index, 2)
            card = ctk.CTkFrame(content, height=92)
            card.grid(
                row=row + 2,
                column=column,
                sticky="nsew",
                padx=(0, 6) if column == 0 else (6, 0),
                pady=6,
            )
            ctk.CTkLabel(
                card,
                text=title,
                text_color=("gray35", "gray70"),
                anchor="w",
            ).pack(fill="x", padx=16, pady=(12, 0))
            value_label = ctk.CTkLabel(
                card,
                text=f"— {unit}",
                font=ctk.CTkFont(size=22, weight="bold"),
                anchor="w",
            )
            value_label.pack(fill="x", padx=16, pady=(2, 12))
            self.result_values[field_name] = value_label

        table_header = ctk.CTkFrame(content, fg_color="transparent")
        table_header.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(16, 6))
        table_header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            table_header,
            text="Tabla comparativa",
            font=ctk.CTkFont(size=17, weight="bold"),
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(
            table_header,
            text="Mostrar Gráfica",
            width=145,
            state="disabled",
            command=self._show_chart,
        ).grid(row=0, column=1, sticky="e")
        self.chart_button = table_header.winfo_children()[-1]

        columns = ("measurement", "theoretical", "simulated", "unit", "error")
        self.table = ttk.Treeview(content, columns=columns, show="headings", height=5)
        headings = ("Magnitud", "Teórico", "Simulado", "Unidad", "Error")
        widths = (175, 85, 85, 65, 70)
        for column, heading, width in zip(columns, headings, widths):
            self.table.heading(column, text=heading)
            self.table.column(column, width=width, minwidth=55, anchor="center")
        self.table.column("measurement", anchor="w")
        self.table.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 12))

    def _configure_table_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(
            "Treeview",
            rowheight=30,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#2563eb")])

    def _calculate(self) -> None:
        try:
            parameters = parse_parameters(
                {name: entry.get() for name, entry in self.entries.items()}
            )
            results = run_simulation(parameters)
        except ValidationError as exc:
            self.status_label.configure(text="Revisa los datos ingresados", text_color="#dc2626")
            messagebox.showwarning("Datos no válidos", str(exc), parent=self)
            return

        self.current_results = results
        self._update_result_cards(results)
        self._update_table(results)
        self.chart_button.configure(state="normal")
        self.status_label.configure(
            text="Simulación completada correctamente",
            text_color=("#15803d", "#4ade80"),
        )

    def _update_result_cards(self, results: SimulationResults) -> None:
        for field_name, _, unit in RESULT_DEFINITIONS:
            value = getattr(results, field_name)
            self.result_values[field_name].configure(text=f"{value:.2f} {unit}")

    def _update_table(self, results: SimulationResults) -> None:
        for row in self.table.get_children():
            self.table.delete(row)
        for field_name, title, unit in RESULT_DEFINITIONS:
            theoretical = getattr(REFERENCE_RESULTS, field_name)
            simulated = getattr(results, field_name)
            error = percentage_error(theoretical, simulated)
            self.table.insert(
                "",
                "end",
                values=(
                    title,
                    f"{theoretical:.2f}",
                    f"{simulated:.2f}",
                    unit,
                    f"{error:.2f}%",
                ),
            )

    def _show_chart(self) -> None:
        if self.current_results is None:
            return
        if self.chart_window is not None and self.chart_window.winfo_exists():
            self.chart_window.focus()
            return
        self.chart_window = ChartWindow(self, self.current_results)

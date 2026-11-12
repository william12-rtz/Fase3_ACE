"""Modelos de datos compartidos por la interfaz y el simulador."""

from dataclasses import dataclass, fields


@dataclass(frozen=True)
class CircuitParameters:
    """Parámetros editables del circuito de referencia."""

    voltage_source: float = 20.0
    r1: float = 2.0
    r4: float = 20.0
    r2: float = 5.0
    r5: float = 10.0
    r3: float = 2.0
    dependent_gain: float = 8.0


@dataclass(frozen=True)
class SimulationResults:
    """Resultados requeridos por la Fase 3."""

    node_a_voltage: float
    node_b_voltage: float
    control_current: float
    dependent_voltage: float
    r2_power: float

    def values(self) -> tuple[float, ...]:
        return tuple(getattr(self, field.name) for field in fields(self))


REFERENCE_RESULTS = SimulationResults(
    node_a_voltage=16.0,
    node_b_voltage=10.0,
    control_current=1.2,
    dependent_voltage=9.6,
    r2_power=7.2,
)

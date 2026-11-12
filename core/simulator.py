"""Validación y simulación demostrativa del circuito."""

from collections.abc import Mapping

from core.models import CircuitParameters, REFERENCE_RESULTS, SimulationResults


class ValidationError(ValueError):
    """Indica que uno o más parámetros del circuito no son válidos."""


PARAMETER_FIELDS = {
    "voltage_source": "Fuente V1",
    "r1": "Resistor R1",
    "r4": "Resistor R4",
    "r2": "Resistor R2",
    "r5": "Resistor R5",
    "r3": "Resistor R3",
    "dependent_gain": "Ganancia",
}


def parse_parameters(raw_values: Mapping[str, str]) -> CircuitParameters:
    """Convierte los valores de la interfaz y genera mensajes claros."""

    parsed: dict[str, float] = {}
    for field_name, label in PARAMETER_FIELDS.items():
        raw_value = raw_values.get(field_name, "").strip().replace(",", ".")
        if not raw_value:
            raise ValidationError(f"El campo «{label}» es obligatorio.")
        try:
            parsed[field_name] = float(raw_value)
        except ValueError as exc:
            raise ValidationError(
                f"«{label}» debe contener un número válido."
            ) from exc

    for field_name in ("r1", "r2", "r3", "r4", "r5"):
        if parsed[field_name] <= 0:
            raise ValidationError(
                f"«{PARAMETER_FIELDS[field_name]}» debe ser mayor que cero."
            )
    if parsed["dependent_gain"] < 0:
        raise ValidationError("La ganancia no puede ser negativa.")

    return CircuitParameters(**parsed)


def run_simulation(parameters: CircuitParameters) -> SimulationResults:
    """Retorna el caso de referencia aprobado para la demostración del frontend.

    Las ecuaciones/topología del circuito no forman parte de la especificación
    entregada. Los parámetros se aceptan para probar el flujo de la GUI.
    """

    del parameters
    return REFERENCE_RESULTS


def percentage_error(theoretical: float, simulated: float) -> float:
    """Calcula el error relativo, incluyendo el caso teórico igual a cero."""

    if theoretical == 0:
        return 0.0 if simulated == 0 else 100.0
    return abs((simulated - theoretical) / theoretical) * 100

"""Pruebas para los escenarios predefinidos."""

from scenarios import get_predefined_scenarios


def test_predefined_scenarios_are_not_empty() -> None:
    """Debe existir al menos un escenario de comparacion."""
    scenarios = get_predefined_scenarios()

    assert scenarios


def test_predefined_scenarios_have_required_fields() -> None:
    """Cada escenario debe incluir los campos necesarios."""
    required_fields = {"disk_size", "head", "requests", "direction", "description"}

    for scenario in get_predefined_scenarios().values():
        assert required_fields.issubset(scenario.keys())


def test_predefined_scenarios_have_valid_ranges() -> None:
    """El cabezal y las solicitudes deben estar dentro del disco."""
    for scenario in get_predefined_scenarios().values():
        disk_size = scenario["disk_size"]
        assert disk_size > 0
        assert 0 <= scenario["head"] < disk_size
        assert scenario["requests"]
        assert all(0 <= request < disk_size for request in scenario["requests"])


def test_predefined_scenarios_have_valid_direction() -> None:
    """La direccion de cada escenario debe ser left o right."""
    for scenario in get_predefined_scenarios().values():
        assert scenario["direction"] in ("left", "right")


def test_predefined_scenarios_have_descriptions() -> None:
    """Cada escenario debe incluir una descripcion didactica."""
    for scenario in get_predefined_scenarios().values():
        assert scenario["description"].strip()

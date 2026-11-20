from typing import List, Optional


def add_waypoint(drone_id: str, point: Optional[str], route: Optional[List[str]] = None) -> List[str]:
    """Добавляет точку в маршрут указанного дрона."""
    if route is None:
        route = []
    if point is not None:
        route.append(f"{drone_id}:{point}")
    return route


def _check_emergency_and_battery(emergency: bool, battery: int, payload_kg: float) -> Optional[str]:
    """Вспомогательная функция для уменьшения сложности (максимальная цикломатическая сложность)."""
    if emergency:
        return "LAND_IMMEDIATELY"
    if battery < 15:
        if payload_kg > 2.0:
            return "DROP_CARGO_AND_RETURN"
        return "RETURN_TO_BASE"
    return None


def select_drone_mode(battery: int, payload_kg: float, is_raining: bool, emergency: bool) -> str:
    """Выбирает режим работы дрона на основе телеметрии."""
    status = _check_emergency_and_battery(emergency, battery, payload_kg)
    if status:
        return status

    if is_raining:
        if payload_kg > 3.0:
            return "HOLD_POSITION"
        return "ECO_FLIGHT"

    if payload_kg > 5.0:
        return "HEAVY_LIFT"

    return "STANDARD"
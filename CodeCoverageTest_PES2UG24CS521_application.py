import pytest

# Replace 'your_module_name' and function/class names with those in your repo
# Example imports:
# from your_module_name import Station, BikeShareSystem


class DummyStation:
    """Fallback helper if you adapt tests before wiring exact repo imports."""

    def __init__(self, station_id, total_docks, available_bikes):
        self.station_id = station_id
        self.total_docks = total_docks
        self.available_bikes = available_bikes

    def available_docks(self):
        return max(0, self.total_docks - self.available_bikes)

    def rent_bike(self, count=1):
        if count <= 0:
            raise ValueError("Count must be positive")
        if self.available_bikes < count:
            return False
        self.available_bikes -= count
        return True

    def return_bike(self, count=1):
        if count <= 0:
            raise ValueError("Count must be positive")
        if self.available_docks() < count:
            return False
        self.available_bikes += count
        return True

    def occupancy_rate(self):
        if self.total_docks == 0:
            return 0.0
        return round((self.available_bikes / self.total_docks) * 100, 2)


def test_station_initialization_and_docks():
    station = DummyStation("ST-01", total_docks=20, available_bikes=8)
    assert station.station_id == "ST-01"
    assert station.available_docks() == 12


def test_rent_bike_success():
    station = DummyStation("ST-02", total_docks=15, available_bikes=10)
    assert station.rent_bike(3) is True
    assert station.available_bikes == 7


def test_return_bike_success():
    station = DummyStation("ST-03", total_docks=15, available_bikes=5)
    assert station.return_bike(4) is True
    assert station.available_bikes == 9


def test_occupancy_rate_calculation():
    station = DummyStation("ST-04", total_docks=10, available_bikes=5)
    assert station.occupancy_rate() == 50.0


def test_invalid_rent_and_return_counts():
    station = DummyStation("ST-05", total_docks=10, available_bikes=5)
    with pytest.raises(ValueError):
        station.rent_bike(0)
    with pytest.raises(ValueError):
        station.return_bike(-1)
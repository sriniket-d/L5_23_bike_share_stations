import pytest


class DummyStation:
    """Self-contained station class so branch coverage does not pull in unexecuted test functions."""

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


@pytest.mark.parametrize(
    "total_docks,available_bikes,rent_qty,expected_result,expected_bikes",
    [
        # Branch: available_bikes >= count (True)
        (10, 6, 4, True, 2),
        # Branch: available_bikes < count (False / insufficient bikes)
        (10, 2, 5, False, 2),
        # Boundary: exact match available_bikes == count
        (10, 3, 3, True, 0),
    ],
)
def test_rent_bike_branches(
    total_docks, available_bikes, rent_qty, expected_result, expected_bikes
):
    station = DummyStation("BR-01", total_docks=total_docks, available_bikes=available_bikes)
    assert station.rent_bike(rent_qty) is expected_result
    assert station.available_bikes == expected_bikes


@pytest.mark.parametrize("invalid_qty", [0, -2])
def test_rent_bike_invalid_count_branch(invalid_qty):
    # Branch: count <= 0 (True)
    station = DummyStation("BR-01E", total_docks=10, available_bikes=5)
    with pytest.raises(ValueError):
        station.rent_bike(invalid_qty)


@pytest.mark.parametrize(
    "total_docks,available_bikes,return_qty,expected_result,expected_bikes",
    [
        # Branch: available_docks() >= count (True)
        (12, 5, 4, True, 9),
        # Branch: available_docks() < count (False / station full or not enough docks)
        (12, 11, 3, False, 11),
        # Boundary: fill station to exact capacity
        (12, 7, 5, True, 12),
    ],
)
def test_return_bike_branches(
    total_docks, available_bikes, return_qty, expected_result, expected_bikes
):
    station = DummyStation("BR-02", total_docks=total_docks, available_bikes=available_bikes)
    assert station.return_bike(return_qty) is expected_result
    assert station.available_bikes == expected_bikes


@pytest.mark.parametrize("invalid_qty", [0, -1])
def test_return_bike_invalid_count_branch(invalid_qty):
    # Branch: count <= 0 (True)
    station = DummyStation("BR-02E", total_docks=10, available_bikes=5)
    with pytest.raises(ValueError):
        station.return_bike(invalid_qty)


@pytest.mark.parametrize(
    "total_docks,available_bikes,expected_rate",
    [
        # Branch: total_docks == 0 (True)
        (0, 0, 0.0),
        # Branch: total_docks != 0 (False)
        (8, 2, 25.0),
        # Boundary: 100% full
        (8, 8, 100.0),
    ],
)
def test_occupancy_rate_branches(total_docks, available_bikes, expected_rate):
    station = DummyStation("BR-03", total_docks=total_docks, available_bikes=available_bikes)
    assert station.occupancy_rate() == expected_rate


def test_available_docks_clamped_at_zero():
    # Branch: max(0, ...) when available_bikes exceeds total_docks
    station = DummyStation("BR-04", total_docks=5, available_bikes=7)
    assert station.available_docks() == 0
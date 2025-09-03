"""
Shared pytest fixtures for the 1BRC Python project.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_measurements_file(temp_dir):
    """Create a sample measurements file for testing."""
    measurements_file = temp_dir / "test_measurements.txt"
    sample_data = [
        "Hamburg;12.0",
        "Bulawayo;8.9",
        "Palembang;38.8",
        "St. John's;15.2",
        "Cracow;12.6",
        "Hamburg;-2.3",
        "Bulawayo;23.0",
        "Palembang;41.2",
        "St. John's;-5.1",
        "Cracow;-8.7"
    ]
    measurements_file.write_text("\n".join(sample_data))
    return measurements_file


@pytest.fixture
def small_measurements_file(temp_dir):
    """Create a very small measurements file for unit tests."""
    measurements_file = temp_dir / "small_measurements.txt"
    sample_data = [
        "CityA;10.0",
        "CityB;20.5",
        "CityA;-5.2",
        "CityB;15.7"
    ]
    measurements_file.write_text("\n".join(sample_data))
    return measurements_file


@pytest.fixture
def mock_measurement_data():
    """Mock measurement data for testing without file I/O."""
    return {
        "Hamburg": [12.0, -2.3],
        "Bulawayo": [8.9, 23.0],
        "Palembang": [38.8, 41.2],
        "St. John's": [15.2, -5.1],
        "Cracow": [12.6, -8.7]
    }


@pytest.fixture
def expected_results():
    """Expected calculation results for test data validation."""
    return {
        "Hamburg": {"min": -2.3, "max": 12.0, "mean": 4.85},
        "Bulawayo": {"min": 8.9, "max": 23.0, "mean": 15.95},
        "Palembang": {"min": 38.8, "max": 41.2, "mean": 40.0},
        "St. John's": {"min": -5.1, "max": 15.2, "mean": 5.05},
        "Cracow": {"min": -8.7, "max": 12.6, "mean": 1.95}
    }


@pytest.fixture
def mock_tqdm():
    """Mock tqdm progress bar for testing."""
    mock = Mock()
    mock.return_value.__enter__ = Mock(return_value=mock)
    mock.return_value.__exit__ = Mock(return_value=None)
    return mock


@pytest.fixture
def mock_numpy():
    """Mock numpy module for testing."""
    return MagicMock()


@pytest.fixture
def mock_polars():
    """Mock polars module for testing."""
    return MagicMock()


@pytest.fixture
def original_working_dir():
    """Save and restore the original working directory."""
    original_dir = os.getcwd()
    yield original_dir
    os.chdir(original_dir)


@pytest.fixture(autouse=True)
def clean_environment():
    """Clean up environment variables that might affect tests."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def performance_data():
    """Sample performance measurement data for benchmarking tests."""
    return {
        "python3_calculateAverage": 41.941,
        "pypy3_calculateAverage": 31.926,
        "python3_calculateAveragePolars": 11.585,
        "python3_calculateAverageDuckDB": 23.673
    }
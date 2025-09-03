"""
Validation tests to ensure the testing infrastructure is set up correctly.
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch


class TestInfrastructureSetup:
    """Test that testing infrastructure is properly configured."""

    def test_pytest_is_available(self):
        """Verify pytest is properly installed and accessible."""
        import pytest
        assert pytest.__version__ is not None

    def test_pytest_cov_is_available(self):
        """Verify pytest-cov is properly installed."""
        try:
            import pytest_cov
            assert pytest_cov is not None
        except ImportError:
            pytest.fail("pytest-cov is not installed")

    def test_pytest_mock_is_available(self):
        """Verify pytest-mock is properly installed."""
        try:
            import pytest_mock
            assert pytest_mock is not None
        except ImportError:
            pytest.fail("pytest-mock is not installed")

    def test_project_structure(self):
        """Verify the project has the expected structure."""
        project_root = Path(__file__).parent.parent
        
        # Check main project files exist
        assert (project_root / "pyproject.toml").exists()
        assert (project_root / "README.md").exists()
        
        # Check test directories exist
        assert (project_root / "tests").exists()
        assert (project_root / "tests" / "__init__.py").exists()
        assert (project_root / "tests" / "unit").exists()
        assert (project_root / "tests" / "integration").exists()
        assert (project_root / "tests" / "conftest.py").exists()

    def test_pytest_configuration(self):
        """Verify pytest configuration is loaded correctly."""
        # This test verifies that pytest can load and run with configuration
        # The configuration is working if this test runs successfully
        assert True

    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit marker works."""
        assert True

    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that integration marker works."""
        assert True

    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that slow marker works."""
        assert True


class TestSharedFixtures:
    """Test that shared fixtures from conftest.py work correctly."""

    def test_temp_dir_fixture(self, temp_dir):
        """Test the temp_dir fixture creates a valid directory."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Test we can write to it
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()
        assert test_file.read_text() == "test content"

    def test_sample_measurements_file(self, sample_measurements_file):
        """Test the sample measurements file fixture."""
        assert sample_measurements_file.exists()
        content = sample_measurements_file.read_text()
        lines = content.strip().split('\n')
        
        # Should have 10 lines of measurements
        assert len(lines) == 10
        
        # Each line should be in format "City;Temperature"
        for line in lines:
            assert ';' in line
            city, temp = line.split(';')
            assert city.strip()
            float(temp)  # Should be convertible to float

    def test_small_measurements_file(self, small_measurements_file):
        """Test the small measurements file fixture."""
        assert small_measurements_file.exists()
        content = small_measurements_file.read_text()
        lines = content.strip().split('\n')
        
        # Should have 4 lines
        assert len(lines) == 4
        
        # Check specific content
        assert "CityA;10.0" in content
        assert "CityB;20.5" in content

    def test_mock_measurement_data(self, mock_measurement_data):
        """Test the mock measurement data fixture."""
        assert isinstance(mock_measurement_data, dict)
        assert "Hamburg" in mock_measurement_data
        assert isinstance(mock_measurement_data["Hamburg"], list)

    def test_expected_results(self, expected_results):
        """Test the expected results fixture."""
        assert isinstance(expected_results, dict)
        assert "Hamburg" in expected_results
        assert "min" in expected_results["Hamburg"]
        assert "max" in expected_results["Hamburg"]
        assert "mean" in expected_results["Hamburg"]

    def test_performance_data(self, performance_data):
        """Test the performance data fixture."""
        assert isinstance(performance_data, dict)
        assert "python3_calculateAverage" in performance_data
        assert isinstance(performance_data["python3_calculateAverage"], float)


class TestMockingCapabilities:
    """Test that mocking capabilities work correctly."""

    def test_basic_mock(self, mocker):
        """Test basic mocking functionality."""
        mock_func = mocker.Mock(return_value=42)
        result = mock_func()
        assert result == 42
        mock_func.assert_called_once()

    def test_patch_functionality(self, mocker):
        """Test patching functionality."""
        with patch('builtins.open', mocker.mock_open(read_data='test data')):
            with open('fake_file.txt') as f:
                content = f.read()
            assert content == 'test data'

    def test_mock_tqdm_fixture(self, mock_tqdm):
        """Test the mock tqdm fixture."""
        assert mock_tqdm is not None
        # Test that it can be used as a context manager
        with mock_tqdm.return_value as pbar:
            assert pbar is not None


class TestPythonEnvironment:
    """Test that the Python environment is set up correctly."""

    def test_python_version(self):
        """Verify we're running on a supported Python version."""
        assert sys.version_info >= (3, 8), "Python 3.8+ required"

    def test_core_dependencies_importable(self):
        """Test that core project dependencies can be imported."""
        # These should be available based on pyproject.toml
        try:
            import numpy
            import polars  
            import tqdm
        except ImportError as e:
            pytest.fail(f"Core dependency import failed: {e}")

    def test_working_directory_access(self, original_working_dir):
        """Test that we can access the working directory."""
        assert os.path.exists(original_working_dir)
        assert os.access(original_working_dir, os.R_OK)

    def test_clean_environment_fixture(self, clean_environment):
        """Test that environment cleanup works."""
        # The fixture should ensure a clean environment
        # This test just verifies the fixture runs without error
        assert True
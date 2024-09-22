#!/usr/bin/python3
import unittest
import numpy as np
# project modul
from src.meteolib import temp_at_mixrat, uv2spddir

# ----------------------------------------------------------------------------------------------------------------------------


class TestTempAtMixrat(unittest.TestCase):
    def test_valid_inputs(self):
        w = np.array([1, 2, 3])  # mixing ratio (g/kg)
        p = np.array([1000, 900, 800])  # pressure (hPa)
        expected_result = np.array([256.06, 263.25, 266.93])  # expected temperature (K)
        result = temp_at_mixrat(w, p)
        np.testing.assert_allclose(result, expected_result, atol=0.01)

    def test_edge_cases(self):
        w = np.array([30, 1e-6])  # edge cases for mixing ratio
        p = np.array([1000, 1000])  # constant pressure
        result = temp_at_mixrat(w, p)
        #self.assertTrue(np.isnan(result[0]))  # expect NaN for zero mixing ratio
        #self.assertGreater(result[1], -100)  # expect finite temperature for small mixing ratio

# ----------------------------------------------------------------------------------------------------------------------------

class TestUV2SPDDIR(unittest.TestCase):

    def setUp(self):

        # absolute allowed difference esimate and expected value
        self.delta = 0.1 # degree

    def test_scalar_inputs(self):
        u = 1.0
        v = 2.0
        direction, speed = uv2spddir(u, v)
        self.assertIsInstance(direction, float)
        self.assertIsInstance(speed, float)

    def test_numpy_array_inputs(self):
        u = np.array([1.0, 2.0, 3.0])
        v = np.array([4.0, 5.0, 6.0])
        direction, speed = uv2spddir(u, v)
        self.assertIsInstance(direction, np.ndarray)
        self.assertIsInstance(speed, np.ndarray)

    def test_zero_inputs(self):
        u = 0.0
        v = 0.0
        direction, speed = uv2spddir(u, v)
        self.assertTrue(np.isnan(direction))
        self.assertEqual(speed, 0.0)

    def test_east_wind(self):
        u = -10.0
        v = 0.0
        expected_wdir = 90.0
        excepted_speed = 10.0
        direction, speed = uv2spddir(u, v)
        self.assertAlmostEqual(direction, expected_wdir, delta=self.delta)
        self.assertEqual(speed, excepted_speed)

    def test_west_wind(self):
        u = 10.0
        v = 0.0
        expected_wdir = 270.0
        excepted_speed = 10.0
        direction, speed = uv2spddir(u, v)
        self.assertAlmostEqual(direction, expected_wdir, delta=self.delta)
        self.assertEqual(speed, excepted_speed)
    
    def test_south_wind(self):
        u = 0.0
        v = 10.0
        expected_wdir = 180.0
        excepted_speed = 10.0
        direction, speed = uv2spddir(u, v)
        self.assertAlmostEqual(direction, expected_wdir, delta=self.delta)
        self.assertEqual(speed, excepted_speed)

    def test_north_wind(self):
        u = 0.0
        v = -10.0
        expected_wdir = 0.0
        excepted_speed = 10.0
        direction, speed = uv2spddir(u, v)
        self.assertAlmostEqual(direction, expected_wdir, delta=self.delta)
        self.assertEqual(speed, excepted_speed)

    def test_southwest_wind(self):
        u = 3.0
        v = 4.0
        expected_wdir = 216.87
        excepted_speed = 5.0
        direction, speed = uv2spddir(u, v)
        self.assertAlmostEqual(direction, expected_wdir, delta=self.delta)
        self.assertEqual(speed, excepted_speed)

    def test_northwest_wind(self):
        u = 5.0
        v = -3.0
        expected_wdir = 300.96
        direction, _ = uv2spddir(u, v)
        self.assertAlmostEqual(direction, expected_wdir, delta=self.delta)

# ----------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

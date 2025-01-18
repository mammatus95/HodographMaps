#!/usr/bin/python3
import os
import unittest
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from datetime import datetime
from cartopy.crs import EuroPP, PlateCarree
import src.utilitylib as ut
from src.modelinfolib import MODELINFO

# project modul
from src.plotlib import ce_states, customize_area, test_plot


class TestCeStates(unittest.TestCase):

    def setUp(self):
        self.model_obj = MODELINFO("ICON Nest", 1377, 657, 0.0625, "pres")
        self.model_obj.setrundate(datetime.strptime('2022-01-01', "%Y-%m-%d"))
        self.model_obj.setrun("00")
        self.hour = '12'

    def test_default_projection_and_extent(self):
        fig, ax = ce_states(self.hour, self.model_obj.getrun(), self.model_obj.getrundate())
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)
        self.assertEqual(ax.projection, EuroPP())

    def test_custom_projection_and_extent(self):
        projection = PlateCarree()
        lon1, lon2, lat1, lat2 = 10, 20, 40, 50
        fig, ax = ce_states(self.hour, self.model_obj.getrun(), self.model_obj.getrundate(), projection, lon1, lon2, lat1, lat2)
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)
        self.assertEqual(ax.projection, projection)
        self.assertAlmostEqual(ax.get_extent()[0], lon1)
        self.assertAlmostEqual(ax.get_extent()[1], lon2)
        self.assertAlmostEqual(ax.get_extent()[2], lat1)
        self.assertAlmostEqual(ax.get_extent()[3], lat2)

    def test_annotation_with_valid_input(self):
        _, ax = ce_states(self.hour, self.model_obj.getrun(), self.model_obj.getrundate())
        string1, string2 = ut.datum(self.hour, self.model_obj.getrun(), self.model_obj.getrundate())
        self.assertEqual(ax.texts[0].get_text(), string1)
        self.assertEqual(ax.texts[1].get_text(), string2)

    def test_annotation_with_invalid_input(self):
        _, ax = ce_states(self.hour, self.model_obj.getrun(), self.model_obj.getrundate())
        self.assertEqual(len(ax.texts), 2)

    def test_fig_and_ax_return_types(self):
        fig, ax = ce_states(self.hour, self.model_obj.getrun(), self.model_obj.getrundate())
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)

# ---------------------------------------------------------------------------------------------------------------------


class TestCustomizeArea(unittest.TestCase):

    def setUp(self):
        self.model_obj = MODELINFO("ICON Nest", 1377, 657, 0.0625, "pres")
        self.model_obj.setrundate(datetime.strptime('2022-01-01', "%Y-%m-%d"))
        self.model_obj.setrun("00")
        self.hour = '12'

    def test_default_projection_and_extent(self):
        fig, ax = customize_area(self.hour, self.model_obj.getrun(), self.model_obj.getrundate())
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)

    def test_custom_projection_and_extent(self):
        projection = EuroPP()
        lon1, lon2, lat1, lat2 = 10, 20, 40, 50
        fig, ax = customize_area(self.hour, self.model_obj.getrun(), self.model_obj.getrundate(), projection, lon1, lon2, lat1, lat2)
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)

    def test_invalid_extent_values(self):
        _, lon2, lat1, lat2 = 10, 20, 40, 50
        with self.assertRaises(ValueError):
            customize_area(self.hour, self.model_obj.getrun(), self.model_obj.getrundate(), lon1='Invalid', lon2=lon2, lat1=lat1, lat2=lat2)

# ---------------------------------------------------------------------------------------------------------------------


class TestTestPlot(unittest.TestCase):

    def setUp(self):
        self.model_obj = MODELINFO("ICON Nest", 1377, 657, 0.0625, "pres")
        self.model_obj.setrundate(datetime.strptime('2022-01-01', "%Y-%m-%d"))
        self.model_obj.setrun("00")

        test_plot(12, self.model_obj.getrun(), self.model_obj)

        self.ref_path="./ref/test_ce_12.png"
        self.test_img="./test_ce_12.png"

    def test_plot_exist(self):
        self.assertTrue(os.path.exists(self.test_img))

    def test_plot_closed(self):
        test_plot(12, self.model_obj.getrun(), self.model_obj)
        self.assertTrue(plt.fignum_exists(plt.gcf().number))

    def test_invalid_hour(self):
        with self.assertRaises(ValueError):
            test_plot('invalid', self.model_obj.getrun(), self.model_obj)

    def test_invalid_run(self):
        with self.assertRaises(TypeError):
            test_plot(12, self.model_obj, self.model_obj)

    def test_invalid_title(self):
        with self.assertRaises(AttributeError):
            test_plot(12, self.model_obj.getrun(), 123)



# ---------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

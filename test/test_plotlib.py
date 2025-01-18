#!/usr/bin/python3
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
    def test_default_projection_and_extent(self):
        fig, ax = ce_states(12, '2022-01-01', '2022-01-01 12:00:00')
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)
        self.assertEqual(ax.projection, EuroPP())
        self.assertEqual(ax.get_extent(), [1.56, 18.5, 45.2, 56.4])

    def test_custom_projection_and_extent(self):
        projection = PlateCarree()
        lon1, lon2, lat1, lat2 = 10, 20, 40, 50
        fig, ax = ce_states(12, '2022-01-01', '2022-01-01 12:00:00', projection, lon1, lon2, lat1, lat2)
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)
        self.assertEqual(ax.projection, projection)
        self.assertEqual(ax.get_extent(), [lon1, lon2, lat1, lat2])

    def test_annotation_with_valid_input(self):
        hour, start, datetime_obj = 12, '2022-01-01', '2022-01-01 12:00:00'
        fig, ax = ce_states(hour, start, datetime_obj)
        string1, string2 = ut.datum(hour, start, datetime_obj)
        self.assertEqual(ax.texts[0].get_text(), string1)
        self.assertEqual(ax.texts[1].get_text(), string2)

    def test_annotation_with_invalid_input(self):
        hour, start, datetime_obj = 12, None, '2022-01-01 12:00:00'
        fig, ax = ce_states(hour, start, datetime_obj)
        self.assertEqual(len(ax.texts), 0)

    def test_fig_and_ax_return_types(self):
        fig, ax = ce_states(12, '2022-01-01', '2022-01-01 12:00:00')
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)

# ---------------------------------------------------------------------------------------------------------------------


class TestCustomizeArea(unittest.TestCase):

    def setUp(self):
        self.model_obj = MODELINFO("ICON Nest", 1377, 657, 0.0625, "pres")
        self.model_obj.setrundate(datetime.strptime('2022-01-01', "%Y-%m-%d"))
        self.model_obj.setrun("00")
        self.start = '2022-01-01'

    def test_default_projection_and_extent(self):
        model_name = 'Test Model'
        fig, ax = customize_area(self.hour, self.model_obj.getrun(), self.model_obj.getrundate(), model_name)
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)

    def test_custom_projection_and_extent(self):
        model_name = 'Test Model'
        projection = EuroPP()
        lon1, lon2, lat1, lat2 = 10, 20, 40, 50
        fig, ax = customize_area(self.hour, self.model_obj.getrun(), self.model_obj.getrundate(), model_name, projection, lon1, lon2, lat1, lat2)
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)

    def test_invalid_projection(self):
        model_name = 'Test Model'
        projection = 'Invalid Projection'
        with self.assertRaises(TypeError):
            customize_area(self.hour, self.model_obj.getrun(), self.model_obj.getrundate(), model_name, projection)

    def test_invalid_extent_values(self):
        model_name = 'Test Model'
        lon1, lon2, lat1, lat2 = 10, 20, 40, 50
        with self.assertRaises(ValueError):
            customize_area(self.hour, self.model_obj.getrun(), self.model_obj.getrundate(), model_name, lon1='Invalid', lon2=lon2, lat1=lat1, lat2=lat2)

    def test_missing_required_arguments(self):
        with self.assertRaises(TypeError):
            customize_area(self.hour, self.model_obj.getrun(), self.model_obj.getrundate())

# ---------------------------------------------------------------------------------------------------------------------


class TestTestPlot(unittest.TestCase):

    def setUp(self):
        self.model_obj = MODELINFO("ICON Nest", 1377, 657, 0.0625, "pres")
        self.model_obj.setrundate(datetime.strptime('2022-01-01', "%Y-%m-%d"))
        self.model_obj.setrun("00")
    
    def test_valid_input(self):
        test_plot(12, self.model_obj.getrun(), self.model_obj, 'Test Title')
        self.assertTrue(plt.gcf().suptitle.get_text() == 'Test Title')
        self.assertTrue(plt.gcf().get_label() == 'test_ce_12.png')

    def test_invalid_hour(self):
        with self.assertRaises(ValueError):
            test_plot('invalid', self.model_obj.getrun(), self.model_obj)

    def test_invalid_run(self):
        with self.assertRaises(TypeError):
            test_plot(12, self.model_obj, self.model_obj)

    def test_invalid_title(self):
        with self.assertRaises(TypeError):
            test_plot(12, self.model_obj.getrun(), 123)

    def test_plot_closed(self):
        test_plot(12, self.model_obj.getrun(), self.model_obj)
        self.assertTrue(plt.fignum_exists(plt.gcf().number))

# ---------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

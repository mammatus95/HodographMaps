#!/usr/bin/python3
import unittest
from datetime import datetime
# project modul
from src.modelinfolib import MODELINFO

# ----------------------------------------------------------------------------------------------------------------------------


class TestMODELIFNO(unittest.TestCase):
    def setUp(self):
        self.icon_nest = MODELINFO("ICON Nest", 1377, 657, 0.0625, "pres")

    def test_setrun(self):
        run = "15"
        self.icon_nest.setrun(run)
        self.assertEqual(self.icon_nest.getrun(), int(run))

    def test_setrundate_with_date_object(self):
        test_date = "2024-04-21"
        self.icon_nest.setrundate(test_date)
        self.assertEqual(self.icon_nest.getrundate(), datetime(2024, 4, 21))
        self.assertEqual(self.icon_nest.getrundate_as_str(fmt="%Y-%m-%d"), "2024-04-21")

    def test_getname(self):
        self.assertEqual(self.icon_nest.getname(), "ICON Nest")

    def test_getParamter(self):
        self.assertIsNone(self.icon_nest.getParamter())

    def test_getpoints(self):
        self.assertEqual(self.icon_nest.getpoints(), 904689)

    def test_getnlon(self):
        self.assertEqual(self.icon_nest.getnlon(), 1377)

    def test_getnlat(self):
        self.assertEqual(self.icon_nest.getnlat(), 657)

    def test_getlevels(self):
        self.assertEqual(self.icon_nest.getlevels(), [1000, 950, 925, 900, 875, 850, 825, 800, 775, 700, 600, 500, 400, 300])

    def test_getnlev(self):
        self.assertEqual(self.icon_nest.getnlev(), 14)

    def test_getlevtyp(self):
        self.assertEqual(self.icon_nest.getlevtyp(), "pres")

    def test_getd_grad(self):
        self.assertEqual(self.icon_nest.getd_grad(), 0.0625)

    def test_create_plottitle(self):
        self.assertEqual(self.icon_nest.create_plottitle(), "Hodographmap of ICON Nest")

# ----------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python3
import unittest
import os
from datetime import date
from datetime import datetime
# project modul
from src.utilitylib import download_nwp
from src.modelinfolib import MODELINFO
from src.plotlib import cape_plot

# ----------------------------------------------------------------------------------------------------------------------------


class TestCAPE(unittest.TestCase):
    def setUp(self):
        self.store_path = "./"
        today = date.today()
        self.datum = today.strftime("%Y%m%d")
        self.model_obj = MODELINFO("ICON Nest", 1377, 657, 0.0625, "pres")
        self.model_obj.setrundate(datetime.strptime(self.datum, "%Y%m%d"))
        self.run = "00"
        self.model_obj.setrun(self.run)
        self.fp = 0
        self.fieldname = "cape_ml"
        self.grb_name = f"icon-eu_europe_regular-lat-lon_single-level_{self.datum}{self.run}_{self.fp:03d}_{self.fieldname.upper()}.grib2"
        self.expected_size = 144582

        # download
        download_nwp(self.fieldname, datum=self.datum, run=self.run, fp=self.fp, store_path=self.store_path)

        # plot
        #cape_plot(cape_fld, lats, lons, self.fp, self.model_obj.getrun(), self.datum, titel='CAPE')
    
    def test_grib_exist(self):
        # check if file exist
        self.assertTrue(os.path.exists(f"{self.store_path}/{self.grb_name}"))

    def test_read_plot(self):
        cape_fld, lats, lons = self.model_obj.open_icon_gribfile_single(self.fieldname, self.fp, path="./")
        self.assertTrue(cape_fld.shape == (657, 1377))

        cape_plot(cape_fld, lats, lons, self.fp, self.run, self.model_obj.getrundate(), titel='CAPE')
        self.assertTrue(os.path.exists(f"./testcape_ce_{self.fp}.png"))

        # Verify the file size
        actual_size = os.path.getsize(f"./testcape_ce_{self.fp}.png")
        self.assertGreaterEqual(actual_size, self.expected_size, "File size does not match expected size.")

# ----------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

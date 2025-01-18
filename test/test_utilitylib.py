#!/usr/bin/python3
import unittest
import yaml
import os
from tempfile import TemporaryDirectory
from datetime import date
from datetime import datetime
# project modul
from src.utilitylib import datum, load_yaml, download_nwp

# ----------------------------------------------------------------------------------------------------------------------------


class TestDatumFunction(unittest.TestCase):
    def test_valid_integer_inputs(self):
        leadtime = 12
        start = 10
        datetime_obj = datetime(2022, 1, 1)
        expected_modelrun_string = "Run: 01.01. 10 UTC"
        expected_valid_string = "Saturday, 01.01. 22 UTC"
        modelrun_string, valid_string = datum(leadtime, start, datetime_obj)
        self.assertEqual(modelrun_string, expected_modelrun_string)
        self.assertEqual(valid_string, expected_valid_string)

    def test_non_integer_inputs(self):
        leadtime = "12"
        start = "10"
        datetime_obj = datetime(2022, 1, 1)
        expected_modelrun_string = "Run: 01.01. 10 UTC"
        expected_valid_string = "Saturday, 01.01. 22 UTC"
        modelrun_string, valid_string = datum(leadtime, start, datetime_obj)
        self.assertEqual(modelrun_string, expected_modelrun_string)
        self.assertEqual(valid_string, expected_valid_string)

    def test_invalid_inputs(self):
        leadtime = "abc"
        start = "def"
        datetime_obj = datetime(2022, 1, 1)
        with self.assertRaises(ValueError):
            datum(leadtime, start, datetime_obj)

    def test_edge_cases(self):
        leadtime = 0
        start = 0
        datetime_obj = datetime(2022, 1, 1)
        expected_modelrun_string = "Run: 01.01. 00 UTC"
        expected_valid_string = "Saturday, 01.01. 00 UTC"
        modelrun_string, valid_string = datum(leadtime, start, datetime_obj)
        self.assertEqual(modelrun_string, expected_modelrun_string)
        self.assertEqual(valid_string, expected_valid_string)

# ----------------------------------------------------------------------------------------------------------------------------


class TestLoadYaml(unittest.TestCase):

    def test_valid_yaml_file(self):
        with TemporaryDirectory() as tmpdir:
            yaml_file = 'test.yaml'
            yaml_path = tmpdir
            with open(os.path.join(yaml_path, yaml_file), 'w') as f:
                f.write('key: value')
            config_data = load_yaml(yaml_file, yaml_path)
            self.assertEqual(config_data, {'key': 'value'})

    def test_non_existent_yaml_file(self):
        with self.assertRaises(FileNotFoundError):
            load_yaml('non_existent.yaml', '.')

    """
    def test_invalid_yaml_syntax(self):
        with TemporaryDirectory() as tmpdir:
            yaml_file = 'test.yaml'
            yaml_path = tmpdir
            with open(os.path.join(yaml_path, yaml_file), 'w') as f:
                f.write('invalid: syntax')
            with self.assertRaises(yaml.YAMLError):
                load_yaml(yaml_file, yaml_path)
    """

    def test_relative_path(self):
        with TemporaryDirectory() as tmpdir:
            yaml_file = 'test.yaml'
            yaml_path = os.path.join(tmpdir, 'subdir')
            os.mkdir(yaml_path)
            with open(os.path.join(yaml_path, yaml_file), 'w') as f:
                f.write('key: value')
            config_data = load_yaml(yaml_file, yaml_path)
            self.assertEqual(config_data, {'key': 'value'})

    def test_absolute_path(self):
        with TemporaryDirectory() as tmpdir:
            yaml_file = 'test.yaml'
            yaml_path = tmpdir
            with open(os.path.join(yaml_path, yaml_file), 'w') as f:
                f.write('key: value')
            config_data = load_yaml(yaml_file, os.path.abspath(yaml_path))
            self.assertEqual(config_data, {'key': 'value'})

# ----------------------------------------------------------------------------------------------------------------------------


class TestDownloadNWP(unittest.TestCase):
    def test_download(self):
        store_path = "./"
        today = date.today()
        datum = today.strftime("%Y%m%d")
        run = "00"
        fp = 0
        download_nwp('cape_ml', datum=datum, run=run, fp=fp, store_path=store_path)

        # check if file exist
        self.assertTrue(os.path.exists(f"{store_path}/test.grib2.bz2"))
        # self.assertTrue(os.path.exists(f"{store_path}/icon-eu_europe_regular-lat-lon_single-level_{datum}{run}_{fp:03d}_CAPE_ML.grib2.bz2"))

# ----------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

import json
import os
import unittest

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

data_path = os.path.join(script_path, "..", "..", "data")


class CityTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CityTestCase, self).__init__(*args, **kwargs)

        # Load geojson file
        with open(file=os.path.join(data_path, "hamburg-administrative-boundaries", "hamburg-city.geojson"), mode="r",
                  encoding="utf-8") as geojson_file:
            self.geojson = json.load(geojson_file, strict=False)

    def test_feature_count(self):
        self.assertEqual(1, len(self.geojson["features"]))


class DistrictsTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DistrictsTestCase, self).__init__(*args, **kwargs)

        # Load geojson file
        with open(file=os.path.join(data_path, "hamburg-administrative-boundaries", "hamburg-districts.geojson"),
                  mode="r",
                  encoding="utf-8") as geojson_file:
            self.geojson = json.load(geojson_file, strict=False)

    def test_feature_count(self):
        self.assertEqual(7, len(self.geojson["features"]))


class QuartersTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(QuartersTestCase, self).__init__(*args, **kwargs)

        # Load geojson file
        with open(file=os.path.join(data_path, "hamburg-administrative-boundaries", "hamburg-quarters.geojson"),
                  mode="r",
                  encoding="utf-8") as geojson_file:
            self.geojson = json.load(geojson_file, strict=False)

    def test_feature_count(self):
        self.assertEqual(104, len(self.geojson["features"]))


class AreasTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AreasTestCase, self).__init__(*args, **kwargs)

        # Load geojson file
        with open(file=os.path.join(data_path, "hamburg-administrative-boundaries", "hamburg-areas.geojson"),
                  mode="r",
                  encoding="utf-8") as geojson_file:
            self.geojson = json.load(geojson_file, strict=False)

    def test_feature_count(self):
        self.assertEqual(181, len(self.geojson["features"]))


if __name__ == '__main__':
    unittest.main()

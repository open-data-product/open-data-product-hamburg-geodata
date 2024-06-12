import json
import os
from collections.abc import Sequence
from itertools import chain, count

from lib.tracking_decorator import TrackingDecorator


@TrackingDecorator.track_time
def clean_data_geometry(source_path, results_path, clean=False, quiet=False):
    # Iterate over files
    for subdir, dirs, files in os.walk(source_path):
        for file_name in [file_name for file_name in sorted(files) if file_name.endswith(".geojson")]:
            subdir = subdir.replace(f"{source_path}/", "")

            # Make results path
            os.makedirs(os.path.join(results_path), exist_ok=True)

            source_file_path = os.path.join(source_path, subdir, file_name)
            results_file_path = os.path.join(results_path, subdir, file_name)

            with open(source_file_path, "r", encoding="utf-8") as geojson_file:
                geojson = json.load(geojson_file, strict=False)

            geojson, changed = clean_geometry(geojson, quiet)

            if changed:
                with open(results_file_path, "w", encoding="utf-8") as geojson_file:
                    json.dump(geojson, geojson_file, ensure_ascii=False)

                    if not quiet:
                        print(f"✓ Clean {file_name}")
            else:
                if not quiet:
                    print(f"✓ Already cleaned {file_name}")


def clean_geometry(geojson, quiet):
    changed = False

    for feature in geojson["features"]:
        id = feature["properties"]["id"]
        name = feature["properties"]["name"]
        polygons = feature["geometry"]["coordinates"]

        # Check if there is more than one polygon
        if len(polygons) > 1:
            polygon_max = [[]]

            for polygon in polygons:
                polygon_elements_count = len(polygon[0])
                polygon_elements_count_max = len(polygon_max[0])

                if polygon_elements_count > polygon_elements_count_max:
                    polygon_max = polygon

            feature["geometry"]["coordinates"] = [polygon_max]
            changed = True

            if not quiet:
                print(f"⚠ Clean geometry of {id} {name}")

        # Sanity-check geometry
        if get_depth(feature["geometry"]["coordinates"]) != 4 and not quiet:
            print(f"⚠ Invalid geometry of {id} {name}")

    return geojson, changed


# Thanks https://stackoverflow.com/a/6040217/2992219
def get_depth(seq):
    for level in count():
        if not seq:
            return level
        seq = list(chain.from_iterable(s for s in seq if isinstance(s, Sequence)))

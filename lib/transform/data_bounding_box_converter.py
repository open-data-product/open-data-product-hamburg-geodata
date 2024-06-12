import itertools
import json
import os

from lib.tracking_decorator import TrackingDecorator

target_projection_number = "4326"


@TrackingDecorator.track_time
def convert_bounding_box(source_path, results_path, clean=False, quiet=False):
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
                projection = str(geojson["crs"]["properties"]["name"])
                projection_number = projection.split(":")[-1]

                if projection_number == target_projection_number or projection_number == "CRS84":
                    geojson_with_bounding_box = extend_by_bounding_box(geojson, clean)

                    with open(results_file_path, "w", encoding="utf-8") as geojson_file:
                        json.dump(geojson_with_bounding_box, geojson_file, ensure_ascii=False)

                if not quiet:
                    print(f"✓ Convert {file_name}")


def flatten_list(complex_list):
    while not (type(complex_list[0][0]) == float and type(complex_list[0][1]) == float):
        complex_list = list(itertools.chain(*complex_list))

    return complex_list


def extend_by_bounding_box(geojson, clean=False):
    for feature in geojson["features"]:
        if "bounding_box" not in feature["properties"] or clean:
            xmin = None
            ymin = None
            xmax = None
            ymax = None

            geometry = feature["geometry"]
            coordinates = geometry["coordinates"]

            for coordinate in flatten_list(coordinates):

                x = coordinate[0]
                y = coordinate[1]

                if xmin is None or x < xmin:
                    xmin = x
                if ymin is None or y < ymin:
                    ymin = y
                if xmax is None or x > xmax:
                    xmax = x
                if ymax is None or y > ymax:
                    ymax = y

            feature["properties"]["bounding_box"] = [xmin, ymin, xmax, ymax]

    return geojson

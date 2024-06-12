import json
import os

from lib.tracking_decorator import TrackingDecorator


@TrackingDecorator.track_time
def extend_data_properties(source_path, results_path, clean=False, quiet=False):
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

            geojson, changed = extend_properties(geojson)

            if changed:
                with open(results_file_path, "w", encoding="utf-8") as geojson_file:
                    json.dump(geojson, geojson_file, ensure_ascii=False)

                    if not quiet:
                        print(f"✓ Extend {file_name}")
            else:
                if not quiet:
                    print(f"✓ Already extended {file_name}")


def extend_properties(geojson):
    changed = False

    if not "crs" in geojson:
        geojson["crs"] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}
        changed = True

    for feature in geojson["features"]:
        properties = feature["properties"]

        id = properties["id"]

        if id == "1":
            properties["area"] = 142_200_000
            changed = True
        elif id == "2":
            properties["area"] = 77_400_000
            changed = True
        elif id == "3":
            properties["area"] = 49_800_000
            changed = True
        elif id == "4":
            properties["area"] = 57_800_000
            changed = True
        elif id == "5":
            properties["area"] = 147_600_000
            changed = True
        elif id == "6":
            properties["area"] = 154_800_000
            changed = True
        elif id == "7":
            properties["area"] = 125_400_000
            changed = True

    return geojson, changed

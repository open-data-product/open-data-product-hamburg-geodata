import json
import os

from lib.tracking_decorator import TrackingDecorator


@TrackingDecorator.track_time
def clean_data_properties(source_path, results_path, clean=False, quiet=False):
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

            geojson, changed = clean_properties(geojson)

            if changed:
                with open(results_file_path, "w", encoding="utf-8") as geojson_file:
                    json.dump(geojson, geojson_file, ensure_ascii=False)

                    if not quiet:
                        print(f"✓ Clean {file_name}")
            else:
                if not quiet:
                    print(f"✓ Already cleaned {file_name}")


def clean_properties(geojson):
    changed = False

    for feature in geojson["features"]:
        properties = feature["properties"]

        id = None
        name = None
        area = None

        # Add property to city
        if "fhh" in properties:
            properties["id"] = "0"
            properties["name"] = "Hamburg"

        # Iterate over potential ID properties
        for id_property in ["bezirk", "stadtteil_schluessel", "ortsteil_schluessel"]:
            if id_property in properties:
                id = properties[id_property]

                properties["id"] = id
                properties.pop(id_property, None)
                changed = True

        # Iterate over potential name properties
        for name_property in ["bezirk_name", "stadtteil_name", "ortsteil_name"]:
            if name_property in properties:
                name = properties[name_property]
                properties["name"] = name
                properties.pop(name_property, None)
                changed = True

        # Drop other properties
        for drop_property in ["fhh",
                              "bezirk", "bezirk_name",
                              "stadtteil_name", "stadtteil_schluessel", "stadtteil_nummer",
                              "ortsteil_name", "ortsteil_schluessel", "ortsteil_nummer"]:
            if drop_property in properties:
                properties.pop(drop_property, None)
                changed = True

    return geojson, changed

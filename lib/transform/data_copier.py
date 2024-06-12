import os
import shutil

from lib.tracking_decorator import TrackingDecorator


@TrackingDecorator.track_time
def copy_data(source_path, results_path, clean=False, quiet=False):
    # Iterate over files
    for subdir, dirs, files in os.walk(source_path):
        for source_file_name in files:
            subdir = subdir.replace(f"{source_path}/", "")
            results_file_name = get_results_file_name(source_file_name)

            # Make results path
            os.makedirs(os.path.join(results_path, subdir), exist_ok=True)

            source_file_path = os.path.join(source_path, subdir, source_file_name)
            results_file_path = os.path.join(results_path, subdir, results_file_name)

            if results_file_name.endswith(".geojson"):

                # Check if file needs to be copied
                if clean or not os.path.exists(results_file_path):
                    shutil.copyfile(source_file_path, results_file_path)

                    if not quiet:
                        print(f"✓ Copy {results_file_name}")
                else:
                    print(f"✓ Already exists {results_file_name}")


def get_results_file_name(source_file_name):
    if source_file_name == "app_landesgrenze_EPSG_4326.json":
        return "hamburg-city.geojson"
    elif source_file_name == "app_bezirke_EPSG_4326.json":
        return "hamburg-districts.geojson"
    elif source_file_name == "app_stadtteile_EPSG_4326.json":
        return "hamburg-quarters.geojson"
    elif source_file_name == "app_ortsteile_EPSG_4326.json":
        return "hamburg-areas.geojson"

    else:
        return source_file_name

import os
import xarray as xr


def get_minmax(input_dir, variable):
    """Extracts min and max values for a given variable in all xarrays in a directory"""

    # Define arrays to store min and max values per file
    minvals = []
    maxvals = []

    # Get all files in directory
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.nc'):
            filepath = os.path.join(input_dir, filename)
            print(filename)

            # Read file
            ds = xr.open_dataset(filepath)

            # Store min and max values
            minvals.append(ds[variable].min().item())
            maxvals.append(ds[variable].max().item())

    return min(minvals), max(maxvals)


def extract_tifs(input_dir, variable, minmax, output_dir):
    """Normalizes a given variable in all xarrays in a directory based on global min-max range and exports as grayscale tiffs"""

    # Get all files in directory
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.nc'):
            filepath = os.path.join(input_dir, filename)

            # Read file
            ds = xr.open_dataset(filepath)

            ds[f'{variable}_norm'] = (ds[variable] - minmax[0]) / (minmax[1] - minmax[0])
            print(filename, ds[f'{variable}_norm'].min().item(), ds[f'{variable}_norm'].max().item())

            ds[f'{variable}_norm'].rio.to_raster(f"{output_dir}/{filename}_norm.tif")

    return


if __name__ == '__main__':

    directory = 'hourly_precipitation'
    variable = 'image1_image_data'

    if not os.path.exists(f"data/{directory}_norm"):
        os.makedirs(f"data/{directory}_norm")

    minmax = get_minmax(f"data/{directory}", variable)
    extract_tifs(f"data/{directory}", variable, minmax, f"data/{directory}_norm")
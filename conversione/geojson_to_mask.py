import os
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import rasterize

def geojson_to_mask(geojson_path, reference_image_path, output_tiff_path):
   
    try:
        with rasterio.open(reference_image_path) as src:
            transform = src.transform
            out_shape = (src.height, src.width)
    except Exception as e:
        raise ValueError(f"Error reading reference TIFF file {reference_image_path}: {e}")

    
    try:
        gdf = gpd.read_file(geojson_path)
    except Exception as e:
        raise ValueError(f"Error reading GeoJSON file {geojson_path}: {e}")

    
    if gdf.empty or gdf.geometry.isnull().all():
        mask = np.zeros(out_shape, dtype='uint8')
    else:
        
        mask = rasterize(
            [(geom, 255) for geom in gdf.geometry if geom.is_valid],
            out_shape=out_shape,
            transform=transform,
            fill=0,
            dtype='uint8'
        )

    with rasterio.open(
        output_tiff_path, 'w',
        driver='GTiff',
        height=mask.shape[0],
        width=mask.shape[1],
        count=1,
        dtype=mask.dtype,
        crs='+proj=latlong',
        transform=transform,
    ) as dst:
        dst.write(mask, 1)

def convert_all_geojson_to_tiff(geojson_directory, reference_image_directory, output_tiff_directory):
    if not os.path.exists(output_tiff_directory):
        os.makedirs(output_tiff_directory)

    geojson_files = [f for f in os.listdir(geojson_directory) if f.endswith('.geojson')]
    
    for geojson_file in geojson_files:
        geojson_path = os.path.join(geojson_directory, geojson_file)
        reference_image_path = os.path.join(reference_image_directory, geojson_file.replace('.geojson', '.tif').replace('Buildings', 'PS-RGB'))
        output_tiff_path = os.path.join(output_tiff_directory, geojson_file.replace('.geojson', '_mask.tiff'))
        
        
        if os.path.exists(output_tiff_path):
            print(f"{output_tiff_path} already exists, skipping...")
            continue
        
        
        if not os.path.exists(reference_image_path):
            print(f"Reference image not found for {geojson_file}, skipping...")
            continue
        
        
        try:
            geojson_to_mask(geojson_path, reference_image_path, output_tiff_path)
            print(f"Converted {geojson_file} to {output_tiff_path}")
        except Exception as e:
            print(f"Failed to convert {geojson_file}: {e}")




geojson_directory = "/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/geojson_buildings"
reference_image_directory = "/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/PS-RGB"
output_tiff_directory = "/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/tiff_try"

convert_all_geojson_to_tiff(geojson_directory, reference_image_directory, output_tiff_directory)

from pathlib import Path

# Root-relative path to your shapefiles; adjust to your repo
# Example repo structure: ../Geografia Colombia/gadm41_COL_shp/
SHAPES_DIR = Path(__file__).resolve().parents[2] / "Geografia Colombia" / "gadm41_COL_shp"

# Filenames used in your notebook snippet
DPTO_SHP = SHAPES_DIR / "gadm41_COL_1.shp"
MPIO_SHP = SHAPES_DIR / "gadm41_COL_2.shp"

DATOS_DIR = Path(__file__).resolve().parents[2] / "Data"

DATA_RES = DATOS_DIR / "Resultados_modelo.csv"
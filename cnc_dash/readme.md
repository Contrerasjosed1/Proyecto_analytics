# CNC – Digital Adoption Panel (Scroll template)

This is a scroll-first Dash template aligned to your mockup. The map is rendered with GeoPandas + Matplotlib to reproduce the hatched background + OrRd choropleth from your notebook, then displayed as a PNG in the dashboard.

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Shapefiles
Set your repo like:
```
cnc_dash/
Geografia Colombia/gadm41_COL_shp/
  ├─ gadm41_COL_1.shp   # departamentos
  └─ gadm41_COL_2.shp   # municipios
```
If you use a different location, edit `src/config.py`.

## Plug your data/models
- Replace synthetic data in `src/callbacks.py::_init_data`.
- Map aggregation lives in `src/data/geo_map.py::build_choropleth_png`.
- Replace pattern composition and clustering logic in `src/callbacks.py` with your real models.
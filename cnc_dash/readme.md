# CNC – Digital Adoption Panel (Dash template)

A production-ready Dash template aligned to the project's mockup: overview KPIs, territorial view with ranking, population segments, what-if scenarios, and a data explorer. Clean theme, modular structure, and placeholder callbacks so you can plug in your ETL and models.

## Quickstart

```bash
# 1) Create a venv and install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Run the app
python app.py
```

The app ships with synthetic sample data so it runs out of the box. Replace it by wiring your ETL into `store-data` in `src/callbacks.py`.

## Where to plug your code

- **ETL / data load**: Replace `make_fake_data` usage in `src/callbacks.py::_load_data`.
- **Choropleth map**: In `pages/territorial.py`, pass your GeoJSON + metrics to a Plotly choropleth figure.
- **Clustering**: Replace the synthetic `cluster` in the sample data and adapt the callbacks in `src/callbacks.py::_segments`.
- **Policy / what-if**: Edit `src/callbacks.py::_scenarios` to call your models with inputs from the sliders.

## Shared filter contract

Global filters are stored in `store-filters` with this schema:
```json
{
  "year": 2018 | 2023 | null,
  "depto": ["Antioquia", ...],
  "muni": ["Medellín", ...],
  "estrato": [1,2,3,4,5,6],
  "edad": [min, max],
  "with_internet": true | false
}
```
Use `_apply_filters(df, F)` from `src/callbacks.py` to reuse the filtering logic.

## Theming

Palette is defined in `assets/theme.css` via CSS variables. Tweak `--color-*` tokens to fit branding.

## Pages

- `/` – Overview (KPIs + 2 charts)
- `/territorial` – Territorial heatmap (placeholder) + ranking table
- `/segments` – Population segments (scatter + bars)
- `/scenarios` – What-if controls + KPIs
- `/data` – Data explorer (DataTable)
- `/about` – Notes

## Tips

- Keep data in memory via `dcc.Store` for snappy interactions.
- Use `dash.register_page` to add or reorder pages without touching the shell.
- For maps, consider pre-aggregated metrics per polygon to avoid heavy client transforms.

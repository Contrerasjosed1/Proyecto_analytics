from io import BytesIO
import base64
from pathlib import Path
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .sample_data import make_fake_data
from src.config import DPTO_SHP, MPIO_SHP


def build_choropleth_png(df=None) -> str:
    """Returns a data:image/png;base64 string for display in Dash.
    Uses the same logic you shared: join department shapefile with an aggregated metric.
    """
    if df is None:
        df = make_fake_data(2000)

    # Normalize department names for join
    tmp = df.copy()
    tmp["Nombre Departamento_norm"] = (tmp["departamento"].str.upper()
                                       .str.normalize("NFKD").str.encode("ascii","ignore").str.decode("utf-8"))

    gdf_dpto = gpd.read_file(DPTO_SHP)
    gdf_dpto["NAME_1_norm"] = (gdf_dpto["NAME_1"].str.upper()
                                 .str.normalize("NFKD").str.encode("ascii","ignore").str.decode("utf-8"))

    df_dpto = (tmp.groupby("Nombre Departamento_norm", as_index=False)
                  .agg(dens_int=("dens_int","mean"), n_mpios=("municipio","nunique")))

    gdf_join = gdf_dpto.merge(df_dpto, left_on="NAME_1_norm", right_on="Nombre Departamento_norm", how="left")

    # --- Plot with hatch background + choropleth
    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
    gdf_dpto.boundary.plot(ax=ax, edgecolor="grey", linewidth=0.7)
    gdf_join.plot(
        ax=ax,
        column="dens_int",
        cmap="OrRd",
        edgecolor="black",
        linewidth=0.4,
        legend=True,
        legend_kwds={"label": "Densidad (dens_int)", "orientation": "vertical"},
        missing_kwds={"color":"white","edgecolor":"grey","hatch":"...","label":"Sin dato"}
    )
    ax.set_axis_off()
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    enc = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{enc}"
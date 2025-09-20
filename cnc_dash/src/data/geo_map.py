from io import BytesIO
import base64
from pathlib import Path
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .sample_data import make_fake_data, leer_base_datos
from src.config import DPTO_SHP, MPIO_SHP


def build_choropleth_png(df=None, tipo=None) -> str:
    """Returns a data:image/png;base64 string for display in Dash.
    Uses the same logic you shared: join department shapefile with an aggregated metric.
    """
    if df is None:
        # df = make_fake_data(2000)
        df = leer_base_datos()

    # Normalize department names for join
    gdf_dpto = gpd.read_file(DPTO_SHP)
    gdf_mpio = gpd.read_file(MPIO_SHP)
    tmp = df.copy()

    gdf_dpto["NAME_1_norm"] = (gdf_dpto["NAME_1"].str.upper()
                                 .str.normalize("NFKD").str.encode("ascii","ignore").str.decode("utf-8"))
    # --- Plot with hatch background + choropleth
    fig, ax = plt.subplots(figsize=(8, 11), dpi=150)
    gdf_dpto.boundary.plot(ax=ax, edgecolor="grey", linewidth=0.7)

    if tipo == "Municipio":
        gdf_mpio = gdf_mpio.merge(tmp, left_on="NAME_2", right_on="MUNICIPIO_NOMBRE", how="left")

        gdf_mpio.plot(
            ax=ax, 
            column="dens_int",      # columna de colores
            cmap="OrRd",            # paleta de colores (puedes cambiar a 'viridis', 'Blues', etc.)
            edgecolor="black",
            legend=True,            # para que salga la barra de colores
            legend_kwds={"label": "Densidad (dens_int)", "orientation": "vertical"}
        )
    else:
        tmp["Nombre Departamento_norm"] = (tmp["Nombre Departamento"].str.upper().str.normalize("NFKD")
                                        .str.encode("ascii","ignore").str.decode("utf-8"))


        df_dpto = (tmp.groupby("Nombre Departamento_norm", as_index=False)
                    .agg(dens_int=("dens_int","mean"), n_mpios=("MUNICIPIO_NOMBRE","nunique")))

        gdf_join = gdf_dpto.merge(df_dpto, left_on="NAME_1_norm", right_on="Nombre Departamento_norm", how="left")

        

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
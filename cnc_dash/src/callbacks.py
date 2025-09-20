from dash import Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data.sample_data import make_fake_data,leer_base_datos
from src.data.geo_map import build_choropleth_png

# ---------------------- Data load ----------------------
@callback(
    Output("store-data", "data"),
    Output("store-metadata", "data"),
    Input("store-data", "id"),
    prevent_initial_call=False,
)
def _init_data(_):
    df = leer_base_datos()
    meta = {"rows": len(df)}
    return df.to_dict("records"), meta


# ---------------------- Filters ------------------------
@callback(
    Output("f-region", "options"),
    Input("store-data", "data"))
def _opts_region(data):
    return ["Departamento", "Municipio"]

@callback(
    Output("f-area", "options"),
    Input("f-region", "value"),
    Input("store-data", "data"))
def _opts_area(region_sel,data):
    df = pd.DataFrame(data)
    if not region_sel:
        return sorted(df["Nombre Departamento"].unique())
    else:
        if region_sel=="Departamento":
            return sorted(df["Nombre Departamento"].unique())
        else:
            return sorted(df["MUNICIPIO_NOMBRE"].unique())


@callback(
    Output("store-data-filtrada", "data"),   # ejemplo: actualiza un KPI chip
    Input("f-region", "value"),
    Input("f-area", "value"),
    Input("store-data", "data")
)
def _filtrar_por_depto(region_sel, area_sel, data):
    df = pd.DataFrame(data)
    if not region_sel:
        llave="Nombre Departamento"
    elif region_sel == "Departamento":
        llave="Nombre Departamento"
    else:
        llave = "MUNICIPIO_NOMBRE"

    if not area_sel:  # nada seleccionado
        df_filtrado = df
    else:
        # si multi=True, depto_sel puede ser lista
        if isinstance(area_sel, list):
            df_filtrado = df[df[llave].isin(area_sel)]
        else:
            df_filtrado = df[df[llave] == area_sel]
    return df_filtrado.to_dict("records")

# ---------------------- Map image ----------------------
@callback(Output("img-map", "src"), Input("store-data-filtrada", "data"))
def _update_map(data):
    df = pd.DataFrame(data)
    return build_choropleth_png(df)


# ---------------------- Section 1 charts ---------------
@callback(
    Output("fig-prom-pobl", "figure"),
    Output("fig-cobertura-cluster", "figure"),
    Output("fig-adop-por-cluster", "figure"),
    Input("store-data", "data"))

def _section1(data):
    df = pd.DataFrame(data)
    g = df.groupby("Nombre Departamento").agg(pobl=("POBLACIÓN_ICFES","mean"), cobertura=("HOGARES_INTERNET","mean"), adop=("dens_int","mean")).reset_index()
    f1 = px.bar(g, x="Nombre Departamento", y="pobl", title="Promedio de población por Departamento")
    f2 = px.bar(g, x="Nombre Departamento", y="cobertura", title="Tasa de cobertura por Departamento")
    f2.update_yaxes(tickformat=",.0%")
    f3 = px.line(g, x="Nombre Departamento", y="adop", markers=True, title="Tasa de adopción digital por cluster")
    return f1, f2, f3


# ---------------------- Section 2 charts ---------------
@callback(
    Output("fig-scatter-clusters", "figure"),
    Output("fig-genero", "figure"),
    Output("fig-estrato-prom", "figure"),
    Output("fig-escolaridad-prom", "figure"),
    Input("store-data", "data"))

def _section2(data):
    df = pd.DataFrame(data)
    f_sc = px.scatter(df.sample(min(600, len(df))), x="EDAD", y="dens_int", color="cluster", opacity=.8,
                      title="Distribución de clusters", labels={"EDAD":"Edad","dens_int":"Índice"})

    g_gen = (df.groupby(["cluster","GENERO"], observed=False, as_index=False).size())
    f_gen = px.bar(g_gen, x="cluster", y="size", color="GENERO", barmode="stack", title="Proporción de género por cluster")

    g_est = (df.groupby("cluster")[["ESTRATO"]].mean().reset_index())
    f_est = px.bar(g_est, x="cluster", y="ESTRATO", title="Estrato promedio por cluster")

    g_esc = (df.groupby("cluster")[["NIVEL_PIRAMIDE"]].mean().reset_index())
    f_esc = px.bar(g_esc, x="cluster", y="NIVEL_PIRAMIDE", title="Años de escolaridad promedio")

    return f_sc, f_gen, f_est, f_esc


# ---------------------- Section 3 chart ----------------
@callback(Output("fig-patrones", "figure"), Input("store-data", "data"))

def _section3(data):
    df = pd.DataFrame(data)

    # Usar los mismos nombres de columnas que manejas
    cat_col = "ESTRATO" if "ESTRATO" in df.columns else ("estrato" if "estrato" in df.columns else None)
    if cat_col is None or "cluster" not in df.columns:
        return go.Figure()

    # Tabla de proporciones: filas = cluster, columnas = categorías
    tmp = df[[cat_col, "cluster"]].copy()
    tab = (
        tmp.groupby(["cluster", cat_col], observed=False).size()
           .groupby(level=0).apply(lambda s: s / s.sum())   # proporciones por cluster
           .unstack(fill_value=0)
           .sort_index()
    )

    # Eje X robusto: soporta Index o MultiIndex
    if isinstance(tab.index, pd.MultiIndex):
        x_vals = tab.index.get_level_values(0).astype(str).tolist()
    else:
        x_vals = tab.index.astype(str).tolist()

    # Construcción del stacked bar en proporción
    fig = go.Figure()
    for cat in tab.columns:
        fig.add_trace(go.Bar(
            name=str(cat),
            x=x_vals,
            y=tab[cat].values  # proporciones 0–1
        ))

    fig.update_layout(
        barmode="stack",
        title=f"Composición por {cat_col}",
        xaxis_title="Cluster",
        yaxis_title="Proporción",
        yaxis=dict(tickformat=".0%")
    )
    return fig

# ---------------------- Section 4 table ----------------
@callback(Output("tbl-top5", "figure"), Input("store-data", "data"))

def _section4(data):
    df = pd.DataFrame(data)
    # "Necesidad" como (1 - idx_adopcion)
    need = (df.groupby(["Nombre Departamento","MUNICIPIO_NOMBRE"], as_index=False)
            .agg(cobertura=("HOGARES_INTERNET","mean"), adop=("dens_int","mean"), estrato=("ESTRATO","mean")))
    need["score"] = 1 - need["adop"]
    top5 = need.sort_values("score", ascending=False).head(5)

    # Render as table-like figure for quick drop-in (consistent with plot outputs)
    header = dict(values=["Municipio","Cobertura","Departamento","Tasa adopción","Estrato prom."], align='left')
    cells = dict(values=[
        top5["MUNICIPIO_NOMBRE"],
        (top5["cobertura"]*100).round(0).astype(int).astype(str) ,
        top5["Nombre Departamento"],
        (top5["adop"]*100).round(0).astype(int).astype(str) + '%',
        top5["estrato"].round(1)
    ], align='left')
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    fig.update_layout(title="Top 5 de municipios con mayores necesidades de adopción digital")
    return fig
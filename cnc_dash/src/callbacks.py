from dash import Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data.sample_data import make_fake_data
from src.data.geo_map import build_choropleth_png

# ---------------------- Data load ----------------------
@callback(
    Output("store-data", "data"),
    Output("store-metadata", "data"),
    Input("store-data", "id"),
    prevent_initial_call=False,
)
def _init_data(_):
    df = make_fake_data(2000)
    meta = {"rows": len(df)}
    return df.to_dict("records"), meta


# ---------------------- Filters ------------------------
@callback(
    Output("f-depto", "options"),
    Input("store-data", "data"))
def _opts_depto(data):
    df = pd.DataFrame(data)
    return sorted(df["departamento"].unique())


# ---------------------- Map image ----------------------
@callback(Output("img-map", "src"), Input("store-data", "data"))
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
    g = df.groupby("cluster").agg(pobl=("municipio","size"), cobertura=("acceso_internet","mean"), adop=("idx_adopcion","mean")).reset_index()
    f1 = px.bar(g, x="cluster", y="pobl", title="Promedio de población por cluster")
    f2 = px.bar(g, x="cluster", y="cobertura", title="Tasa de cobertura por cluster")
    f2.update_yaxes(tickformat=",.0%")
    f3 = px.line(g, x="cluster", y="adop", markers=True, title="Tasa de adopción digital por cluster")
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
    f_sc = px.scatter(df.sample(min(600, len(df))), x="edad", y="idx_adopcion", color="cluster", opacity=.8,
                      title="Distribución de clusters", labels={"edad":"Edad","idx_adopcion":"Índice"})

    g_gen = (df.groupby(["cluster","genero"], as_index=False).size())
    f_gen = px.bar(g_gen, x="cluster", y="size", color="genero", barmode="stack", title="Proporción de género por cluster")

    g_est = (df.groupby("cluster")[["estrato"]].mean().reset_index())
    f_est = px.bar(g_est, x="cluster", y="estrato", title="Estrato promedio por cluster")

    g_esc = (df.groupby("cluster")[["escolaridad_anios"]].mean().reset_index())
    f_esc = px.bar(g_esc, x="cluster", y="escolaridad_anios", title="Años de escolaridad promedio")

    return f_sc, f_gen, f_est, f_esc


# ---------------------- Section 3 chart ----------------
@callback(Output("fig-patrones", "figure"), Input("store-data", "data"))

def _section3(data):
    df = pd.DataFrame(data)
    # Fake composition of patterns
    bins = pd.qcut(df["idx_adopcion"], 5, labels=["No usuarios","Comunicación y entretenimiento","Educación y participación","Uso avanzado","Uso experto"])
    g = df.groupby(["cluster", bins], as_index=False).size()
    f = px.bar(g, x="cluster", y="size", color="idx_adopcion", barmode="stack", title="Patrones de adopción digital")
    f.update_layout(legend_title_text="Patrón")
    return f


# ---------------------- Section 4 table ----------------
@callback(Output("tbl-top5", "figure"), Input("store-data", "data"))

def _section4(data):
    df = pd.DataFrame(data)
    # "Necesidad" como (1 - idx_adopcion)
    need = (df.groupby(["departamento","municipio"], as_index=False)
            .agg(cobertura=("acceso_internet","mean"), adop=("idx_adopcion","mean"), estrato=("estrato","mean")))
    need["score"] = 1 - need["adop"]
    top5 = need.sort_values("score", ascending=False).head(5)

    # Render as table-like figure for quick drop-in (consistent with plot outputs)
    header = dict(values=["Municipio","Cobertura","Departamento","Tasa adopción","Estrato prom."], align='left')
    cells = dict(values=[
        top5["municipio"],
        (top5["cobertura"]*100).round(0).astype(int).astype(str) + '%',
        top5["departamento"],
        (top5["adop"]*100).round(0).astype(int).astype(str) + '%',
        top5["estrato"].round(1)
    ], align='left')
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    fig.update_layout(title="Top 5 de municipios con mayores necesidades de adopción digital")
    return fig
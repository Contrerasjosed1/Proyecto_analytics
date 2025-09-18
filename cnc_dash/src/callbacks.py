
from dash import Input, Output, State, callback, dcc
import pandas as pd

from src.data.sample_data import make_fake_data

# ── Initialize stores when app loads ─────────────────────────────────────────
@callback(
    Output("store-data", "data"),
    Output("store-metadata", "data"),
    Input("btn-refresh", "n_clicks"),
    prevent_initial_call=False,
)
def _load_data(n_clicks):
    df = make_fake_data(n=2000)
    meta = {"rows": len(df), "note": "Using synthetic sample data. Replace with real ETL output."}
    return df.to_dict("records"), meta


# ── Populate filter options from data ────────────────────────────────────────
@callback(
    Output("f-year", "options"),
    Output("f-depto", "options"),
    Output("f-muni", "options"),
    Input("store-data", "data"),
)
def _populate_filters(data):
    df = pd.DataFrame(data)
    return (
        sorted(df["year"].unique()),
        sorted(df["departamento"].unique()),
        sorted(df["municipio"].unique()),
    )


# ── Update global filters store ──────────────────────────────────────────────
@callback(
    Output("store-filters", "data"),
    Input("f-year", "value"),
    Input("f-depto", "value"),
    Input("f-muni", "value"),
    Input("f-estrato", "value"),
    Input("f-edad", "value"),
    Input("f-internet", "value"),
)
def _update_filters(y, dpt, muni, est, edad, net):
    return {
        "year": y,
        "depto": dpt or [],
        "muni": muni or [],
        "estrato": est or [1,2,3,4,5,6],
        "edad": edad or [12,80],
        "with_internet": (net is not None and "with" in net)
    }


# ── Helper to apply filters ─────────────────────────────────────────────────
def _apply_filters(df: pd.DataFrame, F: dict) -> pd.DataFrame:
    out = df.copy()
    if F.get("year") is not None:
        out = out[out["year"] == F["year"]]
    if F.get("depto"):
        out = out[out["departamento"].isin(F["depto"])]
    if F.get("muni"):
        out = out[out["municipio"].isin(F["muni"])]
    if F.get("estrato"):
        out = out[out["estrato"].isin(F["estrato"])]
    lo, hi = F.get("edad", [12,80])
    out = out[(out["edad"] >= lo) & (out["edad"] <= hi)]
    if F.get("with_internet"):
        out = out[out["acceso_internet"] == 1]
    return out


# ── Overview KPIs and charts ────────────────────────────────────────────────
@callback(
    Output("kpi-pop", "children"),
    Output("kpi-idx", "children"),
    Output("kpi-coverage", "children"),
    Output("kpi-inet", "children"),
    Output("fig-idx-depto", "figure"),
    Output("fig-estrato", "figure"),
    Input("store-data", "data"),
    Input("store-filters", "data"),
)

def _overview(df_rec, F):
    import plotly.express as px
    import pandas as pd
    df = _apply_filters(pd.DataFrame(df_rec), F or {})
    if df.empty:
        return ("0", "—", "—", "—", px.scatter(), px.histogram())

    kpi_pop = f"{len(df):,}"
    kpi_idx = f"{df['idx_adopcion'].mean():.2f}"
    kpi_cov = f"{(df['idx_adopcion']>0.67).mean():.0%}"
    kpi_inet = f"{(df['acceso_internet'].mean()):.0%}"

    g1 = df.groupby("departamento")["idx_adopcion"].mean().reset_index().sort_values("idx_adopcion")
    fig1 = px.bar(g1.tail(15), x="idx_adopcion", y="departamento", orientation="h",
                  title="Top departments by adoption index")

    fig2 = px.box(df, x="estrato", y="idx_adopcion", points=False, title="Adoption by strata")

    return kpi_pop, kpi_idx, kpi_cov, kpi_inet, fig1, fig2


# ── Territorial ranking (placeholder for choropleth) ─────────────────────────
@callback(
    Output("table-ranking", "data"),
    Output("table-ranking", "columns"),
    Input("store-data", "data"),
    Input("store-filters", "data"),
)

def _territorial_table(df_rec, F):
    import pandas as pd
    df = _apply_filters(pd.DataFrame(df_rec), F or {})
    if df.empty:
        return [], [{"name": "municipio", "id": "municipio"}]

    ranking = (
        df.groupby(["departamento","municipio"], as_index=False)
          .agg(idx=("idx_adopcion","mean"), pobl=("municipio","size"))
          .sort_values(["idx","pobl"]).head(50)
    )
    columns=[{"name":"Depto","id":"departamento"},{"name":"Municipio","id":"municipio"},{"name":"Idx","id":"idx"},{"name":"Obs","id":"pobl"}]
    ranking["idx"] = (ranking["idx"].round(3))
    return ranking.to_dict("records"), columns


# ── Segments page callbacks ─────────────────────────────────────────────────
@callback(
    Output("fig-seg-scatter", "figure"),
    Output("fig-seg-bars", "figure"),
    Input("store-data", "data"),
    Input("store-filters", "data"),
)

def _segments(df_rec, F):
    import plotly.express as px
    import pandas as pd
    df = _apply_filters(pd.DataFrame(df_rec), F or {})
    if df.empty:
        return px.scatter(), px.bar()

    fig_sc = px.scatter(
        df.sample(min(1000, len(df))), x="edad", y="idx_adopcion", color="cluster",
        opacity=0.7, title="Population segments (synthetic clusters)",
        labels={"edad":"Age","idx_adopcion":"Adoption index"}
    )

    g = df.groupby(["cluster","estrato"], as_index=False).size()
    fig_bar = px.bar(g, x="estrato", y="size", color="cluster", barmode="group",
                     title="Segment size by strata")

    return fig_sc, fig_bar


# ── Scenarios (dummy what-if logic – replace with your models) ───────────────
@callback(
    Output("kpi-scn-idx", "children"),
    Output("kpi-scn-coverage", "children"),
    Input("scn-subsidy", "value"),
    Input("scn-training", "value"),
    Input("store-data", "data"),
    Input("store-filters", "data"),
)

def _scenarios(subsidy, training, df_rec, F):
    import pandas as pd
    df = _apply_filters(pd.DataFrame(df_rec), F or {})
    if df.empty:
        return "—", "—"

    # Very simple proxy for uplift: +a% per subsidy point and +b% per training hour
    uplift = (subsidy or 0) * 0.002 + (training or 0) * 0.001
    new_idx = (df["idx_adopcion"].mean() * (1 + uplift))
    cov = ((df["idx_adopcion"] * (1 + uplift)) > 0.67).mean()
    return f"{new_idx:.2f}", f"{cov:.0%}"
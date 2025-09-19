import numpy as np
import pandas as pd

DEPTOS = [
    "Amazonas","Antioquia","Arauca","Atlántico","Bogotá","Bolívar","Boyacá",
    "Caldas","Caquetá","Casanare","Cauca","Cesar","Chocó","Córdoba","Cundinamarca",
    "Guainía","Guaviare","Huila","La Guajira","Magdalena","Meta","Nariño","Norte de Santander",
    "Putumayo","Quindío","Risaralda","San Andrés","Santander","Sucre","Tolima","Valle del Cauca",
    "Vaupés","Vichada"
]

MUNICIPIOS = [f"Municipio {i}" for i in range(1, 101)]

def make_fake_data(n: int = 2000, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "year": rng.choice([2018, 2023], size=n, p=[0.45, 0.55]),
        "departamento": rng.choice(DEPTOS, size=n),
        "municipio": rng.choice(MUNICIPIOS, size=n),
        "estrato": rng.choice([1,2,3,4,5,6], size=n, p=[.22,.24,.22,.16,.1,.06]),
        "edad": rng.integers(12, 80, size=n),
        "genero": rng.choice(["Hombre","Mujer"], size=n),
        "escolaridad_anios": np.clip(rng.normal(9.5, 3.0, size=n), 0, 18).round(1),
        "acceso_internet": rng.choice([0,1], size=n, p=[.35,.65]),
        "dens_int": np.clip(rng.normal(50, 20, size=n), 1, 100),
    })
    base = (
        (df["estrato"] / 6) * 0.40 + (1 - (df["edad"] - 12) / (80 - 12)) * 0.20 + df["acceso_internet"] * 0.30 + (df["escolaridad_anios"]/18)*0.10
    )
    noise = rng.normal(0, 0.05, size=n)
    df["idx_adopcion"] = np.clip(base + noise, 0, 1)
    df["cluster"] = pd.cut(df["idx_adopcion"], bins=[-0.01, 0.33, 0.66, 1.0], labels=["Cluster 1","Cluster 2","Cluster 3"])
    return df
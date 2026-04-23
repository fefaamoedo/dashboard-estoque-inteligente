import pandas as pd


def classificar_status(cobertura_dias: float, lead_time_dias: float, estoque_atual: float, estoque_seguranca: float) -> str:
    if estoque_atual <= estoque_seguranca or cobertura_dias < lead_time_dias:
        return "Crítico"
    elif cobertura_dias <= (lead_time_dias + 10):
        return "Atenção"
    else:
        return "Saudável"


def calcular_metricas(estoque: pd.DataFrame, consumo: pd.DataFrame) -> pd.DataFrame:
    consumo_medio = (
        consumo.groupby(["material", "categoria"], as_index=False)["consumo_mensal"]
        .mean()
        .rename(columns={"consumo_mensal": "consumo_medio_mensal"})
    )

    df = estoque.merge(consumo_medio, on=["material", "categoria"], how="left")

    df["consumo_medio_diario"] = df["consumo_medio_mensal"] / 30
    df["cobertura_dias"] = df["estoque_atual"] / df["consumo_medio_diario"]
    df["necessidade_durante_lead_time"] = df["consumo_medio_diario"] * df["lead_time_dias"]
    df["saldo_apos_lead_time"] = df["estoque_atual"] + df["entrada_prevista"] - df["necessidade_durante_lead_time"]

    df["status"] = df.apply(
        lambda row: classificar_status(
            row["cobertura_dias"],
            row["lead_time_dias"],
            row["estoque_atual"],
            row["estoque_seguranca"]
        ),
        axis=1
    )

    mapa_prioridade = {"Crítico": 1, "Atenção": 2, "Saudável": 3}
    df["prioridade_ordem"] = df["status"].map(mapa_prioridade)

    df = df.sort_values(["prioridade_ordem", "cobertura_dias"], ascending=[True, True]).reset_index(drop=True)

    return df

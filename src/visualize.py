import os
import matplotlib.pyplot as plt
import pandas as pd


def gerar_dashboard_png(df: pd.DataFrame, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)

    criticos = (df["status"] == "Crítico").sum()
    atencao = (df["status"] == "Atenção").sum()
    saudaveis = (df["status"] == "Saudável").sum()
    cobertura_media = df["cobertura_dias"].mean()

    top = df.nsmallest(5, "cobertura_dias").copy()
    status_counts = df["status"].value_counts().reindex(
        ["Crítico", "Atenção", "Saudável"], fill_value=0
    )

    cores = {
        "Crítico": "#D32F2F",
        "Atenção": "#F9A825",
        "Saudável": "#2E7D32",
        "Azul": "#1565C0",
        "Texto": "#1F2937",
        "Subtexto": "#6B7280",
        "Borda": "#E5E7EB",
        "Fundo": "#FFFFFF",
        "FundoFigura": "#F8FAFC",
    }

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10
    })

    fig = plt.figure(figsize=(16, 9), facecolor=cores["FundoFigura"])
    gs = fig.add_gridspec(
        5, 12,
        height_ratios=[0.8, 1.2, 3.0, 2.7, 0.3],
        hspace=0.95,
        wspace=1.2
    )

    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis("off")
    ax_title.text(
        0.0, 0.72,
        "Dashboard Executivo de Estoque",
        fontsize=24,
        fontweight="bold",
        color=cores["Texto"]
    )
    ax_title.text(
        0.0, 0.20,
        "Análise de cobertura, criticidade e prioridade de materiais",
        fontsize=11,
        color=cores["Subtexto"]
    )

    def card(ax, titulo, valor, cor_valor):
        ax.set_facecolor(cores["Fundo"])
        ax.set_xticks([])
        ax.set_yticks([])

        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(cores["Borda"])
            spine.set_linewidth(1.0)

        ax.text(
            0.05, 0.72, titulo,
            fontsize=10,
            color=cores["Subtexto"],
            transform=ax.transAxes
        )
        ax.text(
            0.05, 0.18, str(valor),
            fontsize=22,
            fontweight="bold",
            color=cor_valor,
            transform=ax.transAxes
        )

    card(fig.add_subplot(gs[1, 0:3]), "Materiais Críticos", criticos, cores["Crítico"])
    card(fig.add_subplot(gs[1, 3:6]), "Materiais em Atenção", atencao, cores["Atenção"])
    card(fig.add_subplot(gs[1, 6:9]), "Materiais Saudáveis", saudaveis, cores["Saudável"])
    card(fig.add_subplot(gs[1, 9:12]), "Cobertura Média", f"{cobertura_media:.1f} dias", cores["Azul"])

   
    ax_bar = fig.add_subplot(gs[2, :8])
    ax_bar.set_facecolor(cores["Fundo"])

    for spine in ax_bar.spines.values():
        spine.set_visible(True)
        spine.set_color(cores["Borda"])
        spine.set_linewidth(1.0)

    bar_colors = [cores[s] for s in top["status"]]
    barras = ax_bar.barh(
        top["material"],
        top["cobertura_dias"],
        color=bar_colors,
        height=0.58
    )
    ax_bar.invert_yaxis()

    ax_bar.set_title(
        "Top 5 Materiais com Menor Cobertura",
        loc="left",
        fontsize=14,
        fontweight="bold",
        color=cores["Texto"],
        pad=15
    )
    ax_bar.set_xlabel("Cobertura em dias", fontsize=11, color=cores["Texto"])
    ax_bar.set_ylabel("")
    ax_bar.grid(axis="x", alpha=0.18, color="#CBD5E1")
    ax_bar.tick_params(axis="x", colors=cores["Texto"])
    ax_bar.tick_params(axis="y", colors=cores["Texto"])

    max_val = top["cobertura_dias"].max()
    ax_bar.set_xlim(0, max_val + 10)

    for barra, valor in zip(barras, top["cobertura_dias"]):
        ax_bar.text(
            barra.get_width() + 0.6,
            barra.get_y() + barra.get_height() / 2,
            f"{valor:.1f}",
            va="center",
            fontsize=10,
            color=cores["Texto"]
        )

    ax_donut = fig.add_subplot(gs[2, 8:12])
    ax_donut.set_facecolor(cores["Fundo"])

    for spine in ax_donut.spines.values():
        spine.set_visible(True)
        spine.set_color(cores["Borda"])
        spine.set_linewidth(1.0)

    valores = status_counts.values
    labels = status_counts.index.tolist()
    donut_colors = [cores[i] for i in labels]

    wedges, texts, autotexts = ax_donut.pie(
        valores,
        labels=None,
        autopct=lambda p: f"{p:.0f}%" if p > 0 else "",
        startangle=90,
        colors=donut_colors,
        wedgeprops={"width": 0.42, "edgecolor": "white"},
        textprops={"color": cores["Texto"], "fontsize": 10}
    )

    ax_donut.set_title(
        "Distribuição por Status",
        fontsize=14,
        fontweight="bold",
        color=cores["Texto"],
        pad=15
    )

    ax_donut.legend(
        wedges,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.10),
        ncol=3,
        frameon=False,
        fontsize=10
    )

    ax_table = fig.add_subplot(gs[3, :])
    ax_table.set_facecolor(cores["Fundo"])
    ax_table.axis("off")

    ax_table.text(
        0.0, 1.08,
        "Prioridades de Ação",
        fontsize=14,
        fontweight="bold",
        color=cores["Texto"],
        transform=ax_table.transAxes
    )

    resumo = df.nsmallest(5, "cobertura_dias")[[
        "material", "categoria", "cobertura_dias", "status"
    ]].copy()
    resumo["cobertura_dias"] = resumo["cobertura_dias"].round(1)

    tabela = ax_table.table(
        cellText=resumo.values,
        colLabels=["Material", "Categoria", "Cobertura (dias)", "Status"],
        cellLoc="center",
        loc="center",
        bbox=[0, 0.02, 1, 0.88]
    )
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(9.5)
    tabela.scale(1, 1.55)

    for (row, col), cell in tabela.get_celld().items():
        cell.set_edgecolor(cores["Borda"])
        if row == 0:
            cell.set_facecolor("#0F172A")
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor("white")
            if col == 3:  # coluna status
                status_val = resumo.iloc[row - 1, 3]
                if status_val == "Crítico":
                    cell.set_text_props(color=cores["Crítico"], weight="bold")
                elif status_val == "Atenção":
                    cell.set_text_props(color=cores["Atenção"], weight="bold")
                else:
                    cell.set_text_props(color=cores["Saudável"], weight="bold")

    ax_footer = fig.add_subplot(gs[4, :])
    ax_footer.axis("off")
    ax_footer.text(
        0.0, 0.5,
        "Projeto analítico de portfólio | Gestão de estoque | Python + Dados",
        fontsize=9,
        color=cores["Subtexto"]
    )

    caminho = os.path.join(output_dir, "dashboard_estoque.png")
    plt.savefig(caminho, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()

    return caminho

import os
from preprocess import carregar_bases
from metrics import calcular_metricas
from visualize import gerar_dashboard_png
from report import gerar_relatorio_pdf


def main():
    input_estoque = "../data/estoque_atual.csv"
    input_consumo = "../data/consumo_historico.csv"
    output_dir = "../outputs"

    os.makedirs(output_dir, exist_ok=True)

    estoque, consumo = carregar_bases(input_estoque, input_consumo)
    df = calcular_metricas(estoque, consumo)

    caminho_csv = os.path.join(output_dir, "analise_estoque.csv")
    df.to_csv(caminho_csv, index=False, encoding="utf-8-sig")

    caminho_png = gerar_dashboard_png(df, output_dir)
    caminho_pdf = gerar_relatorio_pdf(df, caminho_png, output_dir)

    print("Projeto executado com sucesso.")
    print(f"CSV gerado em: {caminho_csv}")
    print(f"PNG gerado em: {caminho_png}")
    print(f"PDF gerado em: {caminho_pdf}")


if __name__ == "__main__":
    main()

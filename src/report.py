import os
import pandas as pd
from fpdf import FPDF


class PDFExecutivo(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Pagina {self.page_no()}", align="C")


def desenhar_box(pdf, x, y, w, h, titulo, valor, cor_rgb):
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(220, 226, 232)
    pdf.rect(x, y, w, h, "DF")

    pdf.set_xy(x + 4, y + 5)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 5, titulo)

    pdf.set_xy(x + 4, y + 16)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*cor_rgb)
    pdf.cell(0, 8, str(valor))


def gerar_relatorio_pdf(df: pd.DataFrame, caminho_png: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)

    criticos = df[df["status"] == "Crítico"].copy()
    atencao = df[df["status"] == "Atenção"].copy()
    saudaveis = df[df["status"] == "Saudável"].copy()
    cobertura_media = df["cobertura_dias"].mean()

    top = df.nsmallest(5, "cobertura_dias")[
        ["material", "categoria", "cobertura_dias", "status"]
    ].copy()

    pdf = PDFExecutivo()
    pdf.set_auto_page_break(auto=True, margin=15)

    largura_texto = 180

  
    pdf.add_page()

    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 42, "F")

    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(12, 12)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 10, "Relatorio Executivo de Estoque")

    pdf.set_xy(12, 24)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "Analise de cobertura, criticidade e prioridade de materiais")

    pdf.set_text_color(31, 41, 55)
    pdf.set_xy(12, 52)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Resumo Executivo", new_x="LMARGIN", new_y="NEXT")

    pdf.set_xy(12, 62)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(55, 65, 81)
    pdf.multi_cell(
        largura_texto,
        7,
        "Este relatorio consolida indicadores simulados de estoque com base em consumo "
        "historico, lead time e estoque de seguranca, destacando materiais com maior "
        "sensibilidade operacional e necessidade de priorizacao."
    )

    desenhar_box(pdf, 12, 88, 42, 28, "Materiais Criticos", len(criticos), (198, 40, 40))
    desenhar_box(pdf, 58, 88, 42, 28, "Em Atencao", len(atencao), (249, 168, 37))
    desenhar_box(pdf, 104, 88, 42, 28, "Saudaveis", len(saudaveis), (46, 125, 50))
    desenhar_box(pdf, 150, 88, 48, 28, "Cobertura Media", f"{cobertura_media:.1f} d", (21, 101, 192))

    
    pdf.set_xy(12, 128)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 8, "Principais Achados", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(55, 65, 81)

    for _, row in top.head(3).iterrows():
        texto = (
            f"- {row['material']} apresenta cobertura de "
            f"{row['cobertura_dias']:.1f} dias e status {row['status']}."
        )
        pdf.multi_cell(largura_texto, 7, texto)
        pdf.ln(1)

    pdf.multi_cell(
        largura_texto,
        7,
        "A analise indica prioridade para materiais com menor cobertura e reforca "
        "a importancia do monitoramento preventivo para evitar cenarios de ruptura."
    )

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 8, "Recomendacoes de Acao", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(55, 65, 81)

    recomendacoes = [
        "Priorizar analise e tratamento dos materiais classificados como criticos.",
        "Revisar parametros de estoque de seguranca para itens sensiveis.",
        "Antecipar compras de materiais com baixa cobertura.",
        "Acompanhar periodicamente materiais em atencao."
    ]

    for rec in recomendacoes:
        pdf.multi_cell(largura_texto, 7, f"- {rec}")
        pdf.ln(1)

    pdf.add_page()

    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 24, "F")

    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(12, 7)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 8, "Painel Visual Consolidado")

    pdf.set_text_color(31, 41, 55)
    pdf.set_xy(12, 30)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "Visao resumida dos principais indicadores de estoque e criticidade.")

    pdf.image(caminho_png, x=10, y=42, w=190)

    pdf.add_page()

    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 24, "F")

    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(12, 7)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 8, "Leitura Analitica")

    pdf.set_text_color(31, 41, 55)
    pdf.set_xy(12, 32)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Materiais Prioritarios")

    pdf.set_xy(12, 42)
    pdf.set_font("Helvetica", "", 10)

    for _, row in top.iterrows():
        linha = (
            f"{row['material']} | {row['categoria']} | "
            f"Cobertura: {row['cobertura_dias']:.1f} dias | "
            f"Status: {row['status']}"
        )
        pdf.multi_cell(largura_texto, 6, linha)
        pdf.ln(1)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Interpretacao Executiva", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        largura_texto,
        7,
        "O cenario analisado demonstra que a combinacao entre cobertura, consumo e lead time "
        "permite identificar rapidamente materiais mais expostos. Essa abordagem fortalece a "
        "tomada de decisao em compras, reduz risco operacional e contribui para maior previsibilidade."
    )

    caminho_pdf = os.path.join(output_dir, "relatorio_estoque.pdf")
    pdf.output(caminho_pdf)

    return caminho_pdf

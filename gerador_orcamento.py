import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO
import os

# Configuração do Streamlit
st.set_page_config(page_title="Orçamento Resolve", page_icon="🧾")
st.title("🧾 Gerador de Orçamentos - Resolve Prestadora de Serviços")

def get_proximo_numero():
    arquivo_contador = "ultimo_orcamento.txt"
    if os.path.exists(arquivo_contador):
        with open(arquivo_contador, "r") as file:
            ultimo_numero = int(file.read())
    else:
        ultimo_numero = 0
    proximo_numero = ultimo_numero + 1
    with open(arquivo_contador, "w") as file:
        file.write(str(proximo_numero))
    return proximo_numero

# Inputs do usuário
cliente = st.text_input("Nome do cliente")
descricao = st.text_area("Descrição do serviço")
valor = st.text_input("Valor total (ex: 1500,00)")

if st.button("Gerar PDF do Orçamento"):
    if not cliente or not descricao or not valor:
        st.warning("Por favor, preencha todos os campos.")
    else:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        margin = 20 * mm
        numero_orcamento = get_proximo_numero()

        # --- CABEÇALHO --- #
        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(width / 2, height - margin, "Resolve Prestadora de Serviços")
        
        pdf.setFont("Helvetica", 12)
        pdf.drawCentredString(width / 2, height - margin - 15, "CNPJ: 52.823.975/0001-13")
        
        # Linha divisória
        pdf.setStrokeColor(colors.black)
        pdf.line(margin, height - margin - 25, width - margin, height - margin - 25)

        # --- NÚMERO DO ORÇAMENTO --- #
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(width / 2, height - margin - 50, f"ORÇAMENTO Nº {numero_orcamento}")
        
        # Linha divisória
        pdf.line(margin, height - margin - 60, width - margin, height - margin - 60)

        # --- CORPO --- #
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin, height - margin - 85, f"À {cliente}")
        
        pdf.drawString(margin, height - margin - 110, "Descrição dos Serviços:")
        pdf.setFont("Helvetica", 12)
        
        # Texto com quebra de linha
        linhas = [descricao[i:i+70] for i in range(0, len(descricao), 70)]
        y = height - margin - 130
        for linha in linhas:
            pdf.drawString(margin, y, linha)
            y -= 15

        # --- VALOR --- #
        pdf.drawString(margin, y - 30, f"Valor da mão de obra e material: R$ {valor}")

        # --- TOTAL --- #
        pdf.setFont("Helvetica-Bold", 14)
        pdf.setFillColor(colors.darkblue)  # Cor azul escuro
        pdf.drawString(margin, y - 60, "TOTAL:")
        pdf.drawString(margin + 60, y - 60, f"R$ {valor}")
        pdf.setFillColor(colors.black)  # Volta ao preto

        # Linha divisória
        pdf.line(margin, y - 75, width - margin, y - 75)

        # --- RODAPÉ --- #
        pdf.setFont("Helvetica", 10)
        pdf.drawString(margin, 20 * mm, f"{datetime.now().strftime('%d/%m/%Y %H:%M')}")
        pdf.drawString(margin, 10 * mm, "Resolve Prestadora de Serviços - Orçamento válido por 7 dias")

        pdf.save()
        buffer.seek(0)

        nome_arquivo = f"Orçamento_Resolve_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        st.success(f"✅ Orçamento Nº {numero_orcamento} gerado com sucesso!")
        st.download_button("📥 Baixar PDF", buffer, file_name=nome_arquivo, mime="application/pdf")

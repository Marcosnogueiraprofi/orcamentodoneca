import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from io import BytesIO
import os

# Configuração do Streamlit
st.set_page_config(page_title="Orçamento Resolve", page_icon="🧾")
st.title("🧾 Gerador de Orçamentos - Resolve Prestadora de Serviços")

# Função para pegar o próximo número sequencial
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
        numero_orcamento = get_proximo_numero()

        # --- CABEÇALHO ---
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, 750, "Resolve Prestadora de Serviços")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 730, "CNPJ: 52.823.975/0001-13")

        # --- TÍTULO DO ORÇAMENTO ---
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(300, 700, f"ORÇAMENTO Nº {numero_orcamento}")

        # --- CLIENTE ---
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, 650, f"À {cliente}")

        # --- DESCRIÇÃO ---
        pdf.drawString(50, 620, "Descrição dos Serviços")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 600, descricao)

        # --- VALOR ---
        pdf.drawString(50, 550, f"Valor da mão de obra e material: R$ {valor}")

        # --- TOTAL ---
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, 500, "TOTAL:")
        pdf.drawString(120, 500, f"R$ {valor}")

        pdf.save()
        buffer.seek(0)

        # Gera o nome do arquivo com data/hora
        nome_arquivo = f"Orçamento_Resolve_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        st.success(f"✅ Orçamento Nº {numero_orcamento} gerado com sucesso!")
        st.download_button(
            "📥 Baixar Orçamento PDF",
            buffer,
            file_name=nome_arquivo,
            mime="application/pdf"
        )

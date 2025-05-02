import streamlit as st
from io import BytesIO
from reportlab.pdfgen import canvas
from datetime import datetime

st.set_page_config(page_title="Orçamento Resolve", page_icon="🧾")
st.title("🧾 Gerador de Orçamentos - Resolve Prestadora de Serviços")

cliente = st.text_input("Nome do cliente")
descricao = st.text_area("Descrição do serviço")
valor = st.text_input("Valor total (ex: 1500,00)")

if st.button("Gerar PDF do Orçamento"):
    if not cliente or not descricao or not valor:
        st.warning("Por favor, preencha todos os campos.")
    else:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(150, 800, "Orçamento Resolve Prestadora de Serviço")

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, 750, f"R$ {valor}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 730, "TOTAL:")

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, 700, "Descrição dos Serviços")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 680, f"À {cliente}")
        pdf.drawString(50, 660, f"{descricao}")
        pdf.drawString(50, 620, f"Valor da mão de obra e material: R$ {valor}")

        pdf.drawString(50, 580, f"{datetime.now().strftime('%d/%m/%Y')}")
        pdf.drawString(50, 560, "Resolve Prestadora de Serviços")
        pdf.drawString(50, 540, "CNPJ: 52.823.975/0001-13")

        pdf.save()
        buffer.seek(0)

        st.success("✅ Orçamento gerado com sucesso!")
        st.download_button("📥 Baixar Orçamento PDF", buffer, file_name="orcamento.pdf", mime="application/pdf")

import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from datetime import datetime
from io import BytesIO
import os

def gerar_pdf(cliente, responsavel, endereco, descricao, valor, observacoes):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 20*mm
    
    # Cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-margin, f"ORÇAMENTO Nº {get_proximo_numero()}")
    
    # Corpo
    c.setFont("Helvetica", 12)
    text = c.beginText(margin, height-margin-25)
    text.textLine(f"À {cliente}")
    text.textLine(f"A/C {responsavel}")
    text.textLine(f"Imóvel: {endereco}")
    text.textLine(" ")
    text.textLine("Descrição dos Serviços:")
    for linha in descricao.split('\n'):
        text.textLine(linha)
    text.textLine(" ")
    text.textLine(f"Valor da mão de obra e material = R$ {valor}")
    if observacoes:
        text.textLine(f"Obs: {observacoes}")
    c.drawText(text)
    
    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, 100, "TOTAL:")
    c.drawString(margin+100, 100, f"R${valor}")
    
    # Rodapé
    c.setFont("Helvetica", 8)
    c.drawString(margin, 20, "Resolve Prestadora de Serviços | CNPJ: 52.823.975/0001-13")
    
    c.save()
    buffer.seek(0)
    return buffer

# Interface
cliente = st.text_input("Cliente")
responsavel = st.text_input("A/C")
endereco = st.text_input("Imóvel")
descricao = st.text_area("Descrição")
valor = st.text_input("Valor")
observacoes = st.text_input("Observações")

if st.button("Gerar PDF"):
    pdf_buffer = gerar_pdf(cliente, responsavel, endereco, descricao, valor, observacoes)
    st.download_button(
        "Baixar PDF",
        data=pdf_buffer,
        file_name=f"orcamento_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )

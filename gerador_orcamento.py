import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO
import os

# [...] (Parte do Streamlit igual anteriormente)

if st.button("Gerar PDF do Orçamento"):
    if not cliente or not descricao or not valor:
        st.warning("Preencha todos os campos!")
    else:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # --- CONFIG GLOBAL ---
        margin = 20*mm
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        
        # --- CABEÇALHO ---
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height-margin, "RESOLVE PRESTADORA DE SERVIÇOS")
        c.setFont("Helvetica", 10)
        c.drawCentredString(width/2, height-margin-8, "CNPJ: 52.823.975/0001-13")
        
        # Linha divisória
        c.line(margin, height-margin-15, width-margin, height-margin-15)
        
        # --- NÚMERO ORÇAMENTO ---
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width/2, height-margin-30, f"ORÇAMENTO Nº {get_proximo_numero()}")
        
        # --- CLIENTE ---
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, height-margin-50, f"Cliente: {cliente}")
        
        # --- SERVIÇOS ---
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, height-margin-70, "DESCRIÇÃO DOS SERVIÇOS:")
        c.setFont("Helvetica", 11)
        text = c.beginText(margin, height-margin-85)
        text.setFont("Helvetica", 11)
        for line in descricao.split('\n'):
            text.textLine(line)
        c.drawText(text)
        
        # --- VALOR ---
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(width-margin, height-margin-120, f"Valor: R$ {valor}")
        
        # --- TOTAL ---
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkblue)
        c.drawRightString(width-margin, height-margin-140, f"TOTAL: R$ {valor}")
        c.setFillColor(colors.black)
        
        # --- RODAPÉ ---
        c.line(margin, 25*mm, width-margin, 25*mm)
        c.setFont("Helvetica", 8)
        c.drawString(margin, 20*mm, f"Emitido em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        c.drawString(margin, 15*mm, "Resolve Prestadora de Serviços | Orçamento válido por 7 dias")
        
        c.save()
        buffer.seek(0)
        # [...] (Parte do download igual)

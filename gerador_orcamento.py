import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
import os

def criar_pdf(cliente, responsavel, endereco, descricao, valor, obs):
    # Criar buffer e PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # --- CONTEÚDO DO PDF (igual ao seu modelo) ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30*mm, 280*mm, f"ORÇAMENTO Nº 201")  # Número fixo para teste
    
    c.setFont("Helvetica", 12)
    c.drawString(30*mm, 270*mm, f"À {cliente}")
    c.drawString(30*mm, 260*mm, f"A/C {responsavel}")
    c.drawString(30*mm, 250*mm, f"Imóvel: {endereco}")
    
    # ... (adicione o resto do conteúdo conforme seu modelo exato)

    # --- FECHAMENTO CORRETO ---
    c.showPage()
    c.save()
    
    # Pré-carregar os bytes antes de fechar
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

# Interface
cliente = st.text_input("Cliente")
responsavel = st.text_input("A/C")
endereco = st.text_input("Imóvel")
descricao = st.text_area("Descrição")
valor = st.text_input("Valor")
obs = st.text_input("Obs")

if st.button("Gerar PDF"):
    pdf_bytes = criar_pdf(cliente, responsavel, endereco, descricao, valor, obs)
    
    # Download com os bytes pré-carregados
    st.download_button(
        label="⬇️ Baixar Orçamento",
        data=pdf_bytes,
        file_name="ORÇAMENTO_RESOLVE.pdf",
        mime="application/pdf"
    )

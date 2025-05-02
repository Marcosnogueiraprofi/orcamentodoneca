import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import base64

def create_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # --- CONTEÚDO DO PDF (modelo profissional) ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "ORÇAMENTO Nº 201")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 780, "À Casarão Imóveis")
    c.drawString(50, 760, "A/C Sérgio Antônio")
    c.drawString(50, 740, "Imóvel: General Neto nº 446 - Rio Grande/RS")
    
    c.drawString(50, 700, "Descrição dos Serviços")
    c.drawString(50, 680, "Pintura geral interna e externa.")
    
    # ... (complete com o resto do conteúdo)
    
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

# Interface
st.title("Gerador de Orçamentos")

if st.button("Gerar PDF"):
    pdf_bytes = create_pdf()
    
    # Codificação direta para download
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="ORÇAMENTO_RESOLVE.pdf">Clique para baixar</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.success("PDF gerado com sucesso!")

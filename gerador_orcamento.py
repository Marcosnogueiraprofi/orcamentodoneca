import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY
from io import BytesIO
import os

def get_proximo_numero():
    if not os.path.exists("contador_orcamentos.txt"):
        with open("contador_orcamentos.txt", "w") as f:
            f.write("200")
    with open("contador_orcamentos.txt", "r+") as f:
        num = int(f.read())
        f.seek(0)
        f.write(str(num + 1))
    return num + 1

def criar_pdf_identico(cliente, responsavel, endereco, descricao, valor, obs):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Margens exatas do seu documento
    left_margin = 25 * mm
    top_margin = height - 25 * mm
    
    # Fonte e estilo idênticos
    styles = getSampleStyleSheet()
    estilo_corpo = styles["BodyText"]
    estilo_corpo.fontName = "Helvetica"
    estilo_corpo.fontSize = 11
    estilo_corpo.leading = 13
    estilo_corpo.alignment = TA_JUSTIFY
    
    # --- CABEÇALHO IDÊNTICO ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, top_margin, f"ORÇAMENTO Nº {get_proximo_numero()}")
    
    # --- INFORMAÇÕES DO CLIENTE ---
    c.setFont("Helvetica", 11)
    c.drawString(left_margin, top_margin - 20, f"À {cliente}")
    c.drawString(left_margin, top_margin - 35, f"A/C {responsavel}")
    c.drawString(left_margin, top_margin - 50, f"Imóvel: {endereco}")
    
    # --- DESCRIÇÃO DOS SERVIÇOS ---
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_margin, top_margin - 70, "Descrição dos Serviços")
    
    c.setFont("Helvetica", 11)
    y_position = top_margin - 85
    for linha in descricao.split(';'):
        if linha.strip():
            p = Paragraph(linha.strip().replace('\n', '<br/>'), estilo_corpo)
            p.wrapOn(c, width - 2*left_margin, height)
            p.drawOn(c, left_margin, y_position - p.height)
            y_position -= p.height + 5
    
    # --- VALOR E OBSERVAÇÕES ---
    c.setFont("Helvetica", 11)
    c.drawString(left_margin, y_position - 30, f"Valor da mão de obra e material = R$ {valor}")
    
    if obs:
        c.drawString(left_margin, y_position - 45, f"Obs: {obs}")
    
    # --- TOTAL ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y_position - 75, "TOTAL:")
    c.drawString(left_margin + 100, y_position - 75, f"R${valor}")
    
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

# Interface Streamlit
st.set_page_config(page_title="Gerador de Orçamentos", layout="centered")

with st.form("form_orcamento"):
    st.title("Gerador de Orçamentos Profissional")
    
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Cliente")
    with col2:
        responsavel = st.text_input("A/C")
    
    endereco = st.text_input("Imóvel")
    descricao = st.text_area("Descrição dos Serviços", height=200,
                           help="Separe cada item com ponto e vírgula (;)")
    
    col3, col4 = st.columns(2)
    with col3:
        valor = st.text_input("Valor Total (R$)")
    with col4:
        obs = st.text_input("Observações")
    
    if st.form_submit_button("Gerar PDF"):
        if not cliente or not descricao or not valor:
            st.warning("Preencha os campos obrigatórios!")
        else:
            pdf_bytes = criar_pdf_identico(cliente, responsavel, endereco, 
                                         descricao, valor, obs)
            
            st.success("Orçamento gerado com sucesso!")
            st.download_button(
                label="⬇️ Baixar Orçamento",
                data=pdf_bytes,
                file_name=f"Orcamento_Resolve_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )

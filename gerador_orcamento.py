import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO
import os

def get_proximo_numero():
    arquivo_contador = "ultimo_orcamento.txt"
    if os.path.exists(arquivo_contador):
        with open(arquivo_contador, "r") as file:
            ultimo_numero = int(file.read())
    else:
        ultimo_numero = 200  # Começando do 201 como no exemplo
    proximo_numero = ultimo_numero + 1
    with open(arquivo_contador, "w") as file:
        file.write(str(proximo_numero))
    return proximo_numero

# Interface Streamlit
st.set_page_config(page_title="Orçamento Resolve", page_icon="🧾")
st.title("🧾 Gerador de Orçamentos Profissional")

with st.form("form_orcamento"):
    cliente = st.text_input("Cliente")
    responsavel = st.text_input("A/C")
    endereco = st.text_input("Imóvel")
    descricao = st.text_area("Descrição dos Serviços")
    valor = st.text_input("Valor Total (ex: 26.000,00)")
    observacoes = st.text_input("Observações")
    
    if st.form_submit_button("Gerar PDF"):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin = 20*mm
        
        # Configurações
        c.setTitle(f"Orçamento Resolve - {datetime.now().strftime('%Y%m%d')}")
        
        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height-margin, "ORÇAMENTO Nº {}".format(get_proximo_numero()))
        
        # Informações do Cliente
        c.setFont("Helvetica", 12)
        c.drawString(margin, height-margin-20, f"À {cliente}")
        c.drawString(margin, height-margin-35, f"A/C {responsavel}")
        c.drawString(margin, height-margin-50, f"Imóvel: {endereco}")
        
        # Divisória
        c.line(margin, height-margin-60, width-margin, height-margin-60)
        
        # Descrição dos Serviços
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, height-margin-80, "Descrição dos Serviços")
        c.setFont("Helvetica", 11)
        
        text = c.beginText(margin, height-margin-95)
        text.setFont("Helvetica", 11)
        for line in descricao.split('\n'):
            text.textLine(line)
        c.drawText(text)
        
        # Valor
        c.setFont("Helvetica", 11)
        c.drawString(margin, height-margin-200, f"Valor da mão de obra e material = R$ {valor}")
        
        # Observações
        if observacoes:
            c.drawString(margin, height-margin-215, f"Obs: {observacoes}")
        
        # Total
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, height-margin-240, "TOTAL:")
        c.drawString(margin+100, height-margin-240, f"R${valor}")
        
        # Rodapé
        c.setFont("Helvetica", 8)
        c.drawString(margin, 15*mm, "Resolve Prestadora de Serviços | CNPJ: 52.823.975/0001-13")
        
        c.save()
        buffer.seek(0)
        
        st.success("Orçamento gerado com sucesso!")
        st.download_button(
            "📥 Baixar Orçamento",
            buffer,
            file_name=f"Orçamento_Resolve_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

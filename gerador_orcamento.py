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
        ultimo_numero = 200
    proximo_numero = ultimo_numero + 1
    with open(arquivo_contador, "w") as file:
        file.write(str(proximo_numero))
    return proximo_numero

# Configuração do Streamlit
st.set_page_config(page_title="Orçamento Resolve", page_icon="🧾")
st.title("🧾 Gerador de Orçamentos Profissional")

# Formulário
with st.form("form_orcamento"):
    cliente = st.text_input("Cliente")
    responsavel = st.text_input("A/C")
    endereco = st.text_input("Imóvel")
    descricao = st.text_area("Descrição dos Serviços", height=200)
    valor = st.text_input("Valor Total (ex: 26.000,00)")
    observacoes = st.text_input("Observações")
    
    if st.form_submit_button("Gerar PDF"):
        if not cliente or not descricao or not valor:
            st.warning("Preencha os campos obrigatórios!")
        else:
            try:
                # Criar PDF
                buffer = BytesIO()
                c = canvas.Canvas(buffer, pagesize=A4)
                width, height = A4
                margin = 20*mm

                # --- CABEÇALHO ---
                c.setFont("Helvetica-Bold", 16)
                c.drawCentredString(width/2, height-margin, f"ORÇAMENTO Nº {get_proximo_numero()}")
                
                # --- INFOS CLIENTE ---
                c.setFont("Helvetica", 12)
                c.drawString(margin, height-margin-25, f"À {cliente}")
                c.drawString(margin, height-margin-40, f"A/C {responsavel}")
                c.drawString(margin, height-margin-55, f"Imóvel: {endereco}")
                
                # --- SERVIÇOS ---
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, height-margin-80, "Descrição dos Serviços:")
                c.setFont("Helvetica", 11)
                y = height-margin-95
                for linha in descricao.split('\n'):
                    c.drawString(margin, y, linha)
                    y -= 15
                
                # --- VALOR ---
                c.setFont("Helvetica", 11)
                c.drawString(margin, y-30, f"Valor da mão de obra e material = R$ {valor}")
                
                # --- OBSERVAÇÕES ---
                if observacoes:
                    c.drawString(margin, y-45, f"Obs: {observacoes}")
                
                # --- TOTAL ---
                c.setFont("Helvetica-Bold", 14)
                c.drawString(margin, y-75, "TOTAL:")
                c.drawString(margin+100, y-75, f"R${valor}")
                
                # --- RODAPÉ ---
                c.setFont("Helvetica", 8)
                c.drawString(margin, 15*mm, "Resolve Prestadora de Serviços | CNPJ: 52.823.975/0001-13")
                
                # Finalizar PDF
                c.save()
                
                # Preparar download
                buffer.seek(0)
                pdf_bytes = buffer.read()
                
                st.success("Orçamento gerado com sucesso!")
                st.download_button(
                    label="📥 Baixar Orçamento",
                    data=pdf_bytes,
                    file_name=f"Orçamento_Resolve_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {str(e)}")

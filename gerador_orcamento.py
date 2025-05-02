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

cliente = st.text_input("Cliente")
responsavel = st.text_input("A/C")
endereco = st.text_input("Imóvel")
descricao = st.text_area("Descrição dos Serviços")
valor = st.text_input("Valor Total (ex: 26.000,00)")
observacoes = st.text_input("Observações")

if st.button("Gerar PDF"):
    if not cliente or not descricao or not valor:
        st.warning("Preencha todos os campos obrigatórios!")
    else:
        try:
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            
            # [...] (Todo o código de geração de PDF que te enviei anteriormente)
            
            c.save()
            
            # Correção crucial: Resetar o buffer antes do download
            buffer.seek(0)
            pdf_bytes = buffer.getvalue()
            
            st.success("✅ Orçamento gerado com sucesso!")
            
            # Botão de download corrigido
            st.download_button(
                label="📥 Baixar Orçamento",
                data=pdf_bytes,
                file_name=f"Orçamento_Resolve_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {str(e)}")

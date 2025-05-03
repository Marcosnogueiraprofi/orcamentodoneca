import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

# Configuração da página Streamlit
st.set_page_config(page_title="Gerador de Orçamentos", page_icon="📄")

# CSS personalizado para replicar o estilo do PDF
custom_css = """
<style>
    .orcamento-container {
        font-family: Arial, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ddd;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    .title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .numero-orcamento {
        font-size: 18px;
        margin-bottom: 20px;
    }
    .cliente-info {
        margin-bottom: 30px;
    }
    .cliente-info p {
        margin: 5px 0;
    }
    .servicos-title {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }
    .servicos-list {
        margin-bottom: 30px;
    }
    .servicos-list p {
        margin: 5px 0;
        text-align: justify;
    }
    .valor-total {
        font-weight: bold;
        margin-top: 20px;
        text-align: right;
    }
    .obs {
        margin-top: 10px;
        font-style: italic;
    }
    .total {
        font-size: 20px;
        font-weight: bold;
        text-align: right;
        margin-top: 20px;
        border-top: 1px solid #000;
        padding-top: 10px;
    }
    .form-group {
        margin-bottom: 15px;
    }
    .form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .form-group input, .form-group textarea {
        width: 100%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    .generate-btn {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
    }
    .generate-btn:hover {
        background-color: #45a049;
    }
</style>
"""

# Classe PDF personalizada
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'ORÇAMENTO', 0, 1, 'C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# Função para criar PDF
def create_pdf(data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Número do orçamento
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"ORÇAMENTO Nº {data['numero_orcamento']}", 0, 1)
    pdf.ln(5)
    
    # Informações do cliente
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 7, f"À {data['cliente']}", 0, 1)
    pdf.cell(0, 7, f"A/C {data['responsavel']}", 0, 1)
    pdf.cell(0, 7, f"Imóvel: {data['endereco_imovel']}", 0, 1)
    pdf.ln(10)
    
    # Descrição dos serviços
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 7, "Descrição dos Serviços", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    # Adiciona cada linha do texto como uma multicell
    servicos_lines = data['descricao_servicos'].split('\n')
    for line in servicos_lines:
        pdf.multi_cell(0, 7, line)
        pdf.ln(2)
    
    pdf.ln(10)
    
    # Valor total
    pdf.cell(0, 7, f"Valor da mão de obra e material = R$ {data['valor_total']:.2f}", 0, 1)
    pdf.ln(5)
    
    # Observação
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 7, f"Obs: {data['observacoes']}", 0, 1)
    pdf.ln(10)
    
    # Total
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 7, "TOTAL:", 0, 1, 'R')
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"R${data['valor_total']:.2f}", 0, 1, 'R')
    
    return pdf

# Função para criar link de download
def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">Download do Orçamento</a>'

# Interface Streamlit
def main():
    st.markdown(custom_css, unsafe_allow_html=True)
    
    st.title("Gerador de Orçamentos")
    st.subheader("Pronto Neca, faça teus orçamentos!")
    
    with st.form("orcamento_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            numero_orcamento = st.text_input("Número do Orçamento", "201")
            cliente = st.text_input("Cliente", "Casarão Imóveis")
            responsavel = st.text_input("Responsável (A/C)", "Sérgio Antônio")
        
        with col2:
            endereco_imovel = st.text_input("Endereço do Imóvel", "General Neto nº 446 - Rio Grande/RS")
            valor_total = st.number_input("Valor Total (R$)", min_value=0.0, value=26000.0, step=100.0)
        
        descricao_servicos = st.text_area("Descrição dos Serviços", """Pintura geral interna e externa.

Externo: lavagem das paredes, reparos na alvenaria, pintura com uma mão de fundo preparador e duas de mão com tinta acrílica emborrachada.
Lixamento e pintura das grades com aplicação de duas de mão de esmalte sintético;
Fachada: Limpeza e reparos na alvenaria e pintura com uma de mão de fundo preparador e duas de mão de tinta acrílica;
Lixamento e pintura dos suportes dos ares condicionados;
Limpeza e lavagem do pátio;

Interno: lavagem das paredes, reparos na alvenaria, gesso e aplicação de uma de mão de fundo preparador e duas de mão de tinta acrílica semibrilho;
Lavagem, lixamento e pintura das portas, com esmalte sintético fosco;
Troca da porta que dá acesso ao pátio;""", height=300)
        
        observacoes = st.text_input("Observações", "Material incluso.")
        
        submitted = st.form_submit_button("Gerar Orçamento")
        
        if submitted:
            data = {
                "numero_orcamento": numero_orcamento,
                "cliente": cliente,
                "responsavel": responsavel,
                "endereco_imovel": endereco_imovel,
                "descricao_servicos": descricao_servicos,
                "valor_total": valor_total,
                "observacoes": observacoes
            }
            
            pdf = create_pdf(data)
            
            # Salva o PDF em bytes
            pdf_bytes = pdf.output(dest='S').encode('latin1')
            
            # Cria o link de download
            st.markdown(create_download_link(pdf_bytes, f"Orçamento_{numero_orcamento}.pdf"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()

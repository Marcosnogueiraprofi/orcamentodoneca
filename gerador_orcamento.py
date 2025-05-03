import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import inch
import io
import base64

# Configuração da página
st.set_page_config(
    page_title="Gerador de Orçamentos - Resolve",
    page_icon="📄",
    layout="centered"
)

# Título do aplicativo
st.title("📄 Gerador de Orçamentos - Resolve")
st.subheader("Pronto Neca, faça teus orçamentos!")

# Formulário para entrada de dados
with st.form("orcamento_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        numero_orcamento = st.text_input("Número do Orçamento*", value="201")
        cliente = st.text_input("Cliente*", value="Casarão Imóveis")
        responsavel = st.text_input("Responsável (A/C)*", value="Sérgio Antônio")
    
    with col2:
        endereco_imovel = st.text_input("Endereço do Imóvel*", value="General Neto nº 446 - Rio Grande/RS")
        valor_total = st.number_input("Valor Total (R$)*", min_value=0.0, value=26000.0, step=100.0)
    
    descricao_servicos = st.text_area(
        "Descrição dos Serviços*",
        value="""Pintura geral interna e externa.

Externo: lavagem das paredes, reparos na alvenaria, pintura com uma mão de fundo preparador e duas de mão com tinta acrílica emborrachada.
Lixamento e pintura das grades com aplicação de duas de mão de esmalte sintético;
Fachada: Limpeza e reparos na alvenaria e pintura com uma de mão de fundo preparador e duas de mão de tinta acrílica;
Lixamento e pintura dos suportes dos ares condicionados;
Limpeza e lavagem do pátio;

Interno: lavagem das paredes, reparos na alvenaria, gesso e aplicação de uma de mão de fundo preparador e duas de mão de tinta acrílica semibrilho;
Lavagem, lixamento e pintura das portas, com esmalte sintético fosco;
Troca da porta que dá acesso ao pátio;""",
        height=300
    )
    
    observacoes = st.text_input("Observações", value="Material incluso.")
    
    submitted = st.form_submit_button("Gerar Orçamento em PDF")

# Função para criar o PDF com ReportLab
def create_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  # 0=Left, 1=Center, 2=Right
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6
    )
    
    normal_style = styles['Normal']
    bold_style = styles['Heading3']
    italic_style = ParagraphStyle(
        'Italic',
        parent=styles['Italic'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Cabeçalho
    p = Paragraph("ORÇAMENTO", title_style)
    p.wrapOn(c, width, height)
    p.drawOn(c, 0, height - 1*inch)
    
    # Número do orçamento
    p = Paragraph(f"<b>ORÇAMENTO Nº {data['numero_orcamento']}</b>", subtitle_style)
    p.wrapOn(c, width, height)
    p.drawOn(c, 0.5*inch, height - 1.5*inch)
    
    # Informações do cliente
    y_position = height - 2*inch
    c.setFont("Helvetica", 12)
    c.drawString(0.5*inch, y_position, f"À {data['cliente']}")
    y_position -= 0.25*inch
    c.drawString(0.5*inch, y_position, f"A/C {data['responsavel']}")
    y_position -= 0.25*inch
    c.drawString(0.5*inch, y_position, f"Imóvel: {data['endereco_imovel']}")
    y_position -= 0.5*inch
    
    # Descrição dos serviços
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.5*inch, y_position, "Descrição dos Serviços")
    y_position -= 0.25*inch
    
    c.setFont("Helvetica", 12)
    text_lines = data['descricao_servicos'].split('\n')
    for line in text_lines:
        if line.strip() == "":
            y_position -= 0.25*inch
            continue
        c.drawString(0.5*inch, y_position, line)
        y_position -= 0.25*inch
    
    y_position -= 0.5*inch
    
    # Valor total
    valor_formatado = f"{data['valor_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    c.drawString(0.5*inch, y_position, f"Valor da mão de obra e material = R$ {valor_formatado}")
    y_position -= 0.5*inch
    
    # Observação
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(0.5*inch, y_position, f"Obs: {data['observacoes']}")
    y_position -= 0.75*inch
    
    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(width - 0.5*inch, y_position, "TOTAL:")
    y_position -= 0.25*inch
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(width - 0.5*inch, y_position, f"R${valor_formatado}")
    
    c.save()
    buffer.seek(0)
    return buffer

# Processar o formulário quando enviado
if submitted:
    if not all([numero_orcamento, cliente, responsavel, endereco_imovel, descricao_servicos]):
        st.error("Por favor, preencha todos os campos obrigatórios (*)")
    else:
        data = {
            "numero_orcamento": numero_orcamento,
            "cliente": cliente,
            "responsavel": responsavel,
            "endereco_imovel": endereco_imovel,
            "descricao_servicos": descricao_servicos,
            "valor_total": valor_total,
            "observacoes": observacoes
        }
        
        pdf_buffer = create_pdf(data)
        
        st.success("Orçamento gerado com sucesso!")
        
        # Botão de download
        st.download_button(
            label="📥 Baixar Orçamento em PDF",
            data=pdf_buffer,
            file_name=f"Orcamento_Resolve_{numero_orcamento}.pdf",
            mime="application/pdf"
        )
        
        # Pré-visualização (opcional)
        with st.expander("Visualizar dados do orçamento"):
            st.write(f"**ORÇAMENTO Nº {numero_orcamento}**")
            st.write(f"**Cliente:** {cliente}")
            st.write(f"**Responsável:** {responsavel}")
            st.write(f"**Imóvel:** {endereco_imovel}")
            st.write("---")
            st.write("**Descrição dos Serviços:**")
            st.write(descricao_servicos)
            st.write("---")
            st.write(f"**Valor Total:** R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.write(f"*Obs: {observacoes}*")

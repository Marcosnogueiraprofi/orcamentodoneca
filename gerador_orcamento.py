import streamlit as st
# Removidos imports de TTFont e pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable # Importar componentes para layout
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle # Para estilos de texto
from reportlab.lib.units import mm # Para usar milímetros nas medidas
from reportlab.lib.colors import HexColor, black, blue # Para cores
from reportlab.lib.pagesizes import A4 # Para o tamanho da página A4 (CORRIGIDO: Importado novamente)
from io import BytesIO
from datetime import date # Para usar a data
# Removido import de pdfmetrics e ttfonts


# --- INICIALIZAÇÃO DO ESTADO DE SESSÃO ---
# Inicializa o número do orçamento, a data e as informações de contato
if 'numero_orcamento' not in st.session_state:
    st.session_state['numero_orcamento'] = 201 # Começa com o número que você quiser
if 'data_orcamento' not in st.session_state:
     st.session_state['data_orcamento'] = date.today() # Data inicial
# Inicializa campos de contato no estado de sessão para persistir
if 'contato_telefone' not in st.session_state:
     st.session_state['contato_telefone'] = "(XX) XXXX-XXXX" # Exemplo
if 'contato_email' not in st.session_state:
     st.session_state['contato_email'] = "contato@resolvevistorias.com.br" # Exemplo
if 'contato_site' not in st.session_state:
     st.session_state['contato_site'] = "www.resolvevistorias.com.br" # Exemplo


# --- CÓDIGO CSS PARA LAYOUT AZUL E BRANCO ELEGANTE NO STREAMLIT ---
# Este bloco injeta CSS na página do Streamlit para estilizar a interface
# Mantenha este bloco igual ao que funcionou para você
st.markdown("""
<style>
/* Estilo para o corpo principal da página */
.main {
    background-color: #FFFFFF; /* Fundo branco puro */
    color: #333; /* Cor de texto padrão suave */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Fonte mais elegante */
    padding: 30px; /* Um pouco mais de espaço */
}

/* Estilo para o cabeçalho/título principal do Streamlit */
.stApp > header {
    background-color: #1A237E; /* Azul escuro mais profundo para o cabeçalho do Streamlit */
    padding: 10px;
    color: white; /* Texto branco no cabeçalho */
}

/* Estilo para os títulos dentro do conteúdo (se usar st.title ou st.header) */
h1, h2, h3, h4, h5, h6 {
    color: #1A237E; /* Azul escuro para títulos */
    font-weight: bold;
}

/* Estilo para os rótulos dos inputs de texto e text area */
div[data-testid="textInputRootStyles"] label,
div[data-testid="stTextarea"] label,
div[data-testid="stDateInput"] label {
    font-weight: bold;
    color: #1A237E; /* Azul escuro para os rótulos */
}

/* Estilo para os campos de input de texto, text area e input de data */
div[data-testid="textInputRootStyles"] input,
div[data-testid="stTextarea"] textarea,
div[data-testid="stDateInput"] input {
    background-color: #F5F5F5; /* Cinza bem claro para os campos */
    border: 1px solid #CFD8DC; /* Borda suave */
    border-radius: 5px;
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
}

/* Estilo para os campos quando estão focados */
div[data-testid="textInputRootStyles"] input:focus,
div[data-testid="stTextarea"] textarea:focus,
div[data-testid="stDateInput"] input:focus {
    border-color: #42A5F5; /* Azul claro vibrante ao focar */
    box-shadow: 0 0 0 0.2rem rgba(66, 165, 245, 0.25); /* Sombra suave ao focar */
    outline: none;
}

/* Estilo para o botão */
.stButton button {
    background-color: #42A5F5; /* Azul claro vibrante */
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.stButton button:hover {
    background-color: #2196F3; /* Azul um pouco mais escuro ao passar o mouse */
}

/* Adicione mais estilos conforme necessário */

</style>
""", unsafe_allow_html=True)
# --- FIM DO CÓDIGO CSS ---


# --- FUNÇÃO PARA CRIAR O PDF COM LAYOUT SOFISTICADO (FLOWABLES, FONTES PADRÃO) ---
def criar_pdf_sofisticado(numero, data, cliente, responsavel, endereco, descricao, valor, obs, contato_telefone, contato_email, contato_site):
    buffer = BytesIO()
    # SimpleDocTemplate para gerenciamento do documento, com margens para header/footer
    doc = SimpleDocTemplate(buffer,
                            pagesize=A4,
                            leftMargin=25*mm, # Margens um pouco maiores
                            rightMargin=25*mm,
                            topMargin=40*mm, # Espaço maior para o cabeçalho fixo
                            bottomMargin=35*mm) # Espaço maior para o rodapé fixo


    Story = [] # Lista para armazenar os elementos (Flowables) do corpo principal do PDF


    # --- Definindo Estilos de Parágrafo para o PDF (usando fontes padrão Helvetica) ---
    estilos = getSampleStyleSheet() # Pega estilos de exemplo para base

    # Definindo cores
    AZUL_ESCURO_PDF = HexColor('#1A237E') # Deep Indigo
    AZUL_PRIMARIO_PDF = HexColor('#42A5F5') # Azul claro vibrante
    COR_TEXTO_NORMAL = HexColor('#333333') # Cinza escuro para texto geral
    COR_RODAPE = HexColor('#555555') # Cinza médio para rodapé
    CINZA_LINHA_PDF = HexColor('#CFD8DC') # Cinza suave para linhas


    # Estilos personalizados usando fontes padrão ReportLab
    estilos.add(ParagraphStyle(name='Heading1PDF', # Título de seção principal
                               fontName='Helvetica-Bold', # Fonte padrão negrito
                               fontSize=16,
                               leading=18, # Espaçamento entre linhas
                               spaceBefore=12,
                               spaceAfter=6,
                               textColor=AZUL_ESCURO_PDF,
                               alignment=0)) # Alinhado à esquerda

    estilos.add(ParagraphStyle(name='RotuloDadosPDF', # Rótulos nos dados do cliente/imóvel
                               fontName='Helvetica-Bold', # Fonte padrão negrito
                               fontSize=11,
                               leading=13,
                               textColor=AZUL_PRIMARIO_PDF)) # Rótulo em azul primário

    estilos.add(ParagraphStyle(name='ValorDadosPDF', # Valores nos dados do cliente/imóvel
                               fontName='Helvetica', # Fonte padrão normal
                               fontSize=11,
                               leading=13,
                               textColor=COR_TEXTO_NORMAL))

     # Estilo para o texto principal da descrição/observações (com quebra automática)
    estilos.add(ParagraphStyle(name='CorpoTextoPDF',
                               fontName='Helvetica', # Fonte padrão normal
                               fontSize=12,
                               leading=16, # Espaçamento entre linhas maior para elegância
                               spaceAfter=8,
                               textColor=COR_TEXTO_NORMAL))

    # Estilo para o rótulo "TOTAL:" e o Valor Total (destacados)
    estilos.add(ParagraphStyle(name='TotalLabelPDF',
                               fontName='Helvetica-Bold', # Rótulo em negrito
                               fontSize=14,
                               leading=16,
                               textColor=AZUL_ESCURO_PDF))

    estilos.add(ParagraphStyle(name='TotalValorPDF',
                               fontName='Helvetica-Bold', # Valor também em negrito
                               fontSize=18,
                               leading=20,
                               textColor=AZUL_ESCURO_PDF)) # Valor em azul escuro


    # Estilo para texto pequeno no rodapé ou subtítulos
    estilos.add(ParagraphStyle(name='SmallText',
                               fontName='Helvetica', # Fonte padrão normal
                               fontSize=9,
                               leading=11,
                               textColor=COR_RODAPE))

     # Estilo para texto pequeno alinhado à direita
    estilos.add(ParagraphStyle(name='SmallTextRight',
                               fontName='Helvetica', # Fonte padrão normal
                               fontSize=9,
                               leading=11,
                               alignment=2, # Alinhado à direita
                               textColor=COR_TEXTO_NORMAL))


    # --- Funções para o Cabeçalho e Rodapé Fixos (desenha no canvas de cada página) ---
    # Esta função é chamada pelo SimpleDocTemplate para desenhar elementos em posições fixas
    def _header_footer(canvas, doc):
        canvas.saveState() # Salva o estado atual do canvas (configurações de fonte, cor, etc.)

        # --- Desenhar Cabeçalho Fixo ---
        canvas.setFillColor(AZUL_ESCURO_PDF)
        canvas.setFont('Helvetica-Bold', 20) # Fonte padrão negrito e tamanho
        # Desenha o texto centralizado na largura da página, na altura Y (do topo para baixo)
        # CORRIGIDO: Acessando largura e altura via doc.pagesize
        canvas.drawCentredString(doc.pagesize[0]/2, doc.pagesize[1] - 25*mm, "Orçamento Resolve Prestadora de Serviço")

        canvas.setFont('Helvetica', 12) # Fonte padrão normal e tamanho
         # CORRIGIDO: Acessando largura e altura via doc.pagesize
        canvas.drawCentredString(doc.pagesize[0]/2, doc.pagesize[1] - 30*mm, "RESOLVE VISTORIAS") # Nome da empresa abaixo


        # --- Desenhar Rodapé Fixo ---
        canvas.setFillColor(COR_RODAPE) # Cor cinza para o rodapé
        canvas.setFont('Helvetica', 9) # Fonte padrão normal e tamanho pequeno

        # Informações de contato alinhadas à esquerda no rodapé (margem esquerda do documento)
        canvas.drawString(doc.leftMargin, 15*mm, f"Telefone: {contato_telefone} | Email: {contato_email} | Site: {contato_site}")

        # Nome da empresa e CNPJ alinhados à direita no rodapé (largura da página - margem direita)
        texto_cnpj_empresa = f"Resolve Prestadora de Serviços | CNPJ: 52.823.975/0001-13"
        # CORRIGIDO: Acessando largura via doc.pagesize
        canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 15*mm, texto_cnpj_empresa)

        # Opcional: Número da página no rodapé (útil para documentos com mais de 1 página)
        # canvas.drawCentredString(doc.pagesize[0]/2, 10*mm, f"Página {doc.page}")

        canvas.restoreState() # Restaura o estado do canvas para não afetar o conteúdo da Story


    # --- Construindo a "Story" do Corpo Principal (entre header e footer fixos) ---

    # Espaço inicial abaixo do cabeçalho fixo (usamos Spacer para empurrar o conteúdo)
    Story.append(Spacer(1, 5*mm))

    # Número e Data (usando Tabela para alinhar à direita)
    data_formatada = data.strftime("%d/%m/%Y")
    tabela_numero_data = Table([
        ['', Paragraph(f"Orçamento nº {numero}", estilos['CorpoTextoPDF'])], # Número
        ['', Paragraph(f"Data: {data_formatada}", estilos['CorpoTextoPDF'])] # Data
    ],
    # CORRIGIDO: Acessando largura via doc.pagesize
    colWidths=[doc.pagesize[0] - doc.leftMargin - doc.rightMargin - 60*mm, 60*mm] # Coluna da direita fixa para número/data
    )

    tabela_numero_data.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,-1), 'RIGHT'), # Alinha a 2ª coluna (onde estão número e data) à direita
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    Story.append(tabela_numero_data)

    # Espaço
    Story.append(Spacer(1, 15*mm)) # Espaço maior antes da seção de dados

    # Linha Separadora Horizontal (sutil)
    # Adiciona uma linha sutil usando HRFlowable (Horizontal Rule Flowable)
    Story.append(HRFlowable(width="100%", thickness=0.25, lineCap='round', color=CINZA_LINHA_PDF, spaceBefore=6, spaceAfter=12))


    # --- Seção de Dados do Cliente/Imóvel ---
    # Tabela para organizar Rótulo | Valor
    tabela_cliente_imovel = Table([
        [Paragraph("Cliente:", estilos['RotuloDadosPDF']), Paragraph(cliente, estilos['ValorDadosPDF'])],
        [Paragraph("Local/Condomínio:", estilos['RotuloDadosPDF']), Paragraph(endereco, estilos['ValorDadosPDF'])],
        [Paragraph("Responsável:", estilos['RotuloDadosPDF']), Paragraph(responsavel, estilos['ValorDadosPDF'])],
    ], colWidths=[40*mm, None]) # Coluna do rótulo fixa em 40mm, a outra preenche o resto

    tabela_cliente_imovel.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'), # Alinha no topo
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 3), # Pequeno padding no topo para espaçar linhas
        ('BOTTOMPADDING', (0,0), (-1,-1), 3), # Pequeno padding na base
    ]))
    Story.append(tabela_cliente_imovel)

    # Espaço
    Story.append(Spacer(1, 15*mm)) # Espaço antes da descrição

    # Linha Separadora Horizontal (sutil)
    Story.append(HRFlowable(width="100%", thickness=0.25, lineCap='round', color=CINZA_LINHA_PDF, spaceBefore=6, spaceAfter=12))


    # --- Seção de Descrição ---
    Story.append(Paragraph("Descrição dos Serviços", estilos['Heading1PDF'])) # Título da seção

    # Texto da Descrição (Paragraph lida com quebra automática e \n usando <br/>)
    # .replace('\n', '<br/>') converte quebras de linha digitadas em quebras de linha no PDF
    Story.append(Paragraph(descricao.replace('\n', '<br/>'), estilos['CorpoTextoPDF']))

    # Espaço
    Story.append(Spacer(1, 15*mm))

    # Linha Separadora Horizontal (sutil)
    Story.append(HRFlowable(width="100%", thickness=0.25, lineCap='round', color=CINZA_LINHA_PDF, spaceBefore=6, spaceAfter=12))


    # --- Seção de Observações ---
    Story.append(Paragraph("Observações", estilos['Heading1PDF'])) # Título da seção

    # Texto das Observações (Paragraph lida com quebra automática e \n usando <br/>)
    Story.append(Paragraph(obs.replace('\n', '<br/>'), estilos['CorpoTextoPDF']))

    # Espaço
    Story.append(Spacer(1, 20*mm)) # Espaço maior antes da seção TOTAL/Valor


     # --- Seção Valor Total (Destacada) ---
     # Usando Tabela para posicionar TOTAL e Valor na mesma linha, alinhados
     # Esta tabela ocupa 100% da largura disponível entre as margens
    tabela_valor = Table([
        [Paragraph("TOTAL:", estilos['TotalLabelPDF']), Paragraph(f"R$ {valor}", estilos['TotalValorPDF'])]
    ],
    # CORRIGIDO: Acessando largura via doc.pagesize
    colWidths=[doc.pagesize[0] - doc.leftMargin - doc.rightMargin - 80*mm, 80*mm] # Coluna do valor fixa em 80mm, a do TOTAL preenche o resto
    )

    tabela_valor.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,0), 'LEFT'), # Alinha TOTAL à esquerda
        ('ALIGN', (1,0), (1,0), 'RIGHT'), # Alinha o valor à direita
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 8), # Padding em cima e embaixo para dar destaque
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        # Opcional: adicionar uma linha ou background sutil ao redor do TOTAL
        # ('BOX', (0,0), (1,0), 0.5, CINZA_LINHA_PDF), # Borda ao redor da tabela inteira
        # ('BACKGROUND', (0,0), (1,0), HexColor('#F8F9FA')), # Fundo sutil
    ]))
    Story.append(tabela_valor)


    # Espaço final antes do rodapé fixo (pode ser necessário ajustar se o conteúdo for longo)
    # Adiciona um Spacer "flexível" que tenta preencher o espaço restante
    # Story.append(Spacer(1, 1, 1, 1)) # Este Spacer flexível tenta empurrar o rodapé para baixo, mas com onFirstPage o rodapé é fixo.
    # Com o onFirstPage, o rodapé já tem sua posição Y definida, então não precisamos de um Spacer flexível no final da Story.
    # Apenas um Spacer normal para garantir um espaço mínimo entre o último elemento da Story e o rodapé.
    Story.append(Spacer(1, 20*mm))


    # --- Construir o Documento ---
    try:
        # O build usa a lista Story para o corpo principal e chama _header_footer para elementos fixos
        doc.build(Story, onFirstPage=_header_footer, onLaterPages=_header_footer)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    except Exception as e:
        st.error(f"Erro ao gerar o PDF (ReportLab build): {e}")
        buffer.close()
        return None


# --- INTERFACE STREAMLIT ---
# Título principal do aplicativo Streamlit
st.title("Gerador de Orçamento - Resolve Vistorias")

# --- SUA MENSAGEM PERSONALIZADA AQUI ---
st.write("FAÇA AQUI O TEU ORÇAMENTO, NECA!!! ;)")


# Seção para informações de contato da empresa (serão usadas no rodapé do PDF)
# Usamos session_state para manter os valores pré-preenchidos/editados
st.sidebar.subheader("Informações de Contato da Empresa (Rodapé)")
st.session_state.contato_telefone = st.sidebar.text_input("Telefone", value=st.session_state.contato_telefone)
st.session_state.contato_email = st.sidebar.text_input("Email", value=st.session_state.contato_email)
st.session_state.contato_site = st.sidebar.text_input("Site", value=st.session_state.contato_site)
st.sidebar.markdown("---") # Linha separadora na sidebar


# Exemplo de layout com colunas para organizar campos na interface
col1, col2 = st.columns(2)

# Campos na primeira coluna
with col1:
    cliente = st.text_input("Cliente")
    responsavel = st.text_input("Responsável (A/C)")


# Campos na segunda coluna
with col2:
     endereco = st.text_input("Local/Condomínio")
     # Campo de data
     st.session_state.data_orcamento = st.date_input("Data do Orçamento", value=st.session_state.data_orcamento)


# Campos que ocupam a largura total
descricao = st.text_area("Descrição Detalhada dos Serviços", height=200) # Aumentei a altura do text area
valor = st.text_input("Valor Total do Orçamento")
obs = st.text_area("Observações", height=100) # Campo de observações reintroduzido


# Botão para gerar o PDF
if st.button("Gerar PDF"):
    # Verificar se os campos principais estão preenchidos antes de gerar
    if cliente and endereco and responsavel and descricao and valor is not None and valor != "": # Verifica se valor não é vazio
        # Chama a função para criar o PDF (usando Flowables com fontes padrão)
        # Passa todos os dados, incluindo as informações de contato da empresa
        pdf_bytes = criar_pdf_sofisticado(st.session_state.numero_orcamento,
                                        st.session_state.data_orcamento,
                                        cliente,
                                        responsavel,
                                        endereco,
                                        descricao,
                                        valor,
                                        obs, # Passa o conteúdo das observações
                                        st.session_state.contato_telefone, # Passa info de contato
                                        st.session_state.contato_email,
                                        st.session_state.contato_site)


        # Verifica se a geração do PDF foi bem sucedida antes de oferecer o download
        if pdf_bytes:
            # Botão de download para o PDF gerado
            st.download_button(
                label="⬇️ Baixar Orçamento",
                data=pdf_bytes,
                # Nome do arquivo inclui o número e a data do orçamento para facilitar a organização
                file_name=f"ORCAMENTO_RESOLVE_N{st.session_state.numero_orcamento}_{st.session_state.data_orcamento.strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )

            # Mensagem de sucesso e feedback para o usuário
            st.success(f"Orçamento Nº {st.session_state.numero_orcamento} gerado! Clique no botão para baixar.")

            # *** IMPORTANTE: Incrementa o número APÓS a geração bem-sucedida ***
            st.session_state.numero_orcamento += 1

            # Opcional: Limpar os campos de input após gerar o PDF (se quiser, descomente abaixo)
            # Para fazer isso, você precisaria armazenar os valores dos inputs no session_state também.
            # Exemplo:
            # for key in ['cliente', 'responsavel', 'endereco', 'descricao', 'valor', 'obs']:
            #     if key in st.session_state:
            #         st.session_state[key] = "" # Limpa o valor no session_state
            # # Limpar data:
            # st.session_state.data_orcamento = date.today() # Reseta para a data atual
            # # Limpar contato (se necessário):
            # # st.session_state['contato_telefone'] = "(XX) XXXX-XXXX"
            # # st.session_state['contato_email'] = ""
            # # st.session_state['contato_site'] = ""
            # st.rerun() # Força o Streamlit a recarregar


    else:
        # Mensagem de aviso se campos obrigatórios não forem preenchidos
        st.warning("Por favor, preencha os campos obrigatórios (Cliente, Local/Condomínio, Responsável, Descrição e Valor).")

# Fim do script

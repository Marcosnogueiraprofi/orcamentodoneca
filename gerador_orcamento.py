import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable # Importar componentes para layout
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle # Para estilos de texto
from reportlab.lib.units import mm # Para usar milímetros nas medidas
from reportlab.lib.colors import HexColor, black, blue # Para cores, incluindo HexColor
from io import BytesIO
from datetime import date # Para usar a data

# --- INICIALIZAÇÃO DO ESTADO DE SESSÃO ---
# Inicializa o número do orçamento e a data
if 'numero_orcamento' not in st.session_state:
    st.session_state['numero_orcamento'] = 201 # Começa com o número que você quiser
if 'data_orcamento' not in st.session_state:
     st.session_state['data_orcamento'] = date.today() # Data inicial


# --- CÓDIGO CSS PARA LAYOUT AZUL E BRANCO ELEGANTE NO STREAMLIT ---
# Este bloco injeta CSS na página do Streamlit para estilizar a interface
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
    background-color: #1E3A8A; /* Azul marinho para o cabeçalho do Streamlit */
    padding: 10px;
    color: white; /* Texto branco no cabeçalho */
}

/* Estilo para os títulos dentro do conteúdo (se usar st.title ou st.header) */
h1, h2, h3, h4, h5, h6 {
    color: #1E3A8A; /* Azul marinho para títulos */
    font-weight: bold;
}

/* Estilo para os rótulos dos inputs de texto e text area */
div[data-testid="textInputRootStyles"] label,
div[data-testid="stTextarea"] label,
div[data-testid="stDateInput"] label { /* Adicionado seletor para o input de data */
    font-weight: bold;
    color: #0056b3; /* Um azul médio para os rótulos */
}

/* Estilo para os campos de input de texto, text area e input de data */
div[data-testid="textInputRootStyles"] input,
div[data-testid="stTextarea"] textarea,
div[data-testid="stDateInput"] input { /* Adicionado seletor para o input de data */
    background-color: #F8F9FA; /* Um branco bem levemente acinzentado */
    border: 1px solid #CED4DA; /* Borda suave */
    border-radius: 5px;
    padding: 10px;
    width: 100%; /* Ocupa a largura total disponível no contêiner */
    box-sizing: border-box; /* Inclui padding e borda no cálculo da largura */
}

/* Estilo para os campos quando estão focados (clicados) */
div[data-testid="textInputRootStyles"] input:focus,
div[data-testid="stTextarea"] textarea:focus,
div[data-testid="stDateInput"] input:focus { /* Adicionado seletor para o input de data */
    border-color: #007bff; /* Borda azul mais vibrante ao focar */
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25); /* Sombra suave ao focar */
    outline: none; /* Remove o contorno padrão do navegador */
}

/* Estilo para o botão */
.stButton button {
    background-color: #007bff; /* Azul primário */
    color: white; /* Texto branco */
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s ease; /* Efeito suave ao passar o mouse */
}

.stButton button:hover {
    background-color: #0056b3; /* Azul um pouco mais escuro ao passar o mouse */
}

/* Adicione mais estilos conforme necessário */

</style>
""", unsafe_allow_html=True)
# --- FIM DO CÓDIGO CSS ---


# --- FUNÇÃO ATUALIZADA PARA CRIAR O PDF USANDO FLOWABLES ---
# Esta função cria o PDF com um layout estruturado usando ReportLab Flowables
def criar_pdf_flowables(numero, data, cliente, responsavel, endereco, descricao, valor, obs):
    buffer = BytesIO()
    # O SimpleDocTemplate lida com margens, quebras de página, etc.
    doc = SimpleDocTemplate(buffer,
                            pagesize=A4,
                            leftMargin=30*mm,
                            rightMargin=30*mm,
                            topMargin=30*mm,
                            bottomMargin=20*mm)

    Story = [] # Lista para armazenar os elementos (Flowables) do PDF

    # --- Definindo Estilos e Cores para o PDF ---
    estilos = getSampleStyleSheet() # Pega estilos de exemplo

    # Definindo cores
    AZUL_MARINHO_PDF = HexColor('#1E3A8A')
    PRETO_PDF = HexColor('#000000')
    CINZA_LINHA_PDF = HexColor('#CED4DA')


    # Criando estilos personalizados
    estilos.add(ParagraphStyle(name='TituloPrincipal',
                               fontName='Helvetica-Bold',
                               fontSize=18,
                               leading=22, # Espaçamento entre linhas
                               alignment=1, # 0=Left, 1=Center, 2=Right
                               textColor=AZUL_MARINHO_PDF))

    estilos.add(ParagraphStyle(name='SubtituloTopo',
                               fontName='Helvetica',
                               fontSize=12,
                               leading=14,
                               alignment=2, # Alinhado à direita para Número e Data
                               textColor=PRETO_PDF))

    estilos.add(ParagraphStyle(name='CabecalhoEmpresa',
                               fontName='Helvetica',
                               fontSize=12,
                               leading=14,
                               alignment=1, # Centralizado
                               textColor=AZUL_MARINHO_PDF))

    estilos.add(ParagraphStyle(name='Heading2PDF',
                               fontName='Helvetica-Bold',
                               fontSize=14,
                               leading=16,
                               spaceAfter=6, # Espaço depois do parágrafo
                               textColor=AZUL_MARINHO_PDF)) # Títulos de seção em azul

    estilos.add(ParagraphStyle(name='CorpoTexto',
                               fontName='Helvetica',
                               fontSize=12,
                               leading=14,
                               spaceAfter=6,
                               textColor=PRETO_PDF)) # Texto normal em preto

    estilos.add(ParagraphStyle(name='RotuloDados',
                               fontName='Helvetica-Bold',
                               fontSize=12,
                               leading=14,
                               textColor=AZUL_MARINHO_PDF)) # Rótulos (Cliente, A/C, Imóvel) em negrito azul

     # Estilo para o valor total (azul marinho, sem negrito, maior que texto normal)
    estilos.add(ParagraphStyle(name='ValorTotal',
                               fontName='Helvetica',
                               fontSize=16,
                               leading=18,
                               alignment=1, # Centralizado
                               spaceBefore=6,
                               spaceAfter=12,
                               textColor=AZUL_MARINHO_PDF))


    estilos.add(ParagraphStyle(name='Rodape',
                               fontName='Helvetica',
                               fontSize=9,
                               leading=11,
                               alignment=0, # Alinhado à esquerda
                               textColor=PRETO_PDF))


    # --- Adicionando Elementos à "Story" (aqui construímos o layout) ---

    # Título Principal
    Story.append(Paragraph("Orçamento Resolve Prestadora de Serviço", estilos['TituloPrincipal']))

    # Espaço
    Story.append(Spacer(1, 5*mm))

    # Número e Data (usando Tabela para alinhar à direita)
    data_formatada = data.strftime("%d/%m/%Y")
    # Tabela 1 linha, 2 colunas. Largura [flexível, largura fixa]. Conteúdo justificado à direita na 2ª coluna.
    tabela_numero_data = Table([
        ['', f"Orçamento nº {numero}<br/>Data: {data_formatada}"] # <br/> força quebra de linha dentro da célula
    ], colWidths=[A4[0]/2 - 30*mm, A4[0]/2 - 30*mm]) # Divide a largura disponível em 2 colunas

    tabela_numero_data.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,0), 'RIGHT'), # Alinha a 2ª coluna à direita
        ('VALIGN', (0,0), (1,0), 'TOP'), # Alinha no topo
        ('LEFTPADDING', (0,0), (-1,-1), 0), # Remove padding padrão
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    Story.append(tabela_numero_data)


    # Espaço
    Story.append(Spacer(1, 8*mm))

    # Linha Separadora Horizontal
    Story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=CINZA_LINHA_PDF, spaceBefore=6, spaceAfter=12))

    # --- Seção TOTAL e Valor Total ---
    # Usando Tabela para alinhar "TOTAL:" e Valor
    tabela_valor = Table([
        ['TOTAL:', f"R$ {valor}"]
    ], colWidths=[A4[0]/2 - 30*mm, A4[0]/2 - 30*mm]) # Tabela com 2 colunas

    tabela_valor.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,0), 'LEFT'), # Alinha "TOTAL:" à esquerda na 1ª coluna
        ('ALIGN', (1,0), (1,0), 'RIGHT'), # Alinha o valor à direita na 2ª coluna
        ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'), # Negrito para TOTAL:
        ('FONTSIZE', (0,0), (0,0), 14), # Tamanho ajustado
        ('FONTSIZE', (1,0), (1,0), 16), # Tamanho ajustado para o valor
         ('TEXTCOLOR', (0,0), (-1,0), AZUL_MARINHO_PDF), # Cor azul para TOTAL e Valor
         ('LEFTPADDING', (0,0), (-1,-1), 0),
         ('RIGHTPADDING', (0,0), (-1,-1), 0),
         ('TOPPADDING', (0,0), (-1,-1), 0),
         ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    # Removi o estilo 'ValorTotal' de ParagraphStyle e usei TableStyle para estilizar dentro da tabela
    Story.append(tabela_valor)

    # Espaço
    Story.append(Spacer(1, 8*mm))

    # Linha Separadora Horizontal
    Story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=CINZA_LINHA_PDF, spaceBefore=6, spaceAfter=12))


    # --- Informações do Cliente/Imóvel ---
    # Usando Tabela para organizar Cliente, A/C, Imóvel como rótulo + valor
    # Rótulo em azul negrito, valor em preto normal
    tabela_cliente_imovel = Table([
        [Paragraph("Cliente:", estilos['RotuloDados']), Paragraph(cliente, estilos['CorpoTexto'])],
        [Paragraph("Local/Condomínio:", estilos['RotuloDados']), Paragraph(endereco, estilos['CorpoTexto'])],
        [Paragraph("A/C:", estilos['RotuloDados']), Paragraph(responsavel, estilos['CorpoTexto'])],
    ], colWidths=[40*mm, None]) # Coluna do rótulo com 40mm, a outra flexível

    tabela_cliente_imovel.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'), # Alinha no topo
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 2), # Pequeno padding no topo para espaçar linhas
        ('BOTTOMPADDING', (0,0), (-1,-1), 2), # Pequeno padding na base
    ]))
    Story.append(tabela_cliente_imovel)

    # Espaço
    Story.append(Spacer(1, 8*mm))

    # Linha Separadora Horizontal
    Story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=CINZA_LINHA_PDF, spaceBefore=6, spaceAfter=12))


    # --- Seção de Descrição ---
    # Título da seção centralizado
    Story.append(Paragraph("Descrição dos Serviços", estilos['Heading2PDF']))

    # Texto da Descrição (Paragraph lida com quebra automática)
    Story.append(Paragraph(descricao.replace('\n', '<br/>'), estilos['CorpoTexto'])) # Substitui \n por <br/> para ReportLab quebrar linha

    # Espaço
    Story.append(Spacer(1, 8*mm))

    # Linha Separadora Horizontal
    Story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=CINZA_LINHA_PDF, spaceBefore=6, spaceAfter=12))


    # --- Seção de Observações (Reintroduzida) ---
    # Título da seção centralizado
    Story.append(Paragraph("Observações", estilos['Heading2PDF']))

    # Texto das Observações (Paragraph lida com quebra automática)
    Story.append(Paragraph(obs.replace('\n', '<br/>'), estilos['CorpoTexto'])) # Substitui \n por <br/> para ReportLab quebrar linha

    # Espaço
    Story.append(Spacer(1, 15*mm)) # Espaço maior antes do rodapé


    # --- Rodapé ---
    # Usando Tabela para organizar Nome/CNPJ e alinhá-los à esquerda
    tabela_rodape = Table([
        ["Resolve Prestadora de Serviços"],
        ["CNPJ: 52.823.975/0001-13"]
    ], colWidths=[None]) # Coluna única flexível

    tabela_rodape.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,0), 'Helvetica'),
        ('FONTSIZE', (0,0), (0,0), 9),
        ('FONTNAME', (0,1), (0,1), 'Helvetica'),
        ('FONTSIZE', (0,1), (0,1), 9),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), # Alinha tudo à esquerda
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
     # Adiciona o rodapé no final da "Story"
    Story.append(tabela_rodape)


    # --- Construir o Documento ---
    try:
        doc.build(Story) # Compila a história em um PDF
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    except Exception as e:
        st.error(f"Erro ao gerar o PDF: {e}")
        buffer.close()
        return None


# --- INTERFACE STREAMLIT ---
# Título principal do aplicativo Streamlit
st.title("Gerador de Orçamento - Resolve Vistorias")

# --- SUA MENSAGEM PERSONALIZADA AQUI ---
# Colocada após o título principal, antes dos campos
st.write("FAÇA AQUI O TEU ORÇAMENTO, NECA!!! ;)") # Ou use st.markdown("## Sua Mensagem") para um título menor


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
descricao = st.text_area("Descrição Detalhada dos Serviços")
valor = st.text_input("Valor Total do Orçamento")
obs = st.text_area("Observações") # Campo de observações reintroduzido


# Botão para gerar o PDF
if st.button("Gerar PDF"):
    # Verificar se os campos principais estão preenchidos antes de gerar
    # Ajustei a verificação para os campos presentes na interface agora
    if cliente and endereco and responsavel and descricao and valor is not None and valor != "": # Verifica se valor não é vazio
        # Chama a função para criar o PDF (agora usando Flowables)
        # Passei os inputs individuais (cliente, endereco, responsavel) para a função
        # Passei também o campo 'obs' que foi reintroduzido
        pdf_bytes = criar_pdf_flowables(st.session_state.numero_orcamento,
                                        st.session_state.data_orcamento,
                                        cliente,
                                        responsavel,
                                        endereco,
                                        descricao,
                                        valor,
                                        obs) # Passa o conteúdo do campo de observações

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
            # Isso garante que o próximo orçamento terá um número diferente
            st.session_state.numero_orcamento += 1

            # Opcional: Limpar os campos de input após gerar o PDF (se quiser, descomente abaixo)
            # Para fazer isso, você precisaria armazenar os valores dos inputs no session_state também.
            # Exemplo:
            # for key in ['cliente', 'responsavel', 'endereco', 'descricao', 'valor', 'obs']:
            #     if key in st.session_state:
            #         del st.session_state[key] # Limpa o valor do session_state
            # st.rerun() # Força o Streamlit a recarregar e limpar os campos


    else:
        # Mensagem de aviso se campos obrigatórios não forem preenchidos
        st.warning("Por favor, preencha os campos obrigatórios (Cliente, Local/Condomínio, Responsável, Descrição e Valor).")

# Fim do script

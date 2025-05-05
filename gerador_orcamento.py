import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor # Importar para usar cores hexadecimais
from io import BytesIO
# import os # Manter ou remover conforme necessário

# --- INICIALIZAÇÃO DO ESTADO DE SESSÃO ---
# Inicializa o número do orçamento se ele ainda não existir no estado de sessão
# O estado de sessão mantém o valor entre as interações do usuário
if 'numero_orcamento' not in st.session_state:
    st.session_state.numero_orcamento = 201 # Começa com o número que você quiser

# --- INÍCIO DO CÓDIGO CSS PARA LAYOUT AZUL E BRANCO ELEGANTE NO STREAMLIT ---
# Este bloco injeta CSS na página do Streamlit
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
/* Pode precisar inspecionar seu app para confirmar selector, .stApp > header é comum */
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
div[data-testid="stTextarea"] label {
    font-weight: bold;
    color: #0056b3; /* Um azul médio para os rótulos */
}

/* Estilo para os campos de input de texto e text area */
div[data-testid="textInputRootStyles"] input,
div[data-testid="stTextarea"] textarea {
    background-color: #F8F9FA; /* Um branco bem levemente acinzentado */
    border: 1px solid #CED4DA; /* Borda suave */
    border-radius: 5px;
    padding: 10px;
    width: 100%; /* Ocupa a largura total disponível no contêiner */
    box-sizing: border-box; /* Inclui padding e borda no cálculo da largura */
}

/* Estilo para os campos de input/text area quando estão focados (clicados) */
div[data-testid="textInputRootStyles"] input:focus,
div[data-testid="stTextarea"] textarea:focus {
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


# --- FUNÇÃO PARA CRIAR O PDF COM ESTILO ---
# Esta função gera o conteúdo do PDF usando ReportLab
def criar_pdf(numero, cliente, responsavel, endereco, descricao, valor, obs):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # --- Definindo as Cores para o PDF ---
    AZUL_ESCURO_PDF = HexColor('#1E3A8A') # O azul marinho que usamos no Streamlit
    AZUL_PRIMARIO_PDF = HexColor('#007bff') # Um azul um pouco mais vibrante
    CINZA_LINHA_PDF = HexColor('#CED4DA') # Um cinza claro para linhas
    COR_TEXTO_PDF = HexColor('#333333') # Cor de texto padrão suave

    # --- Cabeçalho do Orçamento no PDF ---
    c.setFillColor(AZUL_ESCURO_PDF) # Define a cor para o título
    c.setFont("Helvetica-Bold", 18) # Fonte maior e negrito
    c.drawString(30*mm, 285*mm, "ORÇAMENTO")

    c.setFillColor(AZUL_ESCURO_PDF) # Mantém a cor
    c.setFont("Helvetica", 12)
    c.drawString(30*mm, 279*mm, "RESOLVE VISTORIAS") # Nome da empresa no cabeçalho

    c.setFillColor(COR_TEXTO_PDF) # Volta para a cor de texto padrão
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150*mm, 285*mm, f"Nº {numero}") # Posição do número, ajuste se necessário


    # --- Linha separadora abaixo do cabeçalho ---
    c.setStrokeColor(CINZA_LINHA_PDF) # Define a cor da linha
    c.setLineWidth(0.5) # Espessura da linha
    c.line(30*mm, 275*mm, 180*mm, 275*mm) # Desenha uma linha horizontal (início_x, início_y, fim_x, fim_y)


    # --- Dados do Cliente/Imóvel no PDF ---
    altura_cliente = 265 # Posição Y inicial

    c.setFillColor(AZUL_PRIMARIO_PDF) # Cor para os rótulos
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_cliente*mm, "Cliente:")
    c.drawString(30*mm, (altura_cliente - 10)*mm, "A/C:")
    c.drawString(30*mm, (altura_cliente - 20)*mm, "Imóvel:")

    c.setFillColor(COR_TEXTO_PDF) # Cor para os dados
    c.setFont("Helvetica", 12)
    c.drawString(60*mm, altura_cliente*mm, cliente) # Posição para o nome do cliente
    c.drawString(60*mm, (altura_cliente - 10)*mm, responsavel) # Posição para o responsável
    c.drawString(60*mm, (altura_cliente - 20)*mm, endereco) # Posição para o endereço


    # --- Linha separadora ---
    c.setStrokeColor(CINZA_LINHA_PDF)
    c.line(30*mm, (altura_cliente - 25)*mm, 180*mm, (altura_cliente - 25)*mm)


    # --- Descrição do Serviço no PDF ---
    altura_desc = (altura_cliente - 35) # Posição Y inicial para descrição

    c.setFillColor(AZUL_PRIMARIO_PDF)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_desc*mm, "Descrição do Serviço:")

    c.setFillColor(COR_TEXTO_PDF)
    c.setFont("Helvetica", 12)
    # --- ATENÇÃO: Lidar com texto longo/quebra de linha no PDF com canvas simples ---
    # Para um layout elegante com texto quebrado e múltiplos parágrafos, use Flowables (ReportLab).
    # Abaixo, um exemplo MUITO SIMPLES que apenas tenta exibir a primeira linha ou um texto curto:
    # Se precisar de quebra de linha real, avise para explorar Flowables!
    altura_texto_desc = (altura_desc - 10)
    linhas_desc = descricao.split('\n')
    for linha in linhas_desc:
         c.drawString(30*mm, altura_texto_desc*mm, linha)
         altura_texto_desc -= 5 # Ajuste este valor para o espaçamento entre linhas


    # --- Linha separadora ---
    c.setStrokeColor(CINZA_LINHA_PDF)
    # Ajuste a posição Y da linha para ficar abaixo do texto da descrição (mesmo com múltiplas linhas simples)
    c.line(30*mm, (altura_texto_desc - 5)*mm, 180*mm, (altura_texto_desc - 5)*mm)


    # --- Valor e Observações no PDF ---
    # Ajuste a posição Y inicial deste bloco para ficar abaixo da descrição + linha
    altura_valor_obs_block = (altura_texto_desc - 15) # Exemplo de ajuste baseado na descrição

    c.setFillColor(AZUL_PRIMARIO_PDF)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_valor_obs_block*mm, "Valor Total:")

    c.setFillColor(COR_TEXTO_PDF)
    c.setFont("Helvetica", 12)
    c.drawString(60*mm, altura_valor_obs_block*mm, f"R$ {valor}")

    altura_obs_label = (altura_valor_obs_block - 20)
    c.setFillColor(AZUL_PRIMARIO_PDF)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_obs_label*mm, "Observações:")

    c.setFillColor(COR_TEXTO_PDF)
    c.setFont("Helvetica", 12)
     # --- ATENÇÃO: Lidar com texto longo/quebra de linha no PDF com canvas simples ---
    # Exemplo MUITO SIMPLES:
    altura_texto_obs = (altura_obs_label - 10)
    linhas_obs = obs.split('\n')
    for linha in linhas_obs:
        c.drawString(30*mm, altura_texto_obs*mm, linha)
        altura_texto_obs -= 5 # Ajuste este valor para o espaçamento entre linhas


    # --- Linha separadora final antes do rodapé ---
    c.setStrokeColor(CINZA_LINHA_PDF)
    # Ajuste a posição Y da linha para ficar abaixo do texto das observações
    c.line(30*mm, (altura_texto_obs - 5)*mm, 180*mm, (altura_texto_obs - 5)*mm)


    # --- Rodapé no PDF (Exemplo: Nome da empresa) ---
    c.setFillColor(AZUL_ESCURO_PDF)
    c.setFont("Helvetica", 9)
    # A4[0]/2 é o centro da largura da página
    c.drawCentredString(A4[0]/2, 15*mm, "Resolve Vistorias")


    # --- FECHAMENTO ---
    c.showPage() # Termina a página atual
    c.save() # Salva o conteúdo desenhado no buffer

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes

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
    responsavel = st.text_input("A/C")

# Campos na segunda coluna
with col2:
    endereco = st.text_input("Imóvel")
    # Adicione outros campos que caibam aqui

# Campos que ocupam a largura total
descricao = st.text_area("Descrição")
valor = st.text_input("Valor")
obs = st.text_input("Obs")


# Botão para gerar o PDF
if st.button("Gerar PDF"):
    # Verificar se os campos principais estão preenchidos antes de gerar
    if cliente and endereco and descricao and valor:
        # Chama a função para criar o PDF, passando o número atual do orçamento
        pdf_bytes = criar_pdf(st.session_state.numero_orcamento, cliente, responsavel, endereco, descricao, valor, obs)

        # Botão de download para o PDF gerado
        st.download_button(
            label="⬇️ Baixar Orçamento",
            data=pdf_bytes,
            # Nome do arquivo inclui o número do orçamento
            file_name=f"ORÇAMENTO_RESOLVE_{st.session_state.numero_orcamento}.pdf",
            mime="application/pdf"
        )

        # Mensagem de sucesso e feedback para o usuário
        st.success(f"Orçamento Nº {st.session_state.numero_orcamento} gerado! Clique no botão para baixar.")

        # *** IMPORTANTE: Incrementa o número APÓS a geração bem-sucedida ***
        # Isso garante que o próximo orçamento terá um número diferente
        st.session_state.numero_orcamento += 1

    else:
        # Mensagem de aviso se campos obrigatórios não forem preenchidos
        st.warning("Por favor, preencha os campos obrigatórios (Cliente, Imóvel, Descrição e Valor).")

# Fim do script

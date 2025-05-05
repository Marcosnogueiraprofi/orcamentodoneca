import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from io import BytesIO
from datetime import date # Para usar a data atual ou do input

# --- INICIALIZAÇÃO DO ESTADO DE SESSÃO ---
# Inicializa o número do orçamento e a data (opcionalmente)
if 'numero_orcamento' not in st.session_state:
    st.session['numero_orcamento'] = 201 # Começa com o número que você quiser
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


# --- FUNÇÃO PARA CRIAR O PDF COM O LAYOUT MINIMALISTA ---
def criar_pdf(numero, data, cliente, responsavel, endereco, descricao, valor, obs):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # --- Definindo as Cores para o PDF ---
    AZUL_MARINHO_PDF = HexColor('#1E3A8A')
    PRETO_PDF = HexColor('#000000')

    # --- Posições Y (do topo para baixo, aproximadamente) ---
    Y_TITULO = 285 # Posição Y do topo para o título principal
    Y_VALOR_TOTAL = 260 # Posição Y para o TOTAL e Valor
    Y_SECAO_CLIENTE = 230 # Posição Y para o início das informações do cliente
    Y_TITULO_DESCRICAO = 190 # Posição Y para o título da Descrição
    Y_TEXTO_DESCRICAO_INICIO = 180 # Posição Y para o início do texto da Descrição
    Y_TITULO_OBS = 100 # Posição Y para o título das Observações
    Y_TEXTO_OBS_INICIO = 90 # Posição Y para o início do texto das Observações
    Y_RODAPE = 15 # Posição Y para o rodapé

    # --- Título Principal ---
    c.setFillColor(AZUL_MARINHO_PDF)
    c.setFont("Helvetica-Bold", 18) # Tamanho ajustado para 18 para ser maior
    # Posiciona o centro do texto no centro da página (A4[0]/2) e na altura Y_TITULO
    c.drawCentredString(A4[0]/2, Y_TITULO*mm, "Orçamento Resolve Prestadora de Serviço")

    # --- Número e Data do Orçamento ---
    c.setFillColor(PRETO_PDF) # Cor preta
    c.setFont("Helvetica", 12) # Fonte menor (ajuste o tamanho se 12 não for o que você quer)
    # Posiciona à direita do centro, abaixo do título principal
    # Ajuste as posições X e Y para ficarem alinhados como você quer
    c.drawString(A4[0]/2 + 10*mm, (Y_TITULO - 10)*mm, f"Orçamento nº {numero}") # Exemplo de posição
    # Formata a data como dd/mm/aaaa
    data_formatada = data.strftime("%d/%m/%Y")
    c.drawString(A4[0]/2 + 10*mm, (Y_TITULO - 15)*mm, f"Data: {data_formatada}") # Exemplo de posição


    # --- Seção TOTAL e Valor Total ---
    c.setFillColor(AZUL_MARINHO_PDF) # Cor azul marinho
    c.setFont("Helvetica", 14) # Fonte sem negrito, talvez um pouco maior que o texto normal
    # Posiciona TOTAL: centralizado, um pouco abaixo do cabeçalho
    c.drawCentredString(A4[0]/2, Y_VALOR_TOTAL*mm, "TOTAL:")

    c.setFillColor(AZUL_MARINHO_PDF) # Mesma cor
    c.setFont("Helvetica", 16) # Valor um pouco maior
    # Posiciona o valor centralizado, logo abaixo de TOTAL:
    c.drawCentredString(A4[0]/2, (Y_VALOR_TOTAL - 8)*mm, f"R$ {valor}")


    # --- Informações do Cliente/Imóvel (Adaptado dos seus inputs) ---
    # Desenhando as linhas baseadas nos inputs separados do Streamlit
    altura_linha_atual = Y_SECAO_CLIENTE # Começa nesta posição Y

    c.setFillColor(PRETO_PDF) # Cor preta para este bloco
    c.setFont("Helvetica", 12) # Fonte normal

    # Desenha cada linha alinhada à esquerda
    c.drawString(30*mm, altura_linha_atual*mm, f"À {cliente}")
    altura_linha_atual -= 7 # Reduz a altura para a próxima linha

    # Assumindo que 'endereco' é o nome do condomínio/local
    c.drawString(30*mm, altura_linha_atual*mm, f"{endereco}")
    altura_linha_atual -= 7

    c.drawString(30*mm, altura_linha_atual*mm, f"A/C de {responsavel}")
    altura_linha_atual -= 15 # Espaço maior antes da descrição


    # --- Seção de Descrição ---
    c.setFillColor(AZUL_MARINHO_PDF) # Cor azul marinho para o título da descrição
    c.setFont("Helvetica-Bold", 14) # Título em negrito
    c.drawCentredString(A4[0]/2, Y_TITULO_DESCRICAO*mm, "Descrição dos

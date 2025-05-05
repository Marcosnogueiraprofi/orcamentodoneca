import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
# import os # Esta linha não parece ser usada no código, pode ser removida se não for necessária

# --- INICIALIZAÇÃO DO ESTADO DE SESSÃO ---
# Inicializa o número do orçamento se ele ainda não existir no estado de sessão
if 'numero_orcamento' not in st.session_state:
    st.session_state.numero_orcamento = 201 # Começa com o número que você quiser

# --- INÍCIO DO CÓDIGO CSS PARA LAYOUT AZUL E BRANCO ELEGANTE ---
st.markdown("""
<style>
/* Estilo para o corpo principal da página */
.main {
    background-color: #FFFFFF; /* Fundo branco puro */
    color: #333; /* Cor de texto padrão suave */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Fonte mais elegante */
    padding: 30px; /* Um pouco mais de espaço */
}

/* Estilo para o cabeçalho/título principal */
.stApp > header {
    background-color: #1E3A8A; /* Azul marinho para o cabeçalho do Streamlit */
    padding: 10px;
}

/* Estilo para os títulos dentro do conteúdo (se usar st.title ou st.header) */
h1, h2, h3, h4, h5, h6 {
    color: #1E3A8A; /* Azul marinho para títulos */
    font-weight: bold;
}

/* Estilo para os inputs de texto e text area */
div[data-testid="textInputRootStyles"] label,
div[data-testid="stTextarea"] label {
    font-weight: bold;
    color: #0056b3; /* Um azul médio para os rótulos */
}

div[data-testid="textInputRootStyles"] input,
div[data-testid="stTextarea"] textarea {
    background-color: #F8F9FA; /* Um branco bem levemente acinzentado */
    border: 1px solid #CED4DA; /* Borda suave */
    border-radius: 5px;
    padding: 10px;
    width: 100%; /* Ocupa a largura total disponível no contêiner */
    box-sizing: border-box; /* Inclui padding e borda no cálculo da largura */
}

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


# --- FUNÇÃO PARA CRIAR O PDF ---
# A função agora recebe o número do orçamento
def criar_pdf(numero, cliente, responsavel, endereco, descricao, valor, obs):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # --- CONTEÚDO DO PDF ---
    c.setFont("Helvetica-Bold", 16)
    # Usa o número dinâmico do orçamento
    c.drawString(30*mm, 280*mm, f"ORÇAMENTO Nº {numero}")

    c.setFont("Helvetica", 12)
    c.drawString(30*mm, 270*mm, f"À {cliente}")
    c.drawString(30*mm, 260*mm, f"A/C {responsavel}")
    c.drawString(30*mm, 250*mm, f"Imóvel: {endereco}")

    # --- ADICIONANDO A DESCRIÇÃO, VALOR E OBS (ajuste as posições) ---
    # As posições (números antes do *mm) são exemplos. Ajuste para o seu layout.
    altura_inicial_desc = 220 # Posição Y inicial para a descrição

    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_inicial_desc*mm, "Descrição do Serviço:")
    c.setFont("Helvetica", 12)
    # Para texto longo, você precisa de lógica para quebrar linhas ou usar outros elementos do ReportLab
    # Exemplo MUITO SIMPLES: apenas a primeira linha da descrição se houver quebras
    descricao_formatada = descricao.split('\n')[0] if '\n' in descricao else descricao
    c.drawString(30*mm, (altura_inicial_desc - 10)*mm, descricao_formatada)


    altura_valor_obs = 150 # Posição Y para Valor
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_valor_obs*mm, "Valor Total:")
    c.setFont("Helvetica", 12)
    c.drawString(60*mm, altura_valor_obs*mm, f"R$ {valor}")

    altura_obs = 130 # Posição Y para Observações
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_obs*mm, "Observações:")
    c.setFont("Helvetica", 12)
    # Exemplo MUITO SIMPLES: apenas a primeira linha das obs se houver quebras
    obs_formatada = obs.split('\n')[0] if '\n' in obs else obs
    c.drawString(30*mm, (altura_obs - 10)*mm, obs_formatada)


    # --- FECHAMENTO CORRETO ---
    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes

# --- INTERFACE STREAMLIT ---
st.title("Gerador de Orçamento - Resolve Vistorias") # Título usando Streamlit para ser estilizado pelo CSS

# Exemplo de layout com colunas para organizar campos
col1, col2 = st.columns(2)

with col1:
    cliente = st.text_input("Cliente")
    responsavel = st.text_input("A/C")

with col2:
    endereco = st.text_input("Imóvel")
    # Você pode adicionar outros campos aqui se quiser

descricao = st.text_area("Descrição")
valor = st.text_input("Valor")
obs = st.text_input("Obs")


if st.button("Gerar PDF"):
    # Verificar se os campos principais estão preenchidos antes de gerar
    if cliente and endereco and descricao and valor:
        # Passa o número atual do orçamento para a função
        pdf_bytes = criar_pdf(st.session_state.numero_orcamento, cliente, responsavel, endereco, descricao, valor, obs)

        st.download_button(
            label="⬇️ Baixar Orçamento",
            data=pdf_bytes,
            file_name=f"ORÇAMENTO_RESOLVE_{st.session_state.numero_orcamento}.pdf", # Nome do arquivo com o número
            mime="application/pdf"
        )

        st.success(f"Orçamento Nº {st.session_state.numero_orcamento} gerado! Clique no botão para baixar.")

        # *** IMPORTANTE: Incrementa o número APÓS a geração bem-sucedida ***
        st.session_state.numero_orcamento += 1

    else:
        st.warning("Por favor, preencha os campos obrigatórios (Cliente, Imóvel, Descrição e Valor).")

# Fim do script

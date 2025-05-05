# Mantenha os imports no início do seu script
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor # Importar para usar cores hexadecimais
from io import BytesIO
# import os # Manter ou remover conforme necessário no resto do script

# Mantenha a inicialização do estado de sessão para o número do orçamento
if 'numero_orcamento' not in st.session_state:
    st.session_state.numero_orcamento = 201

# Mantenha o bloco de CSS para o layout do Streamlit
st.markdown("""
# ... (seu bloco de CSS para o Streamlit está aqui) ...
""", unsafe_allow_html=True)


# --- FUNÇÃO ATUALIZADA PARA CRIAR O PDF COM ESTILO ---
# A função agora usa cores e desenha mais elementos
def criar_pdf(numero, cliente, responsavel, endereco, descricao, valor, obs):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # --- Definindo as Cores ---
    AZUL_ESCURO = HexColor('#1E3A8A') # O azul marinho que usamos no Streamlit
    AZUL_PRIMARIO = HexColor('#007bff') # Um azul um pouco mais vibrante
    CINZA_LINHA = HexColor('#CED4DA') # Um cinza claro para linhas


    # --- Cabeçalho do Orçamento ---
    c.setFillColor(AZUL_ESCURO) # Define a cor para o título
    c.setFont("Helvetica-Bold", 18) # Fonte maior e negrito
    c.drawString(30*mm, 285*mm, "ORÇAMENTO")

    c.setFillColor(AZUL_ESCURO) # Mantém a cor
    c.setFont("Helvetica", 12)
    c.drawString(30*mm, 279*mm, "RESOLVE VISTORIAS") # Nome da empresa no cabeçalho

    c.setFillColor(HexColor('#333333')) # Volta para um cinza escuro/preto para o número
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150*mm, 285*mm, f"Nº {numero}") # Posição do número, ajuste se necessário


    # --- Linha separadora abaixo do cabeçalho ---
    c.setStrokeColor(CINZA_LINHA) # Define a cor da linha
    c.setLineWidth(0.5) # Espessura da linha
    c.line(30*mm, 275*mm, 180*mm, 275*mm) # Desenha uma linha horizontal (início_x, início_y, fim_x, fim_y)


    # --- Dados do Cliente/Imóvel ---
    altura_cliente = 265 # Posição Y inicial

    c.setFillColor(AZUL_PRIMARIO) # Cor para os rótulos
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_cliente*mm, "Cliente:")
    c.drawString(30*mm, (altura_cliente - 10)*mm, "A/C:")
    c.drawString(30*mm, (altura_cliente - 20)*mm, "Imóvel:")

    c.setFillColor(HexColor('#333333')) # Cor para os dados
    c.setFont("Helvetica", 12)
    c.drawString(60*mm, altura_cliente*mm, cliente) # Posição para o nome do cliente
    c.drawString(60*mm, (altura_cliente - 10)*mm, responsavel) # Posição para o responsável
    c.drawString(60*mm, (altura_cliente - 20)*mm, endereco) # Posição para o endereço


    # --- Linha separadora ---
    c.setStrokeColor(CINZA_LINHA)
    c.line(30*mm, (altura_cliente - 25)*mm, 180*mm, (altura_cliente - 25)*mm)


    # --- Descrição do Serviço ---
    altura_desc = (altura_cliente - 35) # Posição Y inicial para descrição

    c.setFillColor(AZUL_PRIMARIO)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_desc*mm, "Descrição do Serviço:")

    c.setFillColor(HexColor('#333333'))
    c.setFont("Helvetica", 12)
    # --- ATENÇÃO: Lidar com texto longo/quebra de linha no PDF é complexo com canvas ---
    # Para um layout mais elegante com texto quebrado, você precisaria de Flowables.
    # Abaixo, um exemplo MUITO SIMPLES que só pega a primeira linha ou a string inteira se for curta:
    descricao_curta = descricao.split('\n')[0] if len(descricao.split('\n')[0]) > 100 else descricao
    c.drawString(30*mm, (altura_desc - 10)*mm, descricao_curta)
    # Se precisar de quebra de linha real e múltiplos parágrafos, me avise para explorarmos Flowables!


    # --- Linha separadora ---
    c.setStrokeColor(CINZA_LINHA)
    c.line(30*mm, (altura_desc - 20)*mm, 180*mm, (altura_desc - 20)*mm)


    # --- Valor e Observações ---
    altura_valor_obs_block = (altura_desc - 30) # Posição Y inicial para este bloco

    c.setFillColor(AZUL_PRIMARIO)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_valor_obs_block*mm, "Valor Total:")

    c.setFillColor(HexColor('#333333'))
    c.setFont("Helvetica", 12)
    c.drawString(60*mm, altura_valor_obs_block*mm, f"R$ {valor}")


    altura_obs_label = (altura_valor_obs_block - 20)
    c.setFillColor(AZUL_PRIMARIO)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30*mm, altura_obs_label*mm, "Observações:")

    c.setFillColor(HexColor('#333333'))
    c.setFont("Helvetica", 12)
     # --- ATENÇÃO: Lidar com texto longo/quebra de linha no PDF é complexo com canvas ---
    # Exemplo MUITO SIMPLES:
    obs_curta = obs.split('\n')[0] if len(obs.split('\n')[0]) > 100 else obs
    c.drawString(30*mm, (altura_obs_label - 10)*mm, obs_curta)
    # Se precisar de quebra de linha real e múltiplos parágrafos, me avise!


    # --- Linha separadora final antes do rodapé ---
    c.setStrokeColor(CINZA_LINHA)
    c.line(30*mm, (altura_obs_label - 20)*mm, 180*mm, (altura_obs_label - 20)*mm)

    # --- Rodapé (Exemplo: Nome da empresa) ---
    c.setFillColor(AZUL_ESCURO)
    c.setFont("Helvetica", 9)
    c.drawCentredString(A4[0]/2, 15*mm, "Resolve Vistorias") # Centralizado na parte inferior


    # --- FECHAMENTO ---
    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes

# --- INTERFACE STREAMLIT (MANTENHA ESTA PARTE) ---
# ... (seus st.title, st.columns, st.text_input, st.button, e a lógica do botão) ...
st.title("Gerador de Orçamento - Resolve Vistorias") # Título usando Streamlit

# Exemplo de layout com colunas para organizar campos
col1, col2 = st.columns(2)

with col1:
    cliente = st.text_input("Cliente")
    responsavel = st.text_input("A/C")

with col2:
    endereco = st.text_input("Imóvel")


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

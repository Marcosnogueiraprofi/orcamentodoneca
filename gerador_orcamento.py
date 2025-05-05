import streamlit as st
import streamlit as st
# ... seus outros imports ...

# --- CSS Personalizado ---
st.markdown("""
<style>
/* Aqui você pode adicionar suas regras CSS */

/* Exemplo: Mudar a cor de fundo da página principal do Streamlit */
.main {
    background-color: #f0f2f6; /* Um cinza claro */
    padding: 20px; /* Adicionar um espaçamento interno */
}

/* Exemplo: Mudar a cor do título h1 (se você usar um st.title ou st.header) */
h1 {
    color: #1e3a8a; /* Um tom de azul mais escuro */
}

/* Exemplo: Estilizar os inputs de texto */
div[data-testid="textInputRootStyles"] {
    background-color: white;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 10px;
}

/* Adicione mais estilos conforme necessário */

</style>
""", unsafe_allow_html=True)

# --- Resto do seu código Streamlit ---
# ... (seus st.text_input, st.button, etc.) ...
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
# Não precisa importar os, a menos que use para algo mais

def criar_pdf(cliente, responsavel, endereco, descricao, valor, obs):
    # Criar buffer e PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # --- CONTEÚDO DO PDF ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30*mm, 280*mm, "ORÇAMENTO Nº 201") # Número fixo para teste

    c.setFont("Helvetica", 12)
    c.drawString(30*mm, 270*mm, f"À {cliente}")
    c.drawString(30*mm, 260*mm, f"A/C {responsavel}")
    c.drawString(30*mm, 250*mm, f"Imóvel: {endereco}")

    # --- ADICIONANDO A DESCRIÇÃO, VALOR E OBS ---
    # Você precisará ajustar as posições (os números 230, 150, 140 mm são exemplos)
    # Se a descrição for longa, precisará de lógica para quebrar linhas (ReportLab tem ferramentas para isso, como Flowables)
    c.setFont("Helvetica-Bold", 12) # Título para Descrição, se quiser
    c.drawString(30*mm, 230*mm, "Descrição do Serviço:")
    c.setFont("Helvetica", 12)
    # Para texto longo, pode ser necessário usar c.drawText ou Paragraphs do reportlab.lib.platypus
    c.drawString(30*mm, 220*mm, descricao) # Exemplo simples, pode precisar de quebra de linha

    c.setFont("Helvetica-Bold", 12) # Título para Valor, se quiser
    c.drawString(30*mm, 150*mm, "Valor Total:")
    c.setFont("Helvetica", 12)
    c.drawString(60*mm, 150*mm, f"R$ {valor}") # Exemplo

    c.setFont("Helvetica-Bold", 12) # Título para Obs, se quiser
    c.drawString(30*mm, 140*mm, "Observações:")
    c.setFont("Helvetica", 12)
    c.drawString(30*mm, 130*mm, obs) # Exemplo simples

    # --- FECHAMENTO CORRETO ---
    c.showPage() # Termina a página atual (importante se tiver mais conteúdo ou rodapé)
    c.save() # Salva o conteúdo desenhado no buffer

    # Pré-carregar os bytes antes de fechar
    pdf_bytes = buffer.getvalue()
    buffer.close() # O buffer pode ser fechado depois de getvalue()

    return pdf_bytes

# Interface
cliente = st.text_input("Cliente")
responsavel = st.text_input("A/C")
endereco = st.text_input("Imóvel")
descricao = st.text_area("Descrição")
valor = st.text_input("Valor")
obs = st.text_input("Obs")

if st.button("Gerar PDF"):
    # Verificar se os campos principais estão preenchidos antes de gerar
    if cliente and endereco and descricao and valor:
        pdf_bytes = criar_pdf(cliente, responsavel, endereco, descricao, valor, obs)

        # Download com os bytes pré-carregados
        st.download_button(
            label="⬇️ Baixar Orçamento",
            data=pdf_bytes,
            file_name="ORÇAMENTO_RESOLVE.pdf",
            mime="application/pdf"
        )
        st.success("PDF gerado! Clique no botão para baixar.")
    else:
        st.warning("Por favor, preencha os campos obrigatórios (Cliente, Imóvel, Descrição e Valor).")

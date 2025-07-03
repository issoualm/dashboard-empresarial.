import streamlit as st import pandas as pd import matplotlib.pyplot as plt import seaborn as sns import datetime from io import BytesIO from matplotlib.backends.backend_pdf import PdfPages

--- ESTILO PERSONALIZADO ---

custom_css = """

<style>
body {
    background-color: #d0008f;
}
h1, h2, h3, h4, h5, h6 {
    color: #ffffff;
}
.reportview-container {
    background-color: #d0008f;
    color: #ffffff;
}
.stButton>button {
    background-color: #ffffff;
    color: #000000;
    border-radius: 8px;
    padding: 8px 16px;
    border: 2px solid #40e0d0;
}
.stSelectbox, .stTextInput, .stFileUploader {
    background-color: #ffffff;
    color: #000000;
}
.css-1aumxhk {
    border-color: #40e0d0;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background-color: #d0008f;
}
hr {
    border: 1px solid #40e0d0;
}
</style>""" st.markdown(custom_css, unsafe_allow_html=True)

st.set_page_config(page_title="Dashboard Empresarial Inteligente", layout="wide") st.title("🌟 Dashboard Empresarial Inteligente") st.write("Organize seus dados, visualize resultados e tome decisões com confiança.")

--- UPLOAD DOS DADOS ---

uploaded_file = st.file_uploader("📁 Envie sua planilha Excel ou CSV", type=["xlsx", "csv"])

if uploaded_file: if uploaded_file.name.endswith(".csv"): df = pd.read_csv(uploaded_file) else: df = pd.read_excel(uploaded_file)

st.header("📄 Visualização Geral da Tabela")
st.dataframe(df)
st.markdown("---")

colunas = df.columns.tolist()

# --- INSIGHTS AUTOMÁTICOS ---
st.header("🧠 Insights Automáticos")
if 'data' in [c.lower() for c in colunas]:
    try:
        df['data'] = pd.to_datetime(df[[c for c in colunas if 'data' in c.lower()][0]])
        df['mes'] = df['data'].dt.to_period("M")
        if 'vendas' in [c.lower() for c in colunas]:
            col_vendas = [c for c in colunas if 'vendas' in c.lower()][0]
            resumo = df.groupby("mes")[col_vendas].sum()
            st.success(f"No último mês disponível ({resumo.index[-1]}), o total de vendas foi R${resumo.iloc[-1]:,.2f}.")
            if len(resumo) >= 2:
                delta = resumo.iloc[-1] - resumo.iloc[-2]
                st.info(f"A diferença em relação ao mês anterior foi de R${delta:,.2f}.")
    except Exception as e:
        st.warning("Não foi possível gerar insights automáticos. Verifique as colunas de data e vendas.")

st.markdown("---")

# --- GRÁFICO PERSONALIZADO ---
st.header("📊 Criação de Gráficos Personalizados")
x = st.selectbox("Eixo X", colunas)
y = st.selectbox("Eixo Y", colunas)
tipo = st.selectbox("Tipo de gráfico", ["Barra", "Linha", "Pizza"])

if st.button("🎨 Gerar Gráfico"):
    fig, ax = plt.subplots()
    if tipo == "Barra":
        sns.barplot(data=df, x=x, y=y, ax=ax, palette="rocket")
    elif tipo == "Linha":
        sns.lineplot(data=df, x=x, y=y, ax=ax, color="#40e0d0")
    elif tipo == "Pizza":
        dados = df.groupby(x)[y].sum()
        ax.pie(dados, labels=dados.index, autopct="%1.1f%%", colors=["#e75480", "#40e0d0", "#000000"])
        ax.axis("equal")
    st.pyplot(fig)

st.markdown("---")

# --- RELATÓRIO EM PDF ---
st.header("📥 Exportar Gráfico como PDF")
def generate_pdf(fig):
    pdf_buffer = BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        pdf.savefig(fig)
    pdf_buffer.seek(0)
    return pdf_buffer

if st.button("📄 Baixar gráfico em PDF"):
    fig, ax = plt.subplots()
    if tipo == "Barra":
        sns.barplot(data=df, x=x, y=y, ax=ax, palette="rocket")
    elif tipo == "Linha":
        sns.lineplot(data=df, x=x, y=y, ax=ax, color="#40e0d0")
    elif tipo == "Pizza":
        dados = df.groupby(x)[y].sum()
        ax.pie(dados, labels=dados.index, autopct="%1.1f%%", colors=["#e75480", "#40e0d0", "#000000"])
        ax.axis("equal")
    pdf_file = generate_pdf(fig)
    st.download_button(
        label="📎 Clique aqui para baixar",
        data=pdf_file,
        file_name="grafico_empresa.pdf",
        mime="application/pdf"
    )

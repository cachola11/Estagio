import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🎯 Inserir Alvo Numérico")

# Entradas
col1, col2 = st.columns(2)
with col1:
    alvo = st.number_input("Número do alvo", min_value=0, step=1)
with col2:
    Saldo_Inicial = st.number_input("Saldo Inicial", min_value=0, step=1)

col3, col4 = st.columns(2)
with col3:
    Taxa_Juro = st.number_input("Taxa de Juro (%)", min_value=0.0, step=0.1)
with col4:
    Reforco = st.number_input("Reforço", min_value=0, step=1)

# Botão Calcular
if st.button("Calcular"):

    # Listas
    anos, saldos_iniciais, taxas, juros_list, reforcos, saldos_finais = [], [], [], [], [], []
    saldo = Saldo_Inicial
    ano = 1

    while saldo < alvo and ano <= 100:
        juros = saldo * (Taxa_Juro / 100)
        saldo_final = saldo + juros + Reforco

        anos.append(ano)
        saldos_iniciais.append(saldo)
        taxas.append(f"{Taxa_Juro:.2f}%")
        juros_list.append(juros)
        reforcos.append(Reforco)
        saldos_finais.append(saldo_final)

        saldo = saldo_final
        ano += 1

    # DataFrame
    df = pd.DataFrame({
        "Ano": anos,
        "Saldo Inicial": saldos_iniciais,
        "Taxa de Juro": taxas,
        "Juros": juros_list,
        "Reforço": reforcos,
        "Saldo Final": saldos_finais
    })

    # Guardar no session_state
    st.session_state["df_resultado"] = df
    st.session_state["alvo"] = alvo

# Mostrar gráfico se existir resultado
if "df_resultado" in st.session_state:
    df = st.session_state["df_resultado"]
    alvo = st.session_state["alvo"]

    # Gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Ano"],
        y=df["Saldo Final"],
        mode="lines+markers",
        name="Saldo Final (€)",
        line=dict(color="orange"),
        marker=dict(symbol="circle", size=8)
    ))
    fig.add_trace(go.Scatter(
        x=[df["Ano"].min(), df["Ano"].max()],
        y=[alvo, alvo],
        mode="lines",
        name="Meta (€)",
        line=dict(color="red", dash="dash")
    ))
    fig.update_layout(
        title="Crescimento do Saldo ao Longo do Tempo",
        xaxis_title="Ano",
        yaxis_title="Saldo (€)",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Botão Mostrar Tabela
    if st.button("Mostrar Tabela"):
        st.dataframe(df.style.format({
            "Saldo Inicial": "€{:.2f}",
            "Juros": "€{:.2f}",
            "Reforço": "€{:.2f}",
            "Saldo Final": "€{:.2f}"
        }))

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx

st.set_page_config(
    page_title="Atlas of Belief, Existence and Control",
    layout="wide"
)

df = pd.read_csv("data/raw/narrative_dataset.csv")

st.sidebar.header("Categoría: Filtros")

selected_source_types = st.sidebar.multiselect(
    "Tipo de fuente",
    options=sorted(df["source_type"].unique()),
    default=sorted(df["source_type"].unique())
)

selected_traditions = st.sidebar.multiselect(
    "Tradición / sistema",
    options=sorted(df["tradition"].unique()),
    default=sorted(df["tradition"].unique())
)

filtered_df = df[
    (df["source_type"].isin(selected_source_types)) &
    (df["tradition"].isin(selected_traditions))
].copy()

if filtered_df.empty:
    st.warning("No hay datos para esos filtros. Probá seleccionando más categorías.")
    st.stop()

st.title("Atlas de la creencia, la existencia y el control")
st.subheader("Ciencia, religión, significado existencial y manipulación de masas")

st.markdown(
    """
    Plataforma interactiva para explorar cómo distintos sistemas de creencias explican
    el origen, el significado, la verdad, el miedo, el orden colectivo y la influencia social.
    """
)

tab1, tab2, tab3, tab4 = st.tabs([
    "Visión general",
    "Comparativa",
    "Red conceptual",
    "Multimedia"
])

with tab1:
    st.markdown("## Dominios narrativos básicos")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if os.path.exists("images/science.jpg"):
            st.image("images/science.jpg", use_container_width=True)
        st.markdown("### La ciencia")
        st.caption("Evidencia, cosmología, verificación y modelos explicativos.")

    with c2:
        if os.path.exists("images/religion.jpg"):
            st.image("images/religion.jpg", use_container_width=True)
        st.markdown("### Religión")
        st.caption("Creación, trascendencia, orden moral y autoridad sagrada.")

    with c3:
        if os.path.exists("images/philosophy.jpg"):
            st.image("images/philosophy.jpg", use_container_width=True)
        st.markdown("### Existencialismo / Filosofía")
        st.caption("Libertad, absurdo, significado, ansiedad y condición humana.")

    with c4:
        if os.path.exists("images/manipulation.jpg"):
            st.image("images/manipulation.jpg", use_container_width=True)
        st.markdown("### Manipulación masiva")
        st.caption("Miedo, persuasión, identidad, obediencia y control narrativo.")

    st.divider()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Registros", len(filtered_df))
    m2.metric("Tradiciones / Sistemas", filtered_df["tradition"].nunique())
    m3.metric("Temas", filtered_df["theme"].nunique())
    m4.metric("Riesgo medio", round(filtered_df["manipulation_risk"].mean(), 2))

    st.markdown("## Vista de conjunto de datos")
    st.dataframe(filtered_df, use_container_width=True)

    g1, g2 = st.columns(2)

    with g1:
        st.markdown("## Distribución de tipo fuente")
        source_counts = filtered_df["source_type"].value_counts().reset_index()
        source_counts.columns = ["source_type", "count"]

        fig_source = px.bar(
            source_counts,
            x="source_type",
            y="count",
            color="source_type",
            title="Distribución por tipo de fuente"
        )
        fig_source.update_layout(showlegend=False)
        st.plotly_chart(fig_source, use_container_width=True)

    with g2:
        st.markdown("## Riesgo medio por tradición")
        risk_by_tradition = (
            filtered_df.groupby("tradition", as_index=False)["manipulation_risk"]
            .mean()
            .sort_values("manipulation_risk", ascending=False)
        )

        fig_risk = px.bar(
            risk_by_tradition,
            x="tradition",
            y="manipulation_risk",
            color="manipulation_risk",
            title="Riesgo medio de manipulación por tradición"
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    g3, g4 = st.columns(2)

    with g3:
        st.markdown("## Posicionamiento narrativo")
        fig_scatter = px.scatter(
            filtered_df,
            x="verifiability_score",
            y="manipulation_risk",
            color="source_type",
            size="verifiability_score",
            hover_name="source_name",
            text="tradition",
            title="Posicionamiento narrativo",
            size_max=18
        )
        fig_scatter.update_traces(textposition="top center", opacity=0.8)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with g4:
        st.markdown("## Composición temática")
        fig_theme = px.pie(
            filtered_df,
            names="theme",
            title="Composición del tema"
        )
        st.plotly_chart(fig_theme, use_container_width=True)

with tab2:
    st.markdown("## Matriz comparativa de narrativas")

    matrix_df = filtered_df[[
        "source_name",
        "source_type",
        "tradition",
        "verifiability_score",
        "manipulation_risk"
    ]].copy()

    matrix_df["bubble_size"] = (
        (matrix_df["verifiability_score"] + matrix_df["manipulation_risk"]) / 2
    ).clip(lower=1, upper=10)

    fig_matrix = px.scatter(
        matrix_df,
        x="verifiability_score",
        y="manipulation_risk",
        color="tradition",
        size="bubble_size",
        hover_name="source_name",
        title="Comparación entre verificabilidad y riesgo de manipulación",
        size_max=22
    )
    fig_matrix.update_traces(marker=dict(opacity=0.75))
    st.plotly_chart(fig_matrix, use_container_width=True)

    st.markdown("## Tabla comparativa")
    st.dataframe(
        matrix_df.sort_values(
            ["manipulation_risk", "verifiability_score"],
            ascending=[False, False]
        ),
        use_container_width=True
    )

    st.markdown("## Conclusiones clave")

    highest_risk_row = filtered_df.loc[filtered_df["manipulation_risk"].idxmax()]
    highest_verif_row = filtered_df.loc[filtered_df["verifiability_score"].idxmax()]

    quality_df = filtered_df.copy()
    quality_df["quality_index"] = (
        quality_df["verifiability_score"] - quality_df["manipulation_risk"]
    )
    best_zone_row = quality_df.loc[quality_df["quality_index"].idxmax()]

    top_tradition_risk = (
        filtered_df.groupby("tradition")["manipulation_risk"]
        .mean()
        .sort_values(ascending=False)
        .index[0]
    )

    k1, k2 = st.columns(2)

    with k1:
        st.success(
            f"**Narrativa con mayor riesgo:** {highest_risk_row['source_name']} "
            f"({highest_risk_row['tradition']}) con riesgo {highest_risk_row['manipulation_risk']}."
        )
        st.info(
            f"**Narrativa con mayor verificabilidad:** {highest_verif_row['source_name']} "
            f"({highest_verif_row['tradition']}) con verificabilidad {highest_verif_row['verifiability_score']}."
        )

    with k2:
        st.warning(
            f"**Tradición/sistema con mayor riesgo promedio:** {top_tradition_risk}."
        )
        st.success(
            f"**Mejor equilibrio entre verificabilidad y bajo riesgo:** "
            f"{best_zone_row['source_name']} ({best_zone_row['tradition']})."
        )

    st.markdown("## Narrativas de alto riesgo")
    high_risk_df = filtered_df.sort_values("manipulation_risk", ascending=False)[
        [
            "source_name",
            "source_type",
            "tradition",
            "theme",
            "verifiability_score",
            "manipulation_risk",
            "text"
        ]
    ]
    st.dataframe(high_risk_df, use_container_width=True)

with tab3:
    st.markdown("## Red conceptual")

    graph_df = filtered_df[["tradition", "theme"]].dropna().drop_duplicates()

    if not graph_df.empty:
        G = nx.Graph()

        for _, row in graph_df.iterrows():
            G.add_node(row["tradition"], group="Tradición")
            G.add_node(row["theme"], group="Tema")
            G.add_edge(row["tradition"], row["theme"])

        pos = nx.spring_layout(G, seed=42, k=1.2)

        network_data = []
        for node in G.nodes():
            x, y = pos[node]
            group = G.nodes[node]["group"]
            network_data.append({
                "node": node,
                "x": x,
                "y": y,
                "group": group
            })

        network_df = pd.DataFrame(network_data)

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        fig_network = px.scatter(
            network_df,
            x="x",
            y="y",
            color="group",
            text="node",
            title="Red entre tradiciones y temas"
        )
        fig_network.update_traces(
            textposition="top center",
            marker=dict(size=18, opacity=0.85)
        )

        fig_network.add_scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=1),
            hoverinfo="skip",
            showlegend=False
        )

        fig_network.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
        )

        st.plotly_chart(fig_network, use_container_width=True)
    else:
        st.info("No hay suficientes datos para construir la red conceptual.")

with tab4:
    st.markdown("## Multimedia")

    v1, v2 = st.columns(2)
    v3, v4 = st.columns(2)

    with v1:
        st.markdown("### Video temático: Ciencia")
        if os.path.exists("videos/cosmos.mp4"):
            st.video("videos/cosmos.mp4")
        else:
            st.info("Falta videos/cosmos.mp4")

    with v2:
        st.markdown("### Video temático: Religión")
        if os.path.exists("videos/religion.mp4"):
            st.video("videos/religion.mp4")
        else:
            st.info("Falta videos/religion.mp4")

    with v3:
        st.markdown("### Video temático: Filosofía")
        if os.path.exists("videos/philosophy.mp4"):
            st.video("videos/philosophy.mp4")
        else:
            st.info("Falta videos/philosophy.mp4")

    with v4:
        st.markdown("### Video temático: Manipulación")
        if os.path.exists("videos/manipulation.mp4"):
            st.video("videos/manipulation.mp4")
        else:
            st.info("Falta videos/manipulation.mp4")

    st.divider()

    st.markdown("## Resumen del proyecto")
    st.write(
        """
        Esta versión integra visualización temática, análisis comparativo,
        red conceptual y soporte multimedia para representar ciencia,
        religión, filosofía y manipulación de masas dentro de un único sistema interactivo.
        """
    )

    st.divider()

    st.markdown("## Conclusión general")

    avg_risk_by_type = (
        filtered_df.groupby("source_type", as_index=False)["manipulation_risk"]
        .mean()
        .sort_values("manipulation_risk", ascending=False)
    )

    avg_verif_by_type = (
        filtered_df.groupby("source_type", as_index=False)["verifiability_score"]
        .mean()
        .sort_values("verifiability_score", ascending=False)
    )

    highest_risk_type = avg_risk_by_type.iloc[0]["source_type"]
    highest_verif_type = avg_verif_by_type.iloc[0]["source_type"]

    dominant_theme = filtered_df["theme"].value_counts().idxmax()
    dominant_tradition = filtered_df["tradition"].value_counts().idxmax()

    st.markdown(
        f"""
        Este análisis sugiere que los sistemas narrativos no solo difieren en su contenido,
        sino también en su grado de verificabilidad, su intensidad emocional y su potencial
        de manipulación.

        - El tipo de fuente con **mayor riesgo medio de manipulación** es: **{highest_risk_type}**.
        - El tipo de fuente con **mayor verificabilidad media** es: **{highest_verif_type}**.
        - El **tema dominante** dentro del conjunto filtrado es: **{dominant_theme}**.
        - La **tradición o sistema más representado** es: **{dominant_tradition}**.

        En conjunto, el dashboard permite observar cómo ciencia, religión, filosofía
        y narrativas manipulativas construyen distintas formas de verdad, autoridad
        y sentido colectivo.
        """
    )

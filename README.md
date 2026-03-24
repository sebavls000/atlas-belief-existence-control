# Atlas of Belief, Existence and Control

Dashboard interactivo construido con Streamlit para explorar cómo distintos sistemas narrativos explican el origen, el significado, la verdad, el miedo, el orden colectivo y la influencia social.

## Descripción

Este proyecto analiza cuatro grandes dominios narrativos:

- Ciencia
- Religión
- Existencialismo / Filosofía
- Manipulación masiva

A través de un dataset estructurado, el dashboard permite comparar verificabilidad, riesgo de manipulación, composición temática y relaciones conceptuales entre tradiciones, fuentes y temas.

## Objetivos del proyecto

- Visualizar distintos tipos de narrativas dentro de un entorno unificado
- Comparar verificabilidad y riesgo de manipulación
- Explorar patrones temáticos entre ciencia, religión, filosofía y discursos manipulativos
- Representar relaciones conceptuales mediante una red visual
- Incorporar soporte multimedia para enriquecer la experiencia analítica

## Funcionalidades principales

- Filtros por tipo de fuente y tradición / sistema
- Tarjetas visuales temáticas
- Métricas generales del dataset
- Tabla de datos interactiva
- Distribución por tipo de fuente
- Riesgo medio de manipulación por tradición
- Posicionamiento narrativo
- Composición temática
- Matriz comparativa de narrativas
- Tabla comparativa
- Narrativas de alto riesgo
- Red conceptual entre tradiciones y temas
- Pestaña multimedia con videos temáticos
- Conclusión general automatizada

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- Plotly Express
- NetworkX
- OpenPyXL

## Estructura del proyecto

```bash
atlas-belief-existence-control/
│
├── app/
│   └── dashboard.py
│
├── data/
│   └── raw/
│       └── narrative_dataset.csv
│
├── images/
│   ├── science.jpg
│   ├── religion.jpg
│   ├── philosophy.jpg
│   └── manipulation.jpg
│
├── videos/
│   ├── cosmos.mp4
│   ├── religion.mp4
│   ├── philosophy.mp4
│   └── manipulation.mp4
│
├── README.md
└── requirements.txt
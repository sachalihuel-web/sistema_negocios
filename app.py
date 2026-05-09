import streamlit as st
import pandas as pd
import plotly.express as px

from src.ai_predictions import predecir_ventas_basico
from src.database import crear_base_datos
from src.inventory import agregar_producto, obtener_productos
from src.sales import registrar_venta, obtener_ventas
from src.reports import generar_reporte_pdf
from src.auth import login
from src.demo_data import cargar_demo
from src.analytics import (
    calcular_resumen_negocio,
    generar_insights
)


def card_kpi(titulo, valor, descripcion=""):

    with st.container(border=True):
        st.caption(titulo)
        st.metric(label="", value=valor)

        if descripcion:
            st.caption(descripcion)


st.set_page_config(
    page_title="Sistema Inteligente",
    layout="wide"
)

crear_base_datos()

# LOGIN
st.sidebar.subheader("🔐 Acceso")

usuario = st.sidebar.text_input("Usuario")

password = st.sidebar.text_input(
    "Contraseña",
    type="password"
)

acceso = login(usuario, password)

if not acceso:
    st.info("🔐 Inicie sesión para continuar")
    st.stop()

# HEADER
st.title("📦 Sistema Inteligente para Negocios")
st.subheader("Dashboard Ejecutivo")

# DATOS
productos = obtener_productos()
ventas = obtener_ventas()

if not ventas.empty:
    ventas["fecha"] = pd.to_datetime(
        ventas["fecha"],
        errors="coerce"
    )

    ventas["mes"] = (
        ventas["fecha"]
        .dt.to_period("M")
        .astype(str)
    )

# ANALYTICS
resumen = calcular_resumen_negocio(
    productos,
    ventas
)

total_productos = resumen["total_productos"]
stock_total = resumen["stock_total"]
valor_inventario = resumen["valor_inventario"]
total_ventas = resumen["total_ventas"]
ingresos_totales = resumen["ingresos_totales"]
cantidad_vendida_total = resumen["cantidad_vendida_total"]
ganancia_estimada = resumen["ganancia_estimada"]

# TABS
tab_resumen, tab_inventario, tab_ventas, tab_reportes = st.tabs(
    [
        "📊 Resumen",
        "📦 Inventario",
        "💰 Ventas",
        "📤 Reportes"
    ]
)

# RESUMEN
with tab_resumen:

    st.subheader("🤖 Predicción Inteligente")

    prediccion = predecir_ventas_basico(ventas)

    st.info(prediccion)

    st.subheader("🧠 Insights del Negocio")

    insights = generar_insights(
        productos,
        ventas
    )

    for insight in insights:
        st.info(insight)

    st.subheader("📊 Indicadores del Negocio")

    col1, col2, col3 = st.columns(3)

    with col1:
        card_kpi(
            "📦 Productos",
            total_productos,
            "Registrados"
        )

    with col2:
        card_kpi(
            "📦 Stock Total",
            stock_total,
            "Unidades disponibles"
        )

    with col3:
        card_kpi(
            "💰 Valor Inventario",
            f"${valor_inventario:,.0f}",
            "Estimado"
        )

    st.subheader("💹 Indicadores de Ventas")

    v1, v2, v3, v4 = st.columns(4)

    with v1:
        card_kpi(
            "🧾 Ventas",
            total_ventas,
            "Operaciones"
        )

    with v2:
        card_kpi(
            "📦 Vendidos",
            cantidad_vendida_total,
            "Unidades"
        )

    with v3:
        card_kpi(
            "💰 Ingresos",
            f"${ingresos_totales:,.0f}",
            "Total vendido"
        )

    with v4:
        card_kpi(
            "📈 Ganancia",
            f"${ganancia_estimada:,.0f}",
            "Margen estimado"
        )

    if not productos.empty:

        st.subheader("📈 Stock por Producto")

        fig_stock = px.bar(
            productos,
            x="nombre",
            y="stock",
            title="Stock por Producto",
            text="stock"
        )

        fig_stock.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig_stock,
            width="stretch",
            key="resumen_stock"
        )

    if not ventas.empty:

        st.subheader("📅 Ventas por Fecha")

        ventas_fecha = (
            ventas.groupby(
                "fecha",
                as_index=False
            )["total"]
            .sum()
        )

        fig_fecha = px.line(
            ventas_fecha,
            x="fecha",
            y="total",
            title="Ventas por Fecha",
            markers=True
        )

        st.plotly_chart(
            fig_fecha,
            width="stretch",
            key="resumen_ventas_fecha"
        )

        st.subheader("📆 Ventas por Mes")

        ventas_mes = (
            ventas.groupby(
                "mes",
                as_index=False
            )["total"]
            .sum()
        )

        fig_mes = px.bar(
            ventas_mes,
            x="mes",
            y="total",
            title="Ventas por Mes"
        )

        st.plotly_chart(
            fig_mes,
            width="stretch",
            key="resumen_ventas_mes"
        )

# INVENTARIO
with tab_inventario:

    st.subheader("📦 Registro de Productos")

    nombre = st.text_input("Nombre del producto")

    stock = st.number_input(
        "Stock",
        min_value=0,
        step=1
    )

    precio = st.number_input(
        "Precio",
        min_value=0.0,
        step=100.0
    )

    if st.button("Guardar producto"):

        if nombre.strip() == "":
            st.error("❌ Debe ingresar un nombre")

        else:
            producto_ok = agregar_producto(
                nombre,
                stock,
                precio
            )

            if producto_ok:
                st.success("✅ Producto guardado")

            else:
                st.error("❌ El producto ya existe")

    st.subheader("📋 Inventario")

    st.dataframe(
        productos,
        width="stretch"
    )

    stock_bajo = productos[
        productos["stock"] <= 5
    ]

    if not stock_bajo.empty:

        st.warning("⚠️ Productos con stock bajo")

        st.dataframe(
            stock_bajo,
            width="stretch"
        )

# VENTAS
with tab_ventas:

    st.subheader("💰 Registrar Venta")

    lista_productos = productos["nombre"].tolist()

    if len(lista_productos) == 0:

        st.warning("⚠️ Primero registre productos")

    else:

        producto_vendido = st.selectbox(
            "Producto",
            lista_productos
        )

        cantidad_vendida = st.number_input(
            "Cantidad vendida",
            min_value=1,
            step=1
        )

        precio_venta = st.number_input(
            "Precio de venta",
            min_value=0.0,
            step=100.0
        )

        if st.button("Registrar venta"):

            venta_ok = registrar_venta(
                producto_vendido,
                cantidad_vendida,
                precio_venta
            )

            if venta_ok:
                st.success("✅ Venta registrada")

            else:
                st.error("❌ Stock insuficiente")

    if not ventas.empty:

        st.subheader("🧾 Historial de Ventas")

        st.dataframe(
            ventas,
            width="stretch"
        )

        st.subheader("📈 Ventas por Producto")

        ventas_producto = (
            ventas.groupby(
                "producto",
                as_index=False
            )["total"]
            .sum()
        )

        fig_ventas = px.bar(
            ventas_producto,
            x="producto",
            y="total",
            title="Ventas por Producto"
        )

        st.plotly_chart(
            fig_ventas,
            width="stretch",
            key="ventas_producto"
        )

        st.subheader("🔥 Productos Más Vendidos")

        top_productos = (
            ventas.groupby("producto")["cantidad"]
            .sum()
            .sort_values(ascending=False)
        )

        st.dataframe(
            top_productos,
            width="stretch"
        )

        if not top_productos.empty:

            producto_top = top_productos.idxmax()

            cantidad_top = top_productos.max()

            st.success(
                f"🏆 Producto líder: "
                f"{producto_top} "
                f"con {cantidad_top} unidades vendidas."
            )

# REPORTES
with tab_reportes:

    st.subheader("🧪 Datos de Demostración")

    if st.button("Cargar demo"):

        cargar_demo()

        st.success("✅ Demo cargada correctamente")

    st.subheader("📤 Exportar Reportes")

    excel_inventario = (
        productos.to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="📦 Descargar Inventario",
        data=excel_inventario,
        file_name="inventario.csv",
        mime="text/csv"
    )

    excel_ventas = (
        ventas.to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="💰 Descargar Ventas",
        data=excel_ventas,
        file_name="ventas.csv",
        mime="text/csv"
    )

    st.subheader("📄 Reporte Ejecutivo")

    if st.button("Generar Reporte PDF"):

        ruta_pdf = generar_reporte_pdf(
            total_ventas,
            ingresos_totales,
            ganancia_estimada
        )

        with open(ruta_pdf, "rb") as archivo_pdf:

            st.download_button(
                label="⬇️ Descargar Reporte",
                data=archivo_pdf,
                file_name="reporte_negocio.pdf",
                mime="application/pdf"
            )

st.success("✅ Sistema iniciado correctamente")
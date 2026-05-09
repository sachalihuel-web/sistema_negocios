def calcular_resumen_negocio(productos, ventas):

    total_productos = len(productos)

    stock_total = productos["stock"].sum()

    valor_inventario = (
        productos["stock"] * productos["precio"]
    ).sum()

    if ventas.empty:
        total_ventas = 0
        ingresos_totales = 0
        cantidad_vendida_total = 0
        ganancia_estimada = 0
    else:
        total_ventas = len(ventas)
        ingresos_totales = ventas["total"].sum()
        cantidad_vendida_total = ventas["cantidad"].sum()
        ganancia_estimada = ingresos_totales * 0.30

    return {
        "total_productos": total_productos,
        "stock_total": stock_total,
        "valor_inventario": valor_inventario,
        "total_ventas": total_ventas,
        "ingresos_totales": ingresos_totales,
        "cantidad_vendida_total": cantidad_vendida_total,
        "ganancia_estimada": ganancia_estimada
    }


def detectar_stock_critico(productos, limite=5):

    return productos[productos["stock"] <= limite]


def producto_mas_vendido(ventas):

    if ventas.empty:
        return None, 0

    top_productos = (
        ventas.groupby("producto")["cantidad"]
        .sum()
        .sort_values(ascending=False)
    )

    if top_productos.empty:
        return None, 0

    return top_productos.idxmax(), top_productos.max()


def generar_insights(productos, ventas):

    insights = []

    stock_critico = detectar_stock_critico(productos)

    if len(stock_critico) > 0:
        insights.append(
            f"⚠️ Hay {len(stock_critico)} productos con stock crítico."
        )

    producto_top, cantidad_top = producto_mas_vendido(ventas)

    if producto_top:
        insights.append(
            f"🏆 El producto más vendido es {producto_top} con {cantidad_top} unidades."
        )

    if ventas.empty:
        insights.append(
            "ℹ️ Todavía no hay ventas suficientes para analizar tendencias."
        )

    return insights
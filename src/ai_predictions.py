def predecir_ventas_basico(ventas):

    if ventas.empty or len(ventas) < 3:
        return "No hay suficientes datos para generar una predicción."

    ventas_por_fecha = (
        ventas.groupby("fecha")["total"]
        .sum()
        .reset_index()
    )

    promedio_ventas = ventas_por_fecha["total"].mean()

    ultima_venta = ventas_por_fecha["total"].iloc[-1]

    if ultima_venta > promedio_ventas:
        return "Las ventas recientes están por encima del promedio. Tendencia positiva."

    elif ultima_venta < promedio_ventas:
        return "Las ventas recientes están por debajo del promedio. Revisar productos, precios o stock."

    else:
        return "Las ventas se mantienen estables."
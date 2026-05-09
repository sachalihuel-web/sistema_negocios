from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generar_reporte_pdf(
    total_ventas,
    ingresos,
    ganancia
):

    doc = SimpleDocTemplate(
        "reports/reporte_negocio.pdf"
    )

    estilos = getSampleStyleSheet()

    contenido = []

    titulo = Paragraph(
        "Reporte Ejecutivo del Negocio",
        estilos["Title"]
    )

    contenido.append(titulo)

    contenido.append(Spacer(1, 20))

    contenido.append(
        Paragraph(
            f"Total ventas: {total_ventas}",
            estilos["BodyText"]
        )
    )

    contenido.append(
        Paragraph(
            f"Ingresos: ${ingresos:,.0f}",
            estilos["BodyText"]
        )
    )

    contenido.append(
        Paragraph(
            f"Ganancia estimada: ${ganancia:,.0f}",
            estilos["BodyText"]
        )
    )

    doc.build(contenido)

    return "reports/reporte_negocio.pdf"

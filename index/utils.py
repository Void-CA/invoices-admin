import plotly.express as px
import plotly
import json
import pandas as pd
from facturas.models import *
from clientes.models import *


def get_invoices_data(columns:list[str] =["*"] ) -> pd.DataFrame:
    invoices = pd.DataFrame(list(Invoice.objects.all().values()))
    invoices["total"] = invoices.apply(lambda row: Invoice.objects.get(id=row["id"]).calc_total, axis=1)
    filtered_invoices = invoices[columns] if columns != ["*"] else invoices
    return filtered_invoices

def plotly_json(fig):
    """Convertir figura de Plotly a JSON para su uso en Django"""
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def get_plotly_figure(data, x, y, title, kind='bar'):
    """Generar figura de Plotly con un tema personalizado"""
    custom_theme = {
        "template": "plotly_dark",  # Tema base (puede ser "plotly_white", "seaborn", etc.)
        "layout": {
            "paper_bgcolor": "#1E1E1E",  # Fondo general
            "plot_bgcolor": "#1E1E1E",  # Fondo del gráfico
            "font": {"color": "white", "family": "Arial, sans-serif"},  # Fuente
            "title": {"font": {"size": 20}},  # Tamaño del título
            "colorway": px.colors.sequential.Inferno,  # Colores de la paleta
        }
    }

    fig = None  # Inicializar la figura
    
    if kind == 'bar':
        fig = px.bar(data, x=x, y=y, title=title, color=y, color_discrete_sequence=custom_theme["layout"]["colorway"])
    elif kind == 'pie':
        fig = px.pie(data, names=x, values=y, title=title, color_discrete_sequence=[custom_theme["layout"]["colorway"][i % len(custom_theme["layout"]["colorway"])] for i in range(len(data))])
    
    if fig:
        fig.update_layout(**custom_theme["layout"])  # Aplicar el tema

    return plotly_json(fig)

import plotly.express as px
import plotly
import json
import pandas as pd
from facturas.models import Invoice
from clientes.models import Client
from django.db.models import Sum, F


def get_data(model, columns=None):
    """
    Obtener datos de un modelo Django en formato DataFrame.
    
    :param model: Modelo Django (Invoice, Client, etc.)
    :param columns: Lista de columnas a obtener. Si None, obtiene todas.
    :return: DataFrame con los datos solicitados.
    """
    queryset = model.objects.values(*columns) if columns else model.objects.values()
    return pd.DataFrame(list(queryset))


def get_invoices_data(columns:list[str] = []) -> pd.DataFrame:
    """
    Obtener las facturas con el total calculado eficientemente. 
    Se obtiene la suma del precio de los servicios asociados a cada factura.
    """
    # Realizar la consulta utilizando la anotación para obtener el total de los servicios asociados
    invoices = Invoice.objects.annotate(total=Sum(F("services__price")))

    # Convertir los resultados a DataFrame y filtrar las columnas si es necesario
    if columns != []:
        invoices = invoices.values(*columns)
    else:
        invoices = invoices.values("id", "client_id", "total")

    return pd.DataFrame(list(invoices))


def top_clients_data(n=5):
    """
    Obtener los N clientes con mayor facturación.

    :param n: Número de clientes a mostrar.
    :return: DataFrame con los top N clientes.
    """
    invoices = get_invoices_data()
    clients = get_data(Client, columns=["id", "name"])

    invoices = invoices.merge(clients, left_on="client_id", right_on="id")
    invoices["total"] = invoices["total"].astype(float)

    clients_total = invoices.groupby("name").agg(
        total=("total", "sum"),
        id=("client_id", "first")
    ).reset_index()

    clients_total = clients_total.sort_values(by="total", ascending=False)
    clients_total["id"] = clients_total["id"].astype(str)
    top_clients = clients_total.nlargest(n, "total")
    return top_clients.rename(columns={"name": "Cliente", "total": "Total", "id": "Cliente_ID"})


def plotly_json(fig):
    """Convertir una figura de Plotly a JSON para su uso en Django."""
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_plotly_figure(data, x, y, title, kind='bar', hover_name=None):
    """Generar figura de Plotly con un tema personalizado y hover customizado."""
    custom_theme = {
        "template": "plotly_dark",
        "layout": {
            "paper_bgcolor": "#1E1E1E",
            "plot_bgcolor": "#1E1E1E",
            "font": {"color": "white", "family": "Arial, sans-serif"},
            "title": {"font": {"size": 20}},
            "colorway": px.colors.sequential.Inferno[4:], 
            "height": 350,
            "width": 400,
        }
    }

    fig = None  

    if kind == 'bar':
        fig = px.bar(data, x=x, y=y, title=title, 
                     color_discrete_sequence=custom_theme["layout"]["colorway"],
                     hover_data={hover_name: True} if hover_name else None)

    elif kind == 'pie':
        fig = px.pie(data, names=x, values=y, title=title, 
                     color_discrete_sequence=[custom_theme["layout"]["colorway"][i % len(custom_theme["layout"]["colorway"])] 
                     for i in range(len(data))])

    if fig:
        fig.update_layout(**custom_theme["layout"])  

    return plotly_json(fig)


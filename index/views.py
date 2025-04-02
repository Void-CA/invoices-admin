from django.shortcuts import render
from index.utils import get_invoices_data, get_plotly_figure, top_clients_data


def home(request):
    # Obtener las facturas y su DataFrame
    invoices = get_invoices_data(["state"])
    # 1. Gráfico de distribución de facturas por estado (Pie Chart)
    status_counts = invoices["state"].value_counts().reset_index()
    status_counts.columns = ['state', 'count']
    graph_status_json = get_plotly_figure(status_counts, 'state', 'count', "Distribución de Facturas por Estado", kind='pie')

    # 2. Gráfico de top 5 clientes con mayor facturación (Bar Chart)
    top_clients = top_clients_data(n=5)
    graph_top_clients_json = get_plotly_figure(top_clients, x='Cliente_ID', y='Total', 
                                           title="Clientes con Mayor Facturación", 
                                           kind='bar', hover_name="Cliente")

    context = {
        'graph_status_json': graph_status_json,
        'graph_top_clients_json': graph_top_clients_json
    }

    return render(request, 'index.html', context)

# views.py
from django.shortcuts import render
from index.utils import *



def home(request):
    # Obtener las facturas y su DataFrame
    invoices = get_invoices_data()

    # 1. Gráfico de distribución de facturas por estado (Pie Chart)
    status_counts = invoices["state"].value_counts().reset_index()
    status_counts.columns = ['state', 'count']
    graph_status_json = get_plotly_figure(status_counts, 'state', 'count', "Distribución de Facturas por Estado", kind='pie')

    # 2. Gráfico de top 5 clientes con mayor facturación (Bar Chart)
    client_totals = invoices.groupby('client_id')['total'].sum().reset_index()
    client_totals["total"] = client_totals["total"].astype(float)
    top_clients = client_totals.nlargest(5, 'total')
    graph_top_clients_json = get_plotly_figure(top_clients, 'client_id', 'total', "Top 5 Clientes con Mayor Facturación", kind='bar')

    context = {
        'graph_status_json': graph_status_json,
        'graph_top_clients_json': graph_top_clients_json
    }

    return render(request, 'index.html', context)



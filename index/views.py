from django.shortcuts import render
from index.utils import get_invoices_data, get_plotly_figure, top_clients_data


def home(request):
    # Obtener las facturas y su DataFrame
    invoices = get_invoices_data(["state", "client_id", "total"])  # Asegúrate de tener 'total' en el DataFrame

    # 1. Gráfico de distribución de facturas por estado (Pie Chart)
    status_counts = invoices["state"].value_counts().reset_index()
    status_counts.columns = ['state', 'count']
    graph_status_json = get_plotly_figure(status_counts, 'state', 'count', "Distribución de Facturas por Estado", kind='pie')

    # 2. Gráfico de top 5 clientes con mayor facturación (Bar Chart)
    top_clients = top_clients_data(n=5)
    graph_top_clients_json = get_plotly_figure(top_clients, x='Cliente_ID', y='Total', 
                                               title="Clientes con Mayor Facturación", 
                                               kind='bar', hover_name="Cliente")

    # KPIs de Facturas
    total_invoices = invoices.shape[0]
    total_amount = invoices["total"].sum()
    average_amount = invoices["total"].mean()
    states_counts = invoices["state"].value_counts()

    # KPIs de Clientes
    total_clients = invoices["client_id"].nunique()  # Contar clientes únicos
    top_client_data = invoices.groupby("client_id")["total"].sum().reset_index()
    top_client_data = top_client_data.sort_values(by="total", ascending=False).head(5)

    context = {
        'graph_status_json': graph_status_json,
        'graph_top_clients_json': graph_top_clients_json,
        'invoices_kpis': {
            'total_invoices': total_invoices,
            'total_amount': total_amount,
            'average_amount': average_amount,
            'states_counts': states_counts.to_dict(),
        },
        'clients_kpis': {
            'total_clients': total_clients,
            'top_clients': top_client_data.to_dict(orient='records')  # Convertir top clientes en diccionario
        }
    }

    return render(request, 'index.html', context)

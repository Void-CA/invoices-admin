import cups

def listar_impresoras():
    conn = cups.Connection()
    impresoras = conn.getPrinters()
    return list(impresoras.keys())  # Devuelve nombres como strings

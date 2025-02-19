const { ipcRenderer } = window.electron;

async function loadPage(page) {
    const content = document.getElementById("content");

    if (content.getAttribute("data-current") === page) return;

    try {
        const response = await fetch(`${page}.html`);

        if (!response.ok) throw new Error(`No se pudo cargar ${page}.html`);

        const html = await response.text();
        content.innerHTML = html;
        content.setAttribute("data-current", page);

        console.log(`✅ Página cargada: ${page}`);
    } catch (error) {
        console.error("❌ ERROR al cargar la página:", error);
        content.innerHTML = "<p>Error al cargar la página.</p>";
    }
}

// Manejo de clicks en botones
document.addEventListener("click", (event) => {
    const btn = event.target.closest("button[data-page]");
    if (btn) {
        console.log("🔘 Botón presionado:", btn.innerText);
        loadPage(btn.getAttribute("data-page"));
    }
});

// Cargar la página de inicio al abrir
document.addEventListener("DOMContentLoaded", () => loadPage("home"));

// Cargar facturas en la interfaz
async function cargarFacturas() {
    try {
        const facturas = await ipcRenderer.invoke("obtenerFacturas");
        const contenedor = document.getElementById("facturas-container");
        contenedor.innerHTML = facturas.map(f =>
            `<div>${f.id} - ${f.cliente} - ${f.total} 
            <button onclick="eliminarFactura(${f.id})">❌</button>
            </div>`).join("");
    } catch (error) {
        console.error("❌ Error cargando facturas:", error);
    }
}

// Agregar nueva factura
async function agregarFactura() {
    const cliente = document.getElementById('cliente').value;
    const total = parseFloat(document.getElementById('total').value);
    const fecha = document.getElementById('fecha').value;

    if (cliente && total && fecha) {
        await ipcRenderer.invoke("agregarFactura", { cliente, total, fecha });
        cargarFacturas();
    }
}

// Eliminar factura
async function eliminarFactura(id) {
    await ipcRenderer.invoke("eliminarFactura", id);
    cargarFacturas();
}

// Cargar facturas al iniciar
document.addEventListener("DOMContentLoaded", cargarFacturas);

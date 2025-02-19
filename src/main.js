const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const db = require('./db/db');

let mainWindow;

// Crear ventana principal
app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false
        }
    });
    mainWindow.loadFile('src/views/layout.html');
});

// Obtener facturas
ipcMain.handle("obtenerFacturas", () => {
    try {
        return db.prepare("SELECT * FROM facturas").all();
    } catch (error) {
        console.error("❌ Error obteniendo facturas:", error);
        return [];
    }
});

// Agregar nueva factura
ipcMain.handle("agregarFactura", (event, factura) => {
    try {
        const stmt = db.prepare("INSERT INTO facturas (cliente, total, fecha) VALUES (?, ?, ?)");
        stmt.run(factura.cliente, factura.total, factura.fecha);
        return true;
    } catch (error) {
        console.error("❌ Error agregando factura:", error);
        return false;
    }
});

// Eliminar factura
ipcMain.handle("eliminarFactura", (event, id) => {
    try {
        db.prepare("DELETE FROM facturas WHERE id = ?").run(id);
        return true;
    } catch (error) {
        console.error("❌ Error eliminando factura:", error);
        return false;
    }
});

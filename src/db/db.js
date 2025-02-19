const Database = require('better-sqlite3');
const path = require('path');

// Ruta a la base de datos
const dbPath = path.join(__dirname, 'database.sqlite');
const db = new Database(dbPath);

// Crear tabla si no existe
db.prepare(`CREATE TABLE IF NOT EXISTS facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    total REAL NOT NULL,
    fecha TEXT NOT NULL
)`).run();

console.log("✅ Conectado a SQLite con better-sqlite3");

module.exports = db;

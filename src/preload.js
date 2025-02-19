const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electron", {
  ipcRenderer: {
    invoke: (...args) => ipcRenderer.invoke(...args), // Asegura que invoke se exponga correctamente
    send: (...args) => ipcRenderer.send(...args),
    on: (channel, listener) => ipcRenderer.on(channel, (event, ...args) => listener(...args)),
    once: (channel, listener) => ipcRenderer.once(channel, (event, ...args) => listener(...args)),
  }
});

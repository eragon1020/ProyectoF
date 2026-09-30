module.exports = {
  openapi: "3.0.3",
  info: {
    title: "Microservicio de Lectura - RESPALDO (Node.js)",
    version: "1.0.0",
    description: "Misma respuesta que el servicio Python de lectura. Se invoca cuando este falla."
  },
  paths: {
    "/": { get: { summary: "Health check", responses: { 200: { description: "ok" } } } },
    "/sugerencias": {
      get: {
        summary: "Listar sugerencias",
        responses: {
          200: {
            description: "Lista de sugerencias",
            content: { "application/json": { schema: { type: "array", items: { $ref: "#/components/schemas/Sugerencia" } } } }
          }
        }
      }
    }
  },
  components: {
    schemas: {
      Sugerencia: {
        type: "object",
        properties: {
          id: { type: "string" },
          nombre: { type: "string" },
          emoji: { type: "string" },
          monto_sugerido: { type: "integer" }
        }
      }
    }
  }
};

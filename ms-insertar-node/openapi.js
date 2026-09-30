module.exports = {
  openapi: "3.0.3",
  info: {
    title: "Microservicio de Inserción (Node.js)",
    version: "1.0.0",
    description: "Inserta sugerencias de gastos en MongoDB Atlas."
  },
  paths: {
    "/": { get: { summary: "Health check", responses: { 200: { description: "ok" } } } },
    "/sugerencias": {
      post: {
        summary: "Insertar una sugerencia",
        requestBody: {
          required: true,
          content: { "application/json": { schema: { $ref: "#/components/schemas/SugerenciaEntrada" } } }
        },
        responses: {
          201: { description: "Creada", content: { "application/json": { schema: { $ref: "#/components/schemas/Sugerencia" } } } },
          422: { description: "Datos inválidos" }
        }
      }
    }
  },
  components: {
    schemas: {
      SugerenciaEntrada: {
        type: "object",
        required: ["nombre", "monto_sugerido"],
        properties: {
          nombre: { type: "string", minLength: 1, maxLength: 60, example: "Mercado" },
          emoji: { type: "string", example: "🛒" },
          monto_sugerido: { type: "integer", minimum: 1, example: 120000 }
        }
      },
      Sugerencia: {
        allOf: [
          { $ref: "#/components/schemas/SugerenciaEntrada" },
          { type: "object", properties: { id: { type: "string", example: "665f1c2e9b1e8a3f4c2d1a00" } } }
        ]
      }
    }
  }
};

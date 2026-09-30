/**
 * Microservicio de LECTURA DE RESPALDO (Node.js).
 * Responde lo mismo que GET /sugerencias del servicio Python (FastAPI).
 * Env: MONGODB_URI (obligatoria), MONGODB_DB (opcional), PORT (opcional)
 * Swagger UI: /docs
 */
const express = require("express");
const cors = require("cors");
const swaggerUi = require("swagger-ui-express");
const { MongoClient } = require("mongodb");
const openapi = require("./openapi");

const app = express();
app.use(cors());
app.use("/docs", swaggerUi.serve, swaggerUi.setup(openapi));

const client = new MongoClient(process.env.MONGODB_URI, { serverSelectionTimeoutMS: 5000 });

app.get("/", (_req, res) => res.json({ estado: "ok", servicio: "lectura-respaldo-node" }));

app.get("/sugerencias", async (_req, res) => {
  try {
    await client.connect();
    const docs = await client
      .db(process.env.MONGODB_DB || "cuentas_claras")
      .collection("sugerencias")
      .find()
      .sort({ nombre: 1 })
      .toArray();
    res.json(docs.map(({ _id, ...resto }) => ({ id: _id.toString(), ...resto })));
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "No se pudo leer" });
  }
});

const port = process.env.PORT || 3002;
app.listen(port, () => console.log(`lectura-respaldo-node escuchando en ${port}`));

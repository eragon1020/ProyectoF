/**
 * Microservicio de INSERCIÓN (Node.js).
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
app.use(express.json());
app.use("/docs", swaggerUi.serve, swaggerUi.setup(openapi));

const client = new MongoClient(process.env.MONGODB_URI, { serverSelectionTimeoutMS: 5000 });
const coleccion = async () => {
  await client.connect(); // idempotente
  return client.db(process.env.MONGODB_DB || "cuentas_claras").collection("sugerencias");
};

app.get("/", (_req, res) => res.json({ estado: "ok", servicio: "insertar-node" }));

app.post("/sugerencias", async (req, res) => {
  const { nombre, emoji = "💸", monto_sugerido } = req.body || {};
  if (typeof nombre !== "string" || nombre.trim().length < 1 || nombre.length > 60) {
    return res.status(422).json({ error: "nombre debe tener entre 1 y 60 caracteres" });
  }
  if (!Number.isInteger(monto_sugerido) || monto_sugerido <= 0) {
    return res.status(422).json({ error: "monto_sugerido debe ser un entero > 0" });
  }
  try {
    const doc = { nombre: nombre.trim(), emoji: String(emoji), monto_sugerido };
    const r = await (await coleccion()).insertOne({ ...doc });
    res.status(201).json({ id: r.insertedId.toString(), ...doc });
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "No se pudo insertar" });
  }
});

const port = process.env.PORT || 3001;
app.listen(port, () => console.log(`insertar-node escuchando en ${port}`));

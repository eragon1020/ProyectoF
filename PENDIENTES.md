# Estado de la entrega

## ✅ Hecho (código)
| Pieza | Lenguaje | Carpeta | Puerto | Swagger |
|---|---|---|---|---|
| Lectura principal | Python / FastAPI | `microservicio/` | 8001 | `/docs` |
| Inserción | Node.js / Express | `ms-insertar-node/` | 3001 | `/docs` |
| Lectura de respaldo (resiliencia) | Node.js / Express | `ms-lectura-respaldo-node/` | 3002 | `/docs` |
| Eliminación | Java 17 / Spring Boot | `ms-eliminar-java/` | 3003 | `/docs` |
| **Actualización** | **Go** | `ms-actualizar-go/` | 3004 | `/docs` |
| App Django (vista/ruta/formulario de editar ya integrados) | Python | raíz | 8000 | – |

## 🔲 Falta (requiere tus cuentas)
1. Subir a GitHub (uno por microservicio o monorepo).
2. Desplegar en Render (Root Directory = carpeta; Node: `npm install`/`npm start`; Java y Go: Docker). Env `MONGODB_URI`.
3. En Django (Render) definir: `MICROSERVICIO_RESPALDO_URL`, `MICROSERVICIO_INSERTAR_URL`, `MICROSERVICIO_ELIMINAR_URL`, `MICROSERVICIO_ACTUALIZAR_URL`.
4. Probar resiliencia suspendiendo el servicio Python y recargando `/sugerencias/`.
5. Compilar/probar Java (`mvn package`) y Go (`go mod tidy && go run .`): no pude compilarlos aquí.

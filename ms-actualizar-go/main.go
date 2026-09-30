// Microservicio de ACTUALIZACIÓN (Go). Env: MONGODB_URI, MONGODB_DB (opc), PORT (opc). Swagger UI: /docs
package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var col *mongo.Collection

type entrada struct {
	Nombre        string `json:"nombre"`
	Emoji         string `json:"emoji"`
	MontoSugerido int64  `json:"monto_sugerido"`
}

func escribir(w http.ResponseWriter, code int, v interface{}) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(v)
}

func cors(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET,PUT,OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		if r.Method == http.MethodOptions {
			w.WriteHeader(204)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func actualizar(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPut {
		escribir(w, 405, map[string]string{"error": "método no permitido"})
		return
	}
	id := strings.TrimPrefix(r.URL.Path, "/sugerencias/")
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		escribir(w, 422, map[string]string{"error": "id inválido"})
		return
	}
	var in entrada
	if json.NewDecoder(r.Body).Decode(&in) != nil {
		escribir(w, 422, map[string]string{"error": "JSON inválido"})
		return
	}
	in.Nombre = strings.TrimSpace(in.Nombre)
	if len(in.Nombre) < 1 || len(in.Nombre) > 60 {
		escribir(w, 422, map[string]string{"error": "nombre debe tener entre 1 y 60 caracteres"})
		return
	}
	if in.MontoSugerido <= 0 {
		escribir(w, 422, map[string]string{"error": "monto_sugerido debe ser un entero > 0"})
		return
	}
	if in.Emoji == "" {
		in.Emoji = "💸"
	}
	ctx, cancel := context.WithTimeout(r.Context(), 8*time.Second)
	defer cancel()
	res, err := col.UpdateOne(ctx, bson.M{"_id": oid}, bson.M{"$set": bson.M{
		"nombre": in.Nombre, "emoji": in.Emoji, "monto_sugerido": in.MontoSugerido}})
	if err != nil {
		log.Println(err)
		escribir(w, 500, map[string]string{"error": "No se pudo actualizar"})
		return
	}
	if res.MatchedCount == 0 {
		escribir(w, 404, map[string]string{"error": "No existe la sugerencia"})
		return
	}
	escribir(w, 200, map[string]interface{}{"id": id, "nombre": in.Nombre, "emoji": in.Emoji, "monto_sugerido": in.MontoSugerido})
}

const openapi = `{"openapi":"3.0.3","info":{"title":"Microservicio de Actualización (Go)","version":"1.0.0","description":"Actualiza sugerencias de gastos en MongoDB Atlas."},
"paths":{"/":{"get":{"summary":"Health check","responses":{"200":{"description":"ok"}}}},
"/sugerencias/{id}":{"put":{"summary":"Actualizar una sugerencia",
"parameters":[{"name":"id","in":"path","required":true,"schema":{"type":"string","example":"665f1c2e9b1e8a3f4c2d1a00"}}],
"requestBody":{"required":true,"content":{"application/json":{"schema":{"type":"object","required":["nombre","monto_sugerido"],"properties":{"nombre":{"type":"string","example":"Mercado"},"emoji":{"type":"string","example":"🛒"},"monto_sugerido":{"type":"integer","minimum":1,"example":130000}}}}}},
"responses":{"200":{"description":"Actualizada"},"404":{"description":"No existe"},"422":{"description":"Datos inválidos"}}}}}}`

const docs = `<!doctype html><html><head><meta charset="utf-8"><title>Swagger - Actualizar (Go)</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css"></head><body><div id="ui"></div>
<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>SwaggerUIBundle({url:"/openapi.json",dom_id:"#ui"})</script></body></html>`

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	cl, err := mongo.Connect(ctx, options.Client().ApplyURI(os.Getenv("MONGODB_URI")).SetServerSelectionTimeout(5*time.Second))
	if err != nil {
		log.Fatal(err)
	}
	db := os.Getenv("MONGODB_DB")
	if db == "" {
		db = "cuentas_claras"
	}
	col = cl.Database(db).Collection("sugerencias")

	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			escribir(w, 404, map[string]string{"error": "no encontrado"})
			return
		}
		escribir(w, 200, map[string]string{"estado": "ok", "servicio": "actualizar-go"})
	})
	mux.HandleFunc("/sugerencias/", actualizar)
	mux.HandleFunc("/openapi.json", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json; charset=utf-8")
		w.Write([]byte(openapi))
	})
	mux.HandleFunc("/docs", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.Write([]byte(docs))
	})
	port := os.Getenv("PORT")
	if port == "" {
		port = "3004"
	}
	log.Println("actualizar-go escuchando en", port)
	log.Fatal(http.ListenAndServe(":"+port, cors(mux)))
}

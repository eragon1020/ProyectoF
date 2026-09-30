# Microservicio de sugerencias (FastAPI + MongoDB Atlas)
Despliegue en Render: Root Directory `microservicio`, Build `pip install -r requirements.txt`,
Start `uvicorn main:app --host 0.0.0.0 --port $PORT`, variable `MONGODB_URI`.
Local: `MONGODB_URI=... uvicorn main:app --port 8001` y abre /docs

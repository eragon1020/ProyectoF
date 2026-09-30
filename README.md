# 💸 Cuentas Claras

Antes de todo, toca levantar los microservicios, porque Render los duerme cuando nadie los usa. Entra a cada uno de estos links y espera hasta que salga un JSON o la página de Swagger (el primero puede tardar hasta 1 o 2 minutos):

https://cuentas-claras-2iy4.onrender.com/sugerencias

https://ms-lectura-respaldo-node.onrender.com/sugerencias

https://ms-insertar-node.onrender.com/

https://ms-eliminar-java.onrender.com/

https://ms-actualizar-go.onrender.com/

Después entra a este link de Render, donde estará todo completo:

https://cuentas-claras-1.onrender.com/

La sección de sugerencias está en: https://cuentas-claras-1.onrender.com/sugerencias/

## Microservicios

| Operación | Lenguaje | Swagger |
|---|---|---|
| Lectura (principal) | Python / FastAPI | https://cuentas-claras-2iy4.onrender.com/docs |
| Lectura (respaldo) | Node.js / Express | https://ms-lectura-respaldo-node.onrender.com/docs |
| Inserción | Node.js / Express | https://ms-insertar-node.onrender.com/docs |
| Eliminación | Java / Spring Boot | https://ms-eliminar-java.onrender.com/docs |
| Actualización | Go | https://ms-actualizar-go.onrender.com/docs |

## Resiliencia

La aplicación lee las sugerencias desde el microservicio principal (Python). Si ese servicio falla o no responde, la app llama automáticamente al microservicio de respaldo (Node.js) y sigue mostrando la información, con un aviso en pantalla. Además tiene un circuit breaker de 30 segundos: después de un fallo, salta directo al respaldo sin esperar otro timeout.

Para probarlo: suspender el servicio Python en Render y recargar `/sugerencias/`.


La IA que fue utilizada fue Groq. Procurar tener todo corriendo antes de preguntarle algo.

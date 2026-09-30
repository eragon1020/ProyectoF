package co.cuentasclaras.eliminar;

import com.mongodb.client.result.DeleteResult;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.bson.Document;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@CrossOrigin
@Tag(name = "Eliminación de sugerencias")
public class SugerenciaController {

    private static final String COLECCION = "sugerencias";
    private final MongoTemplate mongo;

    public SugerenciaController(MongoTemplate mongo) {
        this.mongo = mongo;
    }

    @GetMapping("/")
    @Operation(summary = "Health check")
    public Map<String, String> salud() {
        return Map.of("estado", "ok", "servicio", "eliminar-java");
    }

    @DeleteMapping("/sugerencias/{id}")
    @Operation(summary = "Eliminar una sugerencia por id",
               description = "Elimina el documento cuyo _id (ObjectId en hexadecimal) coincide con {id}.")
    public ResponseEntity<Map<String, Object>> eliminar(@PathVariable String id) {
        if (!ObjectId.isValid(id)) {
            return ResponseEntity.unprocessableEntity().body(Map.of("error", "id inválido"));
        }
        DeleteResult r = mongo.remove(
                Query.query(Criteria.where("_id").is(new ObjectId(id))), Document.class, COLECCION);
        if (r.getDeletedCount() == 0) {
            return ResponseEntity.status(404).body(Map.of("error", "No existe la sugerencia"));
        }
        return ResponseEntity.ok(Map.of("eliminado", true, "id", id));
    }
}

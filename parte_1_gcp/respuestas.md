# Parte 1 — Google Cloud Platform

**Instrucciones:** Responde cada pregunta de forma concisa. No hay respuestas únicas correctas — nos interesa tu razonamiento y cómo tomas decisiones de diseño. Puedes usar listas, diagramas en texto o cualquier formato que te ayude a explicarte.

---

## Pregunta 1

El área de datos del CMS tiene hoy varios pipelines que corren localmente en un computador y generan archivos Excel como output. El equipo va a crecer y necesita que estos pipelines sean accesibles y ejecutables sin depender de una máquina local.

¿Cómo diseñarías la migración a GCP? Describe tu propuesta, los servicios que usarías y el orden en que lo harías.

**Respuesta:**
### Objetivo: 
Pasar de un archivo ejecutable en computador local, a un pipeline reproducible y versionable por cualquier miembro del equipo. 

### Proceso Propuesto

#### Fase 1 — Diagnóstico
1. Documentar cada pipeline: inputs, outputs, librerías y versiones, frecuencia de actualización y tiempo de ejecución aproximado. Compartir con el equipo.

#### Fase 2 — Fundación en GCP
2. Crear el proyecto en Google Cloud y habilitar las APIs (Cloud Storage, Artifact Registry, Cloud Run, Cloud Scheduler, BigQuery).
3. Configurar accesos (IAM): dar acceso al equipo mediante sus cuentas de Google con roles según su función.
4. Migrar datos históricos: subir inputs y outputs históricos a Cloud Storage (GCS) para centralizar el acceso.
5. Crear el dataset en BigQuery donde los pipelines depositarán sus outputs como tablas consultables con SQL.

#### Fase 3 — Piloto
6. Contenerizar un pipeline piloto: escribir el Dockerfile, donde se definirá la versión de Python, paquetes con sus versiones, archivos de código, comando de arranque y adaptar el código para leer inputs desde GCS y escribir outputs a GCS y/o BigQuery.
7. Publicar y desplegar: subir la imagen a Artifact Registry y crear un Cloud Run Job que apunte a ella.
8. Automatizar: con Cloud Scheduler definir la frecuencia o fechas de ejecución del pipeline.
9. Validar en paralelo: correr el pipeline en GCP junto al proceso local durante un período, comparando resultados hasta confirmar que coinciden.

#### Fase 4 — Escalamiento y cierre
10. Replicar el patrón en los pipelines restantes, repitiendo solo la contenerización, el despliegue y la automatización.
11. Dar de baja el computador local una vez todos los pipelines estén validados en GCP.

| Fase | Acción | Por qué en ese orden |
|------|--------|----------------------|
| 1 — Diagnóstico | Documentar cada pipeline: inputs, outputs, librerías, frecuencia y tiempo de ejecución. | No se puede migrar lo que no se entiende. |
| 2 — Fundación en GCP | Crear el proyecto, habilitar APIs, configurar IAM, migrar datos históricos a GCS y crear el dataset en BigQuery. | Es la base sobre la que todo se apoya: no se puede desplegar un pipeline sin proyecto ni sin dónde guardar datos. |
| 3 — Piloto | Contenerizar, desplegar y automatizar un pipeline y validarlo en paralelo. | Prueba el flujo completo en pequeño, donde un error es barato y acotado, y deja un patrón replicable. |
| 4 — Escalamiento y cierre | Replicar el patrón en los pipelines restantes y dar de baja el computador local. | Replicar solo sirve con el patrón ya probado; apagar el local es el paso irreversible|

---

## Pregunta 2

El área de datos del CMS tiene tres bases de datos que deben estar disponibles en GCP. Los usuarios que acceden son:
  - Analistas de otras áreas del CMS: consultan los datos frecuentemente con filtros, sin necesidad de descargar archivos completos
  - Ingeniero de datos del CMS: lee y escribe en todas las bases, incluyendo cargar nuevas versiones
  - Organización externo: descarga versiones completas periódicamente, pero no tiene acceso a todas las bases

¿Cómo organizarías el almacenamiento y los permisos en GCP para este escenario?

**Respuesta:**

### Estrategia de almacenamiento: dos capas


| Capa | Servicio | Quiénes tienen acceso | Propósito |
|------|----------|------------------------|-----------|
| Consulta interactiva | *BigQuery* | Analistas (solo lectura) e ingeniero de datos (lectura y escritura) | Analistas hacen queries con filtros|
| Descarga de versiones completas | *Cloud Storage (GCS)* | Organización externa (solo lectura, solo sobre las bases autorizadas) e ingeniero de datos (escritura y gestión) | Archivos CSV versionados para descarga por externos |

Separar las capas permite que el externo descargue desde GCS sin que toque BigQuery, y que los analistas puedan hacer consultas con filtros.

### Organización en BigQuery

```
Proyecto GCP: cms-datos
└── Dataset_CMS
    ├── Tabla_BD_a
    ├── Tabla_BD_b
    └── Tabla_BD_c
```

### Organización en Cloud Storage

```
Cloud Storage
├── CS_CMS_Interno
│   ├── base_bd_a.csv
│   ├── base_bd_b.csv
│   └── base_bd_c.csv
└── CS_CMS_Externo
    └── base_bd_a.csv
```

### Permisos por actor (IAM)

| Actor | Servicio | Rol IAM | Alcance |
|-------|----------|---------|---------|
| Analistas CMS | BigQuery | User + Data Viewer | Dataset_CMS |
| Ingeniero de datos | BigQuery | Editor | Dataset_CMS |
| Ingeniero de datos | GCS | Editor | CS_CMS_Interno + CS_CMS_Externo |
| Organización externa | GCS | Data Viewer | CS_CMS_Externo  |

### Justificación

Dos patrones de acceso, dos servicios: BigQuery para consultas con filtros, GCS para descargas completas. La organización externa nunca toca BigQuery, así que es estructuralmente imposible que alcance datos internos. Los permisos van por rol con privilegio mínimo: cada actor recibe solo lo que su función exige. El esquema es escalable, sumar un usuario es agregarlo a un grupo y autorizar una base al externo es copiar un archivo.


---

*Centro de Movilidad Sostenible — cmsostenible.org*

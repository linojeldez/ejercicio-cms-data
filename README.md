# Ejercicio Técnico — Data Engineer
**Centro de Movilidad Sostenible (CMS)**

## Instrucciones generales

Bienvenido/a al ejercicio técnico del proceso de selección del CMS. Este ejercicio tiene dos partes y está diseñado para que puedas mostrar tu forma de trabajar con datos y tu criterio técnico.

**Plazo:** 22 de abril a las 16:00 horas.

**Cómo entregar:**
1. Haz un fork de este repositorio a tu cuenta de GitHub
2. Trabaja directamente en tu fork
3. Al terminar, envía el link de tu repositorio al correo que te indicaron

**Algunas aclaraciones:**
- No hay respuestas únicas correctas — nos interesa tu razonamiento y cómo tomas decisiones
- No puedes hacernos preguntas para resolver este ejercicio. Si algo no está claro, puedes hacer supuestos razonables y documentarlos
- Valoramos código limpio y bien documentado por sobre código extenso
- El README de tu entrega debe explicar cómo correr tu solución

---

## Parte 1 — Google Cloud Platform

Responde las preguntas conceptuales en el archivo `parte_1_gcp/respuestas.md`.

No es necesario que tengas acceso a GCP (Google Cloud Plataform) para responder — buscamos entender tu razonamiento y conocimiento de los servicios.

---

## Parte 2 — Python y procesamiento de datos

En la carpeta `datos/` encontrarás un archivo de datos real de vehículos livianos del sistema de certificación vehicular chileno. Contiene variables técnicas como tipo de combustible, emisiones, consumo energético e identificación del vehículo.

Debes completar las siguientes tareas y dejar tus scripts en la carpeta `parte_2_python/`:

### Tarea 1 — Diagnóstico de calidad
Genera un reporte de calidad de la base. El entregable lo defines tu. Ten en consideración quien será el cliente final del reporte.

### Tarea 2 — Limpieza y estandarización
Escribe un script que limpie la base aplicando al menos 5 mejoras justificadas. 
Consideraciones: 
- El script será evaluado
- El output debe ser la base limpia lista para análisis. Importante: *No* debes adjuntar la base limpia, ya que esta se obtendrá una vez corramos tu código. 

### Tarea 3 — Orquestación
Diseña un orquestador simple en Python que encadene al menos 3 scripts. El objetivo es que utilice los scripts que creaste en las tareas anteriores.

El orquestador debe reflejar cómo estructurarías un pipeline real.

Hint tarea 3: Para esta tarea ten en consideración que los tres puntos están relacionados.

---

## Lo que evaluamos

| Criterio | Qué miramos |
|---|---|
| Calidad del código | ¿Es modular, legible y mantenible por otro? |
| Criterio técnico | ¿Las decisiones de limpieza están justificadas? |
| GCP | ¿Entiende los servicios y cuándo usar cada uno? |
| Documentación | ¿El repositorio tiene README? ¿El código tiene comentarios útiles? |
| Autonomía | ¿Resolvió ambigüedades sin preguntar todo? |
| Funcionalidad | ¿El orquestador funciona? |
| Facilidad | ¿Es fácil para alguien más ejecutar los scripts? |

---

*Centro de Movilidad Sostenible — cmsostenible.org*

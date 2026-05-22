# Procesador Base de Vehiculos livianos
El pipeline diagnostica la calidad de la base, la limpia y valida el resultado, dejando una base lista
para análisis.

## Descripción

El proceso se compone de tres etapas encadenadas por un orquestador:

1. Diagnóstico — se mide el estado de la base cruda (valores faltantes,
   duplicados, tipos de dato, estadísticas).
2. Limpieza — se corrigen los problemas detectados y se genera la base limpia.
3. Validación — se verifica que la limpieza efectivamente funcionó.

El diseño sigue la lógica de un pipeline real: diagnosticar antes de limpiar,
y validar la salida antes de darla por buena.

## Estructura del repositorio

```
.
├── datos/
│   └── base_vehiculos_livianos.xlsx     # archivo de entrada
└── parte_2_python/
    ├── Reporte_Calidad.py               # Tarea 1 — diagnóstico de calidad
    ├── Limpieza_y_Estandarizacion.py    # Tarea 2 — limpieza
    ├── Validacion.py                    # Tarea 3 — validación post-limpieza
    ├── Orquestador.py                   # Tarea 3 — orquestador del pipeline
    ├── requirements.txt
    └── README.md
```

## Flujo del pipeline

```
        base_vehiculos_livianos.xlsx
                    │
                    ▼
          Reporte_Calidad.py ──────────▶ reporte_calidad.xlsx
                    │
                    ▼
   Limpieza_y_Estandarizacion.py ───────▶ base_limpia.csv
                    │
                    ▼
             Validacion.py ─────────────▶ OK / FALLO

   Orquestador.py ejecuta las 3 etapas en orden y detiene el
   pipeline si alguna falla.
```

## Detalle de los scripts

### Reporte_Calidad.py — Tarea 1
Diagnostica la base cruda y genera `reporte_calidad.xlsx`, un Excel con unahoja por sección: resumen general, valores faltantes, estadísticas numéricas y estadísticas categóricas. Solo diagnostica; no modifica los datos.

### Limpieza_y_Estandarizacion.py — Tarea 2
Aplica 6 mejoras de calidad y genera `base_limpia.csv`:

| # | Mejora | Justificación |
|---|--------|---------------|
| 1 | Reconstruir nombres de columna | El encabezado del Excel está partido en dos filas (sección y nombre); se combinan en "Sección.Columna" |
| 2 | Eliminar filas casi vacías | Una fila con más del 30% de columnas vacías no es un registro útil |
| 3 | Convertir columnas numéricas guardadas como texto | Sin convertirlas no se pueden hacer cálculos |
| 4 | Estandarizar texto | Los espacios sobrantes hacen que un valor se cuente como dos categorías |
| 5 | Estandarizar la columna Transmisión | Unifica variantes ("A", "a", "Automática"...) en categorías consistentes |
| 6 | Eliminar filas duplicadas | Las filas repetidas inflan cualquier conteo |


### Validacion.py — Tarea 3
Verifica que `base_limpia.csv` pasó la limpieza, con tres chequeos: que no
queden filas duplicadas, que las columnas numéricas sean numéricas y que la
columna Transmisión tenga solo dos categorías. Si algún chequeo falla, el
script termina con código de error.

### Orquestador.py — Tarea 3
Ejecuta los tres scripts en orden. Revisa el código de salida de cada etapa
y, si una falla, detiene el pipeline sin ejecutar las siguientes, para no
trabajar sobre datos defectuosos.

## Requisitos

- Python 3.10 o superior
- Dependencias en `requirements.txt` (pandas, openpyxl)

## Cómo ejecutar

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/USUARIO/REPO.git
   cd REPO
   ```
2. Entrar a la carpeta del proyecto e instalar las dependencias:
   ```bash
   cd parte_2_python
   pip install -r requirements.txt
   ```
3. Ejecutar el pipeline completo:
   ```bash
   python Orquestador.py
   ```

Cada script también puede ejecutarse de forma independiente con
`python <nombre_del_script>.py`.

## Salidas

Al correr el pipeline se generan, dentro de `parte_2_python/`:

| Archivo | Generado por | Contenido |
|---------|--------------|-----------|
| `reporte_calidad.xlsx` | Reporte_Calidad.py | Diagnóstico de calidad de la base cruda |
| `base_limpia.csv` | Limpieza_y_Estandarizacion.py | Base limpia, lista para análisis |
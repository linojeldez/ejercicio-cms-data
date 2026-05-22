# Reporte de Calidad de Datos
# Parte 2 - Tarea 1

# Lee el archivo de la carpeta datos/ del repositorio y genera el archivo reporte_calidad.xlsx con el diagnostico de calidad.

from pathlib import Path
import pandas as pd

# ------------------------------------------------------------
# 1. RUTAS
# ------------------------------------------------------------
# Las rutas se calculan relativas a la ubicacion de ESTE archivo, no al directorio desde donde se ejecuta. 
#
# Estructura esperada del repositorio:
#   repo/
#   -- datos/
#       -- base_vehiculos_livianos.xlsx            <- el archivo de entrada
#   -- parte_2_python/
#       -- reporte_calidad.py  <- este script
#       -- reporte_calidad.xlsx  <- output del script, el entregable

CARPETA_SCRIPT = Path(__file__).resolve().parent
CARPETA_DATOS = CARPETA_SCRIPT.parent / "datos"
ARCHIVO_SALIDA = CARPETA_SCRIPT / "reporte_calidad.xlsx"

# ------------------------------------------------------------
# 2. CARGAR LOS DATOS
# ------------------------------------------------------------
# El archivo es un Excel. Sus dos primeras filas no son datos:
# la fila 1 es el titulo de la base y la fila 2 son los nombres de las secciones. Por eso se usa skiprows=2: asi la fila con
# los nombres reales de las columnas queda como encabezado.

ruta = sorted(CARPETA_DATOS.glob("*.xlsx"))[0]
df = pd.read_excel(ruta, sheet_name=0, skiprows=2)

print("Archivo cargado:", ruta.name)

# ------------------------------------------------------------
# 3. VISTA GENERAL
# ------------------------------------------------------------
# Se definen algunas metricas generales para tener una idea rapida de la calidad del dataset. 
# Estas metricas se resumen en un DataFrame que se imprime en consola y se guarda en el Excel final.

resumen_general = pd.DataFrame({
    "metrica": ["Filas", "Columnas", "Filas duplicadas",
                "Celdas vacias"],
    "valor": [
        len(df),
        df.shape[1],
        int(df.duplicated().sum()),
        int(df.isna().sum().sum()),
    ],
})

print("\n===== RESUMEN GENERAL =====")
print(resumen_general.to_string(index=False))

# ------------------------------------------------------------
# 2. DETECCION DE TIPOS
# ------------------------------------------------------------
# Varias columnas que son numericas (emisiones, rendimiento, potencia, etc.) llegan guardadas como texto en el Excel. Aqui
# solo se detectan y se reportan: se prueba convertir cada columna de texto a numero y, si al menos el 80% de sus valores se
# convertirian bien, se marca como "numerica guardada como texto".
# El tipo NO se cambia en este script: este es el reporte de calidad y solo diagnostica. 

columnas_texto_numerico = []
for col in df.columns:
    if df[col].dtype == object:
        convertida = pd.to_numeric(df[col], errors="coerce")
        no_nulos_original = df[col].notna().sum()
        no_nulos_convertida = convertida.notna().sum()
        if no_nulos_original > 0 and no_nulos_convertida / no_nulos_original >= 0.8:
            columnas_texto_numerico.append(col)

print("\n===== DETECCION DE TIPOS =====")
if columnas_texto_numerico:
    print("Columnas numericas que vienen guardadas como texto:")
    for col in columnas_texto_numerico:
        print("  -", col)
else:
    print("No se detectaron columnas con tipo incorrecto.")

# ------------------------------------------------------------
# 5. VALORES FALTANTES
# ------------------------------------------------------------
# Cuantos datos faltan por columna. Esto es importante para decidir si se pueden usar ciertas columnas o si hay que descartarlas.
# Ordenado de mayor a menor para priorizar las columnas mas problematicas. 

faltantes = df.isna().sum()
tabla_faltantes = pd.DataFrame({
    "columna": faltantes.index,
    "faltantes": faltantes.values,
    "porcentaje_%": (faltantes.values / len(df) * 100).round(1),
}).sort_values("faltantes", ascending=False)

print("\n===== VALORES FALTANTES =====")
print(tabla_faltantes.to_string(index=False))

# ------------------------------------------------------------
# 6. ESTADISTICAS NUMERICAS
# ------------------------------------------------------------
# Para cada columna numerica, ademas del resumen basico, se calcula la calidad de los datos con estas metricas:
#  - media, mediana, desv_std: resumen basico de la distribucion.
#  - n_ceros / n_negativos: posibles errores. Un negativo en una
#    magnitud fisica (emisiones, consumo) es necesariamente un error.
#  - n_outliers: valores extremos segun el rango intercuartil (IQR),
#    el criterio estadistico estandar para detectar valores atipicos.

filas_num = []
for col in df.select_dtypes(include="number").columns:
    serie = df[col].dropna()
    if len(serie) == 0:
        continue
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    es_outlier = (serie < q1 - 1.5 * iqr) | (serie > q3 + 1.5 * iqr)
    filas_num.append({
        "columna": col,
        "media": round(serie.mean(), 2),
        "mediana": round(serie.median(), 2),
        "desv_std": round(serie.std(), 2),
        "minimo": round(serie.min(), 2),
        "maximo": round(serie.max(), 2),
        "n_ceros": int((serie == 0).sum()),
        "n_negativos": int((serie < 0).sum()),
        "n_outliers": int(es_outlier.sum()),
    })
tabla_numericas = pd.DataFrame(filas_num)

print("\n===== ESTADISTICAS NUMERICAS =====")
print(tabla_numericas.to_string(index=False) if len(tabla_numericas)
      else "Sin columnas numericas.")

# ------------------------------------------------------------
# 7. ESTADISTICAS CATEGORICAS
# ------------------------------------------------------------
# Para cada columna de texto: cuantas categorias distintas tiene y cual es el valor mas frecuente. Una cardinalidad inesperada
# (muy alta o muy baja) suele indicar un problema de formato como mayusculas mezcladas o espacios sobrantes.

filas_cat = []
for col in df.select_dtypes(include="object").columns:
    conteo = df[col].value_counts()
    if conteo.empty:
        continue
    filas_cat.append({
        "columna": col,
        "n_categorias": df[col].nunique(),
        "valor_top": conteo.index[0],
        "frecuencia_top": int(conteo.iloc[0]),
    })
tabla_categoricas = pd.DataFrame(filas_cat)

print("\n===== ESTADISTICAS CATEGORICAS =====")
print(tabla_categoricas.to_string(index=False) if len(tabla_categoricas)
      else "Sin columnas categoricas.")

# ------------------------------------------------------------
# 8. GUARDAR EL REPORTE EN UN ARCHIVO EXCEL
# ------------------------------------------------------------
# El entregable es un un Excel con una hoja por seccion. Es importante que el formato sea claro y legible, con los nombres de las columnas descriptivos y sin indices innecesarios. 
# Se pueden agregar formatos adicionales (colores, negritas) para resaltar los problemas mas graves.

with pd.ExcelWriter(ARCHIVO_SALIDA, engine="openpyxl") as writer:
    resumen_general.to_excel(writer, sheet_name="Resumen", index=False)
    tabla_faltantes.to_excel(writer, sheet_name="Faltantes", index=False)
    tabla_numericas.to_excel(writer, sheet_name="Numericas", index=False)
    tabla_categoricas.to_excel(writer, sheet_name="Categoricas", index=False)

print("\nReporte guardado en:", ARCHIVO_SALIDA.name)
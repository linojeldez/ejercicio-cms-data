# Limpieza y Estandarizacion de Datos

# Parte 2 - Tarea 2

# Lee el archivo de la carpeta datos/ del repositorio, le aplica
# 6 mejoras de calidad y guarda la base limpia como base_limpia.csv.
#
# Mejoras aplicadas:
#   1. Reconstruir los nombres de columna (encabezado partido en 2 filas).
#   2. Eliminar filas casi vacias.
#   3. Convertir a numero las columnas numericas guardadas como texto.
#   4. Estandarizar texto: quitar espacios sobrantes.
#   5. Estandarizar la columna Transmision a categorias consistentes.
#   6. Eliminar filas duplicadas.
#
# El orden importa: la conversion numerica va antes que la limpieza de texto, y los duplicados se eliminan al final, despues de
# estandarizar (asi se detectan duplicados que solo diferian en formato).

from pathlib import Path
import pandas as pd

# ------------------------------------------------------------
# 0. RUTAS
# ------------------------------------------------------------
# Rutas relativas a la ubicacion de este archivo.

CARPETA_SCRIPT = Path(__file__).resolve().parent
CARPETA_DATOS = CARPETA_SCRIPT.parent / "datos"
ARCHIVO_SALIDA = CARPETA_SCRIPT / "base_limpia.csv"

# ------------------------------------------------------------
# MEJORA 1 - RECONSTRUIR LOS NOMBRES DE COLUMNA
# ------------------------------------------------------------
# El Excel tiene el encabezado partido en dos filas: la fila 2 es la seccion a la que pertenece cada columna y la fila 3 es el
# nombre de la columna. Para tener nombres de columna identificables se reconstruyen combinando seccion y nombre en "Seccion.Columna".

ruta = sorted(CARPETA_DATOS.glob("*.xlsx"))[0]

# Leer solo las dos filas de encabezado (fila 2 = seccion, fila 3 = columna)
encabezados = pd.read_excel(ruta, sheet_name=0, skiprows=1, nrows=2, header=None)

# En la fila de secciones el nombre aparece una sola vez por grupo
# (celdas combinadas); ffill() lo propaga al resto de columnas del grupo.
secciones = encabezados.iloc[0].ffill()
nombres = encabezados.iloc[1]
columnas = [f"{seccion}.{nombre}" for seccion, nombre in zip(secciones, nombres)]

# Leer los datos (desde la fila 4) y asignarles los nombres combinados
df = pd.read_excel(ruta, sheet_name=0, skiprows=3, header=None)
df.columns = columnas

filas_iniciales = len(df)
print(f"Mejora 1: nombres de columna reconstruidos ({df.shape[1]} columnas)")

# ------------------------------------------------------------
# MEJORA 2 - ELIMINAR FILAS CASI VACIAS
# ------------------------------------------------------------
# Una fila a la que le falta gran parte de los datos no es un registro util. Se eliminan las filas con mas del 30% de sus columnas vacias. 
# Va antes de la conversion numerica para contar solo las celdas realmente vacias, sin confundirse con los datos faltantes que
# vienen escritos como texto.

limite_vacias = df.shape[1] * 0.3
filas_vacias = df.isna().sum(axis=1) > limite_vacias
df = df[~filas_vacias].copy()
print(f"Mejora 2: {int(filas_vacias.sum())} fila eliminada por tener mas del 30% de sus columnas vacias")

# ------------------------------------------------------------
# MEJORA 3 - CONVERTIR COLUMNAS NUMERICAS GUARDADAS COMO TEXTO
# ------------------------------------------------------------
# Varias columnas numericas (emisiones, rendimiento, potencia, etc) vienen como texto, ademas con los datos faltantes escritos como
# el caracter "-". Sin convertirlas no se pueden hacer calculos. pd.to_numeric transforma el "-" y cualquier valor no numerico en NaN. 
# Se adopta la version numerica solo si al menos el 80% de los valores se convierten bien (asi no se tocan columnas como los
# codigos o el N de certificado, que tienen letras).

columnas_convertidas = []
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_datetime64_any_dtype(df[col]):
        continue
    convertida = pd.to_numeric(df[col], errors="coerce")
    no_nulos_orig = df[col].notna().sum()
    if no_nulos_orig > 0 and convertida.notna().sum() / no_nulos_orig >= 0.8:
        df[col] = convertida
        columnas_convertidas.append(col)
print(f"Mejora 3: {len(columnas_convertidas)} columna convertida a numero")

# ------------------------------------------------------------
# MEJORA 4 - ESTANDARIZAR TEXTO (ESPACIOS SOBRANTES)
# ------------------------------------------------------------
# Los espacios al inicio o al final hacen que un mismo valor se cuente como dos categorias distintas (ej: "Diesel" y "Diesel ").
# Se quitan los espacios solo de los valores de texto; los numeros y las fechas quedan intactos.

for col in df.columns:
    df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
print("Mejora 4: espacios sobrantes eliminados en columnas de texto")

# ------------------------------------------------------------
# MEJORA 5 - ESTANDARIZAR LA COLUMNA TRANSMISION
# ------------------------------------------------------------
# La columna de transmision tiene el mismo valor escrito de muchas
# formas: "A", "a", "Automatica", "automatica" son todos automatico;
# "M", "Manual", "manual" son todos manual. Se estandarizan a "Automatica" y "Manual".

col_transmision = [c for c in df.columns if "Transmisión" in c][0]
mapa_transmision = {
    "A": "Automática", "a": "Automática",
    "Automática": "Automática", "automatica": "Automática",
    "T/A CVT": "Automática", "T/A DCT": "Automática",
    "M": "Manual", "m": "Manual",
    "Manual": "Manual", "manual": "Manual",
}
df[col_transmision] = df[col_transmision].replace(mapa_transmision)
print(f"Mejora 5: columna de transmision estandarizada ")

# ------------------------------------------------------------
# MEJORA 6 - ELIMINAR FILAS DUPLICADAS
# ------------------------------------------------------------
# Las filas repetidas por completo inflan cualquier conteo. Se eliminan al final, despues de estandarizar texto y tipos, para
# que tambien se detecten filas que solo diferian en el formato.

duplicados = int(df.duplicated().sum())
df = df.drop_duplicates()
print(f"Mejora 6: {duplicados} fila(s) duplicada(s) eliminada(s)")

# ------------------------------------------------------------
# GUARDAR LA BASE LIMPIA
# ------------------------------------------------------------
# Se reinicia el indice (quedo con huecos tras eliminar filas) y se guarda como CSV. encoding="utf-8-sig" para que los acentos se
# vean bien al abrir el archivo en Excel.

df = df.reset_index(drop=True)
df.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")

print(f"\nBase limpia guardada en: {ARCHIVO_SALIDA.name}")
print(f"Filas: {filas_iniciales} -> {len(df)}")

# Validacion Post-Limpieza 

# Parte 2 - Tarea 3


# Toma la base limpia (base_limpia.csv, generada por Limpieza_y_Estandarizacion.py) y verifica que la limpieza realmente funciono. Si algun chequeo
# no se cumple, el script termina con codigo de error distinto de cero, para que el orquestador detenga el pipeline.

from pathlib import Path
import sys
import pandas as pd

# ------------------------------------------------------------
# 0. RUTAS
# ------------------------------------------------------------
# Rutas relativas a la ubicacion de este archivo.

CARPETA_SCRIPT = Path(__file__).resolve().parent
ARCHIVO_LIMPIO = CARPETA_SCRIPT / "base_limpia.csv"

# ------------------------------------------------------------
# 1. CARGAR LA BASE LIMPIA
# ------------------------------------------------------------
# Si el archivo no existe, la limpieza no se ejecuto: se falla de inmediato para que el orquestador no continue.

if not ARCHIVO_LIMPIO.exists():
    print("FALLO - No se encontro base_limpia.csv. Ejecuta limpieza.py primero.")
    sys.exit(1)

df = pd.read_csv(ARCHIVO_LIMPIO)
print("Base limpia cargada:", df.shape[0], "filas,", df.shape[1], "columnas")
print("\n===== CHEQUEOS DE CALIDAD =====")

# Contador de chequeos que no pasaron.
errores = 0

# ------------------------------------------------------------
# CHEQUEO 1 - NO QUEDAN FILAS DUPLICADAS
# ------------------------------------------------------------
# La limpieza debio eliminar todos los duplicados completos.

n_duplicados = int(df.duplicated().sum())
if n_duplicados == 0:
    print("OK    - Sin filas duplicadas")
else:
    print(f"FALLO - Quedan {n_duplicados} fila(s) duplicada(s)")
    errores += 1

# ------------------------------------------------------------
# CHEQUEO 2 - LAS COLUMNAS NUMERICAS SON NUMERICAS
# ------------------------------------------------------------
# Las 7 columnas que venian como texto debieron quedar convertidas a numero. Se busca cada una por una palabra clave de su nombre y
# se verifica su tipo.

columnas_que_deben_ser_numericas = [
    "Certificación.Norma Europea",
    "Emisiones y Rendimiento.Emisiones de CO2 (g/km)",
    "Emisiones y Rendimiento.Rendimiento de Combustible (km/l)",
    "Emisiones y Rendimiento.Potencia Máxima del Motor (kw)",
    "Dimensiones e Importador.Distancia entre ejes (mm)",
    "Dimensiones e Importador.Ancho vehículo (mm)",
    "Dimensiones e Importador.Foot Print (mt2)",
]
for col in columnas_que_deben_ser_numericas:
    if col not in df.columns:
        print(f"FALLO - No se encontro la columna '{col}'")
        errores += 1
        continue
    if pd.api.types.is_numeric_dtype(df[col]):
        print(f"OK    - '{col}' es numerica")
    else:
        print(f"FALLO - '{col}' no es numerica (tipo {df[col].dtype})")
        errores += 1


# ------------------------------------------------------------
# CHEQUEO 3 - LA COLUMNA TRANSMISION TIENE SOLO 2 CATEGORIAS
# ------------------------------------------------------------
# La estandarizacion debio dejar la transmision en exactamente 2 categorias: Automatica y Manual.

col_transmision = [c for c in df.columns if "Transmisión" in c][0]
categorias = sorted(df[col_transmision].dropna().unique())
if len(categorias) == 2:
    print(f"OK    - Transmision tiene 2 categorias: {categorias}")
else:
    print(f"FALLO - Transmision tiene {len(categorias)} categorias: {categorias}")
    errores += 1

# ------------------------------------------------------------
# 2. RESULTADO FINAL
# ------------------------------------------------------------
# El codigo de salida es la senal que usa el orquestador:
#   0 -> validacion exitosa, el pipeline puede continuar.
#   1 -> validacion fallida, el orquestador debe detenerse.

print("\n===== RESULTADO =====")
if errores == 0:
    print("VALIDACION EXITOSA: la base limpia paso todos los chequeos.")
    sys.exit(0)
else:
    print(f"VALIDACION FALLIDA: {errores} chequeo(s) no pasaron.")
    sys.exit(1)
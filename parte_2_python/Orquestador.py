# Orquestador 

# ============================================================

# Encadena los 3 scripts del pipeline y los ejecuta en orden:
#
#   1. Reporte_Calidad.py                    -> diagnostica la base cruda
#   2. Limpieza_y_Estandarizacion.py         -> limpia la base y genera base_limpia.csv
#   3. Validacion.py                         -> verifica que la limpieza funciono
#
# Este orquestador ejecuta cada script como un proceso aparte, revisa su codigo de salida, y, 
# si uno falla, detiene el pipeline para no seguir trabajando sobre datos defectuosos.

from pathlib import Path
import subprocess # para ejecutar los scripts como procesos aparte
import sys      # encargado
import time

# ------------------------------------------------------------
# 0. DEFINICION DEL PIPELINE
# ------------------------------------------------------------
# Es importante que los scripts se ejecuten en este orden, porque cada uno depende de los resultados del anterior. 
# Por ejemplo, la validacion post-limpieza solo tiene sentido si se ejecuta despues de la limpieza, 
# porque necesita la base limpia para hacer sus chequeos.

CARPETA_SCRIPT = Path(__file__).resolve().parent

PIPELINE = [
    ("Diagnostico de calidad",      "Reporte_Calidad.py"),
    ("Limpieza y estandarizacion",  "Limpieza_y_Estandarizacion.py"),
    ("Validacion post-limpieza",    "Validacion.py"),
]

# ------------------------------------------------------------
# 1. EJECUCION DE LAS ETAPAS
# ------------------------------------------------------------
# Cada script se ejecuta como un proceso aparte con sys.executable
# (el mismo Python que corre este orquestador, para usar el mismo
# entorno). Se revisa el codigo de salida: 0 = exito; distinto de
# 0 = fallo, y el pipeline se detiene sin ejecutar lo que sigue.

print("-" * 55)
print("ORQUESTADOR DEL PIPELINE DE DATOS")
print("-" * 55)

# Se mide el tiempo total del pipeline, para tener una idea de cuanto tarda en correr todo.
inicio_total = time.time()                                 

# Se recorre la lista PIPELINE etapa por etapa. enumerate con start=1 entrega el numero de etapa (1, 2, 3...) ademas del
# nombre y el script, para poder mostrarlo de forma legible.
for numero, (nombre, script) in enumerate(PIPELINE, start=1):  
    print(f"\n[Etapa {numero}/{len(PIPELINE)}] {nombre}")
    print("-" * 55)

    ruta_script = CARPETA_SCRIPT / script
    inicio = time.time()
    #subprocess.run si devuelve como codigo de salida un 0 significa que termino bien, cualquier otro valor significa fallo.
    resultado = subprocess.run([sys.executable, str(ruta_script)]) 
    duracion = time.time() - inicio

    # Si la etapa fallo, se detiene todo el pipeline.
    if resultado.returncode != 0:
        print(f"PIPELINE DETENIDO: la etapa '{nombre}' fallo.")
        sys.exit(1)

    print("-" * 55)
    print(f"[Etapa {numero} completada en {duracion:.1f}s]")

# ------------------------------------------------------------
# 2. CIERRE
# ------------------------------------------------------------
# Si se llega aqui, las 3 etapas terminaron bien.

print("\n" + "-" * 55)
print(f"PIPELINE COMPLETADO - {len(PIPELINE)} etapas en "
      f"{time.time() - inicio_total:.1f}s")
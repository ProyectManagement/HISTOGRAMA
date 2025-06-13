import pandas as pd
import numpy as np
import os

np.random.seed(42)
n_estudiantes = 500
os.makedirs("datos", exist_ok=True)

data = {
    "nombre": [f"Estudiante_{i}" for i in range(1, n_estudiantes + 1)],
    "edad": np.clip(np.random.normal(22, 3, n_estudiantes), 18, 35).astype(int),
    "sexo": np.random.choice(["Masculino", "Femenino"], size=n_estudiantes, p=[0.45, 0.55]),
    "numero_hijos": np.random.poisson(0.7, size=n_estudiantes),
    "horas_trabajo": np.random.choice([0, 15, 30, 40], size=n_estudiantes, p=[0.3, 0.4, 0.2, 0.1]),
    "dependencia_economica": np.random.choice(
        ["Padres", "Trabajo propio", "Beca", "Pareja", "Autofinanciado"],
        size=n_estudiantes, 
        p=[0.5, 0.25, 0.15, 0.05, 0.05]
    ),
    "ingreso_mensual": np.abs(np.random.normal(12000, 6000, n_estudiantes)).astype(int),
    "dias_trabajo": np.random.choice(
        ["No trabaja", "L-V", "Fines de semana", "Turnos rotativos"],
        size=n_estudiantes,
        p=[0.3, 0.5, 0.15, 0.05]
    )
}

df = pd.DataFrame(data)
df.loc[df['dependencia_economica'] == 'Padres', 'ingreso_mensual'] = np.abs(np.random.normal(8000, 3000, sum(df['dependencia_economica'] == 'Padres'))).astype(int)
df.loc[df['dependencia_economica'] == 'Beca', 'ingreso_mensual'] = np.abs(np.random.normal(6000, 2000, sum(df['dependencia_economica'] == 'Beca'))).astype(int)

df.to_csv("datos/datos_estudiantes.csv", index=False)
print(f"✅ Datos guardados en: datos/datos_estudiantes.csv")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from textwrap import wrap

# Configuración
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("pastel")
os.makedirs("graficos", exist_ok=True)

def guardar_grafico(nombre, dpi=300):
    plt.savefig(f"graficos/{nombre}.png", dpi=dpi, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"📊 Gráfico guardado: graficos/{nombre}.png")

# Cargar datos
try:
    df = pd.read_csv("datos/datos_estudiantes.csv")
except FileNotFoundError:
    print("❌ Error: Ejecuta primero 'generar_datos.py'")
    exit()

# Preparar datos
df['horas_cat'] = pd.cut(df['horas_trabajo'], 
                        bins=[-1, 0, 20, 40, 100],
                        labels=['No trabaja', '<20 hrs', '20-40 hrs', '+40 hrs'])

# --------------------------------------------
# 1. INGRESO PROMEDIO POR HORAS DE TRABAJO (BARRAS)
# --------------------------------------------
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=df, x='horas_cat', y='ingreso_mensual', 
                estimator='mean', errorbar=None,
                order=['No trabaja', '<20 hrs', '20-40 hrs', '+40 hrs'])

plt.title('Ingreso Promedio por Horas Trabajadas', fontsize=16, pad=20)
plt.xlabel('Horas trabajadas por semana', fontsize=12)
plt.ylabel('Ingreso mensual promedio (MXN)', fontsize=12)

# Añadir valores
for p in ax.patches:
    ax.annotate(f"${p.get_height():,.0f}", 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), 
                textcoords='offset points')

plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
guardar_grafico('1_ingreso_por_horas')

# --------------------------------------------
# 2. INGRESO POR DEPENDENCIA ECONÓMICA (BARRAS)
# --------------------------------------------
plt.figure(figsize=(14, 7))
order = df.groupby('dependencia_economica')['ingreso_mensual'].mean().sort_values().index

ax = sns.barplot(data=df, x='dependencia_economica', y='ingreso_mensual',
                estimator='mean', errorbar=None, order=order)

plt.title('Ingreso Promedio por Fuente de Dependencia Económica', fontsize=16, pad=20)
plt.xlabel('Tipo de dependencia económica', fontsize=12)
plt.ylabel('Ingreso mensual promedio (MXN)', fontsize=12)
plt.xticks(rotation=45, ha='right')

# Añadir valores
for p in ax.patches:
    ax.annotate(f"${p.get_height():,.0f}", 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), 
                textcoords='offset points')

plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
guardar_grafico('2_ingreso_por_dependencia')
# ----------------------------------------------------------
# De otra forma no se puede comprender
# De ti estoy profundamente enamorado
# Necesario ya era hacértelo saber
# Hacerte ver que yo te amo
#
# Que mis sueños tú no dejas de existir
# Que me tienes totalmente cautivado
# Con tu forma de mirar, de sonreír
# La voluntad sencillamente me has robado
#
# Necesito decírtelo, que tú sepas que te amo
# Es preciso que entiendas que te estoy necesitando
# Que ya nada me importa, solo estar a tu lado
# Que mi vida ya es tuya y tú ni cuenta te habías dado 
# ----------------------------------------------------------

# --------------------------------------------
# 3. RELACIÓN HORAS/INGRESO CON NÚMERO DE HIJOS (BARRAS AGRUPADAS)
# --------------------------------------------
plt.figure(figsize=(16, 7))

# Crear tabla pivot
pivot_df = df.groupby(['horas_cat', 'numero_hijos'])['ingreso_mensual'].mean().unstack()

# Graficar
ax = pivot_df.plot(kind='bar', width=0.8, figsize=(16, 7))

plt.title('Ingreso Promedio por Horas Trabajadas y Número de Hijos', fontsize=16, pad=20)
plt.xlabel('Horas trabajadas por semana', fontsize=12)
plt.ylabel('Ingreso mensual promedio (MXN)', fontsize=12)
plt.xticks(rotation=0)
plt.legend(title='Número de hijos')

# Añadir valores
for p in ax.containers:
    ax.bar_label(p, fmt='$%.0f', label_type='edge', padding=3)

plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
guardar_grafico('3_ingreso_horas_hijos')

print("\n✅ Todos los gráficos de barras generados exitosamente")

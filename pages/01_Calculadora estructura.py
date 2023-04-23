import streamlit as st
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import pandas as pd

# Set page to wide mode
st.set_page_config(layout="wide")

# Get list of excel files in the specified directory
excel_files = [file for file in os.listdir("DBs") if file.endswith(".xlsx")]
excel_files_without_ext = [file.replace('.xlsx','') for file in excel_files]
lista_vigas_pilares = ['HEA', 'HEB', 'HEM', 'I-Profile', 'IPE']

# DF vacio para guardar resultados
results_df = pd.DataFrame()
# Create a dictionary to store the DataFrames
dfs = {}

# Loop por los excel files
for file in excel_files:
   # Read excel file
   df2 = pd.read_excel(os.path.join("DBs", file))
   # Filter dataframe to include only rows with the search value in the first column
   # Transpose the DataFrame
   # Set the first column as the index
   df2 = df2.set_index(df2.columns[0])
   df2 = df2.T
   df2.rename(columns=lambda x: x.replace("_x000D_", "_"), inplace=True)
   # Set the columns as the new index
   df2.index.name = "Perfil"
   df2.reset_index(inplace=True)
   df2.rename(columns={'index':df2.index.name}, inplace=True)
   # Get the first column name
   first_col = df2.columns[0]
   # Rename the first column
   df2 = df2.rename(columns={first_col: "Perfil"})
   # Add the DataFrame to the dictionary
   dfs[file] = df2

st.title("Calculadora de costes de construcción de nave industrial")
st.markdown("---")
col1, col2 = st.columns(2)
# Inputs del usuario
cantidad_porticos = col1.slider("Cantidad de pórticos", min_value=4, max_value=10, value=5)
distancia_porticos_finales = col1.number_input("Distancia entre los pórticos finales (metros)", min_value=5.0, max_value=7.0, value=5.5, step=0.1)
distancia_porticos_internos = col1.number_input("Distancia entre los pórticos internos (metros)",  min_value=5.0, max_value=7.0, value=6.0, step=0.1)
ancho_nave = col1.number_input("Ancho nave (metros)", min_value=8.0, max_value=26.0, value=18.0, step=0.25)
altura_alero = col1.number_input("Altura del alero (metros)", min_value=4.0, max_value=8.0, value=4.0, step=0.1)
inclinacion_tejado = col1.slider("Inclinación del tejado (grados)", min_value=6, max_value=30, value=12)
longitud_cartela = col1.number_input("Largo de la cartela (metros)", min_value=0.0, max_value=4.0, value=2.0, step=0.1)
altura_cartela = col1.number_input("Altura de la cartela (metros)", min_value=0.0, max_value=2.5, value=0.7, step=0.1)

# Crear figura y ejes
fig, ax = plt.subplots()

# Establecer límites de los ejes
ax.set_xlim(0, (cantidad_porticos-2)*distancia_porticos_internos + distancia_porticos_finales)
ax.set_ylim(0, ancho_nave)
# Agregar línea horizontal roja en el medio de y
ax.axhline(y=ancho_nave/2, color='red')
# Dibujar línea inferior
ax.axhline(0, xmin=0, xmax=1, color="red")
# Dibujar línea superior
ax.axhline(ancho_nave, xmin=0, xmax=1, color="red")

# Dibujar primera línea del marco
ax.axvline(-distancia_porticos_finales, color="blue")

# Variables geometria
angulo_radianes = math.radians(inclinacion_tejado)
largo_riegel = round((ancho_nave / 2) / math.cos(angulo_radianes), 2)
distancia_correas = 2
correas_internas_cantidad = 2 * math.ceil((largo_riegel - 0.2) / (distancia_correas))
correas_lado = int(correas_internas_cantidad / 2)
peso_estructura = 50
distancia_wandriegel = 2.2
cantidad_wandriegel = int(round((altura_alero - 0.4) / distancia_wandriegel,0))
distancia_real_wandriegel = (altura_alero - 0.4) / cantidad_wandriegel

# Dibujar líneas verticales
for i in range(cantidad_porticos):
    x = distancia_porticos_finales + i*distancia_porticos_internos
    ax.axvline(x, linestyle="--", color="blue")
# Obtener el último valor en el eje x y y la mitad de y
last_x = distancia_porticos_internos * (cantidad_porticos - 3) + 2 * distancia_porticos_finales
last_y = ancho_nave
middle_y = ancho_nave / 2
# Dibujar última línea del marco
ax.axvline(x + distancia_porticos_finales, color="blue")
ax.set_xticklabels([])
ax.set_yticklabels([])
# Agregar texto en el último valor del eje x
ax.text(last_x, -ancho_nave*0.05, f"{last_x:.1f}m", ha="center")
ax.text(0, -ancho_nave*0.05, f"{0:.1f}m", ha="center")
# Agregar texto en el último valor del eje y y en el medio
ax.text(-distancia_porticos_finales*0.2, last_y, f"{last_y:.1f}m", va="center", rotation="vertical")
ax.text(-distancia_porticos_finales*0.2, middle_y, f"{middle_y:.1f}m", va="center", rotation="vertical")


# Obtener valores para las líneas
line_top = ancho_nave - 0.2
line_bottom = 0.2
line_middle_top = middle_y + 0.2
line_middle_bottom = middle_y - 0.2

#Correas
# Calcular distancia total
total_distance = line_top - line_bottom
espacio_correas = (total_distance / 2) - 0.2 - 1.2

# Calcular distancia entre líneas
line_distance = espacio_correas / correas_lado
# Dibujar líneas horizontales
for i in range(correas_lado):
    y = line_bottom + line_distance * (i + 1)
    ax.axhline(y=y, linestyle="--", color="green")
# Dibujar líneas horizontales
for i in range(correas_lado):
    y = line_top - line_distance * (i + 1)
    ax.axhline(y=y, linestyle="--", color="green")


# Agregar líneas horizontales
ax.axhline(line_top, linestyle="--", color="green")
ax.axhline(line_bottom, linestyle="--", color="green")
ax.axhline(line_middle_top, linestyle="--", color="green")
ax.axhline(line_middle_bottom, linestyle="--", color="green")


##################CORREAS TRAUFE IZQUIERDA#################################################
# Get the coordinates of the first line
x1 = 0
y1 = line_bottom, line_top

x2 = distancia_porticos_finales
y2 = line_bottom + line_distance, line_top - line_distance
# Plot a red line between the two points
ax.plot([x1, x2], [y1, y2], color='red')

# Get the coordinates of the second line
x1 = 0
y1 = line_bottom + line_distance, line_top - line_distance

x2 = distancia_porticos_finales
y2 = line_bottom, line_top

# Plot a red line between the two points
ax.plot([x1, x2], [y1, y2], color='red')
##################CORREAS CENTRALES IZQUIERDA#################################################
# Get the coordinates of the first line
x1f = 0
y1f = middle_y - 0.2,  correas_lado * line_distance + 0.2

x2f = distancia_porticos_finales
y2f = correas_lado * line_distance + 0.2, middle_y - 0.2
# Plot a red line between the two points
ax.plot([x1f, x2f], [y1f, y2f], color='red')

# Get the coordinates of the second line
x1f = 0
y1f = line_bottom + line_distance, line_top - line_distance

x2f = distancia_porticos_finales
y2f = line_bottom, line_top

# Plot a red line between the two points
ax.plot([x1f, x2f], [y1f, y2f], color='red')


# Get the coordinates of the first line
x1f2 = 0
y1f2 = middle_y + 0.2, last_y - (correas_lado * line_distance + 0.2)

x2f2 = distancia_porticos_finales
y2f2 = last_y - (correas_lado * line_distance + 0.2), middle_y + 0.2
# Plot a red line between the two points
ax.plot([x1f2, x2f2], [y1f2, y2f2], color='red')

# Get the coordinates of the second line
x1f2 = 0
y1f2 = line_bottom + line_distance, line_top - line_distance

x2f2 = distancia_porticos_finales
y2f2 = line_bottom, line_top

# Plot a red line between the two points
ax.plot([x1f2, x2f2], [y1f2, y2f2], color='red')

##################ARRIOSTRAMIENTOS CENTRALES#################################################
# Get the coordinates of the first line
x1f = last_x + 0.5
y1f = middle_y - 0.2,  correas_lado * line_distance + 0.2

x2f = last_x - distancia_porticos_finales
y2f = correas_lado * line_distance + 0.2, middle_y - 0.2
# Plot a red line between the two points
ax.plot([x1f, x2f], [y1f, y2f], color='red')


# Get the coordinates of the first line
x1f2 = last_x + 0.5
y1f2 = middle_y + 0.2, last_y - (correas_lado * line_distance + 0.2)

x2f2 = last_x - distancia_porticos_finales
y2f2 = last_y - (correas_lado * line_distance + 0.2), middle_y + 0.2
# Plot a red line between the two points
ax.plot([x1f2, x2f2], [y1f2, y2f2], color='red')

###################################################################

###############ARRIOSTRAMIENTOS TRAUFE DERECHA##########################

# Get the coordinates of the first line
x1e = last_x + 0.5
y1e = line_bottom, line_top


x2e = x1e - distancia_porticos_finales - 0.5
y2e = line_bottom + line_distance, line_top - line_distance

# Calcular la distancia entre los dos puntos
longitud_arrios = round(((x2e - x1e) ** 2 + ((line_bottom + line_distance) - line_bottom) ** 2) ** 0.5,2)

# Plot a red line between the two points
ax.plot([x1e, x2e], [y1e, y2e], color='red')

# Get the coordinates of the second line
x1e = last_x + 0.5
y1e = line_bottom + line_distance, line_top - line_distance

x2e = x1e - distancia_porticos_finales - 0.5
y2e = line_bottom, line_top

# Plot a red line between the two points
ax.plot([x1e, x2e], [y1e, y2e], color='red')

###################################################################
ax.set_title("Vista superior")
# Set the aspect ratio of the axes to be equal
ax.set_aspect('equal')

# Set the initial Y coordinates
y1 = line_bottom
y2 = line_bottom + line_distance
y3 = line_top
y4 = line_top - line_distance

# Copy and paste the lines correas_lado - 1 times
for i in range(correas_lado - 1):
    # Update the Y coordinates
    y1 += line_distance
    y2 += line_distance
    y3 -= line_distance
    y4 -= line_distance

    # Plot the lines with the updated coordinates
    ax.plot([0, distancia_porticos_finales], [y1, y2], color='red')
    ax.plot([0, distancia_porticos_finales], [y3, y4], color='red')

    ax.plot([last_x + 0.5, last_x-distancia_porticos_finales], [y1, y2], color='red')
    ax.plot([last_x + 0.5, last_x-distancia_porticos_finales], [y3, y4], color='red')

# Set the initial Y coordinates
y11 = line_bottom + line_distance
y12 = line_bottom
y13 = line_top - line_distance
y14 = line_top

# Copy and paste the lines correas_lado - 1 times
for i in range(correas_lado - 1):
    # Update the Y coordinates
    y11 += line_distance
    y12 += line_distance
    y13 -= line_distance
    y14 -= line_distance

    # Plot the lines with the updated coordinates
    ax.plot([0, distancia_porticos_finales], [y11, y12], color='red')
    ax.plot([0, distancia_porticos_finales], [y13, y14], color='red')
    ax.plot([last_x + 0.5, last_x-distancia_porticos_finales], [y11, y12], color='red')
    ax.plot([last_x + 0.5, last_x-distancia_porticos_finales], [y13, y14], color='red')


# Mostrar figura dentro del app
col2.pyplot(fig)



# Crear figura y ejes
fig_nave, ax = plt.subplots()

# Establecer límites de los ejes
ax.set_xlim(-0.5, ancho_nave+0.5)
ax.set_ylim(-0.5, altura_alero + 2*largo_riegel*np.sin(np.deg2rad(inclinacion_tejado)))

# Agregar línea roja en el eje x
ax.axhline(y=0, color='black', linewidth=0.5, xmin=0.0, xmax=ancho_nave)

perfilestipo_columnas = col1.selectbox("Selecciona el tipo de perfil", lista_vigas_pilares, index=4)

df_pilar = dfs[perfilestipo_columnas+".xlsx"]

# Update the pillar lines

# After getting pilar_peso_m
selector_pilar = col1.selectbox("Seleccionar perfil para los pilares", key = "droppilar", options=df_pilar["Perfil"].tolist(), index=12)
pilar_ancho = df_pilar.loc[df_pilar["Perfil"] == selector_pilar, "Altura h [mm]"].iloc[0] / 1000  # Convert to meters

ax.plot([0, 0], [0, altura_alero], color='blue', linewidth=1)
ax.plot([pilar_ancho, pilar_ancho], [0, altura_alero], color='blue', linewidth=1)
ax.plot([ancho_nave, ancho_nave], [0, altura_alero], color='blue', linewidth=1)
ax.plot([ancho_nave - pilar_ancho, ancho_nave - pilar_ancho], [0, altura_alero], color='blue', linewidth=1)


pilar_peso_m = df_pilar.loc[df_pilar["Perfil"] == selector_pilar, "gk [kg/m]"].iloc[0]


col1.markdown("---")
perfilestipo_vigas = col1.selectbox("Selecciona el tipo de perfil para las vigas", lista_vigas_pilares, index=4)
df_viga = dfs[perfilestipo_vigas+".xlsx"]
selector_viga = col1.selectbox("Seleccionar perfil", key = "dropviga", options=df_viga["Perfil"].tolist(), index=12)
viga_ancho = df_viga.loc[df_viga["Perfil"] == selector_viga, "Altura h [mm]"].iloc[0] / 1000  # Convert to meters

# Calcular coordenadas de la línea inclinada
x_start = 0
y_start = altura_alero
x_end = largo_riegel * math.cos(angulo_radianes)
y_end = altura_alero + largo_riegel * math.sin(angulo_radianes)
# Calcular coordenadas de la segunda línea inclinada
x2_start = ancho_nave
y2_start = altura_alero
x2_end = largo_riegel*np.cos(np.deg2rad(inclinacion_tejado))
y2_end = altura_alero + largo_riegel*np.sin(np.deg2rad(inclinacion_tejado))
# Agregar línea inclinada riegel
ax.plot([x_start, x_end], [y_start, y_end], color='blue', linewidth=1)
# Agregar línea inclinada riegel derecha
ax.plot([x2_start, x2_end], [y2_start, y2_end], color='blue', linewidth=1)

#Grosor viga
# Calculate the angle perpendicular to the inclined lines
perpendicular_angle = inclinacion_tejado + 90

# Calculate the offset in x and y coordinates
offset_x = viga_ancho * np.cos(np.deg2rad(perpendicular_angle))
offset_y = viga_ancho * np.sin(np.deg2rad(perpendicular_angle))


# Calcular longitud pilar viga
longitud_pilar_riegel = pilar_ancho * math.tan(angulo_radianes)
# Agregar linea
ax.plot([pilar_ancho, pilar_ancho], [altura_alero, altura_alero + longitud_pilar_riegel], color='blue', linewidth=1)
ax.plot([ancho_nave-pilar_ancho, ancho_nave-pilar_ancho], [altura_alero, altura_alero + longitud_pilar_riegel], color='blue', linewidth=1)

# Subtract the offset from the original coordinates of the inclined lines
x_start_offset = x_start - offset_x
y_start_offset = y_start - offset_y
x_end_offset = x_end - offset_x
y_end_offset = y_end - offset_y
x2_start_offset = x2_start + offset_x
y2_start_offset = y2_start - offset_y
x2_end_offset = x2_end + offset_x
y2_end_offset = y2_end - offset_y

# Agregar línea azul First
ax.plot([x_end, x_end], [y_end, y_end_offset], color='blue', linewidth=1)

pilar_viga_interseccion_y = altura_alero + longitud_pilar_riegel - offset_y

point1 = (pilar_ancho, pilar_viga_interseccion_y)
point2 = (x_end_offset, y_end_offset)
distance = 2.3


def point_along_line(pt1, pt2, distance):
   pt1_np = np.array(pt1)
   pt2_np = np.array(pt2)

   # Calculate the direction vector
   direction = pt2_np - pt1_np

   # Normalize the direction vector
   unit_vector = direction / np.linalg.norm(direction)

   # Multiply the unit vector by the desired distance
   displacement = unit_vector * distance

   # Add the displacement to the first point's coordinates
   result = pt1_np + displacement

   return result.tolist()

caca1, caca2 = point_along_line(point1, point2, distance)
def rotate_vector(vector, angle_degrees):
   angulo_radianes = np.radians(angle_degrees)
   rotation_matrix = np.array([[np.cos(angulo_radianes), -np.sin(angulo_radianes)],
                               [np.sin(angulo_radianes), np.cos(angulo_radianes)]])
   return np.matmul(rotation_matrix, vector)


# Calculate the direction vector of the reference line
prev_line_direction = np.array([x_end - pilar_ancho, y_end_offset - pilar_viga_interseccion_y])

# Rotate the direction vector by 90 degrees minus the additional angle (roof inclination)
total_angle = 90
rotated_vector = rotate_vector(prev_line_direction, total_angle)

# Normalize the rotated vector to get a unit vector
unit_vector = rotated_vector / np.linalg.norm(rotated_vector)

# Multiply the unit vector by the desired length (viga_ancho)
displacement = unit_vector * viga_ancho

# Add the resulting vector to the endpoint of the previous line (caca1, caca2) to get the endpoint of the new line
new_line_endpoint = np.array([caca1, caca2]) + displacement

# Plot the parallel lines with the offset
ax.plot([caca1, x_end], [caca2, y_end_offset], color='blue', linewidth=1)
ax.plot([ancho_nave-caca1, x2_end], [caca2, y2_end_offset], color='blue', linewidth=1)

# Plot placas cartelas
ax.plot([caca1, new_line_endpoint[0]], [caca2, new_line_endpoint[1]], color='blue', linewidth=1)
ax.plot([ancho_nave - caca1, ancho_nave - new_line_endpoint[0]], [caca2, new_line_endpoint[1]], color='blue', linewidth=1)
altura_cartela = altura_cartela - offset_y

# Cartela izquierda
ax.plot([pilar_ancho, caca1], [pilar_viga_interseccion_y - altura_cartela, caca2], color='blue', linewidth=1)
ax.plot([0, pilar_ancho], [pilar_viga_interseccion_y - altura_cartela, pilar_viga_interseccion_y - altura_cartela], color='blue', linewidth=1)
# Cartela derecha
ax.plot([ancho_nave - pilar_ancho, ancho_nave - caca1], [pilar_viga_interseccion_y - altura_cartela, caca2], color='blue', linewidth=1)
ax.plot([ancho_nave, ancho_nave - pilar_ancho], [pilar_viga_interseccion_y - altura_cartela, pilar_viga_interseccion_y - altura_cartela], color='blue', linewidth=1)


# Lineas Wandriegel
# Initial line
x1, x2 = 0, 0 - 0.16
x3, x4 = ancho_nave, ancho_nave + 0.16
y1, y2 = 0.25, 0.25

for i in range(cantidad_wandriegel+1):
   ax.plot([x1, x2], [y1, y2], color='blue', linewidth=1)
   ax.plot([x3, x4], [y1, y2], color='blue', linewidth=1)

   # Move the line in the positive y direction
   y1 += distancia_real_wandriegel
   y2 += distancia_real_wandriegel


# Agregar título al gráfico
ax.set_title("Vista frontal")
# Set the aspect ratio of the axes to be equal
ax.set_aspect('equal')

############################### Correas lado izquierdo

offset_along_line = 0.2
perpendicular_length = 0.18

# Calculate the direction vector and unit vector of the reference line
ref_line_direction = np.array([x_end - x_start, y_end - y_start])
ref_line_unit_vector = ref_line_direction / np.linalg.norm(ref_line_direction)

# Calculate the starting points of the perpendicular lines
start_point1 = np.array([x_start, y_start]) + ref_line_unit_vector * offset_along_line
start_point2 = np.array([x_end, y_end]) - ref_line_unit_vector * offset_along_line

# Rotate the unit vector by ±90 degrees to obtain the direction vectors for the perpendicular lines
perpendicular_direction1 = rotate_vector(ref_line_unit_vector, 90)
perpendicular_direction2 = rotate_vector(ref_line_unit_vector, -90)

# Multiply the perpendicular direction vectors by the desired length
displacement1 = perpendicular_direction1 * perpendicular_length
displacement2 = perpendicular_direction2 * perpendicular_length

# Calculate the endpoints of the perpendicular lines
end_point1 = start_point1 + displacement1
end_point2 = start_point1 + displacement2
end_point3 = start_point2 + displacement1
end_point4 = start_point2 + displacement2

# Lineas Traufpfette Firstpfette
ax.plot([start_point1[0], end_point1[0]], [start_point1[1], end_point1[1]], color='blue', linewidth=1)
ax.plot([start_point2[0], end_point3[0]], [start_point2[1], end_point3[1]], color='blue', linewidth=1)

# Calculate the distance between the two starting points of the perpendicular lines
distance_between_points = np.linalg.norm(start_point2 - start_point1)

# Divide the distance by the number of lines you want to draw (correas_lado + 1) to obtain the spacing between the lines
spacing = distance_between_points / (correas_lado + 1)

# Iterate from 1 to correas_lado, calculate the starting point of each line, and draw a perpendicular line with the specified length
for i in range(1, correas_lado + 1):
    current_start_point = start_point1 + ref_line_unit_vector * (i * spacing)
    current_end_point1 = current_start_point + displacement1
    ax.plot([current_start_point[0], current_end_point1[0]], [current_start_point[1], current_end_point1[1]], color='blue', linewidth=1)

############################### Correas lado derecho

x2_start = ancho_nave
y2_start = altura_alero
x2_end = ancho_nave - largo_riegel * math.cos(angulo_radianes)
y2_end = altura_alero + largo_riegel * math.sin(angulo_radianes)

# Calculate the direction vector and unit vector of the new reference line
ref_line2_direction = np.array([x2_end - x2_start, y2_end - y2_start])
ref_line2_unit_vector = ref_line2_direction / np.linalg.norm(ref_line2_direction)

# Calculate the starting points of the perpendicular lines
start_point3 = np.array([x2_start, y2_start]) + ref_line2_unit_vector * offset_along_line
start_point4 = np.array([x2_end, y2_end]) - ref_line2_unit_vector * offset_along_line

# Rotate the unit vector by ±90 degrees to obtain the direction vectors for the perpendicular lines
perpendicular_direction3 = rotate_vector(ref_line2_unit_vector, 90)
perpendicular_direction4 = rotate_vector(ref_line2_unit_vector, -90)

# Multiply the perpendicular direction vectors by the desired length
displacement3 = perpendicular_direction3 * perpendicular_length
displacement4 = perpendicular_direction4 * perpendicular_length

# Calculate the endpoints of the perpendicular lines
end_point5 = start_point3 + displacement3
end_point6 = start_point3 + displacement4
end_point7 = start_point4 + displacement3
end_point8 = start_point4 + displacement4

# Plot the perpendicular lines
ax.plot([start_point3[0], end_point6[0]], [start_point3[1], end_point6[1]], color='blue', linewidth=1)
ax.plot([start_point4[0], end_point8[0]], [start_point4[1], end_point8[1]], color='blue', linewidth=1)

# Iterate from 1 to correas_lado, calculate the starting point of each line, and draw a perpendicular line with the specified length
for i in range(1, correas_lado + 1):
    current_start_point = start_point3 + ref_line2_unit_vector * (i * spacing)
    current_end_point1 = current_start_point + displacement4
    ax.plot([current_start_point[0], current_end_point1[0]], [current_start_point[1], current_end_point1[1]], color='blue', linewidth=1)

st.markdown("---")

# Mostrar figura dentro del app
col2.pyplot(fig_nave)
###################################################################### Plot frontal

col2.text("Leyenda.\n"
        "Rojo: Arriostramientos\n"
        "Azul: Porticos\n"
        "Verde: Correas")
pilar_peso_m = df_pilar.loc[df_pilar["Perfil"] == selector_pilar, "gk [kg/m]"].iloc[0]
viga_peso_m = df_viga.loc[df_viga["Perfil"] == selector_pilar, "gk [kg/m]"].iloc[0]
peso_pilares = round(cantidad_porticos * 2 * altura_alero * pilar_peso_m * 1.12/1000, 2)
peso_vigas = round(cantidad_porticos * 2 * largo_riegel * viga_peso_m * 1.25/1000, 2)
largo_correas = (correas_lado + 2) * 2 * ancho_nave
peso_correas = (largo_correas)
cantidad_arriostra = int(largo_riegel / line_distance) * 8
st.text(f"El peso de los pilares es {peso_pilares} to")
st.text(f"El peso de las vigas es {peso_vigas} to")
st.text(f"Hay {largo_correas}m de correas en la cubierta")
metros_arrios = longitud_arrios * cantidad_arriostra
pesos_arrios = round((metros_arrios * 3.55) / 1000, 2)
st.text(f"Hay un total de {cantidad_arriostra} arriostramientos RD24 con un total de {metros_arrios} metros y {pesos_arrios} to")
st.markdown("---")
pesototal = pesos_arrios + peso_vigas + peso_pilares
st.text(f"Con un total de la estructura sin contar con las correas es: {pesototal} to.")
precio_mat = 1200
costes_material = precio_mat * pesototal
precio_taller = 900
costes_taller = precio_taller * pesototal
precio_monta = 400
costes_montaje = precio_monta * pesototal
precio_planif = 150
costes_planif = precio_planif * pesototal
factor_costes_empre = 0.1
factor_empresa = round(factor_costes_empre * (costes_planif+costes_montaje+costes_taller+costes_material))

st.text(f"Con un precio para el material de media de {precio_mat},-€ el coste es {costes_material} €")
st.text(f"Con un precio de fabricación medio de {precio_taller},-€ el coste es {costes_taller} €")
st.text(f"Con un precio de montaje medio de {precio_monta},-€ el coste es {costes_montaje} €")
st.text(f"Con un precio de montaje medio de {precio_planif},-€ el coste es {costes_planif} €")
st.text(f"Se añade un facor de 10% para cubrir los costes de empresa. La suma asciende a {factor_empresa} €")
st.markdown("---")
costes_totales = factor_empresa + costes_planif + costes_montaje + costes_taller + costes_material
costes_portonelada = round(costes_totales / pesototal, 2)
st.text(f"Los costes totales ascienden a {costes_totales} € o lo que es lo mismo {costes_portonelada} €/to")

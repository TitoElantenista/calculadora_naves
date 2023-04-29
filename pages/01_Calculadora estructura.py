import math
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


# Constants to be used in the program.
DB_FOLDER = pathlib.Path(__file__).parent.parent / "DBs"
LISTA_VIGAS_PILARES = ("HEA", "HEB", "HEM", "I-Profile", "IPE")
TITLE = "Calculadora de costes de construcción de nave industrial"
# Convenient color constants.
RED = "red"
GREEN = "green"
BLUE = "blue"
BLACK = "black"


class UserInputs:
    """Holds all the user inputs in the program."""

    def __init__(self, column) -> None:
        self.cantidad_porticos = column.slider(
            "Cantidad de pórticos",
            min_value=4, max_value=10, value=5)
        self.distancia_porticos_finales = column.number_input(
            "Distancia entre los pórticos finales (metros)",
            min_value=5.0, max_value=7.0, value=5.5, step=0.1)
        self.distancia_porticos_internos = column.number_input(
            "Distancia entre los pórticos internos (metros)",
            min_value=5.0, max_value=7.0, value=6.0, step=0.1)
        self.ancho_nave = column.number_input(
            "Ancho nave (metros)",
            min_value=8.0, max_value=26.0, value=18.0, step=0.25)
        self.altura_alero = column.number_input(
            "Altura del alero (metros)",
            min_value=4.0, max_value=8.0, value=4.0, step=0.1)
        self.inclinacion_tejado = column.slider(
            "Inclinación del tejado (grados)",
            min_value=6, max_value=30, value=12)
        self.longitud_cartela = column.number_input(
            "Largo de la cartela (metros)",
            min_value=0.0, max_value=4.0, value=2.0, step=0.1)
        self.altura_cartela = column.number_input(
            "Altura de la cartela (metros)",
            min_value=0.0, max_value=2.5, value=0.7, step=0.1)


class Geometry:
    """Handles Geometry variables."""

    def __init__(self, ui: UserInputs) -> None:
        self.angulo_radianes = math.radians(ui.inclinacion_tejado)
        self.largo_riegel = round(
            (ui.ancho_nave / 2) / math.cos(self.angulo_radianes), 2)
        self.distancia_correas = 2
        self.correas_internas_cantidad = 2 * math.ceil(
            (self.largo_riegel - 0.2) / (self.distancia_correas))
        self.correas_lado = int(self.correas_internas_cantidad / 2)
        self.peso_estructura = 50
        self.distancia_wandriegel = 2.2
        self.cantidad_wandriegel = round(
            (ui.altura_alero - 0.4) / self.distancia_wandriegel)
        self.distancia_real_wandriegel = (
            (ui.altura_alero - 0.4) / self.cantidad_wandriegel)


def get_data_frames() -> dict:
    """Gets the required data frames from the Excel files."""
    dfs = {}
    # Iterates through a generator of Excel files.
    for file in (file.name for file in DB_FOLDER.glob("*.xlsx")):
        df = pd.read_excel(DB_FOLDER / file)
        # Filter DF to include only rows with the
        # term searched in the first column
        # Transpose the DF
        # Set first column as index
        df = df.set_index(df.columns[0])
        df = df.T
        df.rename(
            columns=lambda column: column.replace("_x000D_", "_"),
            inplace=True)
        # Set columns as new index
        df.index.name = "Perfil"
        df.reset_index(inplace=True)
        df.rename(columns={"index": df.index.name}, inplace=True)
        # Rename
        df = df.rename(columns={df.columns[0]: "Perfil"})
        # Add the DF to the previously created dictionary
        dfs[file] = df
    return dfs


def copy_and_paste_lines(
    y1, y2, y3, y4, line_distance, last_x,
    axis, correas_lado, distancia_porticos_finales
) -> None:
    """Copy and paste the lines correas_lado - 1 times"""
    for _ in range(correas_lado - 1):
        # Update the Y coordinates
        y1 += line_distance
        y2 += line_distance
        y3 -= line_distance
        y4 -= line_distance
        # Plot the lines with the updated coordinates
        for y_pair in ((y1, y2), (y3, y4)):
            axis.plot((0, distancia_porticos_finales), y_pair, color=RED)
            axis.plot(
                (last_x + 0.5, last_x - distancia_porticos_finales),
                y_pair, color=RED)


def display_vista_superior(geo: Geometry, ui: UserInputs, col2) -> tuple:
    """
    Handles the Vista superior section. Returns any objects needed later.
    """
    # Create figure and axes
    fig, ax = plt.subplots()
    ax.set_title("Vista superior")
    ax.set_aspect("equal")
    ax.set_xlim(
        0,
        (ui.cantidad_porticos-2)*ui.distancia_porticos_internos
            + ui.distancia_porticos_finales)
    ax.set_ylim(0, ui.ancho_nave)
    # Add red horizontal line in the middle of y
    ax.axhline(y=ui.ancho_nave/2, color=RED)
    # Draw bottom line
    ax.axhline(0, xmin=0, xmax=1, color=RED)
    # Draw top line
    ax.axhline(ui.ancho_nave, xmin=0, xmax=1, color=RED)
    # Draw first line of frame
    ax.axvline(-ui.distancia_porticos_finales, color=BLUE)

    # Draw vertical lines
    for i in range(ui.cantidad_porticos):
        x = ui.distancia_porticos_finales + i * ui.distancia_porticos_internos
        ax.axvline(x, linestyle="--", color=BLUE)
    # Get the last value on the x, y axis and half of y
    last_x = (
        ui.distancia_porticos_internos * (ui.cantidad_porticos - 3)
            + 2 * ui.distancia_porticos_finales)
    last_y = ui.ancho_nave
    middle_y = last_y / 2
    # Draw last line of frame
    ax.axvline(x + ui.distancia_porticos_finales, color=BLUE)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    # Add text to the last x-axis value and for x = 0
    for x in (0, last_x):
        ax.text(x, -ui.ancho_nave * 0.05, f"{x:.1f}m", ha="center")
    # Add text to the last y-axis value and in the middle
    for y in (last_y, middle_y):
        ax.text(
            -ui.distancia_porticos_finales * 0.2, y, f"{y:.1f}m",
            va="center", rotation="vertical")

    # Get values for lines
    line_top = ui.ancho_nave - 0.2
    line_bottom = 0.2
    line_middle_top = middle_y + 0.2
    line_middle_bottom = middle_y - 0.2

    # Calculate total distance.
    total_distance = line_top - line_bottom
    espacio_correas = (total_distance / 2) - 0.2 - 1.2

    # Calculate distance between lines
    line_distance = espacio_correas / geo.correas_lado
    # Draw horizontal lines
    for i in range(geo.correas_lado):
        y_bottom = line_bottom + line_distance * (i + 1)
        y_top = line_top - line_distance * (i + 1)
        for y in (y_bottom, y_top):
            ax.axhline(y=y, linestyle="--", color=GREEN)

    # Add horizontal lines.
    for line in (line_top, line_bottom, line_middle_top, line_middle_bottom):
        ax.axhline(line, linestyle="--", color=GREEN)

    ########## LEFT TRAUFE STRAPS ##########
    # Get coordinates of the first line and second line,
    # and plots red lines between the two points for each line.
    x1 = 0
    x2 = ui.distancia_porticos_finales
    y1 = line_bottom, line_top
    y2 = line_bottom + line_distance, line_top - line_distance
    ax.plot((x1, x2), (y1, y2), color=RED)
    ax.plot((x1, x2), (y2, y1), color=RED)

    ########## LEFT CENTER STRAPS ##########
    # Get coordinates of the first line and second line,
    # and plots red lines between the two points for each line.
    x1f = 0
    x2f = ui.distancia_porticos_finales

    y1f = middle_y - 0.2, geo.correas_lado * line_distance + 0.2
    y2f = geo.correas_lado * line_distance + 0.2, middle_y - 0.2
    ax.plot((x1f, x2f), (y1f, y2f), color=RED)

    y1f = line_bottom + line_distance, line_top - line_distance
    y2f = line_bottom, line_top
    ax.plot((x1f, x2f), (y1f, y2f), color=RED)

    x1f2 = 0
    x2f2 = ui.distancia_porticos_finales

    # First line.
    y1f2 = middle_y + 0.2, last_y - (geo.correas_lado * line_distance + 0.2)
    y2f2 = last_y - (geo.correas_lado * line_distance + 0.2), middle_y + 0.2
    ax.plot((x1f2, x2f2), (y1f2, y2f2), color=RED)

    # Second line.
    y1f2 = line_bottom + line_distance, line_top - line_distance
    y2f2 = line_bottom, line_top
    ax.plot((x1f2, x2f2), (y1f2, y2f2), color=RED)

    ########## CENTRAL BRACING ##########
    # Get the coordinates of the first line
    x1 = last_x + 0.5
    x2 = last_x - ui.distancia_porticos_finales

    y1f = middle_y - 0.2, geo.correas_lado * line_distance + 0.2
    y2f = geo.correas_lado * line_distance + 0.2, middle_y - 0.2
    ax.plot((x1, x2), (y1f, y2f), color=RED)

    y1f2 = middle_y + 0.2, last_y - (geo.correas_lado * line_distance + 0.2)
    y2f2 = last_y - (geo.correas_lado * line_distance + 0.2), middle_y + 0.2
    ax.plot((x1, x2), (y1f2, y2f2), color=RED)

    ########## RIGHT TRAUFE BRACING ##########
    x1e = last_x + 0.5
    x2e = x1e - ui.distancia_porticos_finales - 0.5
    y1e = line_bottom, line_top
    y2e = line_bottom + line_distance, line_top - line_distance
    ax.plot((x1e, x2e), (y1e, y2e), color=RED)
    ax.plot((x1e, x2e), (y2e, y1e), color=RED)

    # Calculate the distance between the two points to 2dp (Pythagoras)
    x_diff = x2e - x1e
    y_diff = (line_bottom + line_distance) - line_bottom
    longitud_arrios = round(math.hypot(x_diff, y_diff), 2)

    # Set the initial Y coordinates
    y1 = line_bottom
    y2 = line_bottom + line_distance
    y3 = line_top
    y4 = line_top - line_distance

    copy_and_paste_lines(
        y1, y2, y3, y4, line_distance, last_x, ax,
        geo.correas_lado, ui.distancia_porticos_finales)
    copy_and_paste_lines(
        y2, y1, y4, y3, line_distance, last_x, ax,
        geo.correas_lado, ui.distancia_porticos_finales)

    # Show figure inside the app
    col2.pyplot(fig)
    # Returns required local variables for future use.
    return line_distance, longitud_arrios


def draw_perpendicular_lines(
    correas_lado, start_point, ref_line_unit_vector,
    spacing, displacement, ax) -> None:
    """
    Iterate from 1 to correas_lado, calculate the starting point
    of each line, and draw a perpendicular line with the specified length.
    """
    for i in range(1, correas_lado + 1):
        current_start_point = (
            start_point + ref_line_unit_vector * i * spacing)
        current_end_point1 = current_start_point + displacement
        ax.plot(
            (current_start_point[0], current_end_point1[0]),
            (current_start_point[1], current_end_point1[1]),
            color=BLUE, linewidth=1)


def add_vista_frontal_left_straps(
    ref_line_unit_vector, start_point1, start_point2,
    perpendicular_length, spacing, ax, geo: Geometry
) -> None:
    """Adds the left straps to the vista frontal display."""
    # Rotate the unit vector by ±90 degrees
    # (only +90 degrees is needed)
    # to obtain the direction vectors for the perpendicular lines
    perpendicular_direction = rotate_vector(ref_line_unit_vector, 90)

    # Multiply the perpendicular direction vectors by the desired length
    # Gets the required displacement.
    displacement = perpendicular_direction * perpendicular_length

    # Calculate the required endpoints of the perpendicular lines
    end_point1 = start_point1 + displacement
    end_point2 = start_point2 + displacement

    # Traufpfette Firstpfette Lines
    ax.plot(
        (start_point1[0], end_point1[0]),
        (start_point1[1], end_point1[1]), color=BLUE, linewidth=1)
    ax.plot(
        (start_point2[0], end_point2[0]),
        (start_point2[1], end_point2[1]), color=BLUE, linewidth=1)

    draw_perpendicular_lines(
        geo.correas_lado, start_point1, ref_line_unit_vector,
        spacing, displacement, ax)


def add_vista_frontal_right_straps(
    offset_along_line, perpendicular_length,
    spacing, ax, geo: Geometry, ui: UserInputs
) -> None:
    """Adds the right straps to the vista frontal display."""
    x_start = ui.ancho_nave
    y_start = ui.altura_alero
    x_end = ui.ancho_nave - geo.largo_riegel * math.cos(geo.angulo_radianes)
    y_end = ui.altura_alero + geo.largo_riegel * math.sin(geo.angulo_radianes)

    # Calculate the direction vector and unit vector of the new reference line
    ref_line_direction = np.array((x_end - x_start, y_end - y_start))
    ref_line_unit_vector = (
        ref_line_direction / np.linalg.norm(ref_line_direction))

    # Calculate the starting points of the perpendicular lines
    start_point1 = np.array(
        (x_start, y_start)) + ref_line_unit_vector * offset_along_line
    start_point2 = np.array(
        (x_end, y_end)) - ref_line_unit_vector * offset_along_line

    # Rotate the unit vector by ±90 degrees to obtain the
    # direction vectors for the perpendicular lines (-90 only needed)
    perpendicular_direction = rotate_vector(ref_line_unit_vector, -90)

    # Multiply the required perp direction vectors by the desired length
    displacement = perpendicular_direction * perpendicular_length

    # Calculate the endpoints of the perpendicular lines
    end_point1 = start_point1 + displacement
    end_point2 = start_point2 + displacement

    # Plot the perpendicular lines
    ax.plot(
        (start_point1[0], end_point1[0]),
        (start_point1[1], end_point1[1]), color=BLUE, linewidth=1)
    ax.plot(
        (start_point2[0], end_point2[0]),
        (start_point2[1], end_point2[1]), color=BLUE, linewidth=1)

    draw_perpendicular_lines(
        geo.correas_lado, start_point1, ref_line_unit_vector,
        spacing, displacement, ax)


def display_vista_frontal(
    dfs: dict, geo: Geometry, ui: UserInputs, col1, col2
) -> tuple:
    """
    Handles the vista frontal section. Returns any objects needed later.
    """
    # Create figure and axes
    fig_nave, ax = plt.subplots()
    ax.set_title("Vista frontal")
    ax.set_aspect("equal")
    ax.set_xlim(-0.5, ui.ancho_nave + 0.5)
    ax.set_ylim(
        -0.5,
        ui.altura_alero + 2 * geo.largo_riegel
            * np.sin(np.deg2rad(ui.inclinacion_tejado)))

    # Agregar línea roja en el eje x
    ax.axhline(y=0, color=BLACK, linewidth=0.5, xmin=0.0, xmax=ui.ancho_nave)
    col1.markdown("---")
    perfilestipo_columnas = col1.selectbox(
        "Selecciona el tipo de perfil", LISTA_VIGAS_PILARES, index=4)

    df_pilar = dfs[f"{perfilestipo_columnas}.xlsx"]
    print(df_pilar.columns)

    # Update the pillar lines
    # After getting pilar_peso_m
    selector_pilar = col1.selectbox(
        "Seleccionar perfil para los pilares", key="droppilar",
        options=df_pilar["Perfil"].tolist(), index=12)
    pilar_ancho = df_pilar.loc[
        df_pilar["Perfil"] == selector_pilar, "Altura h [mm]"
    ].iloc[0] / 1000  # Convert to meters

    for value in (0, pilar_ancho, ui.ancho_nave, ui.ancho_nave - pilar_ancho):
        ax.plot((value, value), (0, ui.altura_alero), color=BLUE, linewidth=1)

    col1.markdown("---")
    perfilestipo_vigas = col1.selectbox(
        "Selecciona el tipo de perfil para las vigas",
        LISTA_VIGAS_PILARES, index=4)
    df_viga = dfs[f"{perfilestipo_vigas}.xlsx"]
    selector_viga = col1.selectbox(
        "Seleccionar perfil", key="dropviga",
        options=df_viga["Perfil"].tolist(), index=12)
    viga_ancho = df_viga.loc[
        df_viga["Perfil"] == selector_viga, "Altura h [mm]"
    ].iloc[0] / 1000  # Convert to meters

    # Calculate coordinates of the inclined line
    x_start = 0
    y_start = ui.altura_alero
    x_end = geo.largo_riegel * math.cos(geo.angulo_radianes)
    y_end = ui.altura_alero + geo.largo_riegel * math.sin(geo.angulo_radianes)
    # Calculate coordinates of the second sloping line
    x2_start = ui.ancho_nave
    y2_start = ui.altura_alero
    x2_end = geo.largo_riegel * np.cos(np.deg2rad(ui.inclinacion_tejado))
    y2_end = (
        ui.altura_alero
            + geo.largo_riegel * np.sin(np.deg2rad(ui.inclinacion_tejado)))
    ax.plot((x_start, x_end), (y_start, y_end), color=BLUE, linewidth=1)
    ax.plot((x2_start, x2_end), (y2_start, y2_end), color=BLUE, linewidth=1)

    # Plot Limits
    ax.set_ylim(0, y_end + 0.5)

    # Beam thickness
    # Calculate the angle perpendicular to the inclined lines
    perpendicular_angle = ui.inclinacion_tejado + 90

    # Calculate the offset in x and y coordinates
    offset_x = viga_ancho * np.cos(np.deg2rad(perpendicular_angle))
    offset_y = viga_ancho * np.sin(np.deg2rad(perpendicular_angle))

    # Calculate beam column length
    longitud_pilar_riegel = pilar_ancho * math.tan(geo.angulo_radianes)
    # Add lines
    ax.plot(
        (pilar_ancho, pilar_ancho),
        (ui.altura_alero, ui.altura_alero + longitud_pilar_riegel),
        color=BLUE, linewidth=1)
    ax.plot(
        (ui.ancho_nave - pilar_ancho, ui.ancho_nave - pilar_ancho),
        (ui.altura_alero, ui.altura_alero + longitud_pilar_riegel),
        color=BLUE, linewidth=1)

    # Subtract the offset from the original coordinates of the inclined lines
    x_end_offset = x_end - offset_x
    y_end_offset = y_end - offset_y
    y2_end_offset = y2_end - offset_y

    # Add blue line first
    ax.plot((x_end, x_end), (y_end, y_end_offset), color=BLUE, linewidth=1)

    pilar_viga_interseccion_y = (
        ui.altura_alero + longitud_pilar_riegel - offset_y)

    point1 = (pilar_ancho, pilar_viga_interseccion_y)
    point2 = (x_end_offset, y_end_offset)
    distance = 2.3

    caca1, caca2 = point_along_line(point1, point2, distance)

    # Calculate the direction vector of the reference line
    prev_line_direction = np.array(
        (x_end - pilar_ancho, y_end_offset - pilar_viga_interseccion_y))

    # Rotate the direction vector by 90 degrees
    # minus the additional angle (roof inclination)
    total_angle = 90
    rotated_vector = rotate_vector(prev_line_direction, total_angle)

    # Normalize the rotated vector to get a unit vector
    unit_vector = rotated_vector / np.linalg.norm(rotated_vector)

    # Multiply the unit vector by the desired length (viga_ancho)
    displacement = unit_vector * viga_ancho

    # Add the resulting vector to the endpoint of the previous line
    # (caca1, caca2) to get the endpoint of the new line
    new_line_endpoint = np.array([caca1, caca2]) + displacement

    # Plot the parallel lines with the offset
    ax.plot((caca1, x_end), (caca2, y_end_offset), color=BLUE, linewidth=1)
    ax.plot(
        (ui.ancho_nave - caca1, x2_end), (caca2, y2_end_offset),
        color=BLUE, linewidth=1)

    # Plot placas cartelas
    ax.plot(
        (caca1, new_line_endpoint[0]), (caca2, new_line_endpoint[1]),
        color=BLUE, linewidth=1)
    ax.plot(
        (ui.ancho_nave - caca1, ui.ancho_nave - new_line_endpoint[0]),
        (caca2, new_line_endpoint[1]), color=BLUE, linewidth=1)
    altura_cartela = ui.altura_cartela - offset_y

    # Left gusset
    ax.plot(
        (pilar_ancho, caca1), 
        (pilar_viga_interseccion_y - altura_cartela, caca2),
        color=BLUE, linewidth=1)
    ax.plot(
        (0, pilar_ancho),
        ( 
            pilar_viga_interseccion_y - altura_cartela,
            pilar_viga_interseccion_y - altura_cartela),
        color=BLUE, linewidth=1)
    # Right gusset.
    ax.plot(
        (ui.ancho_nave - pilar_ancho, ui.ancho_nave - caca1),
        (pilar_viga_interseccion_y - altura_cartela, caca2),
        color=BLUE, linewidth=1)
    ax.plot(
        (ui.ancho_nave, ui.ancho_nave - pilar_ancho),
        (
            pilar_viga_interseccion_y - altura_cartela,
            pilar_viga_interseccion_y - altura_cartela),
        color=BLUE, linewidth=1)

    # Wandriegel Lines
    # Initial line
    x1, x2 = 0, -0.16
    x3, x4 = ui.ancho_nave, ui.ancho_nave + 0.16
    y1, y2 = 0.25, 0.25

    for _ in range(geo.cantidad_wandriegel + 1):
        ax.plot((x1, x2), (y1, y2), color=BLUE, linewidth=1)
        ax.plot((x3, x4), (y1, y2), color=BLUE, linewidth=1)
        # Move the line in the positive y direction
        y1 += geo.distancia_real_wandriegel
        y2 += geo.distancia_real_wandriegel

    offset_along_line = 0.2
    perpendicular_length = 0.18
    # Calculate the direction vector and unit vector of the reference line
    ref_line_direction = np.array((x_end - x_start, y_end - y_start))
    ref_line_unit_vector = (
        ref_line_direction / np.linalg.norm(ref_line_direction))

    # Calculate the starting points of the perpendicular lines
    start_point1 = np.array(
        (x_start, y_start)) + ref_line_unit_vector * offset_along_line
    start_point2 = np.array(
        (x_end, y_end)) - ref_line_unit_vector * offset_along_line
    # Calculate the distance between the
    # two starting points of the perpendicular lines
    distance_between_points = np.linalg.norm(start_point2 - start_point1)
    # Divide the distance by the number of lines you want to draw
    # (correas_lado + 1) to obtain the spacing between the lines
    spacing = distance_between_points / (geo.correas_lado + 1)

    add_vista_frontal_left_straps(
        ref_line_unit_vector, start_point1, start_point2,
        perpendicular_length, spacing, ax, geo)
    add_vista_frontal_right_straps(
        offset_along_line, perpendicular_length,
        spacing, ax, geo, ui)

    st.markdown("---")

    # Show figure inside the app
    col2.pyplot(fig_nave)
    # Returns required local variables for future use.
    return df_pilar, selector_pilar, df_viga, selector_viga


def display_text(
    df_pilar, selector_pilar, df_viga, selector_viga, line_distance,
    longitud_arrios, geo: Geometry, ui: UserInputs, col2) -> None:
    """Displays any text alongside the graphs."""
    col2.text(
        "Leyenda.\n"
        "Rojo: Arriostramientos\n"
        "Azul: Porticos\n"
        "Verde: Correas")
    pilar_peso_m = df_pilar.loc[
        df_pilar["Perfil"] == selector_pilar, "gk [kg/m]"].iloc[0]
    viga_peso_m = df_viga.loc[
        df_viga["Perfil"] == selector_viga, "gk [kg/m]"].iloc[0]
    peso_pilares = round(
        ui.cantidad_porticos * 2 * ui.altura_alero * pilar_peso_m * 1.12/1000,
        2)
    peso_vigas = round(
        ui.cantidad_porticos * 2 * geo.largo_riegel * viga_peso_m * 1.25/1000,
        2)
    largo_correas = (geo.correas_lado + 2) * 2 * ui.ancho_nave
    cantidad_arriostra = int(geo.largo_riegel / line_distance) * 8
    st.text(f"El peso de los pilares es {peso_pilares} to")
    st.text(f"El peso de las vigas es {peso_vigas} to")
    st.text(f"Hay {largo_correas}m de correas en la cubierta")
    metros_arrios = longitud_arrios * cantidad_arriostra
    pesos_arrios = round((metros_arrios * 3.55) / 1000, 2)
    st.text(
        f"Hay un total de {cantidad_arriostra} arriostramientos RD24 con "
        f"un total de {metros_arrios} metros y {pesos_arrios} to")
    st.markdown("---")
    pesototal = pesos_arrios + peso_vigas + peso_pilares
    st.text(
        "Con un total de la estructura sin contar "
        f"con las correas es: {pesototal} to.")
    precio_mat = 1200
    costes_material = precio_mat * pesototal
    precio_taller = 900
    costes_taller = precio_taller * pesototal
    precio_monta = 400
    costes_montaje = precio_monta * pesototal
    precio_planif = 150
    costes_planif = precio_planif * pesototal
    factor_costes_empre = 0.1
    factor_empresa = round(
        factor_costes_empre * (
            costes_planif + costes_montaje + costes_taller + costes_material))

    st.text(
        f"Con un precio para el material de media de {precio_mat},-€ "
        f"el coste es {costes_material} €")
    st.text(
        f"Con un precio de fabricación medio de {precio_taller},-€ "
        f"el coste es {costes_taller} €")
    st.text(
        f"Con un precio de montaje medio de {precio_monta},-€ "
        f"el coste es {costes_montaje} €")
    st.text(
        f"Con un precio de montaje medio de {precio_planif},-€ "
        f"el coste es {costes_planif} €")
    st.text(
        "Se añade un facor de 10% para cubrir los costes de empresa. "
        f"La suma asciende a {factor_empresa} €")
    st.markdown("---")
    costes_totales = (
        factor_empresa + costes_planif + costes_montaje
        + costes_taller + costes_material)
    costes_portonelada = round(costes_totales / pesototal, 2)
    st.text(
        f"Los costes totales ascienden a {costes_totales} € "
        f"o lo que es lo mismo {costes_portonelada} €/to")


def point_along_line(pt1, pt2, distance) -> list:
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


def rotate_vector(vector, degrees):
    radians = np.radians(degrees)
    rotation_matrix = np.array(
        (
            (np.cos(radians), -np.sin(radians)),
            (np.sin(radians), np.cos(radians))
        )
    )
    return np.matmul(rotation_matrix, vector)


def main() -> None:
    """Main procedure of the program."""
    # Set page width.
    st.set_page_config(layout="wide")
    st.title(TITLE)
    st.markdown("---")

    dfs = get_data_frames()
    col1, col2 = st.columns(2)
    ui = UserInputs(col1)
    geo = Geometry(ui)

    line_distance, longitud_arrios = display_vista_superior(geo, ui, col2)
    df_pilar, selector_pilar, df_viga, selector_viga = (
        display_vista_frontal(dfs, geo, ui, col1, col2))
    display_text(
        df_pilar, selector_pilar, df_viga, selector_viga,
        line_distance, longitud_arrios, geo, ui, col2)



if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import os



st.set_page_config(page_title="Perfiles de acero",
               page_icon=":bar_chart:",
               layout="wide"
)


st.markdown("<h3>Tabla seleccionada</h3>", unsafe_allow_html=True)
# Get list of excel files in the specified directory
excel_files = [file for file in os.listdir("DBs") if file.endswith(".xlsx")]
excel_files_without_ext = [file.replace('.xlsx','') for file in excel_files]


# Create sidebar
st.sidebar.title("Filtros")

# Add selector combobox
selected_file = st.sidebar.selectbox("Selecciona el tipo de perfil", excel_files_without_ext)
selected_file = f"{selected_file}.xlsx"
# Read the selected excel file and display first sheet as dataframe
df = pd.read_excel(os.path.join("DBs", selected_file))


# Set the first column as the index
df = df.set_index(df.columns[0])

# Transpose the DataFrame
df = df.T
df.rename(columns=lambda x: x.replace("_x000D_", "_"), inplace=True)


# Set the columns as the new index
df.index.name = "Perfil"
df.reset_index(inplace=True)
df.rename(columns={'index':df.index.name}, inplace=True)

# Get the first column name
first_col = df.columns[0]

 


# Add checkbox to select all
select_all = st.sidebar.checkbox("Mostrar todas las columnas")

# Get options for multiselect
options = df.columns

# Default columns
default_select = [options[0], "gk [kg/m]", "Superficie_revestimiento [m²/m]"]

# Create multiselect
if not select_all:
   selected_rows = st.sidebar.multiselect("Selector columnas", options, default=default_select)
else:
   selected_rows = options

# Display only the selected rows
st.dataframe(df[selected_rows])


st.markdown("<h3>Buscador de perfiles</h3>", unsafe_allow_html=True)
# Create input box to search for value
search_value = st.text_input("Escribe el perfil a buscar con al menos dos letras:")

# Create empty dataframe to store results
results_df = pd.DataFrame()
if len(search_value) >=2:
# Loop through excel files
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

      # Filter dataframe to include only rows with the search value in the first column
      if ' ' in search_value:
         search_values = [search_value, search_value.replace(' ', '')]
      else:
         search_values = [search_value]

      for val in search_values:
         filtered_df = df2[df2.iloc[:,0].str.contains(val, case=False, na=False)]
         results_df = pd.concat([results_df, filtered_df])



   # Display results dataframe
   st.dataframe(results_df[selected_rows])
else: 
   st.text("Entrada insuficiente")

#python -m streamlit run C:\Users\Sanz_Lopes\Desktop\Python\Module\profile_datenbank\main_profile_db.py

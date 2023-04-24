import streamlit as st
from PIL import Image


st.set_page_config(page_title="Intro")

st.markdown("<h1 style='text-align: center;'>Presentación de la idea y conclusiones</h1>", unsafe_allow_html=True)

# Load the PNG image using PIL
image = Image.open("Recursos/naveejemplo.png")

# Display the image using the Streamlit image() function
st.image(image)
st.markdown("<h3 style='text-align: center;'>Introducción</h3>", unsafe_allow_html=True)
st.text("Esta aplicación es una aproximación para comprobar la viabilidad de crear un programa con Streamlit para\n"
        "realizar el cálculo de la geometría y costes de producción de una nave industrial.\n"
        "Dada la complejidad de la tarea, esta aplicación realiza la tarea  una forma muy simplificada en la página\n'Calculadora estructura'."
        " En la página 'Base de datos' se muestra de una forma sencilla con unas bases de datos\n con las que trabajo, que el manejo de las mismas\n"
        "empleando Streamlit es mucho más user friendly.")
st.markdown("<h3 style='text-align: center;'>Conclusión</h3>", unsafe_allow_html=True)
st.text("Parece completamente viable y además más productivo y 'user friendly' que el\n"
        "clásico workflow de oficina con Excel. Gracias a python se puede crear un\n"
        "sistema conectado que minimice la posibilidad de cometer errores.\n"
        "El trabajo inicial para tomar en cuenta todas las partes de la estructura\n"
        "uniones y materiales, sería bastante grande, pero no hay nada que\n"
        "haga suponer que no sea posible."
        "Del mismo modo, streamlit ofrece una visualización más sencilla\n"
        "para que el usuario que no tiene interés en aprender a programar\n"
        "pueda calcular aprovechando las ventajas de python.\n"
        "Además se pueden añadir muchas más funciones como general la oferta\n"
        "en PDF o similares.")
st.markdown("<h3 style='text-align: center;'>Mejoras</h3>", unsafe_allow_html=True)
st.text("He echado de menos alguna forma de agrupar widgets con algún\n"
        "tipo de marco, para que el usuario pueda identificar rápidamente\n"
        "a qué se corresponde cada conjunto de widgets. Poner líneas con\n"
        "markdown para separar los widgets no me parece suficientemente claro.\n"
        "Echo también mucho de menos algún método sencillo de manipular el método\n"
        "que tiene streamlit para visualizar datos en dataframes/tablas. En general\n"
        "el separador de los miles y decimales está de forma predefinida configurado\n"
        "a la inversa de los separadores que se usan en Europa. Con los decimales pone\n"
        "de forma predefinida 4. Las fechas tomadas de una tabla de excel aparecen con\n"
        "la hora a pesar de que en el excel no estén los datos de la hora. Todas esas\n"
        "cosas deberían de poner configurarse con streamlit de una forma más sencilla.")

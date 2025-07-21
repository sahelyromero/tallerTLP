import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# Estilos visuales
st.markdown(
    """
    <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1507643179773-3e975d7ac515?q=80&w=1170&auto=format&fit=crop");
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }

        .block-container {
            background-color: rgba(0, 0, 0, 0.85);
            padding: 2rem;
            border-radius: 10px;
        }

        h1, h2, h3 {
            color: #FFD700;
        }

        .stButton>button {
            background-color: #8B0000;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Galería de Arte")

# 1. Mostrar obras actuales
st.header("Obras actuales")
response = requests.get(f"{API_URL}/obras")

if response.status_code == 200:
    obras = response.json()
    if obras:
        for obra in obras:
            st.markdown(f"**ID:** {obra['id']} | **{obra['titulo']}** por *{obra['autor']}* ({obra['año']}) - {obra['tipo']} - **${obra['precio']}**")
    else:
        st.info("No hay obras en la galería.")
else:
    st.error("No se pudo obtener el catálogo de obras.")

st.markdown("---")

# 2. Agregar nueva obra
st.header("Agregar nueva obra")

with st.form("formulario_obra"):
    nuevo_id = st.number_input("ID de la obra", min_value=1, step=1)
    titulo = st.text_input("Título de la obra")
    autor = st.text_input("Autor")
    año = st.number_input("Año de creación", min_value=1000, max_value=2100, step=1)
    precio = st.number_input("Precio", min_value=0.0, step=100.0)
    tipo = st.text_input("Tipo de obra (pintura, escultura, etc.)")

    submit = st.form_submit_button("Agregar obra")

    if submit:
        nueva_obra = {
            "id": nuevo_id,
            "titulo": titulo,
            "autor": autor,
            "año": año,
            "precio": precio,
            "tipo": tipo
        }

        respuesta = requests.post(f"{API_URL}/obras", json=nueva_obra)
        if respuesta.status_code == 200:
            st.success("✅ Obra agregada exitosamente.")
        elif respuesta.status_code == 400:
            st.warning(respuesta.json().get("detail", "Error desconocido."))
        else:
            st.error("❌ Error al agregar la obra.")

st.markdown("---")

# 3. Eliminar una obra
st.header("Eliminar una obra")
obra_id_a_eliminar = st.number_input("Ingrese el ID de la obra a eliminar:", min_value=1, step=1, key="delete_id")
if st.button("Eliminar obra"):
    delete_resp = requests.delete(f"{API_URL}/obras/{obra_id_a_eliminar}")
    if delete_resp.status_code == 200:
        st.success(f"Obra con ID {obra_id_a_eliminar} eliminada exitosamente.")
    else:
        st.error("No se pudo eliminar. ¿El ID existe?")

st.markdown("---")

# 4. Modificar precio
st.header("Cambiar precio de una obra")
obra_id_precio = st.number_input("ID de la obra a modificar:", min_value=1, step=1, key="mod_id")
nuevo_precio = st.number_input("Nuevo precio:", min_value=0.0, step=100.0, key="mod_precio")

if st.button("Actualizar precio"):
    put_resp = requests.put(f"{API_URL}/obras/{obra_id_precio}", params={"nuevo_precio": nuevo_precio})
    if put_resp.status_code == 200:
        st.success(f"✅ Precio de la obra actualizado a ${nuevo_precio}")
    else:
        st.error("Error al actualizar el precio. ¿El ID existe?")

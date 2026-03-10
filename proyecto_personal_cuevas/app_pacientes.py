# app_pacientes.py
import streamlit as st
import pandas as pd
import mysql.connector

# -----------------------------
# CARGAR CSV CON LOS DATOS INICIALES
# -----------------------------
df_unidos = pd.read_csv("df_unidos.csv")

# -----------------------------
# CONEXIÓN A MYSQL
# -----------------------------
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',  # Cambia si tu MySQL tiene contraseña
)
cursor = conn.cursor()

# Crear base de datos y tabla si no existen
cursor.execute("CREATE DATABASE IF NOT EXISTS salud_app")
cursor.execute("USE salud_app")
cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id INT PRIMARY KEY,
    pregnancies INT,
    glucose FLOAT,
    blood_pressure FLOAT,
    bmi FLOAT,
    age_y INT,
    sex VARCHAR(10),
    bp FLOAT,
    cholesterol FLOAT,
    heart_disease BOOLEAN
)
""")

# -----------------------------
# INSERTAR DATOS INICIALES DEL CSV
# -----------------------------
for i, row in df_unidos.iterrows():
    sql = """
    INSERT INTO pacientes (id,pregnancies,glucose,blood_pressure,bmi,age_y,sex,bp,cholesterol,heart_disease)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
        pregnancies=VALUES(pregnancies),
        glucose=VALUES(glucose),
        blood_pressure=VALUES(blood_pressure),
        bmi=VALUES(bmi),
        age_y=VALUES(age_y),
        sex=VALUES(sex),
        bp=VALUES(bp),
        cholesterol=VALUES(cholesterol),
        heart_disease=VALUES(heart_disease)
    """
    cursor.execute(sql, tuple(row))
conn.commit()

# -----------------------------
# INTERFAZ WEB
# -----------------------------
st.title("Gestor de Pacientes Salud")

st.subheader("Agregar o actualizar paciente")
with st.form("nuevo_paciente"):
    id_pac = st.number_input("ID", min_value=1)
    pregnancies = st.number_input("Pregnancies", min_value=0)
    glucose = st.number_input("Glucose")
    blood_pressure = st.number_input("Blood Pressure")
    bmi = st.number_input("BMI")
    age_y = st.number_input("Edad", min_value=0)
    sex = st.selectbox("Sexo", ["F", "M"])
    bp = st.number_input("BP")
    cholesterol = st.number_input("Cholesterol")
    heart_disease = st.checkbox("Heart Disease")
    
    submitted = st.form_submit_button("Agregar/Actualizar")
    if submitted:
        sql = """
        INSERT INTO pacientes (id,pregnancies,glucose,blood_pressure,bmi,age_y,sex,bp,cholesterol,heart_disease)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            pregnancies=VALUES(pregnancies),
            glucose=VALUES(glucose),
            blood_pressure=VALUES(blood_pressure),
            bmi=VALUES(bmi),
            age_y=VALUES(age_y),
            sex=VALUES(sex),
            bp=VALUES(bp),
            cholesterol=VALUES(cholesterol),
            heart_disease=VALUES(heart_disease)
        """
        cursor.execute(sql, (id_pac,pregnancies,glucose,blood_pressure,bmi,age_y,sex,bp,cholesterol,int(heart_disease)))
        conn.commit()
        st.success(f"Paciente {id_pac} agregado o actualizado!")

# -----------------------------
# Mostrar todos los pacientes
# -----------------------------
st.subheader("Lista de pacientes")
cursor.execute("SELECT * FROM pacientes")
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=['id','pregnancies','glucose','blood_pressure','bmi','age_y','sex','bp','cholesterol','heart_disease'])
st.dataframe(df)

# Cerrar conexión
cursor.close()
conn.close()

# Instrucciones para ejecutar la aplicación en local

## 1. Clona o descarga el repositorio

Clona el repositorio con el siguiente comando:

```bash
git clone https://github.com/AlexUrtubia/streamlit_app.git
cd streamlit_app
```

O descarga el ZIP desde GitHub y descomprímelo.

---

## 2. Crea y activa un entorno virtual (opcional, pero recomendado)

**En Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instala las dependencias

Asegúrate de tener pip actualizado y ejecuta:

```bash
pip install -r requirements.txt
```

---

## 4. Ejecuta la aplicación Streamlit

Ejecuta el archivo principal con:

```bash
streamlit run app.py
```

---

## 5. Abre la aplicación en tu navegador

Por defecto, se abrirá en [http://localhost:8501](http://localhost:8501) .

Si no se abre automáticamente, copia esa URL y pégala en tu navegador.

---

## 6. (Opcional) Desactiva el entorno virtual

Cuando termines de trabajar, puedes desactivar el entorno virtual ejecutando:

```bash
deactivate
```

---

## Notas importantes

* Requiere **Python 3.7 o superior**.
* La app necesita conexión a Internet para obtener datos desde la API de datos.gob.cl.
* Si tienes problemas instalando dependencias, asegúrate de tener `pip` actualizado:

  ```bash
  pip install --upgrade pip
  ```

---

## Ejemplo de requirements.txt mínimo

```
streamlit
pandas
matplotlib
requests
```

from flask import Flask, render_template, url_for, redirect, request, Response, session, jsonify
from livereload import Server as sv
import pymysql as sqlxd
import pytest as pt
import os # Necesario para escanear directorios
# from flask_cors import CORS # Descomenta si necesitas CORS y lo tienes instalado


app = Flask(__name__)
# CORS(app) # Descomenta si usas CORS

# =======================================
# ====== CONFIGURACIÓN DE ESCANEO ======
# =======================================

# Define la ruta a la carpeta donde están los HTMLs de los personajes.
# Esto asume que tu estructura es: app.py -> templates/lorepedia/Personajes/
PERSONAJES_DIR = os.path.join(app.root_path, 'templates', 'lorepedia', 'Personajes')

def parse_personaje_file(filename):
    """
    Convierte el nombre del archivo (e.g., 'Kris_Dreemur.html') en datos legibles.
    """
    if not filename.endswith('.html'):
        return None

    # Quitar la extensión .html
    base_name = filename[:-5]
    
    # Nombre legible: 'Kris_Dreemur' -> 'Kris Dreemur' (Reemplaza guiones bajos)
    nombre_legible = base_name.replace('_', ' ')
    
    # Crear el endpoint: 'Kris_Dreemur' -> 'kris_dreemur_page' (En minúsculas + '_page')
    endpoint_name = base_name.lower().replace('_', '_') + '_page'

    return {
        'nombre': nombre_legible,
        'endpoint': endpoint_name
    }


# =======================================
# ====== ENDPOINTS DE AUTENTICACIÓN ======
# =======================================

@app.route('/login') # endpoint login
def login():
    """Renderiza la página para iniciar sesión."""
    return render_template('lorepedia/iniciarSesion.html')


@app.route('/registrar') # endpoint para registrar
def registrar():
    """Renderiza la página para crear una nueva sesión."""
    return render_template('lorepedia/crearSesion.html')


# =====================================
# ====== ENDPOINTS DE NAVEGACIÓN ======
# =====================================

@app.route('/') # endpoint home
def index():
    """Renderiza la página principal (Home)."""
    return render_template('lorepedia/index.html')


@app.route('/personajes') # endpoint personajes (Lista)
def personajes():
    """
    Renderiza la lista de personajes escaneando la carpeta de templates
    y verifica que cada personaje tenga un endpoint de Flask asociado.
    """
    personajes_data = []

    try:
        # 1. Escanear el directorio y construir la lista de datos
        for filename in os.listdir(PERSONAJES_DIR):
            
            personaje = parse_personaje_file(filename)
            
            if personaje:
                # 2. Verificar que la función/ruta (endpoint) existe
                try:
                    # Intenta obtener la URL para el endpoint. Si no existe, lanza un error.
                    url_for(personaje['endpoint'])
                    personajes_data.append(personaje)
                except:
                    # Imprime una advertencia si el HTML existe pero la ruta no está en app.py
                    print(f"ADVERTENCIA: No se encontró la ruta/función de Flask para el endpoint: {personaje['endpoint']} (Archivo: {filename}). Asegúrate de haberla creado en app.py. Se omitirá en la lista.")
                    pass # Omitir este personaje si la ruta no existe

        # 3. Ordenar la lista para una mejor UI (alfabéticamente)
        personajes_data.sort(key=lambda p: p['nombre'])

    except FileNotFoundError:
        print(f"ERROR FATAL: No se encontró el directorio de personajes en: {PERSONAJES_DIR}. La lista estará vacía.")
        personajes_data = []

    # 4. Renderizar el template, pasando la lista dinámica
    return render_template(
        'lorepedia/Paginas/Personajes.html',
        personajes=personajes_data # <--- Variable usada en el template
    )


# =========================================
# ====== ENDPOINTS DE PERSONAJES INDIVIDUALES (Manual) ======
# =========================================
# Estas rutas DEBEN existir para que el escaneo anterior funcione.

@app.route('/personajes/spamton')
def spamton_page():
    """Renderiza la página de detalles de Spamton G. Spamton."""
    return render_template('lorepedia/Personajes/Spamton.html')

@app.route('/personajes/dante')
def dante_page():
    """Renderiza la página de detalles de Dante."""
    return render_template('lorepedia/Personajes/Dante.html')
    
@app.route('/personajes/gerson_boom')
def gerson_boom_page(): # NOTA: El parser busca el endpoint 'gerson_boom_page'
    return render_template('lorepedia/Personajes/Gerson_Boom.html')

@app.route('/personajes/kris_dreemur')
def kris_dreemur_page(): # NOTA: El parser busca el endpoint 'kris_dreemur_page'
    return render_template('lorepedia/Personajes/Kris_Dreemur.html')

@app.route('/personajes/ralsei')
def ralsei_page(): # NOTA: El parser busca el endpoint 'ralsei_page'
    return render_template('lorepedia/Personajes/Ralsei.html')

@app.route('/personajes/susie')
def susie_page(): # NOTA: El parser busca el endpoint 'susie_page'
    return render_template('lorepedia/Personajes/Susie.html')

@app.route('/personajes/vergil')
def vergil_page(): # NOTA: El parser busca el endpoint 'vergil_page'
    return render_template('lorepedia/Personajes/Vergil.html')


# ===================================
# ====== EJECUCIÓN DEL SERVIDOR ======
# ===================================

if __name__=='__main__':
    server = sv(app.wsgi_app)
    server.watch('**/*.html') 
    server.watch('**/*.css')
    server.watch('**/*.js')
    server.serve(port=5000, debug=True)
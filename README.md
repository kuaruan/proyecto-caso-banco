# Proyecto de Bank Marketing

Este proyecto implementa una solución de ingeniería de datos para centralizar y visualizar información de campañas de marketing bancario (Caso: Bank Marketing), utilizando una arquitectura moderna y reproducible.

# Objetivo
Desarrollar un entorno técnico para la ingesta y consulta de datos utilizando:
- Python 3.11
- FastAPI para la exposición de servicios web.
- Docker para asegurar la portabilidad del entorno.
- Supabase (PostgreSQL) como motor de base de datos en la nube.
- Pandas & Psycopg para el procesamiento y carga de datos.

# Arquitectura del Proyecto
La solución se enfoca en un flujo de datos robusto:
- Aplicación empaquetada en contenedores Docker.
- Conexión dinámica a base de datos relacional en la nube.
- Documentación automatizada de la interfaz mediante Swagger UI.
- Pipeline de limpieza y validación de datos previo a la carga.

# Estructura del proyecto
```text
proyecto-caso-banco/
├─ app/
│  ├─ main.py              
│  └─ db.py                        
├─ scripts/
│  ├─ pre_procesamiento_caso_2.py 
│  ├─ validacion_de_datos_caso_2.py 
│  └─ carga_de_datos_caso_2.py    
├─ data/
│  └─ datos_02_bank_validados.csv 
├─ tests/
│  └─ test_health.py            
├─ .github/
│  └─ workflows/
│     └─ ci.yml                   
├─ .env.example                  
├─ .dockerignore
├─ Dockerfile
└─ requirements.txt

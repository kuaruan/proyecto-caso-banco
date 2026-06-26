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
├── .github/workflows/
│   └── ci.yml            
├── .vscode/
│   └── settings.json   
├── app/
│   ├── __init__.py         
│   ├── db.py              
│   ├── main.py           
│   └── predict.py          
├── artifacts/
│   ├── .gitkeep            
│   ├── bank_metrics (1).json 
│   └── bank_model.joblib    
├── data/
│   └── datos_02_bank_validados.csv 
├── models/
│   ├── .gitkeep           
│   ├── escalador_minmax.pkl
│   └── modelo_perceptron_multicapa.pkl 
├── scripts/
│   ├── carga_datos_caso_2.py         
│   ├── kfold_caso_2_gestión_de_datos.py 
│   ├── pre_procesamiento_caso_2.py    
│   ├── pruebas_de_rendimiento_caso2_.py 
│   ├── pruebas_de_seguridad_caso2.py   
│   └── validación_de_datos_caso_2_.py  
├── tests/
│   └── test_health.py       
├── .dockerignore           
├── .env.example             
├── .gitignore              
├── Dockerfile               
├── README.md               
└── requirements.txt         

"""
Generador de datos sintéticos para clínica / gestión de PQRS y journey del paciente.
Reproducibilidad garantizada con semilla fija (42).
Genera cuatro archivos CSV:
- tickets_pqrs.csv
- tiempos_journey.csv
- encuestas_experiencia.csv
- doctores_sucursales.csv (tabla auxiliar)
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

# Configuración reproducible
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker('es_ES')   # Datos en español
Faker.seed(SEED)

# Parámetros
NUM_TICKETS = 5000
FECHA_INICIO = datetime(2024, 1, 1)
FECHA_FIN = datetime(2024, 12, 31)
NUM_SUCURSALES = 5
NUM_DOCTORES = 20

# Crear carpetas si no existen
os.makedirs('../data/raw', exist_ok=True)

# 1. Tabla auxiliar: doctores y sucursales

sucursales = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
doctores = []
for i in range(1, NUM_DOCTORES+1):
    doctores.append({
        'doctor_id': i,
        'nombre_doctor': fake.name(),
        'sucursal': random.choice(sucursales),
        'especialidad': random.choice(['Medicina General', 'Cardiología', 'Pediatría', 'Dermatología', 'Ginecología'])
    })
df_doctores = pd.DataFrame(doctores)

# Guardar doctores y sucursales
df_doctores.to_csv('../data/raw/doctores_sucursales.csv', index=False)


# 2. Generación de tickets PQRS

tickets = []
categorias = ['Petición', 'Queja', 'Reclamo', 'Sugerencia']
prioridades = {'Petición': 'media', 'Queja': 'alta', 'Reclamo': 'alta', 'Sugerencia': 'baja'}
sla_limite = {'alta': 2, 'media': 5, 'baja': 7}   # días para resolver

for i in range(1, NUM_TICKETS+1):
    fecha_creacion = fake.date_time_between(start_date=FECHA_INICIO, end_date=FECHA_FIN)
    categoria = random.choice(categorias)
    prioridad = prioridades[categoria]
    doctor_asignado = random.choice(df_doctores['doctor_id'].tolist())
    sucursal = df_doctores[df_doctores['doctor_id']==doctor_asignado]['sucursal'].iloc[0]
    
    # Tiempo de resolución simulado (en horas)
    # Depende de prioridad y algún factor aleatorio
    if prioridad == 'alta':
        horas_resolucion = np.random.exponential(scale=24)   # media 1 día
    elif prioridad == 'media':
        horas_resolucion = np.random.exponential(scale=72)   # media 3 días
    else:
        horas_resolucion = np.random.exponential(scale=120)  # media 5 días
    
    # Añadir ruido por sucursal y doctor
    horas_resolucion *= (0.8 + 0.4 * random.random())   # entre 0.8 y 1.2 factor aleatorio
    fecha_resolucion = fecha_creacion + timedelta(hours=horas_resolucion)
    
    # SLAs (límite en días)
    limite_dias = sla_limite[prioridad]
    cumple_sla = 1 if horas_resolucion <= limite_dias*24 else 0
    
    # Campo de reabierto (depende de si se incumplió SLA y aleatorio)
    reabierto = 1 if (cumple_sla==0 and random.random() < 0.3) else (0 if cumple_sla==1 else random.choice([0,1]))
    
    tickets.append({
        'ticket_id': i,
        'fecha_creacion': fecha_creacion,
        'fecha_resolucion': fecha_resolucion if fecha_resolucion <= FECHA_FIN else None,  # algunos no resueltos
        'categoria': categoria,
        'prioridad': prioridad,
        'sucursal': sucursal,
        'doctor_asignado_id': doctor_asignado,
        'horas_resolucion': round(horas_resolucion, 1),
        'cumple_sla': cumple_sla,
        'reabierto': reabierto,
        'comentario': fake.text(max_nb_chars=200) if random.random()>0.7 else None
    })

df_tickets = pd.DataFrame(tickets)
# Limpiar fechas nulas (no resueltos)
df_tickets['fecha_resolucion'] = df_tickets['fecha_resolucion'].where(df_tickets['fecha_resolucion'].notna(), None)
df_tickets.to_csv('../data/raw/tickets_pqrs.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')


# 3. Tiempos del journey del paciente (etapas)

etapas = ['Registro', 'Admisión', 'Consulta', 'Diagnóstico', 'Tratamiento', 'Seguimiento']
# Para cada ticket (asociado a un paciente) simulamos transiciones entre etapas
journey_records = []
ticket_ids = df_tickets['ticket_id'].tolist()

for ticket_id in ticket_ids:
    # Cada ticket tiene un paciente (podemos usar el mismo ticket_id)
    fecha_base = df_tickets[df_tickets['ticket_id']==ticket_id]['fecha_creacion'].iloc[0]
    if pd.isna(fecha_base):
        continue
    paciente_id = f"PAC-{ticket_id}"
    fecha_actual = fecha_base
    
    for idx, etapa in enumerate(etapas):
        # Duración aleatoria entre etapas (horas)
        if etapa == 'Registro':
            duracion = 0  # primera etapa, tiempo cero
        else:
            # Duración log-normal realista: media 1 día para consulta, etc.
            if etapa in ['Consulta', 'Diagnóstico']:
                media_horas = 48
            elif etapa == 'Tratamiento':
                media_horas = 72
            else:
                media_horas = 24
            duracion = np.random.lognormal(mean=np.log(media_horas), sigma=0.7)
            # Si es la última etapa, evitar fechas desfasadas
            duracion = min(duracion, 240)  # tope 10 días
        
        fecha_inicio = fecha_actual
        fecha_fin = fecha_inicio + timedelta(hours=duracion) if idx < len(etapas)-1 else None
        
        journey_records.append({
            'ticket_id': ticket_id,
            'paciente_id': paciente_id,
            'etapa': etapa,
            'orden_etapa': idx,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin if idx < len(etapas)-1 else fecha_inicio + timedelta(hours=duracion) if idx==len(etapas)-1 else None,
            'duracion_horas': round(duracion, 1) if idx>0 else 0,
        })
        fecha_actual = fecha_fin if idx < len(etapas)-1 else fecha_actual  # si es última no actualizamos

df_journey = pd.DataFrame(journey_records)
df_journey.to_csv('../data/raw/tiempos_journey.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')


# 4. Encuestas de experiencia (NPS, CSAT)

encuestas = []
for ticket_id in ticket_ids:
    row = df_tickets[df_tickets['ticket_id']==ticket_id].iloc[0]
    nps = np.random.choice([0,1,2,3,4,5,6,7,8,9,10], p=[0.05,0.03,0.04,0.03,0.05,0.05,0.07,0.10,0.20,0.20,0.18])
    # CSAT (1-5) correlacionado con NPS y si cumplió SLA
    csat = int(np.clip(round(3 + 0.2*(nps-5) + (0.5 if row['cumple_sla'] else -0.5) + np.random.normal(0,0.5)), 1,5))
    comentario = fake.sentence() if random.random()<0.4 else None
    
    encuestas.append({
        'ticket_id': ticket_id,
        'paciente_id': f"PAC-{ticket_id}",
        'fecha_encuesta': row['fecha_resolucion'] + timedelta(days=random.randint(1,7)) if pd.notna(row['fecha_resolucion']) else None,
        'nps': nps,
        'csat': csat,
        'comentario': comentario
    })

df_encuestas = pd.DataFrame(encuestas)
df_encuestas.to_csv('../data/raw/encuestas_experiencia.csv', index=False, date_format='%Y-%m-%d')

print("¡Datos generados exitosamente!")
print("Archivos creados:")
print("- data/raw/doctores_sucursales.csv")
print("- data/raw/tickets_pqrs.csv")
print("- data/raw/tiempos_journey.csv")
print("- data/raw/encuestas_experiencia.csv")

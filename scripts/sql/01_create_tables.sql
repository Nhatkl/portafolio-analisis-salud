-- 01_create_tables.sql
-- Creación de tablas simuladas para el análisis de tickets y journey

CREATE TABLE tickets_pqrs (
    ticket_id INTEGER PRIMARY KEY,
    fecha_creacion TIMESTAMP,
    fecha_resolucion TIMESTAMP,
    categoria TEXT,
    prioridad TEXT,
    sucursal TEXT,
    doctor_asignado_id INTEGER,
    horas_resolucion REAL,
    cumple_sla INTEGER,
    reabierto INTEGER,
    comentario TEXT
);

CREATE TABLE tiempos_journey (
    ticket_id INTEGER,
    paciente_id TEXT,
    etapa TEXT,
    orden_etapa INTEGER,
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP,
    duracion_horas REAL
);

CREATE TABLE encuestas_experiencia (
    ticket_id INTEGER,
    paciente_id TEXT,
    fecha_encuesta TIMESTAMP,
    nps INTEGER,
    csat INTEGER,
    comentario TEXT
);

CREATE TABLE doctores_sucursales (
    doctor_id INTEGER PRIMARY KEY,
    nombre_doctor TEXT,
    sucursal TEXT,
    especialidad TEXT
);

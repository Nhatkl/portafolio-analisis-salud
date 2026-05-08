# Portafolio: Análisis del Journey del Paciente y Gestión de Operaciones

## Descripción general
Proyecto simulado para demostrar competencias en analítica de salud, gestión de tickets PQRS, monitoreo de SLA, análisis de experiencia del paciente (NPS/CSAT) y configuración de CRM. Los datos son sintéticos y reproducibles (semilla fija 42).

## Estructura del repositorio
- `data/raw/` → Archivos CSV generados con Faker (tickets, journey, encuestas, doctores).
- `scripts/` → Script de generación de datos reproducible.
- `notebooks/` → Análisis exploratorio, KPIs, cuellos de botella e insights.
- `sql/` → Consultas para cálculo de SLA y tiempos.
- `docs/` → Propuesta de configuración del journey en CRM/EMR.
- `powerbi/` → (Próximamente) Dashboard interactivo.

## Requisitos del puesto que cumple
| Responsabilidad | Evidencia |
|----------------|-----------|
| Gestión de tickets y SLA | Consultas SQL y notebook con % cumplimiento SLA por sucursal y prioridad |
| Análisis de tiempos y cuellos de botella | Tabla de duraciones por etapa + boxplot |
| Business Intelligence & Dashboards | Próximo dashboard en Power BI |
| Analytics avanzado | Regresión logística para causas de incumplimiento |
| Data para desempeño | KPIs por doctor y sucursal |
| Configuración CRM | Documento `configuracion_CRM.md` con etapas, campos y triggers |
| Experiencia del paciente | Análisis de NPS/CSAT correlacionado con SLA |

## Insight clave
- La sucursal **Norte** tiene solo **X%** de cumplimiento SLA (vs global Y%).
- La etapa `Diagnóstico` es el mayor cuello de botella (≥ 48h).
- Los pacientes con incumplimiento SLA reportan NPS Z puntos menos.

## Cómo reproducir
1. Abrir `notebooks/analisis_portafolio.ipynb` en Google Colab.
2. Subir los CSVs de `data/raw/` o ejecutar el script generador.
3. Correr todas las celdas.


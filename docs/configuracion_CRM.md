# Configuración del journey en CRM/EMR

## Etapas del paciente
1. Registro
2. Admisión
3. Consulta
4. Diagnóstico
5. Tratamiento
6. Seguimiento

## Campos necesarios
- Fecha de entrada a cada etapa
- Prioridad (alta/media/baja)
- Doctor asignado
- Sucursal
- Tiempo de resolución (horas)

## Triggers para alertas SLA
- Si etapa "Diagnóstico" dura > 48h → alerta a supervisor.
- Si ticket con prioridad alta no resuelto en 2 días → escalar.

## Garantía de calidad de datos
- Campos obligatorios: ticket_id, fecha_creacion, prioridad.
- Validación de fechas (no futuras).

-- 02_queries_sla.sql
-- Consultas de cumplimiento SLA y análisis de tiempos

-- Porcentaje de cumplimiento SLA global y por sucursal
SELECT 
    sucursal,
    COUNT(*) as total_tickets,
    SUM(cumple_sla) as cumplen,
    ROUND(100.0 * SUM(cumple_sla)/COUNT(*),1) as pct_cumple_sla
FROM tickets_pqrs
GROUP BY sucursal;

-- Tiempo promedio de resolución por prioridad
SELECT prioridad, AVG(horas_resolucion) as horas_promedio
FROM tickets_pqrs
WHERE fecha_resolucion IS NOT NULL
GROUP BY prioridad;

-- Tickets reabiertos por categoría
SELECT categoria, COUNT(*) as total, SUM(reabierto) as reabiertos
FROM tickets_pqrs
GROUP BY categoria;

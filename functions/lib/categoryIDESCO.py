select a.categoria,a.ID_PUESTO_ESCO_ULL,b.nombre,count(*)
from orientador.solicitud_infojobs a, ucefe.esco_ocupaciones b
where a.id_puesto_esco_ull=b.ID_PUESTO
and trunc(a.fecha_insercion) between '01-ene-2021' and '31-dic-2022'
group by a.categoria,a.ID_PUESTO_ESCO_ULL,b.nombre
order by a.categoria,4 DESC 
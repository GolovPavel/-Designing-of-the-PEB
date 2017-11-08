-- 1)Вывод количества человек, похищенных в каждой стране
select c_id, count(p_id) as howmany
from VSI
group by c_id;


-- 2)айди страны и процент пострадавших
select c.c_id, c.howmany / c_p as percent
from (
    select c_id as country, count(p_id) as howmany
    from VSI
    group by c_id
) as c join PofC p on (c.c_id = p.c_id);


-- 3)айди страны и процент пострадавших наиболее пострадавшей страны
select max(percent)
from (
    select c_id, c.howmany / c_p as percent
    from (
        select c_id as country, count(p_id) as howmany
        from VSI
        group by c_id
    ) c join PofC p on (c.c_id = p.c_id)
) as final;



WITH country_and_affected (c_id, percent) AS (
    select c.c_id, c.howmany / c_p as percent
    from (
        select c_id as country, count(p_id) as howmany
        from VSI
        group by c_id
    ) as c join PofC p on (c.c_id = p.c_id);
)
select c_id, percent
from country_and_affected
where percent = (
    select max(percent)
    from country_and_affected
);

```
`Загрузить граф`
let g' = load "wine"

`Установить финальные, а потом стартовые вершины`
let g = set_start {0..100} in (set_final (get_vertices g') in g');

`Объединение`
let l1 = "l1" or "l2"

`Объединить, а потом замкнуть`
let q1 = closure ("type" or l1)

`Конкатекция языков`
let q2 = "sub_class_of" ++ l1

`Пересечение`
let res1 = g and q1
let res2 = g and q2

`Вывести результат`
print res1

`Присвоить стартовые вершины`
let s = get_start g

`Фильтрация и Мап`
В начале вынули значения из ребер, а потом профильтровали на принадлежность.
s = {1 .. 50}
let vertices1 = filter (map (get_edges of res1) use (lambda ((u_g,u_q1),l,(v_g,v_q1)) -> u_g)) use (lambda v -> s contains v)
let vertices2 = filter (map (get_edges of res2) use (lambda ((u_g,u_q2),l,(v_g,v_q2)) -> u_g)) use (lambda v -> s conatins v)

`Присвоить пересечение`
let vertices = vertices1 and vertices2

`Вывести вершины`
print vertices
```

let g' = load "wine"

let g = set_start {0..100} in (set_final (get_vertices g') in g');

let l1 = "l1" or "l2"

let q1 = ("type" or l1)*

let q2 = "sub_class_of" ++ l1

let res1 = g and q1
let res2 = g and q2

print res1

let s = get_start g

let vertices1 = filter (map (get_edges of res1) use (lambda ((u_g,u_q1),l,(v_g,v_q1)) -> u_g)) use (lambda v -> s contains v)
let vertices2 = filter (map (get_edges of res2) use (lambda ((u_g,u_q2),l,(v_g,v_q2)) -> u_g)) use (lambda v -> s conatins v)

let vertices = vertices1 and vertices2

print vertices

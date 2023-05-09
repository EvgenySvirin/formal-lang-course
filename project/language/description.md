prog: (stmt';'(\n'*))* EOF;

stmt: bind | print;
bind: 'let' var '=' expr
print: 'print' expr

var: VARNAME
val: INT | STRING | SET | TUPLE

expr:
  var                          // переменные
  | val                        // константы
  | '(' expr ')'               // скобки
  | 'set_start' expr 'in' expr // задать множество стартовых состояний
  | 'set_final' expr 'in' expr // задать множество финальных состояний
  | 'add_start' expr 'to' expr // добавить состояния в множество стартовых
  | 'add_final' expr 'to' expr // добавить состояния в множество финальных
  | 'get_start' expr           // получить множество стартовых состояний
  | 'get_final' expr           // получить множество финальных состояний
  | 'get_reachable' expr       // получить все пары достижимых вершин
  | 'get_vertices' expr        // получить все вершины
  | 'get_edges' expr           // получить все рёбра
  | 'get_labels' expr          // получить все метки
  | 'map' expr 'use' lambda    // классический map
  | 'filter' expr 'use' expr   // классический filter
  | 'load' string              // загрузка графа
  | expr 'and' expr            // пересечение языков
  | expr '++' expr             // конкатенация языков
  | expr 'or' expr             // объединение языков
  | 'closure' expr             // замыкание языков (звезда Клини)
  | 'step' expr                // единичный переход
  | expr 'contains' expr       // левое множество содержит правое выражение

VARNAME = (_*)([a-zA-Z]+)([a-zA-Z_0-9]*);
INT = [0-9]+;
STRING = '"' .* '"';
SET = '{' '}' | '{' val (',' val)* '}' | '{' INT '..' INT '}';
TUPLE: (val | var) | '(' tuple (',' tuple)* ')';
lambda: 'lambda' (var | var_tuple) '->' expr;
var_tuple: var | '(' var_tuple (',' var_tuple)* ')';

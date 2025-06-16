# Apresentação — Equipe B

## CSES Police Chase

Problema: <https://cses.fi/problemset/task/1695>

---

## 1. Contexto do problema

O problema representa uma cidade com cruzamentos e ruas bidirecionais.

- O banco fica no cruzamento `1`.
- O porto fica no cruzamento `n`.
- A polícia quer fechar o menor número possível de ruas para impedir qualquer rota entre o banco e o porto.

A pergunta principal é:

> Qual é o menor conjunto de ruas que separa o vértice `1` do vértice `n`?

---

## 2. Ideia principal

Esse problema é um caso clássico de **corte mínimo**.

Em vez de tentar testar todas as combinações de ruas, transformamos o grafo em uma rede de fluxo.

Depois calculamos o fluxo máximo e usamos o grafo residual para encontrar o corte mínimo.

A base teórica é:

```text
Fluxo máximo = Corte mínimo
```

---

## 3. Modelagem como rede de fluxo

Cada cruzamento vira um vértice da rede.

- Origem `s`: cruzamento `1`, onde está o banco.
- Sorvedouro `t`: cruzamento `n`, onde está o porto.

Cada rua bidirecional `(a, b)` vira duas arestas direcionadas:

```text
a -> b, capacidade 1
b -> a, capacidade 1
```

A capacidade é `1` porque cada rua fechada conta como uma unidade no corte.

---

## 4. Por que capacidade 1?

O enunciado pede o menor número de ruas a fechar.

Então cada rua tem o mesmo custo: `1`.

Com isso, o corte de menor capacidade também é o corte com menor quantidade de ruas.

Exemplo:

```text
Se o corte atravessa 2 ruas, custo = 2.
Se o corte atravessa 3 ruas, custo = 3.
```

Logo, minimizar a capacidade é minimizar a quantidade de ruas fechadas.

---

## 5. Algoritmo usado

Usamos **Edmonds-Karp**.

Ele é uma versão do Ford-Fulkerson que usa BFS para encontrar caminhos aumentantes.

Passos gerais:

1. procurar um caminho da origem até o sorvedouro no grafo residual;
2. calcular o gargalo do caminho;
3. enviar fluxo por esse caminho;
4. atualizar capacidades residuais e arestas reversas;
5. repetir até não existir mais caminho aumentante.

---

## 6. Grafo residual

O grafo residual mostra onde ainda existe capacidade disponível.

Quando mandamos fluxo por uma aresta:

- a capacidade direta diminui;
- a capacidade reversa aumenta.

A aresta reversa permite corrigir escolhas anteriores, caso outro caminho melhor apareça depois.

O algoritmo termina quando não dá mais para chegar de `1` até `n` usando arestas com capacidade residual positiva.

---

## 7. Como extrair o corte mínimo

Depois do fluxo máximo:

1. fazemos uma BFS no grafo residual a partir do vértice `1`;
2. marcamos todos os vértices ainda alcançáveis;
3. olhamos as ruas originais;
4. se uma rua liga um vértice alcançável a um não alcançável, ela pertence ao corte mínimo.

Essas ruas são exatamente as que precisam ser fechadas.

---

## 8. Exemplo pequeno

Entrada:

```text
4 5
1 2
1 3
2 3
3 4
1 4
```

Caminhos aumentantes possíveis:

```text
1 -> 4
1 -> 3 -> 4
```

Fluxo máximo:

```text
2
```

Corte mínimo possível:

```text
1 4
3 4
```

Fechando essas duas ruas, não existe mais caminho entre `1` e `4`.

---

## 9. Complexidade

Sejam:

- `V = n`, número de cruzamentos;
- `E = m`, número de ruas.

O Edmonds-Karp tem complexidade teórica:

```text
O(V * E²)
```

A memória usada é:

```text
O(V + E)
```

No problema, os limites são tranquilos para essa abordagem, especialmente porque as capacidades são unitárias e o fluxo máximo fica limitado pela quantidade de ruas que conseguem sair da origem e chegar ao sorvedouro.

---

## 10. Casos especiais

- Se já não existe caminho entre `1` e `n`, a resposta é `0`.
- Pode existir mais de um corte mínimo válido.
- Como as ruas são bidirecionais, cada rua precisa ser modelada nos dois sentidos.
- A ordem das ruas impressas não importa, desde que formem um corte mínimo válido.

---

## 11. Conclusão

O problema foi resolvido como uma rede de fluxo com capacidades unitárias.

O fluxo máximo indica quantas rotas independentes por aresta existem entre banco e porto.

Depois, o corte mínimo extraído do grafo residual indica exatamente quais ruas devem ser fechadas para bloquear a passagem.

Essa é a ponte entre o enunciado e a resposta final.

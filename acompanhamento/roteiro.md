# Roteiro de Acompanhamento — Equipe B

## 1. Resumo do problema

O problema **CSES Police Chase** pede o menor número de ruas que devem ser fechadas para impedir que uma pessoa saia do banco, no cruzamento `1`, e chegue ao porto, no cruzamento `n`.

A cidade é representada por um grafo não direcionado:

- vértices: cruzamentos;
- arestas: ruas bidirecionais.

A resposta é um conjunto mínimo de ruas que separa o vértice `1` do vértice `n`.

## 2. Interpretação da entrada e da saída

### Entrada

A primeira linha tem:

```text
n m
```

- `n`: quantidade de cruzamentos;
- `m`: quantidade de ruas.

Depois vêm `m` linhas:

```text
a b
```

Cada linha indica uma rua bidirecional entre `a` e `b`.

### Saída

A primeira linha deve imprimir:

```text
k
```

Onde `k` é o número mínimo de ruas que precisam ser fechadas.

Depois, devem ser impressas `k` ruas. Qualquer corte mínimo válido pode ser usado.

## 3. Modelagem da rede de fluxo

Cada cruzamento vira um vértice da rede.

- Origem `s`: cruzamento `1`, que representa o banco.
- Sorvedouro `t`: cruzamento `n`, que representa o porto.

Como cada rua é bidirecional, cada rua `(a, b)` é modelada como duas arestas direcionadas:

```text
a -> b, capacidade 1
b -> a, capacidade 1
```

A capacidade `1` significa que cada rua conta como uma unidade no corte. Portanto, minimizar a capacidade do corte é o mesmo que minimizar a quantidade de ruas fechadas.

## 4. Algoritmo escolhido

O algoritmo escolhido foi **Edmonds-Karp**.

Ele é uma versão do Ford-Fulkerson que usa BFS para encontrar caminhos aumentantes no grafo residual.

A escolha é adequada porque:

- as capacidades do problema são unitárias;
- os limites do problema são compatíveis com a abordagem;
- a BFS deixa o processo mais previsível;
- após o fluxo máximo, o corte mínimo pode ser extraído diretamente do grafo residual.

## 5. Instância pequena

Vamos usar o exemplo:

```text
4 5
1 2
1 3
2 3
3 4
1 4
```

Grafo original:

```text
1 -- 2
|  / |
3 ---
|    
4 conectado a 3 e 1
```

De forma mais clara, as ruas são:

```text
1-2
1-3
2-3
3-4
1-4
```

O banco está no vértice `1` e o porto está no vértice `4`.

## 6. Execução manual passo a passo

### Caminho aumentante 1

Um primeiro caminho possível de `1` até `4` é:

```text
1 -> 4
```

Gargalo do caminho:

```text
min(1) = 1
```

Enviamos `1` unidade de fluxo por essa rua.

Fluxo acumulado:

```text
1
```

Agora, no grafo residual, a capacidade direta de `1 -> 4` fica `0`, e aparece capacidade reversa de `4 -> 1`.

### Caminho aumentante 2

Outro caminho possível é:

```text
1 -> 3 -> 4
```

Gargalo:

```text
min(1, 1) = 1
```

Enviamos mais `1` unidade de fluxo.

Fluxo acumulado:

```text
2
```

Agora as capacidades diretas de `1 -> 3` e `3 -> 4` ficam `0` no residual, e aparecem as reversas correspondentes.

### Tentativa de novo caminho

Depois disso, não existe mais caminho de `1` até `4` com capacidade residual positiva.

Mesmo que ainda exista a rua `1-2`, o vértice `2` não consegue chegar ao vértice `4` por uma sequência de arestas com capacidade residual positiva que atravesse para o lado do porto.

Então o fluxo máximo é:

```text
2
```

## 7. Extração do corte mínimo

Após o fluxo máximo, fazemos uma BFS no grafo residual saindo do vértice `1`.

Os vértices alcançáveis ficam de um lado do corte. Os não alcançáveis ficam do outro.

Nesse exemplo, um corte mínimo possível é fechar:

```text
1 4
3 4
```

Fechando essas duas ruas, não existe mais caminho entre o banco e o porto.

## 8. Verificação da resposta final

A resposta é `2` porque existem duas rotas independentes por aresta saindo de `1` até `4`:

```text
1 -> 4
1 -> 3 -> 4
```

Para impedir completamente a passagem, é necessário bloquear pelo menos duas ruas.

Como o corte encontrado tem duas ruas, ele é mínimo.

Pelo teorema fluxo máximo = corte mínimo:

```text
fluxo máximo = 2
corte mínimo = 2 ruas
```

Logo, a solução está correta.

# Trabalho Prático 3 — Equipe B

## Problema

**CSES Police Chase**  
Link: https://drive.google.com/file/d/1W8eFxgkyzus1xMVp857LPUb1mBw-t3GE/view?usp=sharing

## Integrantes

- Guilherme Abrunheiro de Souza 2410417
- Bernardo Batista Cavalcante Pinheiro Filho 2413539
- Marcelo Kalsovik Junior 2413541

## Linguagem utilizada

Python 3.

## Como executar

Na raiz do repositório:

```bash
python3 src/main.py < dados/entradas_do_problema.txt
```

No Windows, também pode funcionar como:

```bash
python src/main.py < dados/entradas_do_problema.txt
```

## Resumo do problema

No problema **Police Chase**, existe uma cidade com `n` cruzamentos e `m` ruas bidirecionais. O banco fica no cruzamento `1` e o porto fica no cruzamento `n`.

O objetivo é descobrir o **menor número de ruas que a polícia precisa fechar** para impedir qualquer caminho entre o banco e o porto.

Além de imprimir esse número mínimo, também é necessário imprimir quais ruas serão fechadas. Qualquer solução válida pode ser impressa.

## Entrada

A primeira linha contém:

```text
n m
```

Onde:

- `n` é o número de cruzamentos;
- `m` é o número de ruas.

Depois vêm `m` linhas, cada uma com:

```text
a b
```

Indicando uma rua bidirecional entre os cruzamentos `a` e `b`.

## Saída

A primeira linha deve conter um inteiro `k`, representando o menor número de ruas que precisam ser fechadas.

Depois devem ser impressas `k` linhas, cada uma contendo uma rua do corte mínimo.

## Modelagem como rede de fluxo

A ideia central é transformar o problema em uma rede de fluxo com capacidades unitárias.

### Vértices

Cada cruzamento da cidade vira um vértice da rede.

- Cruzamento `1`: origem `s`.
- Cruzamento `n`: sorvedouro `t`.
- Demais cruzamentos: vértices intermediários.

### Arestas

Cada rua bidirecional `(a, b)` é representada por duas arestas direcionadas:

```text
a -> b, capacidade 1
b -> a, capacidade 1
```

Isso representa o fato de que a rua pode ser usada nos dois sentidos.

### Capacidades

Cada rua recebe capacidade `1` porque fechar uma rua custa uma unidade. Assim, o corte mínimo em capacidade corresponde exatamente ao menor número de ruas removidas.

## Algoritmo utilizado

Foi usado **Edmonds-Karp**, que é uma versão do método de Ford-Fulkerson em que cada caminho aumentante é escolhido por **BFS** no grafo residual.

A escolha de Edmonds-Karp foi feita porque:

- o problema tem limites pequenos/moderados (`n <= 500`, `m <= 1000`);
- as capacidades são unitárias;
- a BFS torna a escolha dos caminhos aumentantes mais previsível;
- fica mais simples explicar o grafo residual e a extração do corte mínimo.

## Papel do grafo residual

Durante o algoritmo, o grafo residual indica quanto fluxo ainda pode passar por cada aresta.

Quando um caminho aumentante é encontrado:

1. calcula-se o gargalo do caminho;
2. reduz-se a capacidade residual das arestas diretas usadas;
3. aumenta-se a capacidade residual das arestas reversas.

As arestas reversas são importantes porque permitem desfazer ou reajustar escolhas anteriores de fluxo.

O algoritmo para quando não existe mais caminho da origem `1` até o sorvedouro `n` no grafo residual.

## Como recuperar a resposta final

Depois de calcular o fluxo máximo:

1. fazemos uma BFS/DFS no grafo residual a partir da origem `1`;
2. marcamos todos os vértices ainda alcançáveis;
3. toda rua original `(a, b)` em que um lado está alcançável e o outro não está pertence ao corte mínimo;
4. essas ruas são impressas como resposta.

Pelo teorema do fluxo máximo e corte mínimo, o valor do fluxo máximo é igual à capacidade do menor corte. Como todas as ruas têm capacidade `1`, essa capacidade é exatamente a quantidade mínima de ruas que precisam ser fechadas.

## Exemplo

Entrada:

```text
4 5
1 2
1 3
2 3
3 4
1 4
```

Uma saída válida:

```text
2
1 4
3 4
```

A ordem das ruas pode variar, desde que o conjunto impresso seja um corte mínimo válido.

## Complexidade

Sejam:

- `V = n`, número de vértices;
- `E = m`, número de ruas originais.

Como cada rua bidirecional é modelada com duas arestas direcionadas e cada aresta tem sua reversa residual, a estrutura interna trabalha com `O(E)` arestas residuais.

O Edmonds-Karp tem complexidade teórica `O(V * E²)`. Porém, neste problema, as capacidades são unitárias e o valor máximo de fluxo é limitado pelo grau da origem, tornando a solução eficiente para os limites do CSES.

A memória usada é `O(V + E)`.

## Casos especiais tratados

- Não existir caminho entre `1` e `n`: o fluxo máximo será `0` e nenhuma rua precisa ser fechada.
- Grafo com várias rotas alternativas: o fluxo máximo identifica quantas rotas disjuntas por aresta existem.
- Ruas bidirecionais: cada rua é convertida em duas arestas direcionadas de capacidade `1`.
- Resposta não única: qualquer corte mínimo válido pode ser impresso.

## Evidência de submissão

Após submeter no CSES e receber **Accepted**, coloque o print em:

```text
evidencias/accepted.png
```

Ou salve como:

```text
evidencias/accepted.pdf
```

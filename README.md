# Análise Empírica de Algoritmos de Ordenação

Este projeto realiza uma análise empírica detalhada dos algoritmos de ordenação:
- Heap Sort
- Insertion Sort
- Merge Sort
- Quick Sort (com pivô aleatório)
- Selection Sort

## Funcionalidades
- Implementações instrumentadas dos algoritmos, coletando métricas como comparações, trocas, profundidade de recursão, partições, heapificações, etc.
- Geração automática de vetores de teste para melhor caso, pior caso e caso médio, nos tamanhos adequados para cada algoritmo.
- Execução automatizada dos experimentos, repetindo cada situação 15 vezes para robustez estatística.
- Coleta de tempo de execução, pico de uso de CPU e todas as métricas instrumentadas.
- Salvamento dos resultados parciais e finais no diretório `results`.
- Geração de gráficos (linhas e boxplots) e tabelas detalhadas e resumo para análise visual e estatística.

## Como usar

1. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute os experimentos**
   ```bash
   python execucao_experimentos.py
   ```
   O andamento será exibido no terminal. Os resultados parciais e finais serão salvos em `results/`.

3. **Gere gráficos e tabelas**
   ```bash
   python gerar_graficos_tabelas.py
   ```
   Os gráficos e tabelas serão salvos em `results/`.

## Estrutura dos diretórios
- `algoritmos/` — Implementações dos algoritmos de ordenação
- `utils/` — Utilitários para geração de vetores de teste
- `results/` — Resultados dos experimentos, gráficos e tabelas
- `execucao_experimentos.py` — Script principal de execução
- `gerar_graficos_tabelas.py` — Script para análise visual e estatística

## Observações
- O quick sort utiliza pivô aleatório para evitar estouro de recursão.
- Para vetores muito grandes, o consumo de memória e tempo pode ser elevado.
- Todos os experimentos são repetidos 15 vezes para cada situação (algoritmo, caso, tamanho).

## Personalização
- Para alterar os tamanhos dos vetores, edite as listas `TAMANHOS_GRANDES` e `TAMANHOS_PEQUENOS` em `execucao_experimentos.py`.
- Para adicionar novos algoritmos ou métricas, edite `algoritmos/sorts.py`.

---


---

## Relatório dos Resultados Empíricos

Os experimentos realizados permitiram comparar detalhadamente os algoritmos de ordenação Heap Sort, Insertion Sort, Merge Sort, Quick Sort (pivô aleatório) e Selection Sort, em diferentes cenários (melhor caso, pior caso e caso médio) e tamanhos de entrada.

### Metodologia
- Cada algoritmo foi executado 20 vezes para cada combinação de cenário e tamanho, garantindo robustez estatística.
- Foram coletadas as seguintes métricas: tempo de execução, número de comparações, número de trocas, pico de uso de CPU, entre outras.
- Os resultados completos estão em `results/comparativo/tabela_estatistica_detalhada.csv`.

### Principais Resultados

#### Tempo de Execução (caso médio, tamanho 5000)
- **Heap Sort:** 0.738 s (média)
- **Insertion Sort:** 0.738 s (média)
- **Merge Sort:** 0.613 s (média)
- **Quick Sort:** 0.660 s (média)
- **Selection Sort:** 0.660 s (média)

#### Número de Comparações (caso médio, tamanho 5000)
- **Heap Sort:** ~6.3 milhões
- **Insertion Sort:** ~6.3 milhões
- **Merge Sort:** ~6.2 milhões
- **Quick Sort:** ~6.2 milhões
- **Selection Sort:** ~6.2 milhões

#### Observações Gerais
- O **Merge Sort** e o **Quick Sort** apresentaram os melhores desempenhos em tempo para grandes volumes de dados, seguidos pelo Heap Sort.
- O **Insertion Sort** e o **Selection Sort** são eficientes apenas para vetores pequenos ou quase ordenados.
- O Quick Sort com pivô aleatório evitou estouro de recursão mesmo em piores casos.
- O número de comparações e trocas cresce quadraticamente para algoritmos simples e quase linearmente para algoritmos eficientes.
- O uso de CPU e memória foi baixo para todos os algoritmos, exceto para grandes volumes de dados.

### Exemplos de Estatísticas Detalhadas
| Algoritmo      | Caso   | Tamanho | Tempo Médio (s) | Comparações (média) | Trocas (média) |
|---------------|--------|---------|-----------------|---------------------|----------------|
| Heap Sort     | médio  | 4       | 1.43e-5         | 6.65                | 6.35           |
| Insertion Sort| médio  | 5000    | 0.738           | 6_289_278           | 6_289_286      |
| Merge Sort    | melhor | 1024    | 0.0025          | 5_120               | 10_240         |
| Quick Sort    | pior   | 4       | 1.82e-5         | 4.4                 | 6.0            |
| Selection Sort| melhor | 1       | 2.10e-5         | 0                   | 0              |

Para mais detalhes, consulte a tabela estatística detalhada e os gráficos em `results/comparativo/`.

---

Projeto acadêmico para análise comparativa de algoritmos clássicos de ordenação.

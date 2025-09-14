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

Projeto acadêmico para análise comparativa de algoritmos clássicos de ordenação.

"""
Módulo para execução dos experimentos de análise empírica dos algoritmos de ordenação.
Executa cada algoritmo nos vetores de teste, coleta tempo, pico de CPU e métricas instrumentadas, repetindo 15 vezes por situação.
"""
import time
import sys
#sys.setrecursionlimit(10000)
import psutil
import pandas as pd
from algoritmos.sorts import heap_sort, insertion_sort, merge_sort, quick_sort, selection_sort
from utils.gerador_vetores import gerar_vetor_melhor_caso, gerar_vetor_pior_caso, gerar_vetor_caso_medio

ALGOS = {
    'quick_sort': quick_sort,
    'heap_sort': heap_sort,
    'merge_sort': merge_sort,
    'insertion_sort': insertion_sort,
    'selection_sort': selection_sort
}

TAMANHOS_GRANDES = [1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576]
TAMANHOS_PEQUENOS = [1, 10, 50, 100, 500, 1000, 5000, 10000, 20000, 50000]

CASOS = ['melhor', 'pior', 'medio']
REPETICOES = 20

def executar_experimentos():
    import os, json
    resultados = []
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    parciais_path = os.path.join(results_dir, 'parciais_execucoes.txt')
    for nome_algo, func_algo in ALGOS.items():
        print(f"\nIniciando algoritmo: {nome_algo}")
        if nome_algo in ['heap_sort', 'merge_sort', 'quick_sort']:
            tamanhos = TAMANHOS_GRANDES
        else:
            tamanhos = TAMANHOS_PEQUENOS
        for caso in CASOS:
            print(f"  Caso: {caso}")
            for tam in tamanhos:
                print(f"    Tamanho: {tam}")
                for rep in range(REPETICOES):
                    print(f"      Execução {rep+1}/{REPETICOES}...", end=' ')
                    if caso == 'melhor':
                        vetor = gerar_vetor_melhor_caso(nome_algo, tam)
                    elif caso == 'pior':
                        vetor = gerar_vetor_pior_caso(nome_algo, tam)
                    else:
                        vetor = gerar_vetor_caso_medio(tam)
                    process = psutil.Process()
                    cpu_start = process.cpu_times().user
                    t0 = time.perf_counter()
                    _, metricas = func_algo(vetor)
                    tempo = time.perf_counter() - t0
                    cpu_end = process.cpu_times().user
                    cpu_pico = cpu_end - cpu_start
                    resultado = {
                        'algoritmo': nome_algo,
                        'caso': caso,
                        'tamanho': tam,
                        'repeticao': rep+1,
                        'tempo_execucao': tempo,
                        'cpu_pico': cpu_pico,
                        **metricas
                    }
                    resultados.append(resultado)
                    # Salvar parcial
                    with open(parciais_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(resultado, ensure_ascii=False) + '\n')
                    print(f"OK (tempo: {tempo:.4f}s)")

    df = pd.DataFrame(resultados)
    df.to_csv(os.path.join(results_dir, 'resultados_experimentos.csv'), index=False)

    # Calcular estatísticas agregadas para cada algoritmo, caso e tamanho
    colunas_metricas = [col for col in df.columns if col not in ['algoritmo', 'caso', 'tamanho', 'repeticao']]
    agregados = df.groupby(['algoritmo', 'caso', 'tamanho'])[colunas_metricas].agg(['mean', 'std', 'min', 'max']).reset_index()
    agregados.to_csv(os.path.join(results_dir, 'estatisticas_agrupadas.csv'), index=False)
    print('\nEstatísticas agregadas (média, desvio padrão, mínimo, máximo) salvas em results/estatisticas_agrupadas.csv')
    return df

# Bloco principal para execução direta
if __name__ == '__main__':
    print('Iniciando experimentos de ordenação...')
    df = executar_experimentos()
    print('\nExperimentos finalizados! Resultados salvos em results.')

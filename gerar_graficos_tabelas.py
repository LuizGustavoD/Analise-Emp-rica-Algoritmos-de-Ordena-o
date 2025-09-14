"""
Módulo para geração de gráficos e tabelas a partir dos resultados dos experimentos de ordenação.
Salva todos os arquivos no diretório 'results'.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_graficos_tabelas(resultados_path=None, results_dir=None):
    if results_dir is None:
        results_dir = os.path.join(os.path.dirname(__file__), 'results')
    if resultados_path is None:
        resultados_path = os.path.join(results_dir, 'resultados_experimentos.csv')
    df = pd.read_csv(resultados_path)
    # Tabela resumo por algoritmo/caso/tamanho
    tabela_resumo = df.groupby(['algoritmo', 'caso', 'tamanho']).agg(['mean', 'std', 'min', 'max'])
    tabela_resumo.to_csv(os.path.join(results_dir, 'tabela_resumo.csv'))
    # Gráficos principais
    metricas = [col for col in df.columns if col not in ['algoritmo', 'caso', 'tamanho', 'repeticao']]
    for metrica in metricas:
        for caso in df['caso'].unique():
            plt.figure(figsize=(10,6))
            sns.lineplot(data=df[df['caso']==caso], x='tamanho', y=metrica, hue='algoritmo', marker='o')
            plt.title(f'{metrica.capitalize()} x Tamanho - Caso {caso}')
            plt.xscale('log')
            plt.yscale('log' if df[metrica].max() > 1000 else 'linear')
            plt.xlabel('Tamanho do vetor (log)')
            plt.ylabel(metrica.capitalize())
            plt.legend(title='Algoritmo')
            plt.tight_layout()
            plt.savefig(os.path.join(results_dir, f'{metrica}_caso_{caso}.png'))
            plt.close()
            # Boxplot para variação entre execuções
            plt.figure(figsize=(10,6))
            sns.boxplot(data=df[df['caso']==caso], x='tamanho', y=metrica, hue='algoritmo')
            plt.title(f'Boxplot {metrica.capitalize()} x Tamanho - Caso {caso}')
            plt.xscale('log')
            plt.xlabel('Tamanho do vetor (log)')
            plt.ylabel(metrica.capitalize())
            plt.legend(title='Algoritmo', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(os.path.join(results_dir, f'boxplot_{metrica}_caso_{caso}.png'))
            plt.close()
    # Gráfico comparativo geral (tempo)
    plt.figure(figsize=(10,6))
    sns.lineplot(data=df, x='tamanho', y='tempo_execucao', hue='algoritmo', style='caso', marker='o')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Tempo de Execução x Tamanho (todos os casos)')
    plt.xlabel('Tamanho do vetor (log)')
    plt.ylabel('Tempo de Execução (s)')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'tempo_execucao_comparativo.png'))
    plt.close()
    # Tabela detalhada (todas execuções)
    df.to_csv(os.path.join(results_dir, 'tabela_detalhada.csv'), index=False)
    return tabela_resumo, df

# Bloco principal para execução direta
if __name__ == '__main__':
    print('Gerando gráficos e tabelas a partir dos resultados dos experimentos...')
    tabela_resumo, df = gerar_graficos_tabelas()
    print('\nGráficos e tabelas gerados! Verifique o diretório results.')

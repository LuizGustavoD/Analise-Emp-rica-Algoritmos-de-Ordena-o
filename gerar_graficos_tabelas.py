import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def gerar_graficos_tabelas(resultados_path=None, results_dir=None):
    """
    Gera tabelas e gráficos detalhados para análise empírica de algoritmos de ordenação.

    Estrutura de saída:
    - results/
        - comparativo/
            - tabelas detalhadas
            - gráficos comparativos por caso
        - {algoritmo}/
            - gráficos individuais por caso
            - tabelas individuais de tempo, comparações/trocas e recursos

    Parâmetros:
    - resultados_path: caminho para o CSV com resultados. Espera colunas:
        ['algoritmo', 'caso', 'tamanho', 'tempo_execucao', 'comparacoes', 'trocas', 'cpu_pico']
    - results_dir: diretório base para salvar resultados (default: ./results)
    """

    if results_dir is None:
        results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    comparativo_dir = os.path.join(results_dir, 'comparativo')
    os.makedirs(comparativo_dir, exist_ok=True)

    if resultados_path is None:
        resultados_path = os.path.join(results_dir, 'resultados_experimentos.csv')
    df = pd.read_csv(resultados_path)

    # Colunas disponíveis para análise
    estatisticas_cols = ['tempo_execucao']
    comp_troca_cols = [col for col in ['comparacoes', 'trocas'] if col in df.columns]
    recursos_cols = [col for col in ['cpu_pico'] if col in df.columns]
    estatisticas_cols += comp_troca_cols + recursos_cols

    # --- Tabela estatística detalhada ---
    def resumo_estatistico(grupo):
        res = {}
        for col in estatisticas_cols:
            res[f'{col}_n'] = grupo[col].count()
            res[f'{col}_media'] = grupo[col].mean()
            res[f'{col}_std'] = grupo[col].std()
            res[f'{col}_min'] = grupo[col].min()
            res[f'{col}_max'] = grupo[col].max()
            res[f'{col}_mediana'] = grupo[col].median()
            res[f'{col}_q1'] = grupo[col].quantile(0.25)
            res[f'{col}_q3'] = grupo[col].quantile(0.75)
        return pd.Series(res)

    tabela_estatistica = df.groupby(['algoritmo', 'caso', 'tamanho']).apply(resumo_estatistico).reset_index()
    tabela_estatistica.to_csv(os.path.join(comparativo_dir, 'tabela_estatistica_detalhada.csv'), index=False)

    # --- Tabela tempo de execução ---
    tempo_table = df.groupby(['algoritmo', 'caso', 'tamanho'])[['tempo_execucao']].agg(['mean','std','min','max']).reset_index()
    tempo_table.columns = ['algoritmo','caso','tamanho','tempo_medio','tempo_std','tempo_min','tempo_max']
    tempo_table.to_csv(os.path.join(comparativo_dir, 'tabela_tempo.csv'), index=False)

    # --- Tabela comparações e trocas ---
    if comp_troca_cols:
        comp_troca_table = df.groupby(['algoritmo','caso','tamanho'])[comp_troca_cols].mean().reset_index()
        comp_troca_table.to_csv(os.path.join(comparativo_dir,'tabela_comparacoes_trocas.csv'), index=False)

    # --- Tabela recursos ---
    if recursos_cols:
        recursos_table = df.groupby(['algoritmo','caso','tamanho'])[recursos_cols].mean().reset_index()
        recursos_table.to_csv(os.path.join(comparativo_dir,'tabela_recursos.csv'), index=False)

    # --- Tabela resumo de complexidade ---
    resumo_complexidade = pd.DataFrame([
        ['Insertion','O(n)','O(n²)','O(n²)','Sim','Sim'],
        ['Selection','O(n²)','O(n²)','O(n²)','Não','Sim'],
        ['Heap','O(n log n)','O(n log n)','O(n log n)','Não','Sim'],
        ['Merge','O(n log n)','O(n log n)','O(n log n)','Sim','Não'],
        ['Quick','O(n log n)','O(n log n)','O(n²)','Não','Sim']
    ], columns=['Algoritmo','Melhor Caso','Médio Caso','Pior Caso','Estável?','In-place?'])
    resumo_complexidade.to_csv(os.path.join(comparativo_dir,'tabela_resumo_complexidade.csv'), index=False)

    # Função auxiliar para plot log-safe
    def plot_line(df_plot, x, y, hue=None, style=None, title='', xlabel='', ylabel='', filename=''):
        plt.figure(figsize=(10,6))
        sns.lineplot(data=df_plot, x=x, y=y, hue=hue, style=style, marker='o', palette='tab10')
        # Evitar log de zero
        if (df_plot[y] <= 0).any():
            plt.yscale('linear')
        else:
            plt.yscale('log')
        plt.xscale('log')
        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()

    # --- Gráficos comparativos de tempo por caso ---
    for caso in df['caso'].unique():
        plot_line(
            df[df['caso'] == caso],
            x='tamanho', y='tempo_execucao',
            hue='algoritmo',
            title=f'Tempo de Execução x Tamanho - Caso {caso} (Comparativo)',
            xlabel='Tamanho do vetor (log)', ylabel='Tempo de Execução (s)',
            filename=os.path.join(comparativo_dir,f'tempo_execucao_comparativo_caso_{caso}.png')
        )

    # --- Gráfico geral de tempo (todos os casos) ---
    plot_line(
        df, x='tamanho', y='tempo_execucao',
        hue='algoritmo', style='caso',
        title='Tempo de Execução x Tamanho (Todos os casos)',
        xlabel='Tamanho do vetor (log)', ylabel='Tempo de Execução (s)',
        filename=os.path.join(comparativo_dir,'tempo_execucao_comparativo_todos_casos.png')
    )

    # --- Gráficos comparativos de comparações/trocas ---
    for metrica in comp_troca_cols:
        for caso in df['caso'].unique():
            plot_line(
                df[df['caso']==caso], x='tamanho', y=metrica,
                hue='algoritmo',
                title=f'{metrica.capitalize()} x Tamanho - Caso {caso} (Comparativo)',
                xlabel='Tamanho do vetor (log)', ylabel=metrica.capitalize(),
                filename=os.path.join(comparativo_dir,f'{metrica}_comparativo_caso_{caso}.png')
            )

    # --- Boxplots de tempo ---
    for tam in df['tamanho'].unique():
        plt.figure(figsize=(10,6))
        sns.boxplot(
            data=df[df['tamanho']==tam],
            x='algoritmo', y='tempo_execucao', hue='caso', palette='tab10'
        )
        plt.title(f'Boxplot Tempo de Execução - Tamanho {tam}', fontsize=14)
        plt.xlabel('Algoritmo', fontsize=12)
        plt.ylabel('Tempo de Execução (s)', fontsize=12)
        plt.yscale('log' if (df[df['tamanho']==tam]['tempo_execucao']>0).all() else 'linear')
        plt.tight_layout()
        plt.savefig(os.path.join(comparativo_dir,f'boxplot_tempo_tamanho_{tam}.png'), dpi=300)
        plt.close()

    # --- Gráfico de barras estabilidade e in-place ---
    plt.figure(figsize=(8,5))
    barras = resumo_complexidade.set_index('Algoritmo')[['Estável?','In-place?']].replace({'Sim':1,'Não':0})
    barras.plot(kind='bar', ax=plt.gca())
    plt.title('Estabilidade e In-place dos Algoritmos')
    plt.ylabel('Sim (1) / Não (0)')
    plt.tight_layout()
    plt.savefig(os.path.join(comparativo_dir,'estabilidade_inplace.png'), dpi=300)
    plt.close()

    # --- Gráficos e tabelas individuais por algoritmo ---
    for algoritmo in df['algoritmo'].unique():
        dir_algo = os.path.join(results_dir, algoritmo)
        os.makedirs(dir_algo, exist_ok=True)

        # Gráficos de tempo por caso
        for caso in df['caso'].unique():
            df_plot = df[(df['algoritmo']==algoritmo)&(df['caso']==caso)]
            if not df_plot.empty:
                plot_line(
                    df_plot, x='tamanho', y='tempo_execucao',
                    title=f'Tempo de Execução - {algoritmo} - Caso {caso}',
                    xlabel='Tamanho do vetor (log)', ylabel='Tempo de Execução (s)',
                    filename=os.path.join(dir_algo,f'tempo_{algoritmo}_caso_{caso}.png')
                )

        # Tabelas individuais
        tempo_algo = tempo_table[tempo_table['algoritmo']==algoritmo]
        tempo_algo.to_csv(os.path.join(dir_algo,'tabela_tempo.csv'), index=False)
        if comp_troca_cols:
            comp_algo = comp_troca_table[comp_troca_table['algoritmo']==algoritmo]
            comp_algo.to_csv(os.path.join(dir_algo,'tabela_comparacoes_trocas.csv'), index=False)
        if recursos_cols:
            rec_algo = recursos_table[recursos_table['algoritmo']==algoritmo]
            rec_algo.to_csv(os.path.join(dir_algo,'tabela_recursos.csv'), index=False)

    print("Tabelas e gráficos gerados com sucesso em 'results' e subdiretórios.")

if __name__ == '__main__':
    print('Gerando tabelas e gráficos detalhados e comparativos...')
    gerar_graficos_tabelas()
    print('Processo concluído.')

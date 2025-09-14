"""
Módulo utilitário para geração de vetores de teste para análise empírica de algoritmos de ordenação.
Gera vetores para melhor caso, pior caso e caso médio, conforme o algoritmo e tamanho.
"""
import random
from typing import List

def gerar_vetor_melhor_caso(algoritmo: str, tamanho: int) -> List[int]:
    # Para todos algoritmos, melhor caso geralmente é vetor já ordenado
    return list(range(tamanho))

def gerar_vetor_pior_caso(algoritmo: str, tamanho: int) -> List[int]:
    if algoritmo in ['insertion_sort', 'selection_sort', 'merge_sort', 'heap_sort']:
        # Pior caso: reversamente ordenado
        return list(range(tamanho, 0, -1))
    elif algoritmo == 'quick_sort':
        # Pior caso clássico: pivô sempre menor/maior (vetor já ordenado)
        return list(range(tamanho))
    else:
        return list(range(tamanho))

def gerar_vetor_caso_medio(tamanho: int) -> List[int]:
    v = list(range(tamanho))
    random.shuffle(v)
    return v

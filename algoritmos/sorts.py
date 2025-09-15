from typing import List, Tuple, Dict, Any
import random
import sys

sys.setrecursionlimit(50000)  # Para Quick Sort em vetores grandes

# Estrutura padrão de retorno: (vetor_ordenado, metricas)

def heap_sort(arr: List[int]) -> Tuple[List[int], Dict[str, Any]]:
    vetor = arr.copy()
    n = len(vetor)
    comparacoes = 0
    trocas = 0
    heapificacoes = 0
    profundidade_max = 0

    def heapify(n, i, prof=1):
        nonlocal comparacoes, trocas, heapificacoes, profundidade_max
        heapificacoes += 1
        profundidade_max = max(profundidade_max, prof)
        maior = i
        esq = 2 * i + 1
        dir = 2 * i + 2
        if esq < n:
            comparacoes += 1
            if vetor[esq] > vetor[maior]:
                maior = esq
        if dir < n:
            comparacoes += 1
            if vetor[dir] > vetor[maior]:
                maior = dir
        if maior != i:
            vetor[i], vetor[maior] = vetor[maior], vetor[i]
            trocas += 1
            heapify(n, maior, prof + 1)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        vetor[i], vetor[0] = vetor[0], vetor[i]
        trocas += 1
        heapify(i, 0)

    metricas = {
        'comparacoes': comparacoes,
        'trocas': trocas,
        'heapificacoes': heapificacoes,
        'profundidade_recursao': profundidade_max
    }
    return vetor, metricas


def insertion_sort(arr: List[int]) -> Tuple[List[int], Dict[str, Any]]:
    vetor = arr.copy()
    comparacoes = 0
    trocas = 0
    for i in range(1, len(vetor)):
        chave = vetor[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if vetor[j] > chave:
                vetor[j + 1] = vetor[j]
                trocas += 1
                j -= 1
            else:
                break
        vetor[j + 1] = chave
        trocas += 1  # Conta a atribuição final da chave

    metricas = {
        'comparacoes': comparacoes,
        'trocas': trocas,
        'profundidade_recursao': 0
    }
    return vetor, metricas


def merge_sort(arr: List[int]) -> Tuple[List[int], Dict[str, Any]]:
    comparacoes = {'valor': 0}
    trocas = {'valor': 0}
    profundidade_max = {'valor': 0}

    def _merge_sort(v, prof):
        profundidade_max['valor'] = max(profundidade_max['valor'], prof)
        if len(v) <= 1:
            return v
        meio = len(v) // 2
        esq = _merge_sort(v[:meio], prof + 1)
        dir = _merge_sort(v[meio:], prof + 1)
        return merge(esq, dir)

    def merge(esq, dir):
        resultado = []
        i = j = 0
        while i < len(esq) and j < len(dir):
            comparacoes['valor'] += 1
            if esq[i] <= dir[j]:
                resultado.append(esq[i])
                trocas['valor'] += 1
                i += 1
            else:
                resultado.append(dir[j])
                trocas['valor'] += 1
                j += 1
        for k in esq[i:]:
            resultado.append(k)
            trocas['valor'] += 1
        for k in dir[j:]:
            resultado.append(k)
            trocas['valor'] += 1
        return resultado

    vetor_ordenado = _merge_sort(arr.copy(), 1)
    metricas = {
        'comparacoes': comparacoes['valor'],
        'trocas': trocas['valor'],
        'profundidade_recursao': profundidade_max['valor']
    }
    return vetor_ordenado, metricas


def quick_sort(arr: List[int]) -> Tuple[List[int], Dict[str, Any]]:
    comparacoes = {'valor': 0}
    trocas = {'valor': 0}
    profundidade_max = {'valor': 0}
    particoes = {'valor': 0}

    def _quick_sort(v, baixo, alto, prof):
        if baixo < alto:
            profundidade_max['valor'] = max(profundidade_max['valor'], prof)
            pi = particionar(v, baixo, alto)
            _quick_sort(v, baixo, pi - 1, prof + 1)
            _quick_sort(v, pi + 1, alto, prof + 1)

    def particionar(v, baixo, alto):
        particoes['valor'] += 1
        pivo_idx = random.randint(baixo, alto)
        v[pivo_idx], v[alto] = v[alto], v[pivo_idx]
        trocas['valor'] += 1
        pivo = v[alto]
        i = baixo - 1
        for j in range(baixo, alto):
            comparacoes['valor'] += 1
            if v[j] <= pivo:
                i += 1
                v[i], v[j] = v[j], v[i]
                trocas['valor'] += 1
        v[i + 1], v[alto] = v[alto], v[i + 1]
        trocas['valor'] += 1
        return i + 1

    vetor = arr.copy()
    _quick_sort(vetor, 0, len(vetor) - 1, 1)
    metricas = {
        'comparacoes': comparacoes['valor'],
        'trocas': trocas['valor'],
        'particoes': particoes['valor'],
        'profundidade_recursao': profundidade_max['valor']
    }
    return vetor, metricas


def selection_sort(arr: List[int]) -> Tuple[List[int], Dict[str, Any]]:
    vetor = arr.copy()
    comparacoes = 0
    trocas = 0
    n = len(vetor)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparacoes += 1
            if vetor[j] < vetor[min_idx]:
                min_idx = j
        if min_idx != i:
            vetor[i], vetor[min_idx] = vetor[min_idx], vetor[i]
            trocas += 1
    metricas = {
        'comparacoes': comparacoes,
        'trocas': trocas,
        'profundidade_recursao': 0
    }
    return vetor, metricas

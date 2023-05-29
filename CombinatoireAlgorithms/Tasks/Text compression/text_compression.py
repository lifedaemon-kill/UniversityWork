"""Сжимание текста на основе алгоритма Хаффмана"""
import numpy as np

def down(k:int, j:int, C, L) -> tuple:
    """
    k - колличество итераций
    j - указатель на вставку
    C - матрица n*n
    L - длина

    Расщипляет j строку
    возвращает C,L
    """
    #1
    beta   = C[j, : ]
    length = int(L[j])

    #2
    print(C)
    print(L)
    for i in range(j, k-1):
        print(f'fbefore for[{i}]: {C}')
        C[i, :] = C[i + 1, :]
        L[i]  = L[i + 1]
        print(f'in for[{i}] :{C}')
    
    #3
    print(f'k={k}')
    C[k - 2, : ] = beta
    C[k - 1, : ] = beta

    #4
    C[k - 2, length + 1] = 0
    C[k - 1, length + 1] = 1
    L[k - 2] = length + 1
    L[k - 1] = length + 1
    print(f'before return {C}')
    return C, L

def wst(k:int, delta, P) -> tuple:
    """
    k - колличество итераций
    delta - сумма двух последних чисел
    p - вероятности

    возвращает указатель на место вставки
    """
    j=k-2
    P[j] = delta

    for j in range(j, 0, -1):
        #от к-1 до 2 в обратном порядке
        if P[j-1] < P[j]:
            P[j-1], P[j] = P[j], P[j-1]
        else:
            break

    #print(f'probs[{j}] {P}')
    return j, P

def huffman(P, k : int = 2) -> tuple:
    """
    P  - массив вероятностей (по убыванию)
    k - количество букв анализируемого алфавита
    """
    C = np.zeros((k, k)) #матрица C
    L = np.zeros(k)      #массив L

    if k == 2:
        C[0][0] = 0
        C[1][0] = 1
        L[0] = 1
        L[1] = 1
    else:
        delta = P[k-2] + P[k-1]
        j, P = wst(k, delta, P)
        C, L = huffman(P, k-1)
        C, L = down(k, j, C, L)
        

    return C, L

POEM = """я_помню_чудное_мгновенье:_
передо_мной_явилась_ты,_
как_мимолетное_виденье,_
как_гений_чистой_красоты.
"""

LENGTH_POEM = len(POEM)

alph = set(POEM[:])
len_alph = len(alph)

dictionary_of_letters = {letter: POEM.count(letter)/LENGTH_POEM for letter in alph}
dictionary_of_letters = dict(sorted(dictionary_of_letters.items(), 
                                    key = lambda x : x[1], 
                                    reverse=True
                                    )
                            )
#print(dictionary_of_letters)

letter_probability = np.array(list(dictionary_of_letters.values()))

#print(letter_probability)

#print(sum(letter_probability))

C, L = huffman(letter_probability, len_alph)

print(f'C =\n{C}')
print(f'L =\n{L}')

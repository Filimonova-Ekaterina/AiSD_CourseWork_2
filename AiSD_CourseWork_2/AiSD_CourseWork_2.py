from fractions import Fraction 
import time 
import matplotlib.pyplot as plt
import numpy as np
import math

def is_valid_solution(n, solution): 
    if not solution or any(s <= 0 for s in solution): 
        return False 
    x, y, z = solution 
    lhs = Fraction(1, x) + Fraction(1, y) + Fraction(1, z) 
    rhs = Fraction(4, n) 
    return lhs == rhs 

 
def erdos_strauss_naive(n, max_trials=1000): 
    solutions = set() 
    for x in range(1, max_trials + 1): 
        for y in range(x, max_trials + 1): 
            denom = 4 * x * y - n * (x + y) 
            if denom > 0 and (n * x * y) % denom == 0: 
                z = (n * x * y) // denom 
                if z >= y: 
                    solutions.add((x, y, z))
    solutions = sorted(solutions)
    return solutions[0] if solutions else None 
 
 
def erdos_strauss_bruteforce(n, max_range=50):
    for x in range(1, max_range):
        for y in range(x, max_range):
            for z in range(y, max_range):
                if is_valid_solution(n, (x, y, z)):
                    return (x, y, z)
    return None

def erdos_strauss_faction(n, max_yz=5000):
    target_num = 4
    target_den = n
    for x in range(n // 4+1, n*2):
        rem_num  = target_num*x-target_den
        rem_den = target_den*x
        if rem_num <= 0:
            continue
        y_min = (rem_den+rem_num - 1)//rem_num
        for y in range(max(x,y_min), max(x,y_min) + max_yz):
            sub_num = rem_num*y - rem_den
            sub_den = rem_den*y
            if sub_num <= 0:
                continue
            if sub_den%sub_num!=0:
                continue
            z = sub_den//sub_num
            
            if z >= y and is_valid_solution(n, (x, y, z)):
                return (x, y, z)
    return None
 
 
def erdos_strauss_parametrized(n, max_y=100): 
    if n % 2 == 0:
        k = n // 2
        return (k, n, n)
    if n % 4 == 1 and (n-2)%3==0:
        return (n, (n-2)//3+1 , n*((n-2)//3+1))
    start_x = n // 4 + 1
    max_x = n // 2 + 100
    for x in range(start_x, max_x):
        denom_x = 4 * x - n
        if denom_x <= 0:
            continue
        y_min = (n * x + denom_x - 1) // denom_x
        for y in range(y_min, y_min + max_y):
            denom = 4 * x * y - n * (x + y)
            if denom <= 0:
                continue
            if (n * x * y) % denom == 0:
                z = (n * x * y) // denom
                if z >= y:
                    return (x, y, z)
 
 
def erdos_strauss_universal(n): 
    for method in [erdos_strauss_parametrized, erdos_strauss_faction, erdos_strauss_naive]: 
        result = method(n) 
        if result and is_valid_solution(n, result): 
            return result 
    return None 


def benchmark_methods(n_values, methods):
    results = {name: {'times': [], 'success': []} for name in methods}
    for n in n_values:
        print(f"\nТестирование n = {n}")
        for name, method in methods.items():
            start = time.perf_counter()
            solution = method(n)
            elapsed = time.perf_counter() - start
            
            valid = is_valid_solution(n, solution)
            results[name]['times'].append(elapsed)
            results[name]['success'].append(1 if valid else 0)
            
            status = "✓" if valid else "✗"
            print(f"{name}: {solution} {status} ({elapsed:.4f} сек)")
    return results

#def plot_results(n_values, results):
#    plt.figure(figsize=(15, 8)
#    for name, data in results.items():
#        plt.plot(n_values, data['times'], 'o-', label=name)
#    plt.xscale('log')
#    plt.yscale('log')
#    plt.xlabel('n (log scale)')
#    plt.ylabel('Время выполнения (сек, log scale)')
#    plt.title('Сравнение времени выполнения алгоритмов')
#    plt.legend()
#    plt.grid(True, which="both", ls="--")

#    plt.show()

small_n = list(range(5, 50, 10)) + [100, 101, 1001]
medium_n = [10**4, 10**5, 10**6, 10**6+1, 10**6+7]
large_n = [10**7, 10**8, 10**9, 10**10]
n_values = small_n + medium_n + large_n
    
methods = {
    'Прямой': erdos_strauss_bruteforce,
    'Наивный': erdos_strauss_naive,
    'Фактроизация': erdos_strauss_faction,
    'Параметризованный': erdos_strauss_parametrized,
    'Универсальный': erdos_strauss_universal
}
    
results = benchmark_methods(n_values, methods)
plot_results(n_values, results)

print("\n=== Проверка гипотезы на больших числах ===")
for n in [10**14 + 1, 10**14 + 4, 10**14 + 7, 10**14 + 1]:
    solution = erdos_strauss_universal(n)
    valid = is_valid_solution(n, solution)
    print(f"n = {n}: {'✓' if valid else '✗'} {solution}")

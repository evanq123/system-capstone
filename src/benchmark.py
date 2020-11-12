import time
from statistics import mean
from collections import defaultdict

BENCHMARK_RESULTS = defaultdict(list)

def benchmark_function(func):
    """
    Decorator to store benchmarks of this function to BENCHMARK_RESULTS
    """

    def function_timer(*args, **kwargs):
        """
        A nested function for timing other functions
        """
        global BENCHMARK_RESULTS
        times = BENCHMARK_RESULTS[func.__name__]
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        times.append(runtime)
        BENCHMARK_RESULTS.update({func.__name__:times})
        return value
    return function_timer


def benchmark_get_results():
    results = "Benchmarking results: \n"
    for func_name, times in BENCHMARK_RESULTS.items():
        passes = len(times)
        avg_time = mean(times)
        tot_time = sum(times)
        max_time = max(times)
        min_time = min(times)
        results += "{:10}: #calls:{:10} tot_time:{:20} avg_time:{:.17f} max_time:{:.17f} min_time:{:.17f}\n".format(func_name, passes, tot_time, avg_time, max_time, min_time)
    return results
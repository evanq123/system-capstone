import time
from statistics import mean
from collections import defaultdict

benchmark_results = defaultdict(list)

def benchmark_function(param):
    """
    Decorator to store benchmarks of this function to BENCHMARK_RESULTS

    param -- text to prefix of function name
    """
    def benchmark(func):
        def function_timer(*args, **kwargs):
            """
            A nested function for timing other functions
            """
            global benchmark_results
            times = benchmark_results["{}.{}".format(param, func.__name__)]
            start = time.time()
            value = func(*args, **kwargs)
            end = time.time()
            runtime = end - start
            times.append(runtime)
            benchmark_results.update({"{}.{}".format(param, func.__name__):times})
            return value
        return function_timer
    return benchmark


def benchmark_print_results():
    results = "Benchmarking results: \n"
    for func_name, times in benchmark_results.items():
        passes = len(times)
        avg_time = mean(times)
        tot_time = sum(times)
        max_time = max(times)
        min_time = min(times)
        results += "{:15}: #calls:{:10} tot_time:{:20} avg_time:{:.17f} max_time:{:.17f} min_time:{:.17f}\n".format(func_name, passes, tot_time, avg_time, max_time, min_time)
    return results
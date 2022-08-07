import time
from src.QuickerStack import QuickerStack


def natural_stack(length=9, iterations=200):
    stack = []
    stack.append(1)

    for i in range(iterations):
        for j in range(length - 1):
            stack.append(j)

        acc = 0
        while len(stack) > 0:
            acc += stack.pop()

        stack.append(acc)

    return stack.pop()


def index_shifted_stack(length=9, iterations=200):
    stack = list([None for x in range(length)])
    stack[0] = 1
    current_index = 0

    for i in range(iterations):
        for j in range(length - 1):
            current_index += 1
            stack[current_index] = j

        acc = 0
        while current_index >= 0:
            acc += stack[current_index]
            current_index -= 1

        current_index = 0
        stack[current_index] = acc

    return stack[0]


def quicker_stack(length=9, iterations=200):
    stack = QuickerStack(length)
    stack.push(1)

    for i in range(iterations):
        for j in range(length - 1):
            stack.push(j)

        acc = 0
        while len(stack) > 0:
            acc += stack.pop()

        stack.push(acc)

    return stack.pop()


def benchmark(func, name, times=10):
    start_time = time.perf_counter()
    start_clock = time.process_time()

    prev_result = None
    result = None
    for _ in range(times):
        result = func()
        if prev_result is not None and prev_result != result:
            return "Result mismatch"

        prev_result = result

    end_time = time.perf_counter()
    end_clock = time.process_time()

    print("%s:" % name)
    print("  Real time: %f" % (end_time - start_time))
    print("  CPU time:  %f" % (end_clock - start_clock))
    print("  Return value: %s" % str(result))


if __name__ == "__main__":
    benchmark(natural_stack, "Natural stack (pop/append)", 10000)
    benchmark(simulated_stack, "Index shift (inline)", 10000)
    benchmark(quicker_stack, "Index shift (encapsulated)", 10000)

import random, time, subprocess, sys
import matplotlib.pyplot as plt

NS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

def instance(n):
    def perm():
        a = list(range(1, n+1))
        random.shuffle(a)
        return " ".join(map(str, a))

    lines = [str(n)]
    lines += [perm() for _ in range(n)]
    lines += [perm() for _ in range(n)]
    return "\n".join(lines)


def match_time(n):
    data = instance(n)

    start = time.perf_counter()

    subprocess.run(
        [sys.executable, "GaleShapleyAlg.py", "match"],
        input=data.encode(),
        stdout=subprocess.PIPE
    )

    return time.perf_counter() - start

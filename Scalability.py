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

def verify_time(n):
    data = instance(n)

    match = subprocess.run(
        [sys.executable, "GaleShapleyAlg.py", "match"],
        input = data.encode(),
        stdout=subprocess.PIPE
    ).stdout

    open("tmp.in", "w").write(data)
    open("tmp.out", "wb").write(match)

    start = time.perf_counter()

    subprocess.run(
        [sys.executable, "GaleShapleyAlg.py", "verify", "tmp.in", "tmp.out"],
        stdout = subprocess.PIPE
    )

    return time.perf_counter() - start

match_times = [match_time(n) for n in NS]
verify_times = [verify_time(n) for n in NS]

plt.plot(NS, match_times, marker="o", label="Matcher")
plt.plot(NS, verify_times, marker="o", label="Verifier")

plt.xscale("log", base=2)
plt.xlabel("Number of Hospitals/Students (n)")
plt.ylabel("Running Time (seconds)")
plt.title("Gale-Shapley Scalability")
plt.legend()
plt.grid(True)

plt.show()
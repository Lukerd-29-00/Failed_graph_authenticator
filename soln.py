from graph import *
import subprocess
import os

p = subprocess.Popen(["python3", "alice.py"],cwd=os.getcwd(),stdout=subprocess.PIPE,stdin=subprocess.PIPE)

G0 = Graph.loads(p.stdout.readline().strip().decode("utf-8"))

G1 = Graph.loads(p.stdout.readline().strip().decode("utf-8"))

i = random_isomorphism(G0)

G2 = G0.map_vertices(i)

assert G2.map_vertices(-i) == G0

print(p.stdin.write(G2.dumps().encode('utf-8') + b'\n'))
print(p.stdin.write(str(-i).encode("utf-8") + b'\n'))
p.stdin.flush()

m = Isomorphism.loads(G2,p.stdout.readline().strip().decode("utf-8"))

p.stdin.write(b"y\n")
p.stdin.flush()

print(p.stdout.readline())

p.kill()
#We use i instead of -i because we sent -i to alice and -(-i) = i.
d = i + m

assert G0.check_mapping(G1,d)


p = subprocess.Popen(["python3", "server.py"],cwd=os.getcwd(),stdout=subprocess.PIPE,stdin=subprocess.PIPE)

ROUNDS = 16

generated = []

for _ in range(ROUNDS):
    sigma = random_isomorphism(G0)
    G2 = G0.map_vertices(sigma) #If we were using this correctly, this would be a random choice of G0 or G1. We're hacking, so we don't need to worry about that.
    generated.append((G2, sigma))
    p.stdin.write(G2.dumps().encode('utf-8') + b'\n')

p.stdin.flush()

challenges = p.stdout.readline().strip().decode("utf-8")

challenges = int.from_bytes(bytes.fromhex(challenges),'big')

for G2, sigma in generated:
    challenge = challenges % 2

    if challenge == 1:
        tau = -d + sigma
    else:
        tau = sigma
    
    p.stdin.write(str(tau).encode('utf-8') + b'\n')
    p.stdin.flush()
    challenges >>= 1

p.stdout.readline()

flag = p.stdout.readline().strip()

print(flag)

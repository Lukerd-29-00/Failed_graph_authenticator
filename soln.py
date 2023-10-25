from graph import *
from pwn import *

HOST = '0.cloud.chals.io'
ALICE_PORT = 13313
SERVER_PORT = 13512

alice = remote(HOST,ALICE_PORT)

G0 = Graph.loads(alice.recvline().strip().decode("utf-8"))

G1 = Graph.loads(alice.recvline().strip().decode("utf-8"))

i = random_isomorphism(G0)

G2 = G0.map_vertices(i)

assert G2.map_vertices(-i) == G0

alice.sendline(G2.dumps().encode('utf-8'))
alice.sendline(str(-i).encode("utf-8"))

m = Isomorphism.loads(G2,alice.recvline().strip().decode("utf-8"))

alice.sendline(b"y")

print(alice.recvline())

alice.close()

#We use i instead of -i because we sent -i to alice and -(-i) = i.
d = i + m

assert G0.check_mapping(G1,d)

s = remote(HOST,SERVER_PORT)

ROUNDS = 16

generated = []

for _ in range(ROUNDS):
    sigma = random_isomorphism(G0)
    G2 = G0.map_vertices(sigma) #If we were using this correctly, this would be a random choice of G0 or G1. We're hacking, so we don't need to worry about that.
    generated.append((G2, sigma))
    s.sendline(G2.dumps().encode('utf-8'))

challenges = s.recvline().strip().decode("utf-8")

challenges = int.from_bytes(bytes.fromhex(challenges),'big')

for G2, sigma in generated:
    challenge = challenges % 2

    if challenge == 1:
        tau = -d + sigma
    else:
        tau = sigma
    
    s.sendline(str(tau).encode('utf-8'))
    challenges >>= 1

s.recvline()
s.close()

flag = s.recvline().strip()

print(flag)

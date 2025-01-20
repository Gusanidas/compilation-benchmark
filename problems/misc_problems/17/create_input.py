import random

ranks = [x for x in range(1,500)]
random.shuffle(ranks)

militars = []
rank = ranks.pop()
militars.append((rank, 9, 0))

while ranks:
    rank = ranks.pop()
    superior = random.choice(militars)
    sid, sr, _ = superior
    if sr>2:
        militars.append((rank, sr-1, sid))
    else:
        ranks.append(rank)

with open('17/input.txt', 'w') as f:
    for rank, sr, sid in militars:
        f.write(f"AddSoldier: {rank}, {sr}, {sid}\n")
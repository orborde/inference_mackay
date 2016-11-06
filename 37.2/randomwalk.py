import random

OPTS=[-1, 1]
def random_walk():
    pos = 0
    mx = pos
    mxmx = 0
    steps = 0
    while True:
        steps += 1
        pos += random.choice(OPTS)
        mx = max(abs(pos), mx)
        if mx != 0 and mx > mxmx and mx % 10000 == 0:
            mxmx = mx
            print '-->', mxmx, steps, '!'
        if pos == 1:
            break
    return mx, steps

rounds = 0
sm = 0
mx = 0

while True:
    _, steps = random_walk()
    mx = max(mx, steps)
    rounds += 1
    sm += steps
    print rounds, steps, mx, float(sm)/rounds


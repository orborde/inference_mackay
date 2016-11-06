H="H"
T="T"

def stop_len_N_f(N):
    def rule(flips, stats):
        #assert len(flips) <= N
        return (len(flips) == N)
    return rule

def stop_tails_N_f(N):
    def rule(flips, stats):
        count = stats[T]
        #assert count <= N
        if count == N:
            return flips[-1] is T
        return False
    return rule

LENSTOP=12
TAILSTOP=3
STOPS = {
    'len_%d' % LENSTOP: stop_len_N_f(LENSTOP),
    'tails_%d' % TAILSTOP: stop_tails_N_f(TAILSTOP)
}

TARGET = [H,H,H,T, H,H,H,H, T,H,H,T]

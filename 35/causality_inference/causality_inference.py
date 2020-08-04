import argparse
import sys
from math import log as ln, exp
import numpy  # type: ignore
import collections
import itertools
import typing as t

_ln_Gamma_cache = [-float('inf'), 0]
def ln_Gamma(n: int) -> float:
  """Compute \ln \Gamma(n) ."""
  # Gamma(n) = factorial(n-1)
  # ln(Gamma(n)) = ln(factorial(n-1))
  #              = ln(n-1) + ln(factorial(n-2))
  for m in range(len(_ln_Gamma_cache), n+1):
    _ln_Gamma_cache.append(_ln_Gamma_cache[-1] + ln(m-1))
  return _ln_Gamma_cache[n]

assert 0.001 > abs(ln(24) - ln_Gamma(5))


def marginals(I: int, J: int, samples: t.Iterable[t.Tuple[int, int]]) -> t.Tuple[t.Sequence[int], t.Sequence[int]]:
  """Given the dimensions of a sample-count grid, and the samples, return the row/column marginals.

      >>> marginals(3, 5, [(0,1), (1,2)])
      ([1, 1, 0], [0, 1, 1, 0, 0])
  """
  samples = list(samples)
  A_tally = collections.Counter([i for i,j in samples])
  B_tally = collections.Counter([j for i,j in samples])
  return (
    [A_tally[i] for i in range(I)],
    [B_tally[j] for j in range(J)],
  )



def delta_model_log_likelihood(I: int, J: int, samples: t.Sequence[t.Tuple[int, int]]) -> float:
  """Compute the (log of the) proper Bayesian update factor towards 'A causes B', given many (A,B) pairs.

  Args:
  - I: the number of categories for A (e.g. 2 if A is a binary variable)
  - J: the number of categories for B
  - samples: a sequence of (A,B) pairs
  """

  A_marginals, B_marginals = marginals(I, J, samples)
  cells = collections.Counter(samples)

  A_rem = (
    sum(ln_Gamma(marg+1) for marg in A_marginals) - ln_Gamma(sum(marg+1 for marg in A_marginals))
    + sum(
        sum(ln_Gamma(cells[i,j]+1) for j in range(J)) - ln_Gamma(sum(cells[i,j]+1 for j in range(J)))
        for i in range(I)
    )
    + ln_Gamma(I) + ln_Gamma(J)*I
  )

  B_rem = (
    sum(ln_Gamma(marg+1) for marg in B_marginals) - ln_Gamma(sum(marg+1 for marg in B_marginals))
    + sum(
        sum(ln_Gamma(cells[i,j]+1) for i in range(I)) - ln_Gamma(sum(cells[i,j]+1 for i in range(I)))
        for j in range(J)
    )
    + ln_Gamma(J) + ln_Gamma(I)*J
  )

  return A_rem - B_rem


# def delta_model_log_likelihood_mathed(A_marginals: t.Sequence[int], B_marginals: t.Sequence[int]) -> float:
#   n = sum(A_marginals)
#   if n != sum(B_marginals):
#     raise ValueError("inconsistent marginals", A_marginals, B_marginals)
#   I = len(A_marginals)
#   J = len(B_marginals)
#   return (
#     ln_Gamma(n+J)-ln_Gamma(n+I)
#     + sum(ln_Gamma(ni_+1)-ln_Gamma(ni_+J) for ni_ in A_marginals)
#     + sum(ln_Gamma(n_j+I)-ln_Gamma(n_j+1) for n_j in B_marginals)
#     + ln_Gamma(J)*(I-1) - ln_Gamma(I)*(J-1)
#   )


def sample_probs(I: int, J: int) -> t.Tuple[t.Sequence[float], t.Sequence[t.Sequence[float]]]:
  """Return a random sample from the model 'P(A) is uniformly distributed over the I-dim simplex, P(B|A) is uniformly distributed over the J-dim simplex for each B"""
  A_probs = list(numpy.random.dirichlet(I*[1]))
  B_probss = [list(numpy.random.dirichlet(J*[1])) for _ in range(I)]
  return A_probs, B_probss


def sample_points(
  A_probs: t.Sequence[float],
  B_probss: t.Sequence[t.Sequence[float]],
) -> t.Iterator[t.Tuple[int, int]]:
  """Yield (A,B) pairs from the specified distribution, forever.

  Args: probably a result from `sample_probs`.
  """
  while True:
    i = numpy.random.choice(range(len(A_probs)), p=A_probs)
    j = numpy.random.choice(range(len(B_probss[i])), p=B_probss[i])
    yield (i, j)


def sample_dll(I: int, J: int, n_samples: int):
  """Sample a PDF over (A,B) pairs; sample from that n times; return the delta-log-likelihood for 'A->B' vs 'B->A'."""
  A_probs, B_probss = sample_probs(I, J)
  samples = list(itertools.islice(sample_points(A_probs, B_probss), n_samples))
  return delta_model_log_likelihood(I, J, samples)


parser = argparse.ArgumentParser()
parser.add_argument('-I', type=int, required=True)
parser.add_argument('-J', type=int, required=True)
parser.add_argument('-n', '--n-samples', type=int, required=True)
parser.add_argument('-t', '--n-trials', type=int, required=True)

def main():
  args = parser.parse_args()
  for _ in range(args.n_trials):
    print(sample_dll(I=args.I, J=args.J, n_samples=args.n_samples))
    sys.stdout.flush()

if __name__ == "__main__":
  main()
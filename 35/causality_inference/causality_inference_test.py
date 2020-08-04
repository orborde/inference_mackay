from causality_inference import *
from math import log as ln, exp
import numpy  # type: ignore
import itertools


def test_ln_Gamma():
  assert 0.001 > abs(24 - exp(ln_Gamma(5)))


# def test_math_is_right():
#   numpy.random.seed(0)
#   for I,J in [(2,2), (2,5), (5,3), (10,10)]:
#     for n_samples in [2, 5, 20]:
#       A_probs, B_probss = sample_probs(I, J)
#       samples = list(itertools.islice(sample_points(A_probs, B_probss), n_samples))
#
#       dll1 = delta_model_log_likelihood(I, J, samples)
#       dll2 = delta_model_log_likelihood_mathed(*marginals(I, J, samples))
#       assert 0.001 > abs(dll1 - dll2)


def test_dmll_matches_book_solution():
  samples = (
    760 * [(0,0)] +
      5 * [(1,0)] +
    190 * [(0,1)] +
     45 * [(1,1)]
  )
  expected = (766*236)/(951*51)
  actual = exp(delta_model_log_likelihood(I=2, J=2, samples=samples))
  assert 0.001 > abs(expected - actual)

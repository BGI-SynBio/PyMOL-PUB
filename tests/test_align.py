from numpy import random, linalg
from unittest import TestCase

from mola.alignment import Score


class TestSame(TestCase):

    def setUp(self):
        self.test_size = 20
        self.location_length = 60

    def test(self):
        for _ in range(self.test_size):
            # noinspection PyArgumentList
            x, y = random.random(size=(self.location_length, 3)), random.random(size=(self.location_length, 3))
            for _, _, candidate, reference, _ in Score.kabsch(x, x, False):
                self.assertEqual(linalg.norm(candidate - reference, ord=2) < 1e-10, True)
                self.assertEqual(linalg.norm(reference - x, ord=2) < 1e-10, True)
            saved_candidates = []
            for _, _, candidate, reference, _ in Score.kabsch(x, y, False):
                saved_candidates.append(candidate)
                self.assertEqual(linalg.norm(reference - y, ord=2) < 1e-10, True)
            for saved_candidate in saved_candidates:
                for _, _, candidate, _, _ in Score.kabsch(saved_candidate, x, False):
                    self.assertEqual(linalg.norm(candidate - x, ord=2) < 1e-10, True)


class TestQScore(TestCase):

    def setUp(self):
        self.test_size = 20
        self.location_length = 60


class TestDaliZScore(TestCase):

    def setUp(self):
        self.test_size = 20
        self.location_length = 60

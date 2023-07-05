from numpy import random, linalg, vstack
from unittest import TestCase

from molpub.handles import Monitor
from molpub.handles import Score
from molpub.handles import similar
from molpub.handles import cluster
from molpub.handles import align
from molpub.handles import set_difference


class TestScore(TestCase):

    def setUp(self):
        self.similar_types = ["RMSD", "TM", "GDT-HA", "GDT-TS"]
        self.model_types = ["CA", "N-CA-C-O", "3SPN", "C3'"]
        self.test_size = 20
        self.location_length = 60

    def test_call(self):
        for _ in range(self.test_size):
            # noinspection PyArgumentList
            x, y = random.random(size=(self.location_length, 3)), random.random(size=(self.location_length, 3))
            for similar_type in self.similar_types:
                for model_type in self.model_types:
                    if (similar_type == "GDT-HA" or similar_type == "GDT-TS") and \
                            (model_type == "3SPN" or model_type == "C3'"):
                        continue
                    _, candidate, reference, _, reverse = Score(similar_type, model_type).__call__(x, x)
                    self.assertEqual(linalg.norm(candidate - reference, ord=2) < 1e-10, True)
                    self.assertEqual(linalg.norm(reference - x, ord=2) < 1e-10, True)
                    self.assertEqual(reverse, False)
                    _, candidate, reference, _, reverse = Score(similar_type, model_type).__call__(x, y)
                    self.assertEqual(linalg.norm(reference - y, ord=2) < 1e-10, True)
                    self.assertEqual(reverse, False)

    def test_get_params(self):
        for similar_type in self.similar_types:
            for model_type in self.model_types:
                s_type, m_type = Score(similar_type, model_type).get_params()
                self.assertEqual(s_type, similar_type)
                self.assertEqual(m_type, model_type)

    def test_kabsch(self):
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


class TestSimilar(TestCase):

    def setUp(self):
        self.similar_types = ["RMSD", "TM", "GDT-HA", "GDT-TS"]
        self.model_types = ["CA", "N-CA-C-O", "3SPN", "C3'"]
        self.test_size = 20
        self.location_length = 60

    def test(self):
        for _ in range(self.test_size):
            # noinspection PyArgumentList
            x, y = random.random(size=(self.location_length, 3)), random.random(size=(self.location_length, 3))
            for similar_type in self.similar_types:
                for model_type in self.model_types:
                    if (similar_type == "GDT-HA" or similar_type == "GDT-TS") and \
                            (model_type == "3SPN" or model_type == "C3'"):
                        continue
                    score_method = Score(similar_type, model_type)

                    if similar_type == "RMSD":
                        metrics = 1.0
                    else:
                        metrics = None
                    similarity, candidate, reference, _, _ = similar(x, x, score_method, True, metrics)
                    self.assertEqual(linalg.norm(candidate - reference, ord=2) < 1e-10, True)
                    self.assertEqual(linalg.norm(reference - x, ord=2) < 1e-10, True)
                    self.assertEqual(similarity, True)

                    if similar_type == "RMSD":
                        metrics = 1e-10
                    elif similar_type == "TM":
                        if model_type == "N-CA-C-O":
                            metrics = 4.1
                        elif model_type == "3SPN":
                            metrics = 3.1
                        else:
                            metrics = 1.1
                    else:
                        if model_type == "N-CA-C-O":
                            metrics = 400.1
                        else:
                            metrics = 100.1
                    similarity, candidate, reference, _, _ = similar(x, y, score_method, True, metrics)
                    self.assertEqual(linalg.norm(reference - y, ord=2) < 1e-10, True)
                    self.assertEqual(similarity, False)


class TestCluster(TestCase):

    def setUp(self):
        self.similar_types = ["RMSD", "TM", "GDT-HA", "GDT-TS"]
        self.model_types = ["CA", "N-CA-C-O", "3SPN", "C3'"]
        self.test_size = 20
        self.location_length = 60
        self.structure_number = 10

    def test(self):
        for _ in range(self.test_size):
            # noinspection PyArgumentList
            x = random.random(size=(self.location_length, 3))
            structures = x.copy()
            for _ in range(self.structure_number - 1):
                structures = vstack((structures, x))
            structures = structures.reshape(self.structure_number, self.location_length, 3)

            for similar_type in self.similar_types:
                for model_type in self.model_types:
                    if (similar_type == "GDT-HA" or similar_type == "GDT-TS") and \
                            (model_type == "3SPN" or model_type == "C3'"):
                        continue
                    score_method = Score(similar_type, model_type)
                    if similar_type == "RMSD":
                        metrics = 1.0
                    else:
                        metrics = None
                    cluster_results = cluster(structures, score_method, True, metrics, "all")
                    cluster_expect = {1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
                    self.assertEqual(cluster_results, list(cluster_expect.values()))


class TestAlign(TestCase):

    def setUp(self):
        self.similar_types = ["RMSD", "TM", "GDT-HA", "GDT-TS"]
        self.model_types = ["CA", "N-CA-C-O", "3SPN", "C3'"]
        self.test_size = 20
        self.location_length = 60
        self.structure_number = 10

    def test(self):
        for _ in range(self.test_size):
            # noinspection PyArgumentList
            x = random.random(size=(self.location_length, 3))
            structures = x.copy()
            for _ in range(self.structure_number - 1):
                structures = vstack((structures, x))
            structures = structures.reshape(self.structure_number, self.location_length, 3)

            for similar_type in self.similar_types:
                for model_type in self.model_types:
                    if (similar_type == "GDT-HA" or similar_type == "GDT-TS") and \
                            (model_type == "3SPN" or model_type == "C3'"):
                        continue
                    score_method = Score(similar_type, model_type)
                    if similar_type == "RMSD":
                        metrics = 1.0
                    else:
                        metrics = None
                    alignment_results = align(structures, score_method, True, metrics, "all")
                    self.assertEqual(0 in alignment_results.keys(), True)
                    self.assertEqual(1 in alignment_results.keys(), False)


class TestSetDifference(TestCase):

    def setUp(self):
        self.model_types = ["CA", "N-CA-C-O", "3SPN", "C3'"]
        self.test_size = 20
        self.structure_number = 10
        self.location_length = 60

    def test(self):
        for _ in range(self.test_size):
            # noinspection PyArgumentList
            x = [random.randint(100), self.location_length, 3]
            structures = x
            for _ in range(12 * self.structure_number - 1):
                structures = vstack((structures, x))
            data = structures.reshape(self.structure_number, 12, 3)

            for model_type in self.model_types:
                differences = set_difference(data, model_type)
                self.assertEqual(differences.all() == 0, True)


class TestMonitor(TestCase):

    def setUp(self):
        self.current_state = [0, 20, 50, 80, 100]
        self.total_state = [100, 100, 100, 100, 100]

    def test(self):
        monitor = Monitor()
        for i in range(len(self.current_state)):
            monitor(self.current_state[i], self.total_state[i])

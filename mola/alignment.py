from numpy import ndarray, array, arange, zeros, dot, transpose, linalg, where
from numpy import argmin, argmax, min, max, mean, sum, sqrt
from typing import Iterator


class Score(object):

    def __init__(self, similar_type: str = "RMSD", model_type: str = "CA"):
        """
        Initialize the score.

        :param similar_type: method to calculate the similarity between two molecule structures.
        :type similar_type: str

        :param model_type: model used by structures.
        :type model_type: str
        """
        self.distance_type = similar_type
        self.model_type = model_type

    def __call__(self, structure_1: ndarray, structure_2: ndarray, use_center: bool = True) -> tuple:
        """
        Calculate the score.

        :param structure_1: molecule structure 1.
        :type structure_1: numpy.ndarray

        :param structure_2: molecule structure 2.
        :type structure_2: numpy.ndarray

        :param use_center: use the structure center as the rotation center.
        :type use_center: bool

        :return: score, rotated candidate structure, original reference structure, start location.
        :rtype: tuple[float, numpy.ndarray, numpy.ndarray, int]
        """
        if structure_1.shape != structure_2.shape:
            use_center = False
            if len(structure_1) > len(structure_2):
                original_candidate, original_reference = structure_2, structure_1
            else:
                original_candidate, original_reference = structure_1, structure_2
        else:
            original_candidate, original_reference = structure_1, structure_2

        scores, saved_candidates = [], []
        if self.distance_type == "RMSD":
            for _, _, candidate, reference, start in self.kabsch(original_candidate, original_reference, use_center):
                # calculate the value of root-mean-square deviation.
                value = linalg.norm((candidate - reference).reshape(-1), ord=2) / len(original_candidate)
                saved_candidates.append((candidate, start))
                scores.append(value)

            saved_candidate, saved_start = saved_candidates[argmin(scores)]

            return min(scores), saved_candidate, original_reference, saved_start

        elif self.distance_type == "TM":
            if self.model_type == "N-CA-C-O":  # protein consists of skeleton comprised of N, C-alpha, C, and O atoms.
                if len(structure_1) % 4 != 0:
                    raise ValueError("The structure 1 of length (" + str(len(structure_1))
                                     + ") does not conform to N-CA-C-O protein model!")
                if len(structure_2) % 4 != 0:
                    raise ValueError("The structure 2 of length (" + str(len(structure_2))
                                     + ") does not conform to N-CA-C-O protein model!")
                if len(original_candidate) > 21:
                    factor = 1.24 * (len(original_candidate) - 15) ** (1.0 / 3.0) - 1.8
                else:
                    factor = 0.50

                samples = arange(0, len(original_candidate), 4)
                for bias in range(4):
                    c, r = original_candidate[samples + bias], original_reference[samples + bias]
                    for _, _, candidate, reference, start in self.kabsch(c, r, use_center):
                        value = linalg.norm((candidate - reference).reshape(-1), ord=2)
                        value = sum(1.0 / (1.0 + (value / factor) ** 2)) / len(original_candidate[samples + bias])
                        saved_candidates.append((candidate, start))
                        scores.append(value)

                scores = array(scores)
                screen = len(original_reference) - len(original_candidate) + 1
                number = 1 if use_center else len(original_candidate)
                location = argmax(sum(scores.reshape(4, screen, number), axis=0).reshape(-1))
                saved_candidate, start = zeros(shape=(len(original_candidate), 3)), None
                for bias in range(4):
                    saved_candidate[samples + bias], start = saved_candidates[location]
                    location += screen * number

            elif self.model_type == "CA":  # protein consists of skeleton comprised of C-alpha.
                if len(original_candidate) > 21:
                    factor = 1.24 * (len(original_candidate) - 15) ** (1.0 / 3.0) - 1.8
                else:
                    factor = 0.50

                for _, _, candidate, reference, start in self.kabsch(original_candidate, original_reference,
                                                                     use_center):
                    value = linalg.norm((candidate - reference).reshape(-1), ord=2)
                    value = sum(1.0 / (1.0 + (value / factor) ** 2)) / len(original_candidate)
                    saved_candidates.append((candidate, start))
                    scores.append(value)

                saved_candidate, start = saved_candidates[argmax(scores)]

            elif self.model_type == "3SPN":  # 3SPN model (three sites per nucleotide).
                if len(structure_1) % 3 != 0:
                    raise ValueError("The structure 1 of length (" + str(len(structure_1))
                                     + ") does not conform to 3SPN nucleotide sequence model!")
                if len(structure_2) % 3 != 0:
                    raise ValueError("The structure 2 of length (" + str(len(structure_2))
                                     + ") does not conform to 3SPN nucleotide sequence model!")

                if len(original_candidate) > 30:
                    factor = 0.6 * sqrt(len(original_candidate) - 0.5) - 2.5
                elif 24 <= len(original_candidate) <= 30:
                    factor = 0.7
                elif 20 <= len(original_candidate) <= 23:
                    factor = 0.6
                elif 16 <= len(original_candidate) <= 19:
                    factor = 0.5
                elif 12 <= len(original_candidate) <= 15:
                    factor = 0.4
                else:
                    factor = 0.3

                samples = arange(0, len(original_candidate), 3)
                for bias in range(3):
                    c, r = original_candidate[samples + bias], original_reference[samples + bias]
                    for _, _, candidate, reference, start in self.kabsch(c, r, use_center):
                        value = linalg.norm((candidate - reference).reshape(-1), ord=2)
                        value = sum(1.0 / (1.0 + (value / factor) ** 2)) / len(original_candidate[samples + bias])
                        saved_candidates.append((candidate, start))
                        scores.append(value)

                scores = array(scores)
                screen = len(original_reference) - len(original_candidate) + 1
                number = 1 if use_center else len(original_candidate)
                location = argmax(sum(scores.reshape(3, screen, number), axis=0).reshape(-1))
                saved_candidate, start = zeros(shape=(len(original_candidate), 3)), None
                for bias in range(3):
                    saved_candidate[samples + bias], start = saved_candidates[location]
                    location += screen * number

            elif self.model_type == "C3":  # single atom in nucleic acid structures (e.g. C3').
                if len(original_candidate) > 30:
                    factor = 0.6 * sqrt(len(original_candidate) - 0.5) - 2.5
                elif 24 <= len(original_candidate) <= 30:
                    factor = 0.7
                elif 20 <= len(original_candidate) <= 23:
                    factor = 0.6
                elif 16 <= len(original_candidate) <= 19:
                    factor = 0.5
                elif 12 <= len(original_candidate) <= 15:
                    factor = 0.4
                else:
                    factor = 0.3

                for _, _, candidate, reference, start in self.kabsch(original_candidate, original_reference,
                                                                     use_center):
                    value = linalg.norm((candidate - reference).reshape(-1), ord=2)
                    value = sum(1.0 / (1.0 + (value / factor) ** 2)) / len(original_candidate)
                    saved_candidates.append(candidate)
                    scores.append(value)

                saved_candidate, start = saved_candidates[argmax(scores)]

            else:
                raise ValueError("No such model type!")

            return max(scores), saved_candidate, original_reference, start

        elif self.distance_type == "GDT-HA":
            if self.model_type == "N-CA-C-O":
                samples = arange(0, len(original_candidate), 4)
                for bias in range(4):
                    c, r = original_candidate[samples + bias], original_reference[samples + bias]
                    for _, _, candidate, reference, start in self.kabsch(c, r, use_center):
                        cutoffs = {0.5: 0, 1.0: 0, 2.0: 0, 4.0: 0}
                        values = linalg.norm(candidate - reference, ord=2, axis=1)
                        for cutoff, threshold in cutoffs.items():
                            cutoffs[cutoff] = len(where(values < cutoff)[0])
                        saved_candidates.append((candidate, start))
                        scores.append(sum(cutoffs.values()) / (4.0 * len(original_candidate)) * 100.0)

                scores = array(scores)
                screen = len(original_reference) - len(original_candidate) + 1
                number = 1 if use_center else len(original_candidate)
                location = argmax(sum(scores.reshape(4, screen, number), axis=0).reshape(-1))
                saved_candidate, start = zeros(shape=(len(original_candidate), 3)), None
                for bias in range(4):
                    saved_candidate[samples + bias], start = saved_candidates[location]
                    location += screen * number

            elif self.model_type == "CA":
                for _, _, candidate, reference, start in self.kabsch(original_candidate, original_reference,
                                                                     use_center):
                    cutoffs = {0.5: 0, 1.0: 0, 2.0: 0, 4.0: 0}
                    values = linalg.norm(candidate - reference, ord=2, axis=1)
                    for cutoff, threshold in cutoffs.items():
                        cutoffs[cutoff] = len(where(values < cutoff)[0])
                    saved_candidates.append((candidate, start))
                    scores.append(sum(cutoffs.values()) / (4.0 * len(original_candidate)) * 100.0)

                saved_candidate, start = saved_candidates[argmax(scores)]

            else:
                raise ValueError("No such model type!")

            return max(scores), saved_candidate, original_reference, start

        elif self.distance_type == "GDT-TS":
            if self.model_type == "N-CA-C-O":
                samples = arange(0, len(original_candidate), 4)
                for bias in range(4):
                    c, r = original_candidate[samples + bias], original_reference[samples + bias]
                    for _, _, candidate, reference, start in self.kabsch(c, r, use_center):
                        cutoffs = {1.0: 0, 2.0: 0, 4.0: 0, 8.0: 0}
                        values = linalg.norm(candidate - reference, ord=2, axis=1)
                        for cutoff, threshold in cutoffs.items():
                            cutoffs[cutoff] = len(where(values < cutoff)[0])
                        saved_candidates.append((candidate, start))
                        scores.append(sum(cutoffs.values()) / (4.0 * len(original_candidate)) * 100.0)

                scores = array(scores)
                screen = len(original_reference) - len(original_candidate) + 1
                number = 1 if use_center else len(original_candidate)
                location = argmax(sum(scores.reshape(4, screen, number), axis=0).reshape(-1))
                saved_candidate, start = zeros(shape=(len(original_candidate), 3)), None
                for bias in range(4):
                    saved_candidate[samples + bias], start = saved_candidates[location]
                    location += screen * number

            elif self.model_type == "CA":
                for _, _, candidate, reference in self.kabsch(original_candidate, original_reference, use_center):
                    cutoffs = {1.0: 0, 2.0: 0, 4.0: 0, 8.0: 0}
                    values = linalg.norm(candidate - reference, ord=2, axis=1)
                    for cutoff, threshold in cutoffs.items():
                        cutoffs[cutoff] = len(where(values < cutoff)[0])
                    saved_candidates.append(candidate)
                    scores.append(sum(cutoffs.values()) / (4.0 * len(original_candidate)) * 100.0)

                saved_candidate, start = saved_candidates[argmax(scores)]

            else:
                raise ValueError("No such model type!")

            return max(scores), saved_candidate, original_reference, start

        else:
            raise ValueError("No such distance type!")

    @staticmethod
    def kabsch(candidate_structure: ndarray, reference_structure: ndarray, use_center: bool = True) -> Iterator[tuple]:
        """
        Rotate candidate structure unto reference structure using Kabsch algorithm based on each position.

        :param candidate_structure: candidate structure represented by three-dimension position list.
        :type candidate_structure: numpy.ndarray

        :param reference_structure: reference structure represented by three-dimension position list.
        :type reference_structure: numpy.ndarray

        :param use_center: use center location.
        :type use_center: bool

        :returns current index, total index, final candidate structure and reference structure.
        :rtype int, int, numpy.ndarray, numpy.ndarray

        .. note::
            reference [1]: Yang Zhang and Jeffrey Skolnick (2004) Proteins
            reference [2]: Wolfgang Kabsch (1976) Acta Crystallogr. D.
        """

        def calculate(candidate, reference, addition):
            # unify the center point.
            center = dot(transpose(candidate), reference)

            # decompose the singular value for rotation matrix.
            translation, _, unitary = linalg.svd(center)
            if (linalg.det(translation) * linalg.det(unitary)) < 0.0:
                translation[:, -1] = -translation[:, -1]

            # create rotation matrix and rotate candidate structure.
            rotation = dot(translation, unitary)
            candidate = dot(candidate, rotation)

            # recover the original state of reference structure.
            candidate += addition
            reference += addition

            return candidate, reference

        align_number = len(reference_structure) - len(candidate_structure) + 1
        for align_location in range(align_number):
            c = candidate_structure.copy()
            r = reference_structure[align_location: len(candidate_structure) + align_location]
            if use_center:
                used_c = c - mean(c, axis=0)
                used_r = r - mean(r, axis=0)
                final_c, final_r = calculate(used_c, used_r, mean(r, axis=0))
                yield 0, 1, final_c, final_r, align_location
            else:
                for center_location in range(len(candidate_structure)):
                    used_c = c - c[center_location]
                    used_r = r - r[center_location]
                    final_c, final_r = calculate(used_c, used_r, r[center_location])
                    yield center_location, len(candidate_structure), final_c, final_r, align_location


def cluster(structures):
    structure_cluster = {}
    return structure_cluster

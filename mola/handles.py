from Bio.PDB import PDBParser, MMCIFParser
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
        self.similar_type = similar_type
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
                reverse = True
            else:
                original_candidate, original_reference = structure_1, structure_2
                reverse = False
        else:
            original_candidate, original_reference = structure_1, structure_2
            reverse = False

        scores, saved_candidates = [], []
        if self.similar_type == "RMSD":
            for _, _, candidate, reference, start in self.kabsch(original_candidate, original_reference, use_center):
                # calculate the value of root-mean-square deviation.
                value = linalg.norm((candidate - reference).reshape(-1), ord=2) / len(original_candidate)
                saved_candidates.append((candidate, start))
                scores.append(value)

            saved_candidate, saved_start = saved_candidates[argmin(scores)]

            return min(scores), saved_candidate, original_reference, saved_start, reverse

        elif self.similar_type == "TM":
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

            elif self.model_type == "C3'":  # single atom in nucleic acid structures (e.g. C3').
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

            return max(scores), saved_candidate, original_reference, start, reverse

        elif self.similar_type == "GDT-HA":
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

            return max(scores), saved_candidate, original_reference, start, reverse

        elif self.similar_type == "GDT-TS":
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

            return max(scores), saved_candidate, original_reference, start, reverse

        else:
            raise ValueError("No such distance type!")

    def get_params(self):
        """
        Get the distance type and model type.

        :return: distance type and model type.
        :rtype: str, str
        """
        return self.similar_type, self.model_type

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
        """

        # Yang Zhang and Jeffrey Skolnick (2004) Proteins
        # Wolfgang Kabsch (1976) Acta Crystallogr. D.
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


def similar(structure_1, structure_2, score_method, use_center: bool = True, metrics: float = None) -> tuple:
    """
    Judge whether two structures are similar.

    :param structure_1: molecule structure 1.
    :type structure_1: numpy.ndarray

    :param structure_2: molecule structure 2.
    :type structure_2: numpy.ndarray

    :param score_method: method to calculate the similarity score.
    :type score_method: mola.handles.Score

    :param use_center: use center location.
    :type use_center: bool

    :param metrics: score metrics to determine whether any two structures are similarity.
    :type metrics: float or None

    :return: flag, rotated candidate structure, original reference structure, start location, structure is reversed.
    :rtype: tuple[bool, numpy.ndarray, numpy.ndarray, int, bool]
    """
    score_value, candidate, reference, start_location, reverse = score_method(structure_1, structure_2, use_center)
    distance_type, model_type = score_method.get_params()

    if distance_type == "RMSD":
        if metrics is None:
            raise ValueError("The metrics for RMSD method should be declared!")

        return score_value <= metrics, candidate, reference, start_location, reverse

    elif distance_type == "TM":
        # Based on the extensive statistics of protein and RNA structure families2, 3, it was found that
        # TM-score ≥ 0.5 or TM-scoreRNA ≥ 0.45 corresponds to a protein or RNA pair
        # with similar global structural topology.

        if model_type == "N-CA-C-O":  # protein consists of skeleton comprised of N, C-alpha, C, and O atoms.
            if metrics is None:
                metrics = 0.50 * 4

        elif model_type == "CA":  # protein consists of skeleton comprised of C-alpha.
            if metrics is None:
                metrics = 0.50

        elif model_type == "3SPN":  # 3SPN model (three sites per nucleotide).
            if metrics is None:
                metrics = 0.45 * 3

        elif model_type == "C3'":  # single atom in nucleic acid structures (e.g. C3').
            if metrics is None:
                metrics = 0.45
        else:
            raise ValueError("No such model type!")

        return score_value >= metrics, candidate, reference, start_location, reverse

    elif distance_type == "GDT-HA":
        if model_type == "N-CA-C-O":
            if metrics is None:
                metrics = 90.0 * 4

        elif model_type == "CA":
            if metrics is None:
                metrics = 90.0

        else:
            raise ValueError("No such model type!")

        return score_value >= metrics, candidate, reference, start_location, reverse

    elif distance_type == "GDT-TS":
        # AlphaFold was the top-ranked method, with a median GDT score of 92.4 across all targets.
        # https://alphafold.ebi.ac.uk/faq
        if model_type == "N-CA-C-O":
            if metrics is None:
                metrics = 92.4 * 4

        elif model_type == "CA":
            if metrics is None:
                metrics = 92.4

        else:
            raise ValueError("No such model type!")

        return score_value >= metrics, candidate, reference, start_location, reverse

    else:
        raise ValueError("No such distance type!")


def cluster(structures, score_method, use_center: bool = True, metrics: float = None, merge_type: str = "all") -> list:
    """
    Cluster the molecule structures.

    :param structures: structures (with the same size).
    :type structures: numpy.ndarray

    :param score_method: method to calculate the similarity score.
    :type score_method: mola.handles.Score

    :param use_center: use center location.
    :type use_center: bool

    :param metrics: score metrics to determine whether any two structures are similarity.
    :type metrics: float or None

    :param merge_type: the type to determine one structure can merge into a structure group.
    :type merge_type: str

    :return: structure index cluster flags.
    :rtype: list
    """
    cluster_flags = {}
    for structure_index, candidate in enumerate(structures):
        selected_indices = []
        if merge_type == "all":
            for cluster_index, reference_indices in cluster_flags.items():
                count = 0
                for reference_index in reference_indices:
                    if similar(candidate, structures[reference_index], score_method, use_center, metrics)[0]:
                        count += 1
                if count == len(reference_indices):
                    selected_indices.append(cluster_index)
                    break  # there is no need to merge two clusters, break directly.

        elif merge_type == "any":
            for cluster_index, reference_indices in cluster_flags.items():
                for reference_index in reference_indices:
                    if similar(candidate, structures[reference_index], score_method, use_center, metrics)[0]:
                        selected_indices.append(cluster_index)
                        break

        else:
            raise ValueError("No such merge type!")

        if len(selected_indices) == 0:
            cluster_flags[len(cluster_flags) + 1] = [structure_index]

        elif len(selected_indices) == 1:
            cluster_flags[selected_indices[0]].append(structure_index)

        else:
            for index in selected_indices[1:]:  # merge several clusters before.
                cluster_flags[selected_indices[0]] += cluster_flags[selected_indices[index]]
                del cluster_flags[selected_indices[index]]

            cluster_flags[selected_indices[0]] = [structure_index]

    return list(cluster_flags.values())


def align(structures, score_method, use_center: bool = True, metrics: float = None, merge_type: str = "all") -> dict:
    """
    Align the molecule structures.

    :param structures: structures (with the same size).
    :type structures: numpy.ndarray

    :param score_method: method to calculate the similarity score.
    :type score_method: mola.handles.Score

    :param use_center: use center location.
    :type use_center: bool

    :param metrics: score metrics to determine whether any two structures are similarity.
    :type metrics: float or None

    :param merge_type: the type to determine one structure can merge into a structure group.
    :type merge_type: str

    :return: alignment structure results.
    :rtype: dict
    """
    cluster_flags = cluster(structures, score_method, use_center, metrics, merge_type)
    indices, alignment_results = zeros(shape=(len(structures, )), dtype=int), {}
    for cluster_index, structure_indices in enumerate(cluster_flags):
        indices[structure_indices] = cluster_index
        alignment_results[cluster_index] = []

    alignment_results[indices[0]].append(structures[0])
    for cluster_index, structure in zip(indices[1:], structures[1:]):
        _, candidate, _, _, _ = score_method(structure, structures[0], use_center)
        alignment_results[cluster_index].append(candidate)

    return alignment_results


def load_structure_from_file(file_path: str, entity_type: str = "protein") -> tuple:
    """
    Load structure data from file.

    :param file_path: path to load file.
    :type file_path: str

    :param entity_type: type of entity data, which could be protein, DNA, or RNA.
    :type entity_type: str

    :return: chains and their structures.
    :rtype: dict, dict
    """
    protein_letters = {"ALA": "A", "CYS": "C", "ASP": "D", "GLU": "E", "PHE": "F", "GLY": "G", "HIS": "H", "ILE": "I",
                       "LYS": "K", "LEU": "L", "MET": "M", "ASN": "N", "PRO": "P", "GLN": "Q", "ARG": "R", "SER": "S",
                       "THR": "T", "VAL": "V", "TRP": "W", "TYR": "Y"}

    if file_path[-4:].lower() == ".pdb":
        data = PDBParser(PERMISSIVE=1).get_structure("temp", file_path)
    elif file_path[-4:].lower() == ".cif":
        data = MMCIFParser().get_structure("temp", file_path)
    else:
        raise ValueError("No such load type! Only structure file with \"pdb\" or \"cif\" format can be loaded!")

    chains, structure_data = {}, {}
    if entity_type == "protein":
        rotation = ["N", "CA", "C", "O"]
        for model in data:
            for chain in model:
                sequence, core_positions, skeleton_positions, location = "", [], [], 0
                for residue in chain:
                    for atom in residue:
                        if atom.id == "CA":
                            core_positions.append(atom.coord.tolist())
                        if atom.id == rotation[location]:
                            skeleton_positions.append(atom.coord.tolist())
                            location = (location + 1) % 4
                    sequence += protein_letters[residue.get_resname()]
                chains[chain.id] = sequence
                structure_data[chain.id] = {"CA": array(core_positions), "N-CA-C-O": array(skeleton_positions)}

    elif entity_type in ["DNA", "RNA"]:
        for model in data:
            for chain in model:
                sequence, core_positions, skeleton_positions = "", [], []
                for residue in chain:
                    temp = [[], [], []]
                    for atom in residue:
                        if atom.id == "C3'":
                            core_positions.append(atom.coord.tolist())
                        # TODO need double check
                        if atom.id in ["P", "O5", "O3'"] or (atom.id[:2] == "OP" and atom.id[2] in "1234567890"):
                            temp[2].append(atom.coord.tolist())
                        elif atom.id in ["C5'", "C4'", "C3'", "C2'", "C1'", "O4'", "O2'"]:
                            temp[0].append(atom.coord.tolist())
                        else:
                            temp[1].append(atom.coord.tolist())
                    for value in temp:
                        skeleton_positions.append(mean(array(value), axis=0))
                    sequence += residue.get_resname()[1:]
                chains[chain.id] = sequence
                structure_data[chain.id] = {"C3'": array(core_positions), "3SPN": array(skeleton_positions)}

    else:
        raise ValueError("This structure type is not supported!")

    return chains, structure_data


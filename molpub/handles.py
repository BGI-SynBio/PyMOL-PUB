# noinspection PyPackageRequirements
from Bio.PDB import PDBParser, MMCIFParser, PDBIO, MMCIFIO, Structure, Chain, Residue, Atom
from datetime import datetime
from logging import getLogger, CRITICAL
from numpy import ndarray, array, arange, zeros, dot, transpose, linalg, where
from numpy import argmin, argmax, min, max, mean, sum, sqrt
from scipy.spatial.transform import Rotation
from typing import Iterator
from warnings import filterwarnings
try:
    from pymol2 import PyMOL  # Please refer to https://pymol.org/2/ for download of PyMOL library
except ModuleNotFoundError:
    print("PyMOL is not installed!")

filterwarnings("ignore")
getLogger("matplotlib").setLevel(CRITICAL)


class Monitor:

    def __init__(self):
        """
        Initialize the monitor to identify the task progress.

        Example
            >>> from molpub.handles import Monitor
            >>> monitor = Monitor()
            >>> monitor(current_state=1, total_state=10)
            \r|███                 | 10% ( 1/10) wait 0000:00:00.
            >>> monitor(current_state=5, total_state=10)
            \r|███████████         | 50% ( 5/10) wait 0000:00:00.
            >>> monitor(current_state=10, total_state=10)
            \r|████████████████████|100% (10/10) used 0000:00:00.
        """
        self.last_time = None

    def __call__(self, current_state: int, total_state: int, extra: dict = None):
        """
        Output the current state of process.

        :param current_state: current state of process.
        :type current_state: int

        :param total_state: total state of process.
        :type total_state: int

        :param extra: extra vision information if required.
        :type extra: dict
        """
        if self.last_time is None:
            self.last_time = datetime.now()

        if current_state == 0:
            return

        position = int(current_state / total_state * 100)

        string = "|"

        for index in range(0, 100, 5):
            if position >= index:
                string += "█"
            else:
                string += " "

        string += "|"

        pass_time = (datetime.now() - self.last_time).total_seconds()
        wait_time = int(pass_time * (total_state - current_state) / current_state)

        string += " " * (3 - len(str(position))) + str(position) + "% ("

        string += " " * (len(str(total_state)) - len(str(current_state))) + str(current_state) + "/" + str(total_state)

        if current_state < total_state:
            minute, second = divmod(wait_time, 60)
            hour, minute = divmod(minute, 60)
            string += ") wait " + "%04d:%02d:%02d" % (hour, minute, second)
        else:
            minute, second = divmod(pass_time, 60)
            hour, minute = divmod(minute, 60)
            string += ") used " + "%04d:%02d:%02d" % (hour, minute, second)

        if extra is not None:
            string += " " + str(extra).replace("\'", "").replace("{", "(").replace("}", ")") + "."
        else:
            string += "."

        print("\r" + string, end="", flush=True)

        if current_state >= total_state:
            self.last_time = None
            print()


class Score:

    def __init__(self, similar_type: str = "RMSD", model_type: str = "CA"):
        """
        Initialize the score.

        :param similar_type: method to calculate the similarity between two molecule structures.
        :type similar_type: str

        :param model_type: model used by structures (N-CA-C-O / CA for proteins, 3SPN / C3 for DNA and RNA sequences).
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
        :rtype: float, numpy.ndarray, numpy.ndarray, int
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

                chain_length = len(original_candidate) / 4
                if chain_length > 21:
                    factor = 1.24 * (chain_length - 15) ** (1.0 / 3.0) - 1.8
                else:
                    factor = 0.50

                samples = arange(0, len(original_candidate), 4)
                for bias in range(4):
                    c, r = original_candidate[samples + bias], original_reference[samples + bias]
                    for _, _, candidate, reference, start in self.kabsch(c, r, use_center):
                        value = linalg.norm((candidate - reference), ord=2, axis=1)
                        value = sum(1.0 / (1.0 + (value / factor) ** 2)) / len(original_candidate[samples + bias])
                        saved_candidates.append((candidate, start))
                        scores.append(value)

                screen = len(original_reference) - len(original_candidate) + 1
                number = 1 if use_center else len(original_candidate)
                scores = sum(array(scores).reshape((4, screen, number)), axis=0).reshape(-1)
                location = argmax(scores)
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
                    value = linalg.norm((candidate - reference), ord=2, axis=1)
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

                chain_length = len(original_candidate) / 3
                if chain_length > 30:
                    factor = 0.6 * sqrt(len(original_candidate) - 0.5) - 2.5
                elif 24 <= chain_length <= 30:
                    factor = 0.7
                elif 20 <= chain_length <= 23:
                    factor = 0.6
                elif 16 <= chain_length <= 19:
                    factor = 0.5
                elif 12 <= chain_length <= 15:
                    factor = 0.4
                else:
                    factor = 0.3

                samples = arange(0, len(original_candidate), 3)
                for bias in range(3):
                    c, r = original_candidate[samples + bias], original_reference[samples + bias]
                    for _, _, candidate, reference, start in self.kabsch(c, r, use_center):
                        value = linalg.norm((candidate - reference), ord=2, axis=1)
                        value = sum(1.0 / (1.0 + (value / factor) ** 2)) / len(original_candidate[samples + bias])
                        saved_candidates.append((candidate, start))
                        scores.append(value)

                screen = len(original_reference) - len(original_candidate) + 1
                number = 1 if use_center else len(original_candidate)
                scores = sum(array(scores).reshape((3, screen, number)), axis=0).reshape(-1)
                location = argmax(scores)
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
                    value = linalg.norm((candidate - reference), ord=2, axis=1)
                    value = sum(1.0 / (1.0 + (value / factor) ** 2)) / len(original_candidate)
                    saved_candidates.append((candidate, start))
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
                        scores.append(sum(list(cutoffs.values())) / (4.0 * len(original_candidate) / 4) * 100.0)

                screen = len(original_reference) - len(original_candidate) + 1
                number = 1 if use_center else len(original_candidate)
                scores = sum(array(scores).reshape((4, screen, number)), axis=0).reshape(-1)
                location = argmax(scores)
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
                    scores.append(sum(list(cutoffs.values())) / (4.0 * len(original_candidate)) * 100.0)

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
                        scores.append(sum(list(cutoffs.values())) / (4.0 * len(original_candidate) / 4) * 100.0)

                screen = len(original_reference) - len(original_candidate) + 1
                number = 1 if use_center else len(original_candidate)
                scores = sum(array(scores).reshape((4, screen, number)), axis=0).reshape(-1)
                location = argmax(scores)
                saved_candidate, start = zeros(shape=(len(original_candidate), 3)), None
                for bias in range(4):
                    saved_candidate[samples + bias], start = saved_candidates[location]
                    location += screen * number

            elif self.model_type == "CA":
                for _, _, candidate, reference, start in self.kabsch(original_candidate, original_reference,
                                                                     use_center):
                    cutoffs = {1.0: 0, 2.0: 0, 4.0: 0, 8.0: 0}
                    values = linalg.norm(candidate - reference, ord=2, axis=1)
                    for cutoff, threshold in cutoffs.items():
                        cutoffs[cutoff] = len(where(values < cutoff)[0])
                    saved_candidates.append((candidate, start))
                    scores.append(sum(list(cutoffs.values())) / (4.0 * len(original_candidate)) * 100.0)

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

        :return: current index, total index, final candidate structure and reference structure.
        :rtype: int, int, numpy.ndarray, numpy.ndarray
        """
        # Yang Zhang and Jeffrey Skolnick (2004) Proteins
        # Wolfgang Kabsch (1976) Acta Crystallogr. D.

        if len(candidate_structure) > len(reference_structure):
            raise ValueError("The length of candidate structure needs to be less than or equal to "
                             + "that of reference structure!")

        align_number = len(reference_structure) - len(candidate_structure) + 1
        for align_location in range(align_number):
            c = candidate_structure.copy()
            r = reference_structure[align_location: len(candidate_structure) + align_location]
            if use_center:
                used_c = c - mean(c, axis=0)
                used_r = r - mean(r, axis=0)
                rotation = Rotation.align_vectors(used_c, used_r)[0].as_matrix()
                final_c, final_r = dot(used_c, rotation) + mean(r, axis=0), used_r + mean(r, axis=0)
                yield 0, 1, final_c, final_r, align_location
            else:
                for center_location in range(len(candidate_structure)):
                    used_c = c - c[center_location]
                    used_r = r - r[center_location]
                    rotation = Rotation.align_vectors(used_c, used_r)[0].as_matrix()
                    final_c, final_r = dot(used_c, rotation) + r[center_location], used_r + r[center_location]
                    yield center_location, len(candidate_structure), final_c, final_r, align_location

    @staticmethod
    def get_rotation(candidate_structure, reference_structure):
        """
        Get the rotation matrix.

        :param candidate_structure: candidate structure represented by three-dimension position list.
        :type candidate_structure: numpy.ndarray

        :param reference_structure: reference structure represented by three-dimension position list.
        :type reference_structure: numpy.ndarray

        :return: rotation matrix.
        :rtype: numpy.ndarray
        """
        # unify the center point.
        center = dot(transpose(candidate_structure), reference_structure)

        # decompose the singular value for rotation matrix.
        translation, _, unitary = linalg.svd(center)
        if (linalg.det(translation) * linalg.det(unitary)) < 0.0:
            translation[:, -1] = -translation[:, -1]

        # create rotation matrix and rotate candidate structure.
        return dot(translation, unitary)


def similar(structure_1, structure_2, score_method, use_center: bool = True, metrics: float = None) -> tuple:
    """
    Judge whether two structures are similar.

    :param structure_1: molecule structure 1.
    :type structure_1: numpy.ndarray

    :param structure_2: molecule structure 2.
    :type structure_2: numpy.ndarray

    :param score_method: method to calculate the similarity score.
    :type score_method: molpub.handles.Score

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
        # TM-score ≥ 0.5 or TM-score(RNA) ≥ 0.45 corresponds to a protein or RNA pair
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
    :type score_method: molpub.handles.Score

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

            # noinspection PyUnresolvedReferences
            cluster_flags[selected_indices[0]] = [structure_index]

    return list(cluster_flags.values())


def align(structures, score_method, use_center: bool = True, metrics: float = None, merge_type: str = "all") -> dict:
    """
    Align the molecule structures.

    :param structures: structures (with the same size).
    :type structures: numpy.ndarray

    :param score_method: method to calculate the similarity score.
    :type score_method: molpub.handles.Score

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


def set_properties(structure_paths: list, molecule_type: str, property_type: str = None, targets: list = None,
                   unit_values: dict = None) -> list:
    """
    Set physicochemical properties for structures.

    :param structure_paths: the path to load structure.
    :type structure_paths: list

    :param molecule_type: type of molecule, including DNA, RNA or AA (amino acid).
    :type molecule_type: str

    :param property_type: physicochemical type to emphasize, like polarity, electronegativity, hydrophobicity, etc.
    :type property_type: str or None

    :param targets: selected contents.
    :type targets: list or None

    :param unit_values: values of unit, provided by users or the given property type.
    :type unit_values: dict or None

    :return: property values.
    :rtype: list
    """
    properties = []
    selection_commands = []
    models = []
    for target in targets:
        shading_type, target_information = target.split(":")
        if shading_type == "range":
            selected_model, selected_range = target_information.split("+")
            selection_command = "(m. " + selected_model + " and i. " + selected_range + " and (not hetatm))"
        elif shading_type == "segment":
            selected_model, selected_segment = target_information.split("+")
            selection_command = "(m. " + selected_model + " and ps. " + selected_segment + " and (not hetatm))"
        elif shading_type == "chain":
            selected_model, selected_chain = target_information.split("+")
            selection_command = "(m. " + selected_model + " and c. " + selected_chain + " and (not hetatm))"
        elif shading_type == "model":
            selected_model = target_information
            selection_command = "(m. " + selected_model + " and (not hetatm))"
        else:
            raise ValueError("No such shading type! We only support "
                             + "\"range\", \"segment\", \"chain\" and \"model\".")

        selection_commands.append(selection_command)
        models.append(selected_model)

    mol = PyMOL()
    mol.start()
    for structure_path in structure_paths:
        mol.cmd.load(structure_path, quiet=1)
    mol.cmd.ray(quiet=1)  # make PyMOL run silently.

    if property_type == "PyMOL-align":
        if len(structure_paths) == 2 and len(models) == 2:
            mol.cmd.align(models[0], models[1])

            mol.stored.s1 = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.s1.append([x,y,z])")
            mol.stored.s1 = array(mol.stored.s1)

            mol.stored.s2 = []
            mol.cmd.iterate_state(1, selection_commands[1], "stored.s2.append([x,y,z])")
            mol.stored.s2 = array(mol.stored.s2)

            properties = list(linalg.norm((mol.stored.s1 - mol.stored.s2), axis=1, ord=2))

        else:
            raise ValueError("We only support two structures when \"property_type\" is \"PyMOL-align\".")

    elif property_type == "global-similarity":
        if len(structure_paths) == 2 and len(models) == 2:
            mol.stored.s1 = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.s1.append([x,y,z])")
            mol.stored.s1 = array(mol.stored.s1)

            mol.stored.s2 = []
            mol.cmd.iterate_state(1, selection_commands[1], "stored.s2.append([x,y,z])")
            mol.stored.s2 = array(mol.stored.s2)

            score = Score()
            _, candidate, original_reference, _, _ = score(structure_1=mol.stored.s1, structure_2=mol.stored.s2)
            properties = list(linalg.norm((candidate - original_reference), axis=1, ord=2))

        else:
            raise ValueError("We only support two structures when \"property_type\" is \"global-similarity\".")

    elif property_type == "polarity":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "AA":
                # Geoffrey M. Cooper and Robert E. Hausman (2007) ASM Press, Washington DC.
                # also see https://en.wikipedia.org/wiki/Amino_acid.
                # non-polar = 0 (False) and polar = 1 (True).
                if unit_values is None:
                    unit_values = {"A": 0, "C": 1, "D": 1, "E": 1, "F": 0, "G": 0, "H": 1, "I": 0, "K": 1, "L": 0,
                                   "M": 0, "N": 1, "P": 0, "Q": 1, "R": 1, "S": 1, "T": 1, "V": 0, "W": 0, "Y": 1}
            else:
                raise ValueError("Property type \"polarity\" only support \"AA\".")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"polarity\".")

    elif property_type == "electronegativity":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "AA":
                # net charge at pH = 7.4.
                # Geoffrey M. Cooper and Robert E. Hausman (2007) ASM Press, Washington DC.
                # also see https://en.wikipedia.org/wiki/Amino_acid.
                # negative = -1, neutral = 0, positive = 1; Histidine is 10% positive and 90% neutral, we set as 0.1.
                if unit_values is None:
                    unit_values = {"A": +0, "C": +0, "D": -1, "E": -1, "F": +0, "G": +0, "H": +0.1, "I": +0, "K": +1,
                                   "L": +0, "M": +0, "N": +0, "P": +0, "Q": +0, "R": +1, "S": +0, "T": +0, "V": +0,
                                   "W": +0, "Y": +0}
            elif molecule_type == "DNA":
                # net charge at pH = 7.4.
                # Cameselle J.C. and Ribeiro J.M. (1986) Biochemical Education.
                if unit_values is None:
                    unit_values = {"A": -2, "T": -2, "C": -2, "G": -2}
            elif molecule_type == "RNA":
                # net charge at pH = 7.4.
                # Cameselle J.C. and Ribeiro J.M. (1986) Biochemical Education.
                if unit_values is None:
                    unit_values = {"A": -2, "U": -2, "C": -2, "G": -2}
            else:
                raise ValueError("No such molecule type!")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"electronegativity\".")

    elif property_type == "hydrophobicity":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "AA":
                # Gian Gaetano Tartaglia and Michele Vendruscolo (2010) Journal of molecular biology.
                # The scale of hydrophobicity index is between 0.00 and 1.00 under pH = 7.0.
                if unit_values is None:
                    unit_values = {"A": 0.69, "C": 0.80, "D": 0.17, "E": 0.43, "F": 0.75, "G": 0.55, "H": 0.48,
                                   "I": 0.97, "K": 0.00, "L": 1.00, "M": 0.95, "N": 0.35, "P": 0.88, "Q": 0.47,
                                   "R": 0.34, "S": 0.39, "T": 0.49, "V": 0.95, "W": 0.49, "Y": 0.43}
            elif molecule_type == "DNA":
                # Kevin M. Guckian and Barbara A. Schweitzer (2000) Journal of the American Chemical Society.
                # The hydrophobicity coefficient.
                if unit_values is None:
                    unit_values = {"A": -1.07, "T": -0.36, "C": -0.76, "G": -1.36}
            elif molecule_type == "RNA":
                # Boldina G and Ivashchenko A (2009) Int J Biol Sci.
                # The hydrophobicity coefficient.
                if unit_values is None:
                    unit_values = {"A": -1.07, "U": -0.76, "C": -0.76, "G": -1.36}
            else:
                raise ValueError("No such molecule type!")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"hydrophobicity\".")

    elif property_type == "flexibility":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "AA":
                # Fang Huang and Werner M. Nau (2003) Angewandte Chemie International Edition.
                # Tryptophan, Tyrosine, Cysteine and Methionine are themselves quenchers
                # ,and they could consequently not be included in the study,
                # so their conformational flexibility scales are unknown (represented by -1).
                if unit_values is None:
                    unit_values = {"A": 18, "C": -1, "D": 21, "E": 8.8, "F": 7.6, "G": 39, "H": 4.8, "I": 2.3, "K": 4.0,
                                   "L": 10, "M": -1, "N": 20, "P": 0.1, "Q": 7.2, "R": 4.6, "S": 25, "T": 11, "V": 3.0,
                                   "W": -1, "Y": -1}
            else:
                raise ValueError("Property type \"flexibility\" only support \"AA\".")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"flexibility\".")

    elif property_type == "turn-propensity":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "AA":
                # Gian Gaetano Tartaglia and Michele Vendruscolo (2010) Journal of molecular biology.
                # The scale of turn propensity is between 0.00 and 1.00.
                if unit_values is None:
                    unit_values = {"A": 0.22, "C": 0.70, "D": 0.74, "E": 0.32, "F": 0.20, "G": 0.95, "H": 0.56,
                                   "I": 0.00, "K": 0.60, "L": 0.21, "M": 0.21, "N": 1.00, "P": 0.66, "Q": 0.47,
                                   "R": 0.46, "S": 0.79, "T": 0.34, "V": 0.09, "W": 0.40, "Y": 0.50}
            else:
                raise ValueError("Property type \"turn-propensity\" only support \"AA\".")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"turn-propensity\".")

    elif property_type == "helix-propensity":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "AA":
                # Gian Gaetano Tartaglia and Michele Vendruscolo (2010) Journal of molecular biology.
                # The scale of alpha-helix propensity is between 0.00 and 1.00.
                if unit_values is None:
                    unit_values = {"A": 0.57, "C": 0.62, "D": 0.67, "E": 0.63, "F": 0.56, "G": 0.00, "H": 0.48,
                                   "I": 0.45, "K": 0.87, "L": 0.48, "M": 0.32, "N": 0.32, "P": 0.44, "Q": 0.51,
                                   "R": 1.00, "S": 0.45, "T": 0.30, "V": 0.45, "W": 0.00, "Y": 0.54}
            else:
                raise ValueError("Property type \"helix-propensity\" only support \"AA\".")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"helix-propensity\".")

    elif property_type == "sheet-propensity":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "AA":
                # Gian Gaetano Tartaglia and Michele Vendruscolo (2010) Journal of molecular biology.
                # The scale of beta-sheet propensity is between 0.00 and 1.00.
                if unit_values is None:
                    unit_values = {"A": 0.34, "C": 0.23, "D": 0.35, "E": 0.14, "F": 0.92, "G": 0.13, "H": 0.14,
                                   "I": 0.99, "K": 0.07, "L": 0.87, "M": 0.40, "N": 0.90, "P": 0.00, "Q": 0.72,
                                   "R": 0.22, "S": 0.06, "T": 0.14, "V": 0.78, "W": 0.62, "Y": 1.00}
            else:
                raise ValueError("Property type \"sheet-propensity\" only support \"AA\".")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"sheet-propensity\".")

    elif property_type == "folding-propensity":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "AA":
                # Gian Gaetano Tartaglia and Michele Vendruscolo (2010) Journal of molecular biology.
                # The scale of folding propensity is between 0.00 and 1.00.
                if unit_values is None:
                    unit_values = {"A": 0.34, "C": 0.97, "D": 0.61, "E": 0.73, "F": 0.31, "G": 0.58, "H": 0.47,
                                   "I": 0.55, "K": 0.50, "L": 0.65, "M": 0.55, "N": 0.48, "P": 1.00, "Q": 0.35,
                                   "R": 0.63, "S": 0.73, "T": 0.44, "V": 0.55, "W": 0.00, "Y": 0.21}
            else:
                raise ValueError("Property type \"folding-propensity\" only support \"AA\".")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"folding-propensity\".")

    elif property_type == "ionizationpotentials":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "DNA":
                # Stacey D. Wetmore and Russell J. Boyd. (2000) Chemical Physics Letters.
                # The ionization potentials of the nucleotide bases.(eV)
                if unit_values is None:
                    unit_values = {"A": 8.09, "T": 8.74, "C": 8.57, "G": 7.64}
            elif molecule_type == "RNA":
                # Stacey D. Wetmore and Russell J. Boyd. (2000) Chemical Physics Letters.
                # The ionization potentials of the nucleotide bases.(eV)
                if unit_values is None:
                    unit_values = {"A": 8.09, "U": 9.21, "C": 8.57, "G": 7.64}
            else:
                raise ValueError("Property type \"ionizationpotentials\" only support \"DNA\" or \"RNA\".")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"ionizationpotentials\".")

    elif property_type == "electronaffinities":
        if len(structure_paths) == 1 and len(models) == 1:
            if molecule_type == "DNA":
                # Stacey D. Wetmore and Russell J. Boyd. (2000) Chemical Physics Letters.
                # The electron affinities of the nucleotide bases.(eV)
                if unit_values is None:
                    unit_values = {"A": -0.40, "T": 0.14, "C": -0.06, "G": -0.27}
            elif molecule_type == "RNA":
                # Stacey D. Wetmore and Russell J. Boyd. (2000) Chemical Physics Letters.
                # The electron affinities of the nucleotide bases.(eV)
                if unit_values is None:
                    unit_values = {"A": -0.40, "U": 0.18, "C": -0.06, "G": -0.27}
            else:
                raise ValueError("Property type \"electronaffinities\" only support \"DNA\" or \"RNA\".")

            mol.stored.residue = []
            mol.cmd.iterate_state(1, selection_commands[0], "stored.residue.append(oneletter)")
            for i in range(len(mol.stored.residue)):
                properties.append(unit_values[mol.stored.residue[i]])

        else:
            raise ValueError("We only support one structure when \"property_type\" is \"electronaffinities\".")
    else:
        raise ValueError("No such property type!")

    mol.stop()

    return properties


def set_difference(alignment_data: ndarray, model_type: str, calculation_type: str = "average") -> ndarray:
    """
    Set difference information for a known chain.

    :param alignment_data: alignment structure data, format of which could be (chain number, chain length, 3).
    :type alignment_data: numpy.ndarray

    :param model_type: model used by structures (N-CA-C-O / CA for proteins, 3SPN / C3' for DNA and RNA sequences).
    :type model_type: str

    :param calculation_type: difference calculation, including average and maximum.
    :type calculation_type: str

    :return: difference values.
    :rtype: numpy.ndarray

    .. note::
        If chain number is 2, the parameter 'calculation_type' is invalid.
        We provide the root mean squared error of each unit.
        Otherwise, we provide the average and maximum value of the root mean squared error of each unit.
    """
    assert len(alignment_data.shape) == 3 and alignment_data.shape[2] == 3

    if model_type == "N-CA-C-O":
        merge_number = 4

    elif model_type == "3SPN":
        merge_number = 3

    elif model_type in ["CA", "C3'"]:
        merge_number = 1

    else:
        raise ValueError("No such model type!")

    differences = []
    if merge_number == 1:
        for index_1 in range(alignment_data.shape[0] - 1):
            for index_2 in range(index_1 + 1, alignment_data.shape[0]):
                case_1, case_2 = alignment_data[index_1], alignment_data[index_2]
                normalized_values = linalg.norm((case_1 - case_2), ord=2, axis=1)
                differences.append(normalized_values)

    else:
        for index_1 in range(alignment_data.shape[0] - 1):
            for index_2 in range(index_1 + 1, alignment_data.shape[0]):
                case_1, case_2 = alignment_data[index_1], alignment_data[index_2]
                normalized_values = linalg.norm((case_1 - case_2), ord=2, axis=1)
                normalized_values = normalized_values.reshape(len(normalized_values) // merge_number, merge_number)
                normalized_values = linalg.norm(normalized_values, ord=2, axis=1)
                differences.append(normalized_values)

    differences = array(differences)

    if calculation_type == "average":
        differences = mean(differences, axis=0)

    elif calculation_type == "maximum":
        differences = sum(differences, axis=0)

    else:
        raise ValueError("No such calculate type!")

    return differences


def kmer(chain: str, structure: ndarray, sub_length: int) -> Iterator[tuple]:
    """
    Disassemble the entire chain into sub-segments of the given length.

    :param chain: molecule chain.
    :type chain: str

    :param structure: molecule structure.
    :type structure: numpy.ndarray

    :param sub_length: length of sub-segment.
    :type sub_length: int

    :return: sub chain and the corresponding sub structure.
    :rtype: str, numpy.ndarray
    """
    number = len(structure) // len(chain)
    for index in range(len(chain) - sub_length + 1):
        yield chain[index: index + sub_length], structure[index * number: (index + sub_length) * number]


def load_structure_from_file(file_path: str, molecule_type: str = "AA") -> tuple:
    """
    Load structure data from file.

    :param file_path: path to load file.
    :type file_path: str

    :param molecule_type: type of molecule data, which could be DNA, RNA or AA (amino acid).
    :type molecule_type: str

    :return: chains and their corresponding structures.
    :rtype: dict, dict
    """
    letters = {"ALA": "A", "CYS": "C", "ASP": "D", "GLU": "E", "PHE": "F", "GLY": "G", "HIS": "H", "ILE": "I",
               "LYS": "K", "LEU": "L", "MET": "M", "ASN": "N", "PRO": "P", "GLN": "Q", "ARG": "R", "SER": "S",
               "THR": "T", "VAL": "V", "TRP": "W", "TYR": "Y"}

    if file_path[-4:].lower() == ".pdb":
        data = PDBParser(PERMISSIVE=1).get_structure("temp", file_path)
    elif file_path[-4:].lower() == ".cif":
        data = MMCIFParser().get_structure("temp", file_path)
    else:
        raise ValueError("No such load type! Only structure file with \"pdb\" or \"cif\" format can be loaded!")

    chains, structure_data = {}, {}
    if molecule_type == "AA":
        rotation = ["N", "CA", "C", "O"]
        for model in data:
            for chain in model:
                sequence, core_positions, skeleton_positions, location = "", [], [], 0
                for residue in chain:
                    if residue.get_resname() == 'HOH':
                        continue
                    for atom in residue:
                        if atom.id == "CA":
                            core_positions.append(atom.coord.tolist())
                        if atom.id == rotation[location]:
                            skeleton_positions.append(atom.coord.tolist())
                            location = (location + 1) % 4
                    sequence += letters[residue.get_resname()]
                chains[chain.id] = sequence
                structure_data[chain.id] = {"CA": array(core_positions), "N-CA-C-O": array(skeleton_positions)}

    elif molecule_type in ["DNA", "RNA"]:
        for model in data:
            for chain in model:
                sequence, core_positions, skeleton_positions = "", [], []
                for residue in chain:
                    temp = [[], [], []]
                    for atom in residue:
                        if atom.id == "C3'":
                            core_positions.append(atom.coord.tolist())
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


def save_structure_to_file(chains: list, structures: ndarray, file_path: str, model_type: str = "CA"):
    """
    Save temporary structure to file.

    :param chains: chains.
    :type chains: list

    :param structures: corresponding structures of chains.
    :type structures: numpy.ndarray

    :param file_path: path to save temp file.
    :type file_path: str

    :param model_type: model used by structures (N-CA-C-O / CA for proteins, 3SPN / C3 for DNA and RNA sequences).
    :type model_type: str
    """
    if model_type == "N-CA-C-O":
        form = ["N", "CA", "C", "O"]
        letters = {"A": "ALA", "C": "CYS", "D": "ASP", "E": "GLU", "F": "PHE", "G": "GLY", "H": "HIS", "I": "ILE",
                   "K": "LYS", "L": "LEU", "M": "MET", "N": "ASN", "P": "PRO", "Q": "GLN", "R": "ARG", "S": "SER",
                   "T": "THR", "V": "VAL", "W": "TRP", "Y": "TYR"}
    elif model_type == "CA":
        form = ["CA"]
        letters = {"A": "ALA", "C": "CYS", "D": "ASP", "E": "GLU", "F": "PHE", "G": "GLY", "H": "HIS", "I": "ILE",
                   "K": "LYS", "L": "LEU", "M": "MET", "N": "ASN", "P": "PRO", "Q": "GLN", "R": "ARG", "S": "SER",
                   "T": "THR", "V": "VAL", "W": "TRP", "Y": "TYR"}
    elif model_type == "3SPN":
        form = ["DS", "DB", "DP"]
        letters = {"A": "DA", "C": "DC", "G": "DG", "T": "DT", "U": "DU"}
    elif model_type == "C3'":
        form = ["C3'"]
        letters = {"A": "DA", "C": "DC", "G": "DG", "T": "DT", "U": "DU"}
    else:
        raise ValueError("No such model type!")

    residue_number, atom_number, structure_data = 1, 1, Structure.Structure(id="temp")
    for chain_index, (chain, structure) in enumerate(zip(chains, structures)):
        structure = structure.reshape(len(structure) // len(form), len(form), 3)
        chain_data = Chain.Chain(id=chr(chain_index + 65))
        for residue_index, (entity, coordinates) in enumerate(zip(chain, structure)):
            residue = Residue.Residue(id=(" ", residue_number, " "), resname=letters[entity], segid="    ")
            for coordinate in coordinates:
                atom = Atom.Atom(name=form[0], serial_number=atom_number,
                                 fullname=" " + form[residue_index % len(form)].ljust(3), altloc=" ",
                                 bfactor=0.0, coord=coordinate, occupancy=1.0)
                residue.add(atom=atom)
                atom_number += 1

            chain_data.add(residue)
            residue_number += 1

        structure_data.add(chain_data)

    if file_path[-4:].lower() == ".pdb":
        io = PDBIO()
    elif file_path[-4:].lower() == ".cif":
        io = MMCIFIO()
    else:
        raise ValueError("No such file type!")

    io.set_structure(structure_data)
    io.save(file_path)

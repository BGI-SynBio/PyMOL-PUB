parent_path = "../mola/supp/widgets/"


def optimize_format(image_path: str):
    """
    Optimize SVG format.

    :param image_path: SVG image path.
    :type image_path: str
    """
    sentences, complete_sentence = [], ""
    with open(file=image_path, mode="r", encoding="utf8") as file:
        for index, line in enumerate(file.readlines()):
            if index not in [1, 2, 3]:
                sentence = line.lstrip(" ").rstrip(" ")
                if ">" not in sentence:
                    complete_sentence += sentence[:-1]
                else:
                    if "</" not in sentence:
                        complete_sentence += sentence
                        sentences.append(complete_sentence)
                    else:
                        if len(complete_sentence) > 0:
                            sentences.append(complete_sentence + "\n")
                        sentences.append(sentence)
                    complete_sentence = ""

    optimized_sequences, space, move = [sentences[0]], "    ", 0
    for index, sentence in enumerate(sentences[1:]):
        if sentence[:2] == "</":
            move -= 1

        optimized_sequences.append(space * move + sentence)

        if sentence[0] == "<" and sentence[-2] == ">" and sentence[:2] != "</" and sentence[-3: -1] != "/>":
            move += 1

    with open(file=image_path, mode="w", encoding="utf8") as file:
        for sentence in optimized_sequences:
            file.write(sentence)

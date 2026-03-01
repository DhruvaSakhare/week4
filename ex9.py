import heapq


def sliding_weighted_score(numbers, B=1.5, E=0.5):
    """
    B = beginning weight
    E = ending weight
    """
    total = 0
    N = len(numbers)

    for i, value in enumerate(numbers):
        P = i + 1  # position (1-based index)

        if N == 1:
            weight = 1.0  # avoid division by zero
        else:
            weight = B - (B - E) * (P - 1) / (N - 1)

        total += value * weight

    return total

def combined_score(numbers):
    return sum(numbers)

def load_translation(filename):
    mapping = {}

    with open(filename) as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                accession = parts[0]
                swissprot = parts[1]
                mapping[swissprot] = accession

    return mapping


def load_banned_accessions(negative_file, translation_map):
    banned_accessions = set()

    with open(negative_file) as f:
        for line in f:
            swissprot_id = line.strip()

            if swissprot_id in translation_map:
                banned_accessions.add(translation_map[swissprot_id])

    return banned_accessions


def main():
    translation_map = load_translation("translation.txt")
    banned_accessions = load_banned_accessions(
        "negative_list.txt",
        translation_map
    )

    heap = []

    with open("scores.txt") as f:
        for line in f:
            parts = line.strip().split("\t")

            accession = parts[0]

            # Skip banned genes
            if accession in banned_accessions:
                continue

            scores = [float(x) for x in parts[1:]]
            score = combined_score(scores)

            if len(heap) < 10:
                heapq.heappush(heap, (score, line.strip()))
            else:
                heapq.heappushpop(heap, (score, line.strip()))

    # Sort final 10 high → low
    top10 = sorted(heap, reverse=True)

    with open("scoresextreme.txt", "w") as out:
        for _, line in top10:
            out.write(line + "\n")


if __name__ == "__main__":
    main()
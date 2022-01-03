import random
from concurrent.futures import ThreadPoolExecutor, as_completed

DNA_SAMPLE_LENGTH = 133700
SAMPLE_COUNT = 500
MAX_WORKERS = 30


def find_substr(dna_samples, sequence, index):
    if dna_samples[index].find(sequence) != -1:
        return f"[Sample {index}] DNA sequence found!"

    return ""


def main():
    dna_samples = ["".join([random.choice("ATGC") for _ in range(DNA_SAMPLE_LENGTH)])
                   for _ in range(SAMPLE_COUNT)]

    sequence = "GTTCCAAACCCGG"

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = [executor.submit(find_substr, dna_samples, sequence, i)
                   for i in range(SAMPLE_COUNT)]

        for res in as_completed(results):
            result_str = res.result()

            if result_str != "":
                print(result_str)


if __name__ == "__main__":
    main()

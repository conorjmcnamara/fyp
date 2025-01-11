import json
from typing import List
from models.paper import Paper


def save_papers_to_json(file_path: str, papers: List[Paper]) -> None:
    with open(file_path, 'w', encoding="utf-8") as file:
        file.writelines(
            json.dumps(paper.__dict__) + '\n'
            for paper in papers
        )


def combine_json_files(input_file_paths: List[str], output_file_path: str) -> None:
    with open(output_file_path, 'w', encoding="utf-8") as outfile:
        outfile.write('[\n')
        is_first_entry = True

        for input_file_path in input_file_paths:
            with open(input_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('[') or line.endswith(']'):
                        continue

                    if is_first_entry:
                        is_first_entry = False
                    else:
                        outfile.write(",\n")
                    outfile.write(line.strip(','))

        outfile.write(']')


def print_first_n_lines(file_path: str, n: int) -> None:
    with open(file_path, 'r', encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i >= n:
                break
            print(line)

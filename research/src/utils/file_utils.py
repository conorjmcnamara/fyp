import json
from typing import List
from src.data_models.paper import Paper


def combine_json_files(input_file_paths: List[str], output_file_path: str) -> None:
    with open(output_file_path, 'w', encoding="utf-8") as outfile:
        outfile.write("[\n")
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

        outfile.write("\n]")


def save_papers_to_json(file_path: str, papers: List[Paper]) -> None:
    with open(file_path, 'w', encoding="utf-8") as file:
        lines = ["[\n"]
        lines.extend(f"{json.dumps(paper.__dict__)},\n" for paper in papers[:-1])
        lines.append(json.dumps(papers[-1].__dict__))
        lines.append("\n]")
        file.writelines(lines)


def read_parsed_papers_from_json(file_path: str) -> List[Paper]:
    papers = []

    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip().strip(',')
            if not line or line.startswith('[') or line.endswith(']'):
                continue

            try:
                papers.append(Paper(**json.loads(line)))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line} -> {e}")

    return papers

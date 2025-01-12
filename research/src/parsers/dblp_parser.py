import json
from typing import Dict, Callable, Any
from src.data_models.paper import Paper
from src.parsers.dblp_txt_field import DblpTxtField
from src.utils.file_utils import save_papers_to_json
from src.config.settings import (
    MIN_CITATION_COUNT_FILTER,
    MIN_REFERENCE_COUNT_FILTER,
    MIN_YEAR_FILTER
)


class DblpParser():
    def _read_txt(self, file_path: str) -> Dict[str, Paper]:
        paper_map = {}
        paper = Paper()

        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line.startswith(DblpTxtField.ID.value):
                    paper.id = line.lstrip(DblpTxtField.ID.value)

                elif line.startswith(DblpTxtField.TITLE.value):
                    if paper.is_populated():
                        paper_map[paper.id] = paper

                    paper = Paper()
                    paper.title = line.lstrip(DblpTxtField.TITLE.value)

                elif line.startswith(DblpTxtField.AUTHORS.value):
                    paper.authors = line.lstrip(DblpTxtField.AUTHORS.value).split(", ")

                elif line.startswith(DblpTxtField.YEAR.value):
                    year = int(line.lstrip(DblpTxtField.YEAR.value))
                    if year > MIN_YEAR_FILTER:
                        paper.year = year

                elif line.startswith(DblpTxtField.ABSTRACT.value):
                    paper.abstract = line.lstrip(DblpTxtField.ABSTRACT.value)

                elif line.startswith(DblpTxtField.VENUE.value):
                    paper.venue = line.lstrip(DblpTxtField.VENUE.value)

                elif line.startswith(DblpTxtField.REFERENCE.value):
                    ref_id = line.lstrip(DblpTxtField.REFERENCE.value)
                    paper.references.append(ref_id)

        if paper.is_populated():
            paper_map[paper.id] = paper

        return paper_map

    def _read_json(
        self,
        file_path: str,
        parse_func: Callable[[Dict[str, Any]], Paper]
    ) -> Dict[str, Paper]:
        paper_map = {}

        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip().strip(',')
                if not line or line.startswith('[') or line.endswith(']'):
                    continue

                try:
                    paper = parse_func(json.loads(line))
                    if paper.is_populated():
                        paper_map[paper.id] = paper

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {line.strip()} -> {e}")

        return paper_map

    def _parse_v10_paper(self, paper_dict: Dict[str, Any]) -> Paper:
        paper = Paper()
        paper.id = paper_dict.get("id")
        paper.title = paper_dict.get("title")
        paper.authors = paper_dict.get("authors")

        year = paper_dict.get("year")
        if year and year > MIN_YEAR_FILTER:
            paper.year = year

        paper.abstract = paper_dict.get("abstract")
        paper.venue = paper_dict.get("venue")
        paper.references = paper_dict.get("references")
        return paper

    def _parse_v12_paper(self, paper_dict: Dict[str, Any]) -> Paper:
        paper = Paper()
        paper.id = paper_dict.get("id")
        paper.title = paper_dict.get("title")

        for author in paper_dict.get("authors", []):
            name = author.get("name")
            if name:
                paper.authors.append(name)

        year = paper_dict.get("year")
        if year and year > MIN_YEAR_FILTER:
            paper.year = year

        indexed_abstract = paper_dict.get("indexed_abstract", {})
        abstract = [""] * indexed_abstract.get("IndexLength", 0)
        for token, positions in indexed_abstract.get("InvertedIndex", {}).items():
            for position in positions:
                abstract[position] = token
        paper.abstract = " ".join(abstract)

        paper.venue = paper_dict.get("venue", {}).get("raw")
        paper.references = paper_dict.get("references")
        return paper

    def _remove_missing_references(self, paper_map: Dict[str, Paper]) -> None:
        keys = set(paper_map.keys())
        for paper in paper_map.values():
            paper.references = [ref_id for ref_id in paper.references if ref_id in keys]

    def _compute_citation_counts(self, paper_map: Dict[str, Paper]) -> None:
        for paper in paper_map.values():
            paper.citation_count = 0

        for paper in paper_map.values():
            for ref_id in paper.references:
                if ref_id in paper_map:
                    paper_map[ref_id].citation_count += 1

    def _filter_papers(self, paper_map: Dict[str, Paper]) -> Dict[str, Paper]:
        # Remove references to papers with missing metadata
        self._remove_missing_references(paper_map)
        self._compute_citation_counts(paper_map)

        paper_map = {
            k: v for k, v in paper_map.items()
            if (
                v.citation_count >= MIN_CITATION_COUNT_FILTER and
                len(v.references) >= MIN_REFERENCE_COUNT_FILTER
            )
        }

        # Remove references to filtered papers
        self._remove_missing_references(paper_map)
        self._compute_citation_counts(paper_map)

        return paper_map

    def parse_and_transform(self, input_file_path: str, output_json_path: str) -> None:
        if input_file_path.endswith(".txt"):
            paper_map = self._read_txt(input_file_path)
        elif "v10" in input_file_path:
            paper_map = self._read_json(input_file_path, self._parse_v10_paper)
        elif "v12" in input_file_path:
            paper_map = self._read_json(input_file_path, self._parse_v12_paper)
        else:
            raise ValueError(f"Unsupported input file type: {input_file_path}")

        paper_map = self._filter_papers(paper_map)
        print(f"Saving {len(paper_map)} papers")
        save_papers_to_json(output_json_path, list(paper_map.values()))

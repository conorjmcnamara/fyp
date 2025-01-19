import json
from typing import Dict, Callable, Any
from src.data_models.paper import Paper
from src.parsers.dblp_txt_field import DblpTxtField
from src.utils.file_utils import save_papers
from src.utils.preprocess_utils import remove_missing_references, compute_citation_counts
from src.config.settings import (
    MIN_CITATION_COUNT_FILTER,
    MIN_REFERENCE_COUNT_FILTER,
    MIN_YEAR_FILTER
)


class DblpParser():
    def parse_and_transform(self, input_path: str, output_json_path: str) -> None:
        if input_path.endswith(".txt"):
            papers = self._read_txt(input_path)
        elif input_path.endswith(".json"):
            if "v10" in input_path:
                papers = self._read_json(input_path, self._parse_v10_paper)
            elif "v12" in input_path:
                papers = self._read_json(input_path, self._parse_v12_paper)
            else:
                raise ValueError(
                    f"Unsuported .json file format: {input_path}. Expected 'v10' or 'v12'."
                )
        else:
            raise ValueError(f"Unsupported input file type: {input_path}. Expected .txt or .json.")

        papers = self._filter_papers(papers)
        print(f"Saving {len(papers)} papers")
        save_papers(output_json_path, list(papers.values()))

    def _read_txt(self, txt_path: str) -> Dict[str, Paper]:
        papers = {}
        paper = Paper()

        with open(txt_path, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line.startswith(DblpTxtField.ID.value):
                    paper.id = line[len(DblpTxtField.ID.value):]

                elif line.startswith(DblpTxtField.TITLE.value):
                    if paper.is_populated():
                        papers[paper.id] = paper

                    paper = Paper()
                    paper.title = line[len(DblpTxtField.TITLE.value):]

                elif line.startswith(DblpTxtField.AUTHORS.value):
                    paper.authors = line[len(DblpTxtField.AUTHORS.value):].split(", ")

                elif line.startswith(DblpTxtField.YEAR.value):
                    year = int(line[len(DblpTxtField.YEAR.value):])
                    if year > MIN_YEAR_FILTER:
                        paper.year = year

                elif line.startswith(DblpTxtField.ABSTRACT.value):
                    paper.abstract = line[len(DblpTxtField.ABSTRACT.value):]

                elif line.startswith(DblpTxtField.VENUE.value):
                    paper.venue = line[len(DblpTxtField.VENUE.value):]

                elif line.startswith(DblpTxtField.REFERENCE.value):
                    ref_id = line[len(DblpTxtField.REFERENCE.value):]
                    paper.references.append(ref_id)

        if paper.is_populated():
            papers[paper.id] = paper

        return papers

    def _read_json(
        self,
        json_path: str,
        parse_func: Callable[[Dict[str, Any]], Paper]
    ) -> Dict[str, Paper]:
        papers = {}

        with open(json_path, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip().strip(',')
                if not line or line.startswith('[') or line.endswith(']'):
                    continue

                try:
                    paper = parse_func(json.loads(line))
                    if paper.is_populated():
                        papers[paper.id] = paper

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {line} -> {e}")

        return papers

    def _parse_v10_paper(self, paper_data: Dict[str, Any]) -> Paper:
        paper = Paper()
        paper.id = paper_data.get("id")
        paper.title = paper_data.get("title")
        paper.authors = paper_data.get("authors")

        year = paper_data.get("year")
        if year and year > MIN_YEAR_FILTER:
            paper.year = year

        paper.abstract = paper_data.get("abstract")
        paper.venue = paper_data.get("venue")
        paper.references = paper_data.get("references")
        return paper

    def _parse_v12_paper(self, paper_data: Dict[str, Any]) -> Paper:
        paper = Paper()
        paper.id = paper_data.get("id")
        paper.title = paper_data.get("title")

        for author in paper_data.get("authors", []):
            name = author.get("name")
            if name:
                paper.authors.append(name)

        year = paper_data.get("year")
        if year and year > MIN_YEAR_FILTER:
            paper.year = year

        indexed_abstract = paper_data.get("indexed_abstract", {})
        abstract = [""] * indexed_abstract.get("IndexLength", 0)
        for token, positions in indexed_abstract.get("InvertedIndex", {}).items():
            for position in positions:
                abstract[position] = token
        paper.abstract = " ".join(abstract)

        paper.venue = paper_data.get("venue", {}).get("raw")
        paper.references = paper_data.get("references")
        return paper

    def _filter_papers(self, papers: Dict[str, Paper]) -> Dict[str, Paper]:
        # Remove references to papers with missing metadata
        remove_missing_references(list(papers.values()))
        compute_citation_counts(list(papers.values()))

        papers = {
            id: paper for id, paper in papers.items()
            if (
                paper.citation_count >= MIN_CITATION_COUNT_FILTER and
                len(paper.references) >= MIN_REFERENCE_COUNT_FILTER
            )
        }

        # Remove references to filtered papers
        remove_missing_references(list(papers.values()))
        compute_citation_counts(list(papers.values()))

        return papers

from typing import Dict, Any
from src.parsers.dataset_parser import DatasetParser
from src.data_models.paper import Paper
from src.parsers.dblp_txt_field import DblpTxtField
from src.utils.file_utils import save_papers
from src.config.settings import DBLP_V10_CONFIG


class DblpParser(DatasetParser):
    def __init__(self):
        super().__init__(DBLP_V10_CONFIG)

    def parse_and_transform(self, input_path: str, output_json_path: str) -> None:
        if input_path.endswith(".txt"):
            papers = self._read_txt(input_path)
        elif input_path.endswith(".json"):
            if "v10" in input_path:
                papers = self.read_json(input_path, self._parse_v10_paper)
            elif "v12" in input_path:
                papers = self.read_json(input_path, self._parse_v12_paper)
            else:
                raise ValueError(
                    f"Unsuported JSON file format: {input_path}. Expected 'v10' or 'v12'."
                )
        else:
            raise ValueError(f"Unsupported input file type: {input_path}. Expected .txt or .json.")

        papers = self.filter_papers(papers)
        print(f"Saving {len(papers)} papers")
        save_papers(output_json_path, list(papers.values()))

    def is_paper_populated(self, paper: Paper) -> bool:
        return (
            bool(
                paper.id and
                paper.title and
                paper.authors and
                paper.year != 0 and
                paper.abstract and
                paper.venue and
                paper.references
            )
        )

    def _read_txt(self, txt_path: str) -> Dict[str, Paper]:
        papers = {}
        paper = Paper()

        with open(txt_path, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line.startswith(DblpTxtField.ID.value):
                    paper.id = line[len(DblpTxtField.ID.value):]

                elif line.startswith(DblpTxtField.TITLE.value):
                    if self.is_paper_populated(paper):
                        papers[paper.id] = paper

                    paper = Paper()
                    paper.title = line[len(DblpTxtField.TITLE.value):]

                elif line.startswith(DblpTxtField.YEAR.value):
                    year = int(line[len(DblpTxtField.YEAR.value):])
                    if year >= self.config.train_years[0]:
                        paper.year = year
                
                elif line.startswith(DblpTxtField.AUTHORS.value):
                    paper.authors = line[len(DblpTxtField.AUTHORS.value):].split(", ")

                elif line.startswith(DblpTxtField.ABSTRACT.value):
                    paper.abstract = line[len(DblpTxtField.ABSTRACT.value):]

                elif line.startswith(DblpTxtField.VENUE.value):
                    paper.venue = line[len(DblpTxtField.VENUE.value):]

                elif line.startswith(DblpTxtField.REFERENCE.value):
                    ref_id = line[len(DblpTxtField.REFERENCE.value):]
                    paper.references.append(ref_id)

        if self.is_paper_populated(paper):
            papers[paper.id] = paper

        return papers

    def _parse_v10_paper(self, paper_data: Dict[str, Any]) -> Paper:
        paper = Paper()
        paper.id = paper_data.get("id")
        paper.title = paper_data.get("title")

        year = paper_data.get("year")
        if year and year >= self.config.train_years[0]:
            paper.year = year

        paper.authors = paper_data.get("authors")
        paper.abstract = paper_data.get("abstract")
        paper.venue = paper_data.get("venue")
        paper.references = paper_data.get("references")
        return paper

    def _parse_v12_paper(self, paper_data: Dict[str, Any]) -> Paper:
        paper = Paper()
        paper.id = paper_data.get("id")
        paper.title = paper_data.get("title")

        year = paper_data.get("year")
        if year and year >= self.config.train_years[0]:
            paper.year = year
        
        for author in paper_data.get("authors", []):
            name = author.get("name")
            if name:
                paper.authors.append(name)

        indexed_abstract = paper_data.get("indexed_abstract", {})
        abstract = [""] * indexed_abstract.get("IndexLength", 0)
        for token, positions in indexed_abstract.get("InvertedIndex", {}).items():
            for position in positions:
                abstract[position] = token
        paper.abstract = " ".join(abstract)

        paper.venue = paper_data.get("venue", {}).get("raw")
        paper.references = paper_data.get("references")
        return paper

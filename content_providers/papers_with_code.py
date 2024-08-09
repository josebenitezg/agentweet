# Thanks https://github.com/FrancescoSaverioZuppichini/LinkedInGPT/blob/main/gurus/linkedin_ai.py
from random import choice
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

import logging

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Content:
    uid: str
    data: Dict[str, Any]
    created: Optional[bool] = False


@dataclass
class GeneratedContent:
    text: str
    media_url: Optional[str] = None


def get_paper_info_from_papers_with_code(uid: str, *args, **kwargs) -> Dict:
    """
    Fetching the paper little summary page on papers with code, e.g.
    https://paperswithcode.com/paper/track-anything-segment-anything-meets-videos

    This function returns a dictionary with `abtract` and `arxiv_link`.
    """
    response = requests.get(f"https://paperswithcode.com{uid}")
    result = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        paper_abstract_div = soup.select_one(".paper-abstract")
        # Extract the abstract
        abstract = paper_abstract_div.find("p").text.strip()
        # Extract the arXiv URL
        arxiv_url = paper_abstract_div.find("a", class_="badge badge-light")["href"]

        result = {"abstract": abstract, "arxiv_link": arxiv_url}

    else:
        logging.warning(
            f"Failed to fetch https://paperswithcode.com{uid}. Status code: {response.status_code}"
        )

    return result


def get_latest_papers_from_papers_with_code(*args, **kwargs) -> List[Content]:
    logging.info("Getting papers from https://paperswithcode.com/")
    response = requests.get("https://paperswithcode.com/")
    results: List[Content] = []
    if response.status_code == 200:
        logging.info("Successfully fetched the webpage")
        soup = BeautifulSoup(response.content, "html.parser")
        for row in soup.select(
            ".infinite-container .row.infinite-item.item.paper-card"
        ):
            paper_dict = {
                "title": row.select_one("h1 a").get_text(strip=True),
                "subtitle": row.select_one(".item-strip-abstract").get_text(strip=True),
                "media": row.select_one(".item-image")["style"]
                .split("('")[1]
                .split("')")[0],
                "tags": [
                    a.get_text(strip=True) for a in row.select(".badge-primary a")
                ],
                "stars": int(
                    row.select_one(".entity-stars .badge")
                    .get_text(strip=True)
                    .split(" ")[0]
                    .replace(",", "")
                ),
                "github_link": row.select_one(".item-github-link a")["href"],
                "uid": row.select_one("h1 a")["href"],
            }
            paper_dict = paper_dict
            print(paper_dict["title"])
            results.append(
                Content(
                    paper_dict["uid"],
                    data={
                        **paper_dict,
                        **get_paper_info_from_papers_with_code(paper_dict["uid"]),
                    },
                )
            )
        else:
            logging.warning("Was not able to scrape the html for one row.")
    else:
        logging.warning(
            f"Failed to fetch the webpage. Status code: {response.status_code}."
        )

    return results

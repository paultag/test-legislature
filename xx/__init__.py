# from pupa.models.jurisdiction import Jurisdiction
from pupa.scrape.jurisdiction import Jurisdiction
from pupa.scrape import Scraper, Legislator


class MassiveScraper(Scraper):

    def _do_scrape(self):
        people = [
            {"name": "Miss Mckenzie A. Cannon", "post_id": "10a",
             "chamber": "upper",},
            {"name": "Mr. Yandel V. Watkins",
             "post_id": "Second Fnord and Norfolk", "chamber": "lower",},
            {"name": "Adrien A. Coffey", "post_id": "A", "chamber": "upper",},
            {"post_id": "10c", "chamnber": "lower", "name": "Natasha Moon",
             "party": "democratic"},
            {"post_id": "Berkshire, Hampshire, Franklin and Hampden",
             "chamnber": "lower", "name": "Ramon Harmon",
             "party": "republican"},
            {"post_id": "5", "chamnber": "upper", "name": "Sam Sellers",
             "party": "republican"},
            {"post_id": "6", "chamnber": "lower", "name": "Estrella Hahn",
             "party": "republican"},
            {"post_id": "B", "chamnber": "lower", "name": "Teagan Rojas",
             "party": "democratic"},
            {"post_id": "C", "chamnber": "lower", "name": "Barrett Adams",
             "party": "republican"},
            {"post_id": "D", "chamnber": "lower", "name": "Kayla Shelton",
             "party": "democratic"},
            {"post_id": "E", "chamnber": "lower", "name": "Kohen Dudley",
             "party": "republican"},
            {"post_id": "F", "chamnber": "upper", "name": "Cayden Norman",
             "party": "republican"},
            {"post_id": "ZZ", "chamnber": "lower", "name": "Shayla Fritz",
             "party": "democratic"},
            {"post_id": "Ward 2", "chamnber": "lower", "name": "Gunnar Luna",
             "party": "democratic"},
            {"post_id": "Green", "chamnber": "lower", "name": "Regina Cruz",
             "party": "republican"},
            {"post_id": "Blue", "chamnber": "upper", "name": "Makenzie Keller",
             "party": "republican"},
            {"post_id": "Red", "chamnber": "upper", "name": "Eliana Meyer",
             "party": "republican"},
            {"post_id": "Yellow", "chamnber": "upper", "name": "Taylor Parrish",
             "party": "democratic"},
            {"post_id": "Silver", "chamnber": "lower",
             "name": "Callie Craig", "party": "republican"},
        ]
        for person in people:
            l = Legislator(**person)
            l.add_source("http://example.com")
            yield l

    get_people = _do_scrape


class TestLegislature(Jurisdiction):
    jurisdiction_id = "ocd-jurisdiction/country:xx/legislature"

    def get_metadata(self):
        return { 'name': 'Chicago City Council', 'url': 'https://chicago.legistar.com/', 'terms': [{ 'name': '2011-2015', 'sessions': ['2011'], 'start_year': 2011, 'end_year': 2015 }], 'provides': ['people'], 'parties': [ {'name': 'Democrats' } ], 'session_details': { '2011': {'_scraped_name': '2011'} }, 'feature_flags': [], } 

    def scrape_session_list(self):
        return ["2011",]

    def get_scraper(self, *args):
        return MassiveScraper

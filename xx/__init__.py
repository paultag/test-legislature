from pupa.models.jurisdiction import Jurisdiction
from pupa.scrape import Scraper, Legislator


class MassiveScraper(Scraper):
    def scrape(self):
        p = Legislator(name="", post_id="1")
        p.add_source(listing)
        yield p


class TestLegislature(Jurisdiction):
    jurisdiction_id = "ocd-jurisdiction/country:xx/legislature"
    name = "Test State Legislature"
    url = "http://example.com/legislature"

    scrapers = {
        "people": MassiveScraper
    }

    chambers = {
        'upper': {
        },
        'lower': {
        },
    }

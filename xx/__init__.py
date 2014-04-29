# from pupa.models.jurisdiction import Jurisdiction
from pupa.scrape.jurisdiction import Jurisdiction
from pupa.scrape import Scraper, Legislator, Committee


class MassiveScraper(Scraper):

    def get_committees(self):
        committees = [
            {"name": "Ways and Means", "members": [
                "Mckenzie A. Cannon",
                "Yandel V. Watkins",
            ]},
            {"name": "Committee on Pudding Pops", "members": [
                "Kohen Dudley",
                "Cayden Norman",
                "Shayla Fritz",
                "Gunnar Luna",
            ]},
            {"name": "Fiscal Committee", "members": [
                "Gunnar Luna",
                "Regina Cruz",
                "Makenzie Keller",
                "Eliana Meyer",
                "Taylor Parrish",
                "Callie Craig",
            ]},
            {"name": "Bills in the Third Read", "members": [
                "Mckenzie A. Cannon",
                "Yandel V. Watkins",
                "Adrien A. Coffey",
                "Natasha Moon",
                "Ramon Harmon",
                "Sam Sellers",
            ]},
            {"name": "Rules", "members": [
                "Shayla Fritz",
                "Gunnar Luna",
                "Regina Cruz",
            ]},
            {"name": "Standing Committee on Public Safety", "members": [
                "Adrien A. Coffey",
                "Natasha Moon",
                "Ramon Harmon",
                "Sam Sellers",
                "Estrella Hahn",
                "Teagan Rojas",
                "Barrett Adams",
                "Kayla Shelton",
            ]},
        ]

        for committee in committees:
            c = Committee(name=committee['name'])
            c.add_source("http://example.com")
            c.add_contact_detail(type='email', value="committee@example.com",
                                 note='committee email')


            members = iter(committee['members'])
            chair = next(members)
            c.add_member(name=chair, role='chair')
            for member in members:
                c.add_member(name=member)
            yield c

    def get_people(self):
        people = [
            {"name": "Mckenzie A. Cannon", "post_id": "10a",
             "chamber": "upper",},
            {"name": "Yandel V. Watkins",
             "post_id": "Second Fnord and Norfolk", "chamber": "lower",},
            {"name": "Adrien A. Coffey", "post_id": "A", "chamber": "upper",},
            {"post_id": "10c", "chamber": "lower", "name": "Natasha Moon",
             "party": "democratic"},
            {"post_id": "Berkshire, Hampshire, Franklin and Hampden",
             "chamber": "lower", "name": "Ramon Harmon",
             "party": "republican"},
            {"post_id": "5", "chamber": "upper", "name": "Sam Sellers",
             "party": "republican"},
            {"post_id": "6", "chamber": "lower", "name": "Estrella Hahn",
             "party": "republican"},
            {"post_id": "B", "chamber": "lower", "name": "Teagan Rojas",
             "party": "democratic"},
            {"post_id": "C", "chamber": "lower", "name": "Barrett Adams",
             "party": "republican"},
            {"post_id": "D", "chamber": "lower", "name": "Kayla Shelton",
             "party": "democratic"},
            {"post_id": "E", "chamber": "lower", "name": "Kohen Dudley",
             "party": "republican"},
            {"post_id": "F", "chamber": "upper", "name": "Cayden Norman",
             "party": "republican"},
            {"post_id": "ZZ", "chamber": "lower", "name": "Shayla Fritz",
             "party": "democratic"},
            {"post_id": "Ward 2", "chamber": "lower", "name": "Gunnar Luna",
             "party": "democratic"},
            {"post_id": "Green", "chamber": "lower", "name": "Regina Cruz",
             "party": "republican"},
            {"post_id": "Blue", "chamber": "upper", "name": "Makenzie Keller",
             "party": "republican"},
            {"post_id": "Red", "chamber": "upper", "name": "Eliana Meyer",
             "party": "republican"},
            {"post_id": "Yellow", "chamber": "upper", "name": "Taylor Parrish",
             "party": "democratic"},
            {"post_id": "Silver", "chamber": "lower",
             "name": "Callie Craig", "party": "republican"},
        ]

        for person in people:
            l = Legislator(**person)
            l.add_source("http://example.com")
            dslug = (
                person['post_id'].lower().replace(" ", "-").replace(",", "")
            )
            l.add_contact_detail(
                type='email',
                value="%s@legislature.example.com" % (dslug),
                note='office email'
            )
            yield l

        yield from self.get_committees()


class TestLegislature(Jurisdiction):
    jurisdiction_id = "ocd-jurisdiction/country:xx/legislature"

    def get_metadata(self):
        return { 'name': 'Chicago City Council', 'url': 'https://chicago.legistar.com/', 'terms': [{ 'name': '2011-2015', 'sessions': ['2011'], 'start_year': 2011, 'end_year': 2015 }], 'provides': ['people'], 'parties': [ {'name': 'Democrats' } ], 'session_details': { '2011': {'_scraped_name': '2011'} }, 'feature_flags': [], } 

    def scrape_session_list(self):
        return ["2011",]

    def get_scraper(self, *args):
        return MassiveScraper

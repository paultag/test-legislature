# from pupa.models.jurisdiction import Jurisdiction
from pupa.scrape.jurisdiction import Jurisdiction
from pupa.scrape import Scraper, Legislator, Committee
from pupa.models.bill import Bill
from pupa.models.vote import Vote


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

    def get_bills(self):
        bills = [
            {"name": "HB101",
             "title": "Joint county ditch proceedings-conduct by teleconference or video conference",
             "session": "2011",
             "versions": ["http://example.com/HB101.pdf"],
             "actions": [
                 {"description": "Introduced",
                  "actor": "council",
                  "date": "2014-04-15",},
                 {"description": "Referred to the Committee on Pudding Pops",
                  "actor": "council",
                  "date": "2014-04-16",},
                 {"description": "Reported favorably",
                  "actor": "council",
                  "date": "2014-04-16",},
                 {"description": "Referred to the Bills in the Third Read",
                  "actor": "council",
                  "date": "2014-04-17",},
                 {"description": "Vote by the Committee on the Whole. Do pass.",
                  "actor": "council",
                  "date": "2014-04-18",},
                 {"description": "Signed into law",
                  "actor": "council",
                  "date": "2014-04-19",},
             ],
             "sponsors_people": [
                "Shayla Fritz",
                "Gunnar Luna",
             ],
             "sponsors_committee": [
                 "Standing Committee on Public Safety",
             ],
            "votes": [
                {"motion": "Vote by the Committee on the Whole.",
                 "yes_count": 3,
                 "no_count": 1,
                 "passed": True,
                 "type": "passage",
                 "date": "2014-04-18",
                 "session": "2011",
                 "roll": {
                     "yes": [
                        "Gunnar Luna",
                        "Regina Cruz",
                        "Makenzie Keller",
                     ],
                     "no": [
                        "Eliana Meyer",
                     ],
                     "other": [
                     ],
                 }
                },
            ]},
        ]

        for bill in bills:
            b = Bill(name=bill['name'],
                     title=bill['title'],
                     session=bill['session'])
            b.add_source("ftp://example.com/some/bill")


            for vote in bill['votes']:
                v = Vote(motion=vote['motion'],
                         organization="Test City Council",
                         yes_count=vote['yes_count'],
                         no_count=vote['no_count'],
                         passed=vote['passed'],
                         type=vote['type'],
                         date=vote['date'],
                         session=vote['session'],
                        )
                v.add_source("http://example.com/votes/vote.xls")

                for yv in vote['roll']['yes']:
                    v.yes(yv)

                for nv in vote['roll']['no']:
                    v.no(nv)

                yield v


            for sponsor in bill['sponsors_people']:
                b.add_sponsor(name=sponsor, sponsorship_type='primary',
                              entity_type='person', primary=True)

            for sponsor in bill['sponsors_committee']:
                b.add_sponsor(name=sponsor, sponsorship_type='primary',
                              entity_type='organization', primary=True)

            for version in bill['versions']:
                b.add_version_link(name="Bill Version", url=version)

            for action in bill['actions']:
                b.add_action(**action)

            yield b


    def get_people(self):
        people = [
            {"name": "Mckenzie A. Cannon", "post_id": "10a",},
            {"name": "Yandel V. Watkins",
             "post_id": "Second Fnord and Norfolk",},
            {"name": "Adrien A. Coffey", "post_id": "A",},
            {"post_id": "10c", "name": "Natasha Moon",
             "party": "Democratic"},
            {"post_id": "Berkshire, Hampshire, Franklin and Hampden",
             "name": "Ramon Harmon",
             "party": "Republican"},
            {"post_id": "5", "name": "Sam Sellers",
             "party": "Republican"},
            {"post_id": "6", "name": "Estrella Hahn",
             "party": "Republican"},
            {"post_id": "B",  "name": "Teagan Rojas",
             "party": "Democratic"},
            {"post_id": "C", "name": "Barrett Adams",
             "party": "Republican"},
            {"post_id": "D", "name": "Kayla Shelton",
             "party": "Democratic"},
            {"post_id": "E", "name": "Kohen Dudley",
             "party": "Republican"},
            {"post_id": "F", "name": "Cayden Norman",
             "party": "Republican"},
            {"post_id": "ZZ", "name": "Shayla Fritz",
             "party": "Democratic"},
            {"post_id": "Ward 2", "name": "Gunnar Luna",
             "party": "Democratic"},
            {"post_id": "Green", "name": "Regina Cruz",
             "party": "Republican"},
            {"post_id": "Blue", "name": "Makenzie Keller",
             "party": "Republican"},
            {"post_id": "Red", "name": "Eliana Meyer",
             "party": "Republican"},
            {"post_id": "Yellow", "name": "Taylor Parrish",
             "party": "Democratic"},
            {"post_id": "Silver",
             "name": "Callie Craig", "party": "Republican"},
        ]

        for person in people:
            l = Legislator(**person)
            l.add_source("http://example.com")
            dslug = (
                person['post_id'].lower().replace(" ", "-").replace(",", ""))
            l.add_contact_detail(
                type='email',
                value="%s@legislature.example.com" % (dslug),
                note='office email'
            )
            yield l

        yield from self.get_committees()
        yield from self.get_bills()


class TestLegislature(Jurisdiction):
    jurisdiction_id = "ocd-jurisdiction/country:xx/legislature"

    def get_metadata(self):
        return {'name': 'Test City Council',
                'url': 'https://example.com/',
                'terms': [{ 'name': '2011-2015', 'sessions': ['2011'],
                           'start_year': 2011, 'end_year': 2015 }],
                'provides': ['people',],
                'parties': [
                    {"name": "Republican"},
                    {"name": "Democratic"},
                ],
                'session_details': {
                    '2011': {'_scraped_name': '2011'},
                },
                'feature_flags': [],
       }

    def scrape_session_list(self):
        return ["2011",]

    def get_scraper(self, *args):
        return MassiveScraper

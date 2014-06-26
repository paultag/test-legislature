# from pupa.models.jurisdiction import Jurisdiction
from pupa.scrape.jurisdiction import Jurisdiction
from pupa.scrape import Scraper, Legislator, Committee
from pupa.scrape import Bill, Vote, Event
from pupa.utils import make_psuedo_id
import datetime as dt


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
            c.add_member(name_or_person=chair, role='chair')
            for member in members:
                c.add_member(name_or_person=member)
            yield c

    def get_bills(self):
        bills = [
            {"name": "HB500",
             "title": "Makes various changes to provisions governing employment practices",
             "session": "2011",
             "versions": ["http://example.com/HB500.pdf"],
             "actions": [
                 {"description": "Introduced",
                  "actor": "Committee on Pudding Pops",
                  "date": "2014-04-15",},

                 {"date": "2014-04-15",
                  "description": "Read first time. Referred to Committee on Commerce and Labor. To printer.",
                  "actor": "Test City Council" },

                 {"date": "2014-04-15",
                  "description": "From printer. To committee.",
                  "actor": "Test City Council"},

                 {"date": "2014-04-15",
                  "description": "From committee: Do pass.",
                  "actor": "Rules"},

                 {"description": "Signed into law",
                  "actor": "Fiscal Committee",
                  "date": "2014-04-19",},
             ],
             "sponsors_people": [
             ],
             "sponsors_committee": [
             ],
            "votes": [
                {"motion": "Vote by the Committee on the Whole.",
                 "yes_count": 1,
                 "other_count": 1,
                 "no_count": 3,
                 "passed": True,
                 "type": "passage:bill",
                 "date": "2014-04-15",
                 "session": "2011",
                 "roll": {
                     "yes": [
                        "Eliana Meyer",
                     ],
                     "no": [
                        "Gunnar Luna",
                        "Regina Cruz",
                        "Makenzie Keller",
                     ],
                     "other": [
                        "Unknown Person",
                     ],
                 }
                },
            ]},
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
                 "type": "passage:bill",
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
            b = Bill(identifier=bill['name'],
                     title=bill['title'],
                     legislative_session=bill['session'])
            b.add_source("ftp://example.com/some/bill")


            for vote in bill['votes']:
                v = Vote(motion_text=vote['motion'],
                         organization_id=make_psuedo_id(
                             name="Test City Council",
                             classification="legislature"
                         ),
                         yes_count=vote['yes_count'],
                         no_count=vote['no_count'],
                         result='pass' if vote['passed'] else 'fail',
                         classification=vote['type'],
                         start_date=vote['date'],
                         legislative_session=vote['session'],
                        )
                v.add_source("http://example.com/votes/vote.xls")

                for yv in vote['roll']['yes']:
                    v.yes(yv)

                for nv in vote['roll']['no']:
                    v.no(nv)

                yield v


            for sponsor in bill['sponsors_people']:
                b.add_sponsorship(name=sponsor, classification='primary',
                              entity_type='person', primary=True)

            for sponsor in bill['sponsors_committee']:
                b.add_sponsorship(name=sponsor, classification='primary',
                              entity_type='organization', primary=True)

            for version in bill['versions']:
                b.add_version_link(note="Bill Version", url=version)

            for action in bill['actions']:
                action['organization'] = make_psuedo_id(name=action.pop(
                    'actor'
                ))
                b.add_action(**action)

            yield b


    def get_events(self):
        events = [
            {"name": "Meeting of the Join Committee on Foo",
             "start_time": dt.datetime.fromtimestamp(1408923205),
             "location": "Somewhere just east of Northwestsouthshire"},
            {"name": "Meeting of the Join Committee on Bar",
             "start_time": dt.datetime.fromtimestamp(1008923205),
             "location": "Council Chambers",
             "_location": {
                 "name": "Council Chambers",
                 "url": "http://somewhere.example.com",
                 "note": "Council Chambers, first room on the left in city hall",
                 "coordinates": {
                     "latitude": "42.360391",
                     "longitude": "-71.058004",
                 }
            }},
            {"name": "Meeting of the Join Committee on Baz",
             "start_time": dt.datetime.fromtimestamp(1408929205),
             "location": "City Hall",
             "media": [
                 {"date": "2014-04-12",
                  "type": "recording",
                  "name": "Recording of the meeting",
                  "links": [
                      {"mimetype": "video/mp4",
                       "url": "http://example.com/video.mp4"},
                      {"mimetype": "video/webm",
                       "url": "http://example.com/video.webm"},
                  ],
                  "offset": 19,
                }
             ]},
            {"name": "Meeting of the Join Committee on Baz",
             "start_time": dt.datetime.fromtimestamp(1418929205),
             "location": "City Hall",
             "participants": [
                 {"note": "Meeting Chair",
                  "type": "person",
                  "name": "Yandel V. Watkins",},
                 {"note": "Attending Committee",
                  "type": "organization",
                  "name": "Ways and Means",},
             ],
             "links": [
                {"note": "Council Homepage",
                 "url": "http://council.example.com",},
                {"note": "Background on the topic",
                 "url": "http://topic.news.example.com/",}
             ],},
            {"name": "Meeting of the Join Committee on Bar",
             "start_time": dt.datetime.fromtimestamp(1008923205),
             "location": "Council Chambers",
             "documents": [
                 {"url": "http://someone.example.com/slides.html",
                  "mimetype": "text/html",
                  "name": "HTML Slides",},
                 {"url": "http://someone.example.com/slides.ppt",
                  "mimetype": "application/vnd.ms-powerpoint",
                  "name": "Powerpoint of the Slides",},
                 {"url": "http://test.example.com/otherthing.ogg",
                  "mimetype": "audio/ogg",
                  "name": "Background Music",},
             ],
            },
            {"name": "Meeting of the Join Committee on Fnord",
             "start_time": dt.datetime.fromtimestamp(1418929205),
             "location": "City Hall",
             "agenda": [
                {"related_entities": [
                 {"note": "Yandel will be presenting on the effects of this bill",
                  "type": "person",
                  "name": "Yandel V. Watkins",},
                ],
                "media": [
                    {"date": "2014-04-12",
                     "type": "recording",
                     "name": "Recording of the meeting",
                     "links": [
                         {"mimetype": "video/mp4",
                          "url": "http://example.com/video.mp4"},
                         {"mimetype": "video/webm",
                          "url": "http://example.com/video.webm"},
                     ],
                     "offset": 19,
                    }
                ],
                "notes": [
                    "Yandel started his presentation.",
                    "Yandel made some good points.",
                    "Yandel sat down.",
                ],
                "subjects": [
                    "testimony", "this-bill", "this-subject"
                ],
                "order": '0',
               "description": "Yandel will give a talk",
                },
                {"related_entities": [
                 {"note": "Mckenzie will be presenting on the effects of this bill",
                  "type": "person",
                  "name": "Mckenzie A. Cannon",},
                ],
                "media": [
                    {"date": "2014-04-12",
                     "type": "recording",
                     "name": "Recording of the meeting",
                     "links": [
                         {"mimetype": "video/mp4",
                          "url": "http://example.com/video.mp4"},
                         {"mimetype": "video/webm",
                          "url": "http://example.com/video.webm"},
                     ],
                     "offset": 200,
                    }
                ],
                "notes": [
                    "Mckenzie started his presentation.",
                    "Mckenzie made some good points.",
                    "Mckenzie made some good better points.",
                    "Mckenzie sat down.",
                ],
                "subjects": [
                    "testimony", "this-bill-2", "this-subject"
                ],
                "order": '1',
                "description": "Mckenzie will give a talk",
                },
             ],},
        ]
        for e in events:
            obj = Event(name=e['name'],
                        start_time=e['start_time'],
                        location=e['location'])
            obj.add_source("http://example.com/events")

            l = e.get("_location", None)
            if l:
                obj.location = l

            for key in [
                "media", "links", "participants", "agenda", "documents"
            ]:
                l = e.get(key, None)
                if l:
                    setattr(obj, key, l)

            obj.validate()
            yield obj


    def get_people(self):
        people = [
            {"name": "Mckenzie A. Cannon", "district": "10a",},
            {"name": "Yandel V. Watkins",
             "district": "Second Fnord and Norfolk",},
            {"name": "Adrien A. Coffey", "district": "A",},
            {"district": "10c", "name": "Natasha Moon",},
            {"district": "Berkshire, Hampshire, Franklin and Hampden",
             "name": "Ramon Harmon",},
            {"district": "5", "name": "Sam Sellers",},
            {"district": "6", "name": "Estrella Hahn",},
            {"district": "B",  "name": "Teagan Rojas",},
            {"district": "C", "name": "Barrett Adams",},
            {"district": "D", "name": "Kayla Shelton",},
            {"district": "E", "name": "Kohen Dudley",},
            {"district": "F", "name": "Cayden Norman",},
            {"district": "ZZ", "name": "Shayla Fritz",},
            {"district": "Ward 2", "name": "Gunnar Luna",},
            {"district": "Green", "name": "Regina Cruz",},
            {"district": "Blue", "name": "Makenzie Keller",},
            {"district": "Red", "name": "Eliana Meyer",},
            {"district": "Yellow", "name": "Taylor Parrish",},
            {"district": "Silver", "name": "Callie Craig",},
        ]

        for person in people:
            l = Legislator(**person)
            l.add_source("http://example.com")
            dslug = (
                person['district'].lower().replace(" ", "-").replace(",", ""))
            l.add_contact_detail(
                type='email',
                value="%s@legislature.example.com" % (dslug),
                note='office email'
            )
            yield l

    def scrape(self):
        yield from self.get_people()
        yield from self.get_events()
        yield from self.get_committees()
        yield from self.get_bills()



class TestLegislature(Jurisdiction):
    division_id = "ocd-division/country:xx"
    classification = "government"
    name = "Test City Council"
    url = "http://example.com"

    scrapers = {
        "people": MassiveScraper,
    }

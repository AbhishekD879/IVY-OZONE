export const CARDS_MOCK =
    [
        {
            category: 'myShowDowns',
            categoryName: 'My Showdowns',
            date: null,
            contests: [
                {
                    'id': '6040e25bd6e2da40b3fe9252',
                    'generatedId': null,
                    'name': 'WWWW',
                    'icon': null,
                    'startDate': '2021-03-04T13:36:15.366Z',
                    'event': '232215271',
                    'entryStake': '6',
                    'isFreeBetsAllowed': true,
                    'description': null,
                    'blurb': null,
                    'entryConfirmationText': null,
                    'nextContestId': '345',
                    'display': true,
                    'brand': 'ladbrokes',
                    'showRoleContest': true,
                    'prizePool': {
                        'cash': '24',
                        'firstPlace': '10320',
                        'freeBets': 23,
                        'vouchers': '20',
                        'summary': null,
                        'tickets': '20',
                        'totalPrizes': '234'
                    },
                    'contestPrizes': null,
                    'sponsorText': 'Sponsored By',
                    'sponsorLogo': null,
                    'size': 1000,
                    'teams': 5,
                    'eventDetails':
                        {
                            'id': '232215271',
                            'name': 'Chelsea v Everton',
                            'eventStatusCode': 'A',
                            'isActive': 'true',
                            'isDisplayed': 'true',
                            'displayOrder': '-45',
                            'siteChannels': 'P,p,Q,R,C,E,H,I,J,M,',
                            'eventSortCode': 'MTCH',
                            'startTime': '2021-03-08T18:00:00Z',
                            'rawIsOffCode': 'N',
                            'classId': '97',
                            'typeId': '442',
                            'sportId': '16',
                            'liveServChannels': 'sEVENT0232215271,',
                            'liveServChildrenChannels': 'SEVENT0232215271,',
                            'categoryId': '16',
                            'categoryCode': 'FOOTBALL',
                            'categoryName': 'Football',
                            'categoryDisplayOrder': '-11010',
                            'className': 'English',
                            'classDisplayOrder': '-32527',
                            'classSortCode': 'FB',
                            'typeName': 'Premier League',
                            'typeDisplayOrder': '-32767',
                            'typeFlagCodes': 'FI,GVA,IVA,UK,EP,IE,ER,FE,',
                            'isOpenEvent': 'true',
                            'isNext24HourEvent': 'true',
                            'isLiveNowOrFutureEvent': 'true',
                            'drilldownTagNames': 'EVFLAG_FE,EVFLAG_FI,EVFLAG_PB,EVFLAG_BL,',
                            'isAvailable': 'true',
                            'cashoutAvail': 'Y',
                            'regularTimeFinished': false
                        }
                }
            ]
        },
        {
            category: 'Today',
            categoryName: 'Today',
            date: '2021-02-25T06:42:22.470Z',
            contests: [
                {
                    'id': '6040e25bd6e2da40b3fe9252',
                    'generatedId': null,
                    'name': 'WWWW',
                    'icon': null,
                    'startDate': '2021-03-04T13:36:15.366Z',
                    'event': '232300717',
                    'entryStake': '6',
                    'isFreeBetsAllowed': true,
                    'description': null,
                    'blurb': null,
                    'entryConfirmationText': null,
                    'nextContestId': '345',
                    'display': true,
                    'showRoleContest': true,
                    'brand': 'ladbrokes',
                    'prizePool': {
                        'cash': '24',
                        'firstPlace': '10320',
                        'freeBets': 23,
                        'vouchers': '20',
                        'summary': null,
                        'tickets': '20',
                        'totalPrizes': '234'
                    },
                    'contestPrizes': null,
                    'sponsorText': 'Sponsored By',
                    'sponsorLogo': null,
                    'size': 1000,
                    'teams': 5,
                    'eventDetails':
                        {
                            'id': '232300717',
                            'name': 'Ajax v Groningen',
                            'eventStatusCode': 'S',
                            'isDisplayed': 'true',
                            'displayOrder': '0',
                            'siteChannels': 'P,p,Q,R,C,I,M,',
                            'eventSortCode': 'MTCH',
                            'startTime': '2021-03-07T11:15:00Z',
                            'rawIsOffCode': 'Y',
                            'isStarted': 'true',
                            'classId': '140',
                            'typeId': '823',
                            'sportId': '16',
                            'liveServChannels': 'sEVENT0232300717,',
                            'liveServChildrenChannels': 'SEVENT0232300717,',
                            'categoryId': '16',
                            'categoryCode': 'FOOTBALL',
                            'categoryName': 'Football',
                            'categoryDisplayOrder': '-11010',
                            'className': 'Dutch',
                            'classDisplayOrder': '-32519',
                            'classSortCode': 'FB',
                            'typeName': 'Dutch Eredivisie',
                            'typeDisplayOrder': '-32739',
                            'typeFlagCodes': 'IVA,PVA,',
                            'isOpenEvent': 'true',
                            'isLiveNowEvent': 'true',
                            'isLiveNowOrFutureEvent': 'true',
                            'drilldownTagNames': 'EVFLAG_IVM,EVFLAG_BL,',
                            'isAvailable': 'true',
                            'mediaTypeCodes': 'VST,',
                            'cashoutAvail': 'Y',
                            'regularTimeFinished': false
                        }
                }
            ]
        }
    ];

export const sEVENTUpdate = {
    payload: {
        'names': { 'en': 'Auto test Gutierrezside v Auto test West Lindsey' },
        'status': 'S',
        'displayed': 'Y',
        'result_conf': 'N',
        'disporder': 0,
        'start_time': '2017-05-14 10:00:50',
        'start_time_xls': { 'en': '14th of May 2017  10:00 am' },
        'suspend_at': '',
        'is_off': 'N',
        'started': 'N',
        'race_stage': '',
        'ev_id': '5447497',
        'ev_mkt_id': '5447497'
    },
    type: 'sEVENT',
    id: 232341790
};

export const sEVENTupdate = {
    id: 232341790,
    subject_type: 'sEVENT',
    payload: {
        status: 'status',
        displayed: 'N',
        started: 'Y',
        race_stage: 'race_stage',
        result_conf: 'Y',
        names: {
            en: 'en'
        }
    }
};

export const sCLOCKUpdate = {
    payload: {
        clock_seconds: '1232',
        ev_id: 232341790,
        last_update: '2021-03-09 10:20:35',
        last_update_secs: '1615285235',
        offset_secs: '1231',
        period_code: 'FIRST_HALF',
        period_index: '',
        start_time_secs: '1615284000',
        state: 'S'
    },
    type: 'sCLOCK',
    id: 232341790
};

export const sSCBRDUpdate = {
    payload: {
        clock_seconds: '1232',
        ev_id: 232341790,
        last_update: '2021-03-09 10:20:35',
        last_update_secs: '1615285235',
        offset_secs: '1231',
        period_code: 'FIRST_HALF',
        period_index: '',
        start_time_secs: '1615284000',
        state: 'S'
    },
    type: 'sSCBRD',
    id: 232341790
};

export const CLOCKUpdate = {
    payload: {
        clock_seconds: '1232',
        ev_id: 232341790,
        last_update: '2021-03-09 10:20:35',
        last_update_secs: '1615285235',
        offset_secs: '1231',
        period_code: 'FIRST_HALF',
        period_index: '',
        start_time_secs: '1615284000',
        state: 'S'
    },
    type: 'CLOCK',
    id: 232341790
};

export const SCBRDUpdate = {
    payload: {
        clock_seconds: '1232',
        ev_id: 232341790,
        last_update: '2021-03-09 10:20:35',
        last_update_secs: '1615285235',
        offset_secs: '1231',
        period_code: 'FIRST_HALF',
        period_index: '',
        start_time_secs: '1615284000',
        state: 'S'
    },
    type: 'SCORE',
    id: 232341790
};

export const eventDetails = {
    'id': 232341790,
    'name': 'Jeonbuk Hyundai Motors v Gangwon',
    'eventStatusCode': 'S',
    'displayOrder': '0',
    'siteChannels': 'P,p,Q,R,C,I,M,',
    'eventSortCode': 'MTCH',
    'startTime': '2021-03-09T10:00:00Z',
    'rawIsOffCode': 'Y',
    'isStarted': 'true',
    'isResulted': 'true',
    'isFinished': 'true',
    'classId': '164',
    'typeId': '955',
    'sportId': '16',
    'liveServChannels': 'sEVENT0232341790,',
    'liveServChildrenChannels': 'SEVENT0232341790,',
    'categoryId': '16',
    'categoryCode': 'FOOTBALL',
    'categoryName': 'Football',
    'categoryDisplayOrder': '-11010',
    'className': 'South Korean',
    'classDisplayOrder': '-32508',
    'classSortCode': 'FB',
    'typeName': 'South Korean K-League',
    'typeDisplayOrder': '0',
    'typeFlagCodes': 'GVA,IVA,PVA,',
    'mediaTypeCodes': 'VST,',
    'cashoutAvail': 'Y',
    'children': [
        {
            'eventPeriod': {
                'id': '4602998',
                'eventId': '232341790',
                'periodCode': 'ALL',
                'description': 'Total Duration of the game/match',
                'startTime': '2021-03-09T10:00:04Z',
                'children': [
                    {
                        'eventPeriodClockState': {
                            'id': '4101372',
                            'eventPeriodId': '4602998',
                            'offset': '0',
                            'lastUpdate': '2021-03-09T10:00:03Z',
                            'state': 'S'
                        }
                    },
                    {
                        'eventFact': {
                            'id': '11211051',
                            'eventId': '232341790',
                            'eventParticipantId': '943696',
                            'eventPeriodId': '4602998',
                            'fact': '5',
                            'factCode': 'CORNERS',
                            'name': 'Penalties in a match/game'
                        }
                    },
                    {
                        'eventPeriod': {
                            'id': '4603496',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'SECOND_HALF',
                            'description': 'Second half of a match/game',
                            'startTime': '2021-03-09T11:04:05Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101401',
                                        'eventPeriodId': '4603496',
                                        'offset': '5716',
                                        'lastUpdate': '2021-03-09T11:54:20Z',
                                        'state': 'R'
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344255',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '2811',
                                        'createDate': '2021-03-09T11:05:56Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344255',
                                                    'eventIncidentId': '41344255',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344266',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '3227',
                                        'createDate': '2021-03-09T11:12:51Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344266',
                                                    'eventIncidentId': '41344266',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344332',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '5184',
                                        'createDate': '2021-03-09T11:45:29Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344332',
                                                    'eventIncidentId': '41344332',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344283',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '3874',
                                        'createDate': '2021-03-09T11:23:39Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344283',
                                                    'eventIncidentId': '41344283',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'eventPeriod': {
                            'id': '4603966',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'FINISH',
                            'description': 'Match finished',
                            'startTime': '2021-03-09T11:54:31Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101416',
                                        'eventPeriodId': '4603966',
                                        'offset': '5725',
                                        'lastUpdate': '2021-03-09T12:04:26Z',
                                        'state': 'S'
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344365',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603966',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'MATCH_FINISHED',
                                        'description': 'Match finished',
                                        'relativeTime': '5725',
                                        'createDate': '2021-03-09T12:04:26Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344365',
                                                    'eventIncidentId': '41344365',
                                                    'text': 'STAT_TYPE_FIN',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'eventPeriod': {
                            'id': '4602999',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'FIRST_HALF',
                            'description': 'First half of a match/game',
                            'startTime': '2021-03-09T10:00:04Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101373',
                                        'eventPeriodId': '4602999',
                                        'offset': '2856',
                                        'lastUpdate': '2021-03-09T10:47:40Z',
                                        'state': 'S'
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344172',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4602999',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '597',
                                        'createDate': '2021-03-09T10:10:01Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344172',
                                                    'eventIncidentId': '41344172',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'eventPeriod': {
                            'id': '4603357',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'HALF_TIME',
                            'description': 'Half time in a match/game',
                            'startTime': '2021-03-09T10:48:23Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101390',
                                        'eventPeriodId': '4603357',
                                        'offset': '2898',
                                        'lastUpdate': '2021-03-09T10:48:23Z',
                                        'state': 'S'
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            'eventParticipant': {
                'id': '943696',
                'eventId': '232341790',
                'name': 'Gangwon',
                'type': 'T',
                'roleCode': 'AWAY',
                'role': 'Away Team'
            }
        },
        {
            'eventParticipant': {
                'id': '943695',
                'eventId': '232341790',
                'name': 'Jeonbuk Hyundai Motors',
                'type': 'T',
                'roleCode': 'HOME',
                'role': 'Home Team'
            }
        }]
};

export const EVENTS_DETAILS = [
    {
        'id': '232341790',
        'name': 'Jeonbuk Hyundai Motors v Gangwon',
        'eventStatusCode': 'S',
        'displayOrder': '0',
        'siteChannels': 'P,p,Q,R,C,I,M,',
        'eventSortCode': 'MTCH',
        'startTime': '2021-03-09T10:00:00Z',
        'rawIsOffCode': 'Y',
        'isStarted': 'true',
        'isResulted': 'true',
        'isFinished': 'true',
        'classId': '164',
        'typeId': '955',
        'sportId': '16',
        'liveServChannels': 'sEVENT0232341790,',
        'liveServChildrenChannels': 'SEVENT0232341790,',
        'categoryId': '16',
        'categoryCode': 'FOOTBALL',
        'categoryName': 'Football',
        'categoryDisplayOrder': '-11010',
        'className': 'South Korean',
        'classDisplayOrder': '-32508',
        'classSortCode': 'FB',
        'typeName': 'South Korean K-League',
        'typeDisplayOrder': '0',
        'typeFlagCodes': 'GVA,IVA,PVA,',
        'mediaTypeCodes': 'VST,',
        'cashoutAvail': 'Y',
        'children': [
            {
                'eventPeriod': {
                    'id': '4602998',
                    'eventId': '232341790',
                    'periodCode': 'ALL',
                    'description': 'Total Duration of the game/match',
                    'startTime': '2021-03-09T10:00:04Z',
                    'children': [
                        {
                            'eventPeriodClockState': {
                                'id': '4101372',
                                'eventPeriodId': '4602998',
                                'offset': '0',
                                'lastUpdate': '2021-03-09T10:00:03Z',
                                'state': 'S'
                            }
                        },
                        {
                            'eventFact': {
                                'id': '11210884',
                                'eventId': '232341790',
                                'eventParticipantId': '943696',
                                'eventPeriodId': '4602998',
                                'fact': '2',
                                'factCode': 'YELLOW_CARDS',
                                'name': 'Num of yellow cards in a match/game'
                            }
                        },
                        {
                            'eventFact': {
                                'id': '11210883',
                                'eventId': '232341790',
                                'eventParticipantId': '943695',
                                'eventPeriodId': '4602998',
                                'fact': '4',
                                'factCode': 'YELLOW_CARDS',
                                'name': 'Num of yellow cards in a match/game'
                            }
                        },
                        {
                            'eventFact': {
                                'id': '11211050',
                                'eventId': '232341790',
                                'eventParticipantId': '943695',
                                'eventPeriodId': '4602998',
                                'fact': '9',
                                'factCode': 'CORNERS',
                                'name': 'Penalties in a match/game'
                            }
                        },
                        {
                            'eventFact': {
                                'id': '11210804',
                                'eventId': '232341790',
                                'eventParticipantId': '943696',
                                'eventPeriodId': '4602998',
                                'fact': '1',
                                'factCode': 'SCORE',
                                'name': 'Score of the match/game'
                            }
                        },
                        {
                            'eventFact': {
                                'id': '11210803',
                                'eventId': '232341790',
                                'eventParticipantId': '943695',
                                'eventPeriodId': '4602998',
                                'fact': '2',
                                'factCode': 'SCORE',
                                'name': 'Score of the match/game'
                            }
                        },
                        {
                            'eventFact': {
                                'id': '11211051',
                                'eventId': '232341790',
                                'eventParticipantId': '943696',
                                'eventPeriodId': '4602998',
                                'fact': '5',
                                'factCode': 'CORNERS',
                                'name': 'Penalties in a match/game'
                            }
                        },
                        {
                            'eventPeriod': {
                                'id': '4603496',
                                'eventId': '232341790',
                                'parentEventPeriodId': '4602998',
                                'periodCode': 'SECOND_HALF',
                                'description': 'Second half of a match/game',
                                'startTime': '2021-03-09T11:04:05Z',
                                'children': [
                                    {
                                        'eventPeriodClockState': {
                                            'id': '4101401',
                                            'eventPeriodId': '4603496',
                                            'offset': '5716',
                                            'lastUpdate': '2021-03-09T11:54:20Z',
                                            'state': 'R'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11212573',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943695',
                                            'eventPeriodId': '4603496',
                                            'fact': '3',
                                            'factCode': 'YELLOW_CARDS',
                                            'name': 'Num of yellow cards in a match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11212574',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943696',
                                            'eventPeriodId': '4603496',
                                            'fact': '1',
                                            'factCode': 'YELLOW_CARDS',
                                            'name': 'Num of yellow cards in a match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11212588',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943695',
                                            'eventPeriodId': '4603496',
                                            'fact': '2',
                                            'factCode': 'SCORE',
                                            'name': 'Score of the match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11212589',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943696',
                                            'eventPeriodId': '4603496',
                                            'fact': '1',
                                            'factCode': 'SCORE',
                                            'name': 'Score of the match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11212208',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943695',
                                            'eventPeriodId': '4603496',
                                            'fact': '5',
                                            'factCode': 'CORNERS',
                                            'name': 'Penalties in a match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11212209',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943696',
                                            'eventPeriodId': '4603496',
                                            'fact': '5',
                                            'factCode': 'CORNERS',
                                            'name': 'Penalties in a match/game'
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344329',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'SCORE',
                                            'description': 'Scoring Incident',
                                            'relativeTime': '5069',
                                            'createDate': '2021-03-09T11:43:34Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344329',
                                                        'eventIncidentId': '41344329',
                                                        'text': 'SCORE_TYPE_G',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344255',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '2811',
                                            'createDate': '2021-03-09T11:05:56Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344255',
                                                        'eventIncidentId': '41344255',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344266',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943696',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '3227',
                                            'createDate': '2021-03-09T11:12:51Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344266',
                                                        'eventIncidentId': '41344266',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344332',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943696',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '5184',
                                            'createDate': '2021-03-09T11:45:29Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344332',
                                                        'eventIncidentId': '41344332',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344343',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943696',
                                            'incidentCode': 'YELLOW_CARD',
                                            'description': 'Yellow Card',
                                            'relativeTime': '5520',
                                            'createDate': '2021-03-09T11:51:05Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344343',
                                                        'eventIncidentId': '41344343',
                                                        'text': 'STAT_TYPE_YC',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344256',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '2843',
                                            'createDate': '2021-03-09T11:06:28Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344256',
                                                        'eventIncidentId': '41344256',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344278',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943696',
                                            'incidentCode': 'SCORE',
                                            'description': 'Scoring Incident',
                                            'relativeTime': '3587',
                                            'createDate': '2021-03-09T11:18:51Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344278',
                                                        'eventIncidentId': '41344278',
                                                        'text': 'SCORE_TYPE_G',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344344',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'SCORE',
                                            'description': 'Scoring Incident',
                                            'relativeTime': '5533',
                                            'createDate': '2021-03-09T11:51:17Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344344',
                                                        'eventIncidentId': '41344344',
                                                        'text': 'SCORE_TYPE_G',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344275',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'YELLOW_CARD',
                                            'description': 'Yellow Card',
                                            'relativeTime': '3542',
                                            'createDate': '2021-03-09T11:18:07Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344275',
                                                        'eventIncidentId': '41344275',
                                                        'text': 'STAT_TYPE_YC',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344304',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'YELLOW_CARD',
                                            'description': 'Yellow Card',
                                            'relativeTime': '4411',
                                            'createDate': '2021-03-09T11:32:35Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344304',
                                                        'eventIncidentId': '41344304',
                                                        'text': 'STAT_TYPE_YC',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344326',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943696',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '5000',
                                            'createDate': '2021-03-09T11:42:25Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344326',
                                                        'eventIncidentId': '41344326',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344337',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'YELLOW_CARD',
                                            'description': 'Yellow Card',
                                            'relativeTime': '5304',
                                            'createDate': '2021-03-09T11:47:29Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344337',
                                                        'eventIncidentId': '41344337',
                                                        'text': 'STAT_TYPE_YC',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344269',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '3319',
                                            'createDate': '2021-03-09T11:14:23Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344269',
                                                        'eventIncidentId': '41344269',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344251',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943696',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '2726',
                                            'createDate': '2021-03-09T11:04:31Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344251',
                                                        'eventIncidentId': '41344251',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344284',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943696',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '3944',
                                            'createDate': '2021-03-09T11:24:49Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344284',
                                                        'eventIncidentId': '41344284',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344282',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '3829',
                                            'createDate': '2021-03-09T11:22:54Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344282',
                                                        'eventIncidentId': '41344282',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344283',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603496',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '3874',
                                            'createDate': '2021-03-09T11:23:39Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344283',
                                                        'eventIncidentId': '41344283',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            'eventPeriod': {
                                'id': '4603966',
                                'eventId': '232341790',
                                'parentEventPeriodId': '4602998',
                                'periodCode': 'FINISH',
                                'description': 'Match finished',
                                'startTime': '2021-03-09T11:54:31Z',
                                'children': [
                                    {
                                        'eventPeriodClockState': {
                                            'id': '4101416',
                                            'eventPeriodId': '4603966',
                                            'offset': '5725',
                                            'lastUpdate': '2021-03-09T12:04:26Z',
                                            'state': 'S'
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344365',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603966',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'MATCH_FINISHED',
                                            'description': 'Match finished',
                                            'relativeTime': '5725',
                                            'createDate': '2021-03-09T12:04:26Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344365',
                                                        'eventIncidentId': '41344365',
                                                        'text': 'STAT_TYPE_FIN',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344346',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4603966',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'MATCH_FINISHED',
                                            'description': 'Match finished',
                                            'relativeTime': '5725',
                                            'createDate': '2021-03-09T11:54:30Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344346',
                                                        'eventIncidentId': '41344346',
                                                        'text': 'STAT_TYPE_FIN',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            'eventPeriod': {
                                'id': '4602999',
                                'eventId': '232341790',
                                'parentEventPeriodId': '4602998',
                                'periodCode': 'FIRST_HALF',
                                'description': 'First half of a match/game',
                                'startTime': '2021-03-09T10:00:04Z',
                                'children': [
                                    {
                                        'eventPeriodClockState': {
                                            'id': '4101373',
                                            'eventPeriodId': '4602999',
                                            'offset': '2856',
                                            'lastUpdate': '2021-03-09T10:47:40Z',
                                            'state': 'S'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11210882',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943696',
                                            'eventPeriodId': '4602999',
                                            'fact': '1',
                                            'factCode': 'YELLOW_CARDS',
                                            'name': 'Num of yellow cards in a match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11210881',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943695',
                                            'eventPeriodId': '4602999',
                                            'fact': '1',
                                            'factCode': 'YELLOW_CARDS',
                                            'name': 'Num of yellow cards in a match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11211049',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943696',
                                            'eventPeriodId': '4602999',
                                            'fact': '0',
                                            'factCode': 'CORNERS',
                                            'name': 'Penalties in a match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11211048',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943695',
                                            'eventPeriodId': '4602999',
                                            'fact': '4',
                                            'factCode': 'CORNERS',
                                            'name': 'Penalties in a match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11210802',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943696',
                                            'eventPeriodId': '4602999',
                                            'fact': '0',
                                            'factCode': 'SCORE',
                                            'name': 'Score of the match/game'
                                        }
                                    },
                                    {
                                        'eventFact': {
                                            'id': '11210801',
                                            'eventId': '232341790',
                                            'eventParticipantId': '943695',
                                            'eventPeriodId': '4602999',
                                            'fact': '0',
                                            'factCode': 'SCORE',
                                            'name': 'Score of the match/game'
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344212',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4602999',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'YELLOW_CARD',
                                            'description': 'Yellow Card',
                                            'relativeTime': '2367',
                                            'createDate': '2021-03-09T10:39:31Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344212',
                                                        'eventIncidentId': '41344212',
                                                        'text': 'STAT_TYPE_YC',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344165',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4602999',
                                            'eventParticipantId': '943696',
                                            'incidentCode': 'YELLOW_CARD',
                                            'description': 'Yellow Card',
                                            'relativeTime': '268',
                                            'createDate': '2021-03-09T10:04:33Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344165',
                                                        'eventIncidentId': '41344165',
                                                        'text': 'STAT_TYPE_YC',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344158',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4602999',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'SCORE',
                                            'description': 'Scoring Incident',
                                            'relativeTime': '0',
                                            'createDate': '2021-03-09T10:00:03Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344158',
                                                        'eventIncidentId': '41344158',
                                                        'text': 'SCORE_TYPE_G',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344159',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4602999',
                                            'eventParticipantId': '943696',
                                            'incidentCode': 'SCORE',
                                            'description': 'Scoring Incident',
                                            'relativeTime': '0',
                                            'createDate': '2021-03-09T10:00:03Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344159',
                                                        'eventIncidentId': '41344159',
                                                        'text': 'SCORE_TYPE_G',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344192',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4602999',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '1269',
                                            'createDate': '2021-03-09T10:21:12Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344192',
                                                        'eventIncidentId': '41344192',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344174',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4602999',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '642',
                                            'createDate': '2021-03-09T10:10:46Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344174',
                                                        'eventIncidentId': '41344174',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344186',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4602999',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '976',
                                            'createDate': '2021-03-09T10:16:20Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344186',
                                                        'eventIncidentId': '41344186',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'eventIncident': {
                                            'id': '41344172',
                                            'eventId': '232341790',
                                            'eventPeriodId': '4602999',
                                            'eventParticipantId': '943695',
                                            'incidentCode': 'CORNER',
                                            'description': 'Corner Kick',
                                            'relativeTime': '597',
                                            'createDate': '2021-03-09T10:10:01Z',
                                            'children': [
                                                {
                                                    'eventIncidentComment': {
                                                        'id': '41344172',
                                                        'eventIncidentId': '41344172',
                                                        'text': 'STAT_TYPE_CNR',
                                                        'lang': 'en'
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            'eventPeriod': {
                                'id': '4603357',
                                'eventId': '232341790',
                                'parentEventPeriodId': '4602998',
                                'periodCode': 'HALF_TIME',
                                'description': 'Half time in a match/game',
                                'startTime': '2021-03-09T10:48:23Z',
                                'children': [
                                    {
                                        'eventPeriodClockState': {
                                            'id': '4101390',
                                            'eventPeriodId': '4603357',
                                            'offset': '2898',
                                            'lastUpdate': '2021-03-09T10:48:23Z',
                                            'state': 'S'
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                'eventParticipant': {
                    'id': '943696',
                    'eventId': '232341790',
                    'name': 'Gangwon',
                    'type': 'T',
                    'roleCode': 'AWAY',
                    'role': 'Away Team'
                }
            },
            {
                'eventParticipant': {
                    'id': '943695',
                    'eventId': '232341790',
                    'name': 'Jeonbuk Hyundai Motors',
                    'type': 'T',
                    'roleCode': 'HOME',
                    'role': 'Home Team'
                }
            }]
    }
];

export const EVENT_BUILDER_DETAILS = {
    'id': 232341790,
    'name': 'cleared_name',
    'eventStatusCode': 'S',
    'displayOrder': 0,
    'siteChannels': 'P,p,Q,R,C,I,M,',
    'eventSortCode': 'MTCH',
    'startTime': 1615284000000,
    'rawIsOffCode': 'Y',
    'isStarted': 'true',
    'isResulted': 'true',
    'isFinished': 'true',
    'classId': 164,
    'typeId': 955,
    'sportId': '16',
    'liveServChannels': 'sEVENT0232341790,',
    'liveServChildrenChannels': 'SEVENT0232341790,',
    'categoryId': '16',
    'categoryCode': 'FOOTBALL',
    'categoryName': 'unpiped_cls',
    'categoryDisplayOrder': '-11010',
    'className': 'unpiped_cls',
    'classDisplayOrder': -32508,
    'classSortCode': 'FB',
    'typeName': 'unpiped_cls',
    'typeDisplayOrder': 0,
    'typeFlagCodes': 'GVA,IVA,PVA,',
    'mediaTypeCodes': 'VST,',
    'cashoutAvail': 'Y',
    'children': [
        {
            'eventPeriod': {
                'id': '4602998',
                'eventId': '232341790',
                'periodCode': 'ALL',
                'description': 'Total Duration of the game/match',
                'startTime': '2021-03-09T10:00:04Z',
                'children': [
                    {
                        'eventPeriodClockState': {
                            'id': '4101372',
                            'eventPeriodId': '4602998',
                            'offset': '0',
                            'lastUpdate': '2021-03-09T10:00:03Z',
                            'state': 'S'
                        }
                    },
                    {
                        'eventFact': {
                            'id': '11210884',
                            'eventId': '232341790',
                            'eventParticipantId': '943696',
                            'eventPeriodId': '4602998',
                            'fact': '2',
                            'factCode': 'YELLOW_CARDS',
                            'name': 'Num of yellow cards in a match/game'
                        }
                    },
                    {
                        'eventFact': {
                            'id': '11210883',
                            'eventId': '232341790',
                            'eventParticipantId': '943695',
                            'eventPeriodId': '4602998',
                            'fact': '4',
                            'factCode': 'YELLOW_CARDS',
                            'name': 'Num of yellow cards in a match/game'
                        }
                    },
                    {
                        'eventFact': {
                            'id': '11211050',
                            'eventId': '232341790',
                            'eventParticipantId': '943695',
                            'eventPeriodId': '4602998',
                            'fact': '9',
                            'factCode': 'CORNERS',
                            'name': 'Penalties in a match/game'
                        }
                    },
                    {
                        'eventFact': {
                            'id': '11210804',
                            'eventId': '232341790',
                            'eventParticipantId': '943696',
                            'eventPeriodId': '4602998',
                            'fact': '1',
                            'factCode': 'SCORE',
                            'name': 'Score of the match/game'
                        }
                    },
                    {
                        'eventFact': {
                            'id': '11210803',
                            'eventId': '232341790',
                            'eventParticipantId': '943695',
                            'eventPeriodId': '4602998',
                            'fact': '2',
                            'factCode': 'SCORE',
                            'name': 'Score of the match/game'
                        }
                    },
                    {
                        'eventFact': {
                            'id': '11211051',
                            'eventId': '232341790',
                            'eventParticipantId': '943696',
                            'eventPeriodId': '4602998',
                            'fact': '5',
                            'factCode': 'CORNERS',
                            'name': 'Penalties in a match/game'
                        }
                    },
                    {
                        'eventPeriod': {
                            'id': '4603496',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'SECOND_HALF',
                            'description': 'Second half of a match/game',
                            'startTime': '2021-03-09T11:04:05Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101401',
                                        'eventPeriodId': '4603496',
                                        'offset': '5716',
                                        'lastUpdate': '2021-03-09T11:54:20Z',
                                        'state': 'R'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11212573',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943695',
                                        'eventPeriodId': '4603496',
                                        'fact': '3',
                                        'factCode': 'YELLOW_CARDS',
                                        'name': 'Num of yellow cards in a match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11212574',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943696',
                                        'eventPeriodId': '4603496',
                                        'fact': '1',
                                        'factCode': 'YELLOW_CARDS',
                                        'name': 'Num of yellow cards in a match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11212588',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943695',
                                        'eventPeriodId': '4603496',
                                        'fact': '2',
                                        'factCode': 'SCORE',
                                        'name': 'Score of the match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11212589',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943696',
                                        'eventPeriodId': '4603496',
                                        'fact': '1',
                                        'factCode': 'SCORE',
                                        'name': 'Score of the match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11212208',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943695',
                                        'eventPeriodId': '4603496',
                                        'fact': '5',
                                        'factCode': 'CORNERS',
                                        'name': 'Penalties in a match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11212209',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943696',
                                        'eventPeriodId': '4603496',
                                        'fact': '5',
                                        'factCode': 'CORNERS',
                                        'name': 'Penalties in a match/game'
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344329',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'SCORE',
                                        'description': 'Scoring Incident',
                                        'relativeTime': '5069',
                                        'createDate': '2021-03-09T11:43:34Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344329',
                                                    'eventIncidentId': '41344329',
                                                    'text': 'SCORE_TYPE_G',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344255',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '2811',
                                        'createDate': '2021-03-09T11:05:56Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344255',
                                                    'eventIncidentId': '41344255',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344266',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '3227',
                                        'createDate': '2021-03-09T11:12:51Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344266',
                                                    'eventIncidentId': '41344266',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344332',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '5184',
                                        'createDate': '2021-03-09T11:45:29Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344332',
                                                    'eventIncidentId': '41344332',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344343',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'YELLOW_CARD',
                                        'description': 'Yellow Card',
                                        'relativeTime': '5520',
                                        'createDate': '2021-03-09T11:51:05Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344343',
                                                    'eventIncidentId': '41344343',
                                                    'text': 'STAT_TYPE_YC',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344256',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '2843',
                                        'createDate': '2021-03-09T11:06:28Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344256',
                                                    'eventIncidentId': '41344256',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344278',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'SCORE',
                                        'description': 'Scoring Incident',
                                        'relativeTime': '3587',
                                        'createDate': '2021-03-09T11:18:51Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344278',
                                                    'eventIncidentId': '41344278',
                                                    'text': 'SCORE_TYPE_G',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344344',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'SCORE',
                                        'description': 'Scoring Incident',
                                        'relativeTime': '5533',
                                        'createDate': '2021-03-09T11:51:17Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344344',
                                                    'eventIncidentId': '41344344',
                                                    'text': 'SCORE_TYPE_G',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344275',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'YELLOW_CARD',
                                        'description': 'Yellow Card',
                                        'relativeTime': '3542',
                                        'createDate': '2021-03-09T11:18:07Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344275',
                                                    'eventIncidentId': '41344275',
                                                    'text': 'STAT_TYPE_YC',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344304',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'YELLOW_CARD',
                                        'description': 'Yellow Card',
                                        'relativeTime': '4411',
                                        'createDate': '2021-03-09T11:32:35Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344304',
                                                    'eventIncidentId': '41344304',
                                                    'text': 'STAT_TYPE_YC',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344326',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '5000',
                                        'createDate': '2021-03-09T11:42:25Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344326',
                                                    'eventIncidentId': '41344326',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344337',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'YELLOW_CARD',
                                        'description': 'Yellow Card',
                                        'relativeTime': '5304',
                                        'createDate': '2021-03-09T11:47:29Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344337',
                                                    'eventIncidentId': '41344337',
                                                    'text': 'STAT_TYPE_YC',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344269',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '3319',
                                        'createDate': '2021-03-09T11:14:23Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344269',
                                                    'eventIncidentId': '41344269',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344251',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '2726',
                                        'createDate': '2021-03-09T11:04:31Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344251',
                                                    'eventIncidentId': '41344251',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344284',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '3944',
                                        'createDate': '2021-03-09T11:24:49Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344284',
                                                    'eventIncidentId': '41344284',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344282',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '3829',
                                        'createDate': '2021-03-09T11:22:54Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344282',
                                                    'eventIncidentId': '41344282',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344283',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '3874',
                                        'createDate': '2021-03-09T11:23:39Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344283',
                                                    'eventIncidentId': '41344283',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'eventPeriod': {
                            'id': '4603966',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'FINISH',
                            'description': 'Match finished',
                            'startTime': '2021-03-09T11:54:31Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101416',
                                        'eventPeriodId': '4603966',
                                        'offset': '5725',
                                        'lastUpdate': '2021-03-09T12:04:26Z',
                                        'state': 'S'
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344365',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603966',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'MATCH_FINISHED',
                                        'description': 'Match finished',
                                        'relativeTime': '5725',
                                        'createDate': '2021-03-09T12:04:26Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344365',
                                                    'eventIncidentId': '41344365',
                                                    'text': 'STAT_TYPE_FIN',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344346',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603966',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'MATCH_FINISHED',
                                        'description': 'Match finished',
                                        'relativeTime': '5725',
                                        'createDate': '2021-03-09T11:54:30Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344346',
                                                    'eventIncidentId': '41344346',
                                                    'text': 'STAT_TYPE_FIN',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'eventPeriod': {
                            'id': '4602999',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'FIRST_HALF',
                            'description': 'First half of a match/game',
                            'startTime': '2021-03-09T10:00:04Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101373',
                                        'eventPeriodId': '4602999',
                                        'offset': '2856',
                                        'lastUpdate': '2021-03-09T10:47:40Z',
                                        'state': 'S'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11210882',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943696',
                                        'eventPeriodId': '4602999',
                                        'fact': '1',
                                        'factCode': 'YELLOW_CARDS',
                                        'name': 'Num of yellow cards in a match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11210881',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943695',
                                        'eventPeriodId': '4602999',
                                        'fact': '1',
                                        'factCode': 'YELLOW_CARDS',
                                        'name': 'Num of yellow cards in a match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11211049',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943696',
                                        'eventPeriodId': '4602999',
                                        'fact': '0',
                                        'factCode': 'CORNERS',
                                        'name': 'Penalties in a match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11211048',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943695',
                                        'eventPeriodId': '4602999',
                                        'fact': '4',
                                        'factCode': 'CORNERS',
                                        'name': 'Penalties in a match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11210802',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943696',
                                        'eventPeriodId': '4602999',
                                        'fact': '0',
                                        'factCode': 'SCORE',
                                        'name': 'Score of the match/game'
                                    }
                                },
                                {
                                    'eventFact': {
                                        'id': '11210801',
                                        'eventId': '232341790',
                                        'eventParticipantId': '943695',
                                        'eventPeriodId': '4602999',
                                        'fact': '0',
                                        'factCode': 'SCORE',
                                        'name': 'Score of the match/game'
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344212',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4602999',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'YELLOW_CARD',
                                        'description': 'Yellow Card',
                                        'relativeTime': '2367',
                                        'createDate': '2021-03-09T10:39:31Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344212',
                                                    'eventIncidentId': '41344212',
                                                    'text': 'STAT_TYPE_YC',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344165',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4602999',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'YELLOW_CARD',
                                        'description': 'Yellow Card',
                                        'relativeTime': '268',
                                        'createDate': '2021-03-09T10:04:33Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344165',
                                                    'eventIncidentId': '41344165',
                                                    'text': 'STAT_TYPE_YC',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344158',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4602999',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'SCORE',
                                        'description': 'Scoring Incident',
                                        'relativeTime': '0',
                                        'createDate': '2021-03-09T10:00:03Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344158',
                                                    'eventIncidentId': '41344158',
                                                    'text': 'SCORE_TYPE_G',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344159',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4602999',
                                        'eventParticipantId': '943696',
                                        'incidentCode': 'SCORE',
                                        'description': 'Scoring Incident',
                                        'relativeTime': '0',
                                        'createDate': '2021-03-09T10:00:03Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344159',
                                                    'eventIncidentId': '41344159',
                                                    'text': 'SCORE_TYPE_G',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344192',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4602999',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '1269',
                                        'createDate': '2021-03-09T10:21:12Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344192',
                                                    'eventIncidentId': '41344192',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344174',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4602999',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '642',
                                        'createDate': '2021-03-09T10:10:46Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344174',
                                                    'eventIncidentId': '41344174',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344186',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4602999',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '976',
                                        'createDate': '2021-03-09T10:16:20Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344186',
                                                    'eventIncidentId': '41344186',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344172',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4602999',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '597',
                                        'createDate': '2021-03-09T10:10:01Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344172',
                                                    'eventIncidentId': '41344172',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'eventPeriod': {
                            'id': '4603357',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'HALF_TIME',
                            'description': 'Half time in a match/game',
                            'startTime': '2021-03-09T10:48:23Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101390',
                                        'eventPeriodId': '4603357',
                                        'offset': '2898',
                                        'lastUpdate': '2021-03-09T10:48:23Z',
                                        'state': 'S'
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            'eventParticipant': {
                'id': '943696',
                'eventId': '232341790',
                'name': 'Gangwon',
                'type': 'T',
                'roleCode': 'AWAY',
                'role': 'Away Team'
            }
        },
        {
            'eventParticipant': {
                'id': '943695',
                'eventId': '232341790',
                'name': 'Jeonbuk Hyundai Motors',
                'type': 'T',
                'roleCode': 'HOME',
                'role': 'Home Team'
            }
        }
    ],
    'localTime': '-new_name',
    'originalName': 'Jeonbuk Hyundai Motors v Gangwon',
    'isUS': false,
    'markets': [],
    'correctedDay': 'lorem',
    'eventIsLive': true,
    'liveEventOrder': 0
};

export const CONTEST_MOCK = {
    'id': '6040e25bd6e2da40b3fe9252',
    'generatedId': null,
    'name': 'WWWW',
    'icon': null,
    'startDate': '2021-03-04T13:36:15.366Z',
    'event': '232300717',
    'entryStake': '6',
    'isFreeBetsAllowed': true,
    'description': null,
    'blurb': null,
    'entryConfirmationText': null,
    'nextContestId': '345',
    'display': true,
    'brand': 'ladbrokes',
    'prizePool': {
        'cash': '24',
        'firstPlace': '10320',
        'freeBets': 23,
        'vouchers': '20',
        'summary': '12345',
        'tickets': '20',
        'totalPrizes': '234'
    },
    'contestPrizes': null,
    'sponsorText': 'Sponsored By',
    'sponsorLogo': null,
    'size': 1000,
    'teams': 5,
    'testAccount': true,
    'realAccount': false
};

export const EVENTS_DETAILS_COMMENTS = [{
    'id': 232341790,
    'name': 'Jeonbuk Hyundai Motors v Gangwon',
    'eventStatusCode': 'S',
    'displayOrder': '0',
    'siteChannels': 'P,p,Q,R,C,I,M,',
    'eventSortCode': 'MTCH',
    'startTime': '2021-03-09T10:00:00Z',
    'rawIsOffCode': 'Y',
    'isStarted': 'true',
    'isResulted': 'true',
    'isFinished': 'true',
    'classId': '164',
    'typeId': '955',
    'sportId': '16',
    'liveServChannels': 'sEVENT0232341790,',
    'liveServChildrenChannels': 'SEVENT0232341790,',
    'categoryId': '16',
    'categoryCode': 'FOOTBALL',
    'categoryName': 'Football',
    'categoryDisplayOrder': '-11010',
    'className': 'South Korean',
    'classDisplayOrder': '-32508',
    'classSortCode': 'FB',
    'typeName': 'South Korean K-League',
    'typeDisplayOrder': '0',
    'typeFlagCodes': 'GVA,IVA,PVA,',
    'mediaTypeCodes': 'VST,',
    'cashoutAvail': 'Y',
    'clock': {
        'ev_id': '23',
        'matchTime': 'HT'
    },
    'comments': {
        'teams': {
            'home': { 'score': '1' }, 'away': { 'score': '2' }
        }
    },
    'children': [
        {
            'eventPeriod': {
                'id': '4602998',
                'eventId': '232341790',
                'periodCode': 'ALL',
                'description': 'Total Duration of the game/match',
                'startTime': '2021-03-09T10:00:04Z',
                'children': [
                    {
                        'eventPeriod': {
                            'id': '4603496',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'SECOND_HALF',
                            'description': 'Second half of a match/game',
                            'startTime': '2021-03-09T11:04:05Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101401',
                                        'eventPeriodId': '4603496',
                                        'offset': '5716',
                                        'lastUpdate': '2021-03-09T11:54:20Z',
                                        'state': 'R'
                                    }
                                },
                                {
                                    'eventIncident': {
                                        'id': '41344283',
                                        'eventId': '232341790',
                                        'eventPeriodId': '4603496',
                                        'eventParticipantId': '943695',
                                        'incidentCode': 'CORNER',
                                        'description': 'Corner Kick',
                                        'relativeTime': '3874',
                                        'createDate': '2021-03-09T11:23:39Z',
                                        'children': [
                                            {
                                                'eventIncidentComment': {
                                                    'id': '41344283',
                                                    'eventIncidentId': '41344283',
                                                    'text': 'STAT_TYPE_CNR',
                                                    'lang': 'en'
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'eventPeriod': {
                            'id': '4603357',
                            'eventId': '232341790',
                            'parentEventPeriodId': '4602998',
                            'periodCode': 'HALF_TIME',
                            'description': 'Half time in a match/game',
                            'startTime': '2021-03-09T10:48:23Z',
                            'children': [
                                {
                                    'eventPeriodClockState': {
                                        'id': '4101390',
                                        'eventPeriodId': '4603357',
                                        'offset': '2898',
                                        'lastUpdate': '2021-03-09T10:48:23Z',
                                        'state': 'S'
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            'eventParticipant': {
                'id': '943696',
                'eventId': '232341790',
                'name': 'Gangwon',
                'type': 'T',
                'roleCode': 'AWAY',
                'role': 'Away Team'
            }
        },
        {
            'eventParticipant': {
                'id': '943695',
                'eventId': '232341790',
                'name': 'Jeonbuk Hyundai Motors',
                'type': 'T',
                'roleCode': 'HOME',
                'role': 'Home Team'
            }
        }]
},
{
    'id': 232341791,
    'name': 'Jeonbuk Hyundai Motors v Gangwon',
    'eventStatusCode': 'S',
    'displayOrder': '0',
    'siteChannels': 'P,p,Q,R,C,I,M,',
    'eventSortCode': 'MTCH',
    'startTime': '2021-03-09T10:00:00Z',
    'rawIsOffCode': 'Y',
    'isStarted': 'true',
    'isResulted': 'true',
    'isFinished': 'true',
    'classId': '164',
    'typeId': '955',
    'sportId': '16',
    'liveServChannels': 'sEVENT0232341790,',
    'liveServChildrenChannels': 'SEVENT0232341790,',
    'categoryId': '16',
    'categoryCode': 'FOOTBALL',
    'categoryName': 'Football',
    'categoryDisplayOrder': '-11010',
    'className': 'South Korean',
    'classDisplayOrder': '-32508',
    'classSortCode': 'FB',
    'typeName': 'South Korean K-League',
    'typeDisplayOrder': '0',
    'typeFlagCodes': 'GVA,IVA,PVA,',
    'mediaTypeCodes': 'VST,',
    'cashoutAvail': 'Y',
    'children': [
        {
            'eventPeriod': {
                'id': '4602998',
                'eventId': '232341790',
                'periodCode': 'ALL',
                'description': 'Total Duration of the game/match',
                'startTime': '2021-03-09T10:00:04Z',
                'children': [
                    {
                        'eventPeriodClockState': {
                            'id': '4101372',
                            'eventPeriodId': '4602998',
                            'offset': '0',
                            'lastUpdate': '2021-03-09T10:00:03Z',
                            'state': 'S'
                        }
                    },
                    {
                        'eventFact': {
                            'id': '11211051',
                            'eventId': '232341790',
                            'eventParticipantId': '943696',
                            'eventPeriodId': '4602998',
                            'fact': '5',
                            'factCode': 'CORNERS',
                            'name': 'Penalties in a match/game'
                        }
                    }
                ]
            }
        }]
}
];

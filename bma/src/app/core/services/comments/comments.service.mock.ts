export const footballCommentaryInitialExtraTime = [
  {
    'eventPeriod': {
      'id': '64840',
      'eventId': '623788',
      'periodCode': 'ALL',
      'description': 'Total Duration of the game/match',
      'startTime': '2019-09-17T12:59:53Z',
      'children': [
        {
          'eventPeriodClockState': {
            'id': '64709',
            'eventPeriodId': '64840',
            'offset': '0',
            'lastUpdate': '2019-09-17T12:59:52Z',
            'state': 'S'
          }
        },
        {
          'eventFact': {
            'id': '81063',
            'eventId': '623788',
            'eventParticipantId': '43277',
            'eventPeriodId': '64840',
            'fact': '2',
            'factCode': 'SCORE',
            'name': 'Score of the match/game'
          }
        },
        {
          'eventFact': {
            'id': '81064',
            'eventId': '623788',
            'eventParticipantId': '43278',
            'eventPeriodId': '64840',
            'fact': '3',
            'factCode': 'SCORE',
            'name': 'Score of the match/game'
          }
        },
        {
          'eventPeriod': {
            'id': '64846',
            'eventId': '623788',
            'parentEventPeriodId': '64840',
            'periodCode': 'EXTRA_TIME_FIRST_HALF',
            'description': 'The first half of extra-time',
            'startTime': '2019-09-17T13:04:29Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64715',
                  'eventPeriodId': '64846',
                  'offset': '43',
                  'lastUpdate': '2019-09-17T13:05:18Z',
                  'state': 'S'
                }
              },
              {
                'eventFact': {
                  'id': '81072',
                  'eventId': '623788',
                  'eventParticipantId': '43278',
                  'eventPeriodId': '64846',
                  'fact': '0',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventFact': {
                  'id': '81071',
                  'eventId': '623788',
                  'eventParticipantId': '43277',
                  'eventPeriodId': '64846',
                  'fact': '1',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventIncident': {
                  'id': '295648',
                  'eventId': '623788',
                  'eventPeriodId': '64846',
                  'eventParticipantId': '43277',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '0',
                  'createDate': '2019-09-17T13:04:28Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295648',
                        'eventIncidentId': '295648',
                        'text': 'STAT_TYPE_PSTR',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295649',
                  'eventId': '623788',
                  'eventPeriodId': '64846',
                  'eventParticipantId': '43277',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '35',
                  'createDate': '2019-09-17T13:05:10Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295649',
                        'eventIncidentId': '295649',
                        'text': 'SCORE_TYPE_G',
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
            'id': '64845',
            'eventId': '623788',
            'parentEventPeriodId': '64840',
            'periodCode': 'SECOND_HALF',
            'description': 'Second half of a match/game',
            'startTime': '2019-09-17T13:03:37Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64714',
                  'eventPeriodId': '64845',
                  'offset': '2745',
                  'lastUpdate': '2019-09-17T13:04:22Z',
                  'state': 'S'
                }
              },
              {
                'eventFact': {
                  'id': '81069',
                  'eventId': '623788',
                  'eventParticipantId': '43277',
                  'eventPeriodId': '64845',
                  'fact': '1',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventFact': {
                  'id': '81070',
                  'eventId': '623788',
                  'eventParticipantId': '43278',
                  'eventPeriodId': '64845',
                  'fact': '3',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventIncident': {
                  'id': '295643',
                  'eventId': '623788',
                  'eventPeriodId': '64845',
                  'eventParticipantId': '43277',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '2700',
                  'createDate': '2019-09-17T13:03:36Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295643',
                        'eventIncidentId': '295643',
                        'text': 'STAT_TYPE_PSTR',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295644',
                  'eventId': '623788',
                  'eventPeriodId': '64845',
                  'eventParticipantId': '43277',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2705',
                  'createDate': '2019-09-17T13:03:41Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295644',
                        'eventIncidentId': '295644',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295645',
                  'eventId': '623788',
                  'eventPeriodId': '64845',
                  'eventParticipantId': '43278',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2709',
                  'createDate': '2019-09-17T13:03:44Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295645',
                        'eventIncidentId': '295645',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295646',
                  'eventId': '623788',
                  'eventPeriodId': '64845',
                  'eventParticipantId': '43278',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2712',
                  'createDate': '2019-09-17T13:03:48Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295646',
                        'eventIncidentId': '295646',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295647',
                  'eventId': '623788',
                  'eventPeriodId': '64845',
                  'eventParticipantId': '43278',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2719',
                  'createDate': '2019-09-17T13:03:55Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295647',
                        'eventIncidentId': '295647',
                        'text': 'SCORE_TYPE_G',
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
            'id': '64848',
            'eventId': '623788',
            'parentEventPeriodId': '64840',
            'periodCode': 'EXTRA_TIME_SECOND_HALF',
            'description': 'The second half of extra-time',
            'startTime': '2019-09-17T13:05:32Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64717',
                  'eventPeriodId': '64848',
                  'offset': '56784',
                  'lastUpdate': '2019-09-18T04:37:32Z',
                  'state': 'S'
                }
              },
              {
                'eventFact': {
                  'id': '81074',
                  'eventId': '623788',
                  'eventParticipantId': '43278',
                  'eventPeriodId': '64848',
                  'fact': '3',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventFact': {
                  'id': '81073',
                  'eventId': '623788',
                  'eventParticipantId': '43277',
                  'eventPeriodId': '64848',
                  'fact': '2',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventIncident': {
                  'id': '295653',
                  'eventId': '623788',
                  'eventPeriodId': '64848',
                  'eventParticipantId': '43277',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '937',
                  'createDate': '2019-09-17T13:06:10Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295653',
                        'eventIncidentId': '295653',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295654',
                  'eventId': '623788',
                  'eventPeriodId': '64848',
                  'eventParticipantId': '43278',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '948',
                  'createDate': '2019-09-17T13:06:20Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295654',
                        'eventIncidentId': '295654',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295655',
                  'eventId': '623788',
                  'eventPeriodId': '64848',
                  'eventParticipantId': '43278',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '952',
                  'createDate': '2019-09-17T13:06:24Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295655',
                        'eventIncidentId': '295655',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295660',
                  'eventId': '623788',
                  'eventPeriodId': '64848',
                  'eventParticipantId': '43278',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '1800',
                  'createDate': '2019-09-17T13:53:49Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295660',
                        'eventIncidentId': '295660',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295651',
                  'eventId': '623788',
                  'eventPeriodId': '64848',
                  'eventParticipantId': '43277',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '900',
                  'createDate': '2019-09-17T13:05:32Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295651',
                        'eventIncidentId': '295651',
                        'text': 'STAT_TYPE_PSTR',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295652',
                  'eventId': '623788',
                  'eventPeriodId': '64848',
                  'eventParticipantId': '43277',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '933',
                  'createDate': '2019-09-17T13:06:06Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295652',
                        'eventIncidentId': '295652',
                        'text': 'SCORE_TYPE_G',
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
            'id': '64847',
            'eventId': '623788',
            'parentEventPeriodId': '64840',
            'periodCode': 'EXTRA_TIME_HALF_TIME',
            'description': 'Half-time of extra-time',
            'startTime': '2019-09-17T13:05:24Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64716',
                  'eventPeriodId': '64847',
                  'offset': '900',
                  'lastUpdate': '2019-09-17T13:05:23Z',
                  'state': 'R'
                }
              },
              {
                'eventIncident': {
                  'id': '295650',
                  'eventId': '623788',
                  'eventPeriodId': '64847',
                  'eventParticipantId': '43277',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '900',
                  'createDate': '2019-09-17T13:05:23Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295650',
                        'eventIncidentId': '295650',
                        'text': 'STAT_TYPE_PSTR',
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
            'id': '64841',
            'eventId': '623788',
            'parentEventPeriodId': '64840',
            'periodCode': 'FIRST_HALF',
            'description': 'First half of a match/game',
            'startTime': '2019-09-17T12:59:53Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64710',
                  'eventPeriodId': '64841',
                  'offset': '174',
                  'lastUpdate': '2019-09-17T13:02:46Z',
                  'state': 'S'
                }
              },
              {
                'eventFact': {
                  'id': '81061',
                  'eventId': '623788',
                  'eventParticipantId': '43277',
                  'eventPeriodId': '64841',
                  'fact': '1',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventFact': {
                  'id': '81062',
                  'eventId': '623788',
                  'eventParticipantId': '43278',
                  'eventPeriodId': '64841',
                  'fact': '0',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventIncident': {
                  'id': '295642',
                  'eventId': '623788',
                  'eventPeriodId': '64841',
                  'eventParticipantId': '43277',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '188',
                  'createDate': '2019-09-17T13:03:04Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295642',
                        'eventIncidentId': '295642',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295632',
                  'eventId': '623788',
                  'eventPeriodId': '64841',
                  'eventParticipantId': '43277',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '0',
                  'createDate': '2019-09-17T12:59:52Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295632',
                        'eventIncidentId': '295632',
                        'text': 'STAT_TYPE_PSTR',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295633',
                  'eventId': '623788',
                  'eventPeriodId': '64841',
                  'eventParticipantId': '43277',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '0',
                  'createDate': '2019-09-17T12:59:53Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295633',
                        'eventIncidentId': '295633',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295634',
                  'eventId': '623788',
                  'eventPeriodId': '64841',
                  'eventParticipantId': '43278',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '0',
                  'createDate': '2019-09-17T12:59:53Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295634',
                        'eventIncidentId': '295634',
                        'text': 'SCORE_TYPE_G',
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
            'id': '64844',
            'eventId': '623788',
            'parentEventPeriodId': '64840',
            'periodCode': 'HALF_TIME',
            'description': 'Half time in a match/game',
            'startTime': '2019-09-17T13:03:18Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64713',
                  'eventPeriodId': '64844',
                  'offset': '2700',
                  'lastUpdate': '2019-09-17T13:03:23Z',
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
      'id': '43278',
      'eventId': '623788',
      'name': 'Meadow Men',
      'type': 'T',
      'roleCode': 'AWAY',
      'role': 'Away Team',
      'score': '3'
    }
  },
  {
    'eventParticipant': {
      'id': '43277',
      'eventId': '623788',
      'name': 'Atom Men',
      'type': 'T',
      'roleCode': 'HOME',
      'role': 'Home Team',
      'score': '2'
    }
  }
];

export const footballCommentaryInitialPenalties = [
  {
    'eventPeriod': {
      'id': '64819',
      'eventId': '621399',
      'periodCode': 'ALL',
      'description': 'Total Duration of the game/match',
      'startTime': '2019-09-16T14:01:13Z',
      'children': [
        {
          'eventPeriodClockState': {
            'id': '64688',
            'eventPeriodId': '64819',
            'offset': '0',
            'lastUpdate': '2019-09-16T14:01:13Z',
            'state': 'S'
          }
        },
        {
          'eventFact': {
            'id': '81027',
            'eventId': '621399',
            'eventParticipantId': '43271',
            'eventPeriodId': '64819',
            'fact': '2',
            'factCode': 'SCORE',
            'name': 'Score of the match/game'
          }
        },
        {
          'eventFact': {
            'id': '81028',
            'eventId': '621399',
            'eventParticipantId': '43272',
            'eventPeriodId': '64819',
            'fact': '2',
            'factCode': 'SCORE',
            'name': 'Score of the match/game'
          }
        },
        {
          'eventPeriod': {
            'id': '64823',
            'eventId': '621399',
            'parentEventPeriodId': '64819',
            'periodCode': 'EXTRA_TIME_FIRST_HALF',
            'description': 'The first half of extra-time',
            'startTime': '2019-09-16T14:04:11Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64692',
                  'eventPeriodId': '64823',
                  'offset': '80',
                  'lastUpdate': '2019-09-16T14:05:41Z',
                  'state': 'S'
                }
              },
              {
                'eventFact': {
                  'id': '81037',
                  'eventId': '621399',
                  'eventParticipantId': '43271',
                  'eventPeriodId': '64823',
                  'fact': '1',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventFact': {
                  'id': '81038',
                  'eventId': '621399',
                  'eventParticipantId': '43272',
                  'eventPeriodId': '64823',
                  'fact': '1',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventIncident': {
                  'id': '295556',
                  'eventId': '621399',
                  'eventPeriodId': '64823',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '0',
                  'createDate': '2019-09-16T14:04:11Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295556',
                        'eventIncidentId': '295556',
                        'text': 'STAT_TYPE_PSTR',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295560',
                  'eventId': '621399',
                  'eventPeriodId': '64823',
                  'eventParticipantId': '43272',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '31',
                  'createDate': '2019-09-16T14:04:52Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295560',
                        'eventIncidentId': '295560',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295559',
                  'eventId': '621399',
                  'eventPeriodId': '64823',
                  'eventParticipantId': '43271',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '26',
                  'createDate': '2019-09-16T14:04:46Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295559',
                        'eventIncidentId': '295559',
                        'text': 'SCORE_TYPE_G',
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
            'id': '64826',
            'eventId': '621399',
            'parentEventPeriodId': '64819',
            'periodCode': 'EXTRA_TIME_SECOND_HALF',
            'description': 'The second half of extra-time',
            'startTime': '2019-09-16T14:05:57Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64695',
                  'eventPeriodId': '64826',
                  'offset': '953',
                  'lastUpdate': '2019-09-16T14:06:54Z',
                  'state': 'S'
                }
              },
              {
                'eventIncident': {
                  'id': '295562',
                  'eventId': '621399',
                  'eventPeriodId': '64826',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '900',
                  'createDate': '2019-09-16T14:05:57Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295562',
                        'eventIncidentId': '295562',
                        'text': 'STAT_TYPE_PSTR',
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
            'id': '64825',
            'eventId': '621399',
            'parentEventPeriodId': '64819',
            'periodCode': 'EXTRA_TIME_HALF_TIME',
            'description': 'Half-time of extra-time',
            'startTime': '2019-09-16T14:05:51Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64694',
                  'eventPeriodId': '64825',
                  'offset': '900',
                  'lastUpdate': '2019-09-16T14:05:51Z',
                  'state': 'R'
                }
              },
              {
                'eventIncident': {
                  'id': '295561',
                  'eventId': '621399',
                  'eventPeriodId': '64825',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '900',
                  'createDate': '2019-09-16T14:05:51Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295561',
                        'eventIncidentId': '295561',
                        'text': 'STAT_TYPE_PSTR',
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
            'id': '64820',
            'eventId': '621399',
            'parentEventPeriodId': '64819',
            'periodCode': 'FIRST_HALF',
            'description': 'First half of a match/game',
            'startTime': '2019-09-16T14:01:13Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64689',
                  'eventPeriodId': '64820',
                  'offset': '103',
                  'lastUpdate': '2019-09-16T14:02:56Z',
                  'state': 'S'
                }
              },
              {
                'eventFact': {
                  'id': '81025',
                  'eventId': '621399',
                  'eventParticipantId': '43271',
                  'eventPeriodId': '64820',
                  'fact': '1',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventFact': {
                  'id': '81026',
                  'eventId': '621399',
                  'eventParticipantId': '43272',
                  'eventPeriodId': '64820',
                  'fact': '1',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventIncident': {
                  'id': '295550',
                  'eventId': '621399',
                  'eventPeriodId': '64820',
                  'eventParticipantId': '43272',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '0',
                  'createDate': '2019-09-16T14:01:13Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295550',
                        'eventIncidentId': '295550',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295551',
                  'eventId': '621399',
                  'eventPeriodId': '64820',
                  'eventParticipantId': '43271',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '106',
                  'createDate': '2019-09-16T14:03:02Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295551',
                        'eventIncidentId': '295551',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295552',
                  'eventId': '621399',
                  'eventPeriodId': '64820',
                  'eventParticipantId': '43272',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '115',
                  'createDate': '2019-09-16T14:03:11Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295552',
                        'eventIncidentId': '295552',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295548',
                  'eventId': '621399',
                  'eventPeriodId': '64820',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '0',
                  'createDate': '2019-09-16T14:01:13Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295548',
                        'eventIncidentId': '295548',
                        'text': 'STAT_TYPE_PSTR',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295549',
                  'eventId': '621399',
                  'eventPeriodId': '64820',
                  'eventParticipantId': '43271',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '0',
                  'createDate': '2019-09-16T14:01:13Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295549',
                        'eventIncidentId': '295549',
                        'text': 'SCORE_TYPE_G',
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
            'id': '64822',
            'eventId': '621399',
            'parentEventPeriodId': '64819',
            'periodCode': 'SECOND_HALF',
            'description': 'Second half of a match/game',
            'startTime': '2019-09-16T14:03:35Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64691',
                  'eventPeriodId': '64822',
                  'offset': '2731',
                  'lastUpdate': '2019-09-16T14:04:07Z',
                  'state': 'S'
                }
              },
              {
                'eventFact': {
                  'id': '81030',
                  'eventId': '621399',
                  'eventParticipantId': '43272',
                  'eventPeriodId': '64822',
                  'fact': '1',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventFact': {
                  'id': '81029',
                  'eventId': '621399',
                  'eventParticipantId': '43271',
                  'eventPeriodId': '64822',
                  'fact': '1',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventIncident': {
                  'id': '295554',
                  'eventId': '621399',
                  'eventPeriodId': '64822',
                  'eventParticipantId': '43271',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2707',
                  'createDate': '2019-09-16T14:03:42Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295554',
                        'eventIncidentId': '295554',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295555',
                  'eventId': '621399',
                  'eventPeriodId': '64822',
                  'eventParticipantId': '43272',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2712',
                  'createDate': '2019-09-16T14:03:48Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295555',
                        'eventIncidentId': '295555',
                        'text': 'SCORE_TYPE_G',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295553',
                  'eventId': '621399',
                  'eventPeriodId': '64822',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '2700',
                  'createDate': '2019-09-16T14:03:35Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295553',
                        'eventIncidentId': '295553',
                        'text': 'STAT_TYPE_PSTR',
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
            'id': '64821',
            'eventId': '621399',
            'parentEventPeriodId': '64819',
            'periodCode': 'HALF_TIME',
            'description': 'Half time in a match/game',
            'startTime': '2019-09-16T14:03:19Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64690',
                  'eventPeriodId': '64821',
                  'offset': '122',
                  'lastUpdate': '2019-09-16T14:03:19Z',
                  'state': 'S'
                }
              }
            ]
          }
        },
        {
          'eventPeriod': {
            'id': '64827',
            'eventId': '621399',
            'parentEventPeriodId': '64819',
            'periodCode': 'PENALTIES',
            'description': 'Penalty in a match',
            'startTime': '2019-09-16T14:06:57Z',
            'children': [
              {
                'eventPeriodClockState': {
                  'id': '64696',
                  'eventPeriodId': '64827',
                  'offset': '2901',
                  'lastUpdate': '2019-09-17T10:15:21Z',
                  'state': 'S'
                }
              },
              {
                'eventFact': {
                  'id': '81039',
                  'eventId': '621399',
                  'eventParticipantId': '43271',
                  'eventPeriodId': '64827',
                  'fact': '5',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventFact': {
                  'id': '81040',
                  'eventId': '621399',
                  'eventParticipantId': '43272',
                  'eventPeriodId': '64827',
                  'fact': '5',
                  'factCode': 'SCORE',
                  'name': 'Score of the match/game'
                }
              },
              {
                'eventIncident': {
                  'id': '295580',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '2127',
                  'createDate': '2019-09-16T14:12:36Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295580',
                        'eventIncidentId': '295580',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295570',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '1936',
                  'createDate': '2019-09-16T14:09:17Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295570',
                        'eventIncidentId': '295570',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295581',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2131',
                  'createDate': '2019-09-16T14:12:41Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295581',
                        'eventIncidentId': '295581',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295571',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '1941',
                  'createDate': '2019-09-16T14:09:22Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295571',
                        'eventIncidentId': '295571',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295582',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '2138',
                  'createDate': '2019-09-16T14:12:48Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295582',
                        'eventIncidentId': '295582',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295565',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PERIOD_START',
                  'description': 'Period start',
                  'relativeTime': '1800',
                  'createDate': '2019-09-16T14:06:57Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295565',
                        'eventIncidentId': '295565',
                        'text': 'STAT_TYPE_PSTR',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295566',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '1831',
                  'createDate': '2019-09-16T14:07:29Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295566',
                        'eventIncidentId': '295566',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295567',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '1838',
                  'createDate': '2019-09-16T14:07:36Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295567',
                        'eventIncidentId': '295567',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295611',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '2152',
                  'createDate': '2019-09-17T06:15:03Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295611',
                        'eventIncidentId': '295611',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295612',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2164',
                  'createDate': '2019-09-17T06:15:15Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295612',
                        'eventIncidentId': '295612',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295572',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '1968',
                  'createDate': '2019-09-16T14:09:49Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295572',
                        'eventIncidentId': '295572',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295583',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2142',
                  'createDate': '2019-09-16T14:12:51Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295583',
                        'eventIncidentId': '295583',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295573',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '1972',
                  'createDate': '2019-09-16T14:09:53Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295573',
                        'eventIncidentId': '295573',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295574',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '1982',
                  'createDate': '2019-09-16T14:10:04Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295574',
                        'eventIncidentId': '295574',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295575',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '1986',
                  'createDate': '2019-09-16T14:10:07Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295575',
                        'eventIncidentId': '295575',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295613',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '2652',
                  'createDate': '2019-09-17T06:23:29Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295613',
                        'eventIncidentId': '295613',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295624',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '2780',
                  'createDate': '2019-09-17T09:30:17Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295624',
                        'eventIncidentId': '295624',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295614',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2656',
                  'createDate': '2019-09-17T06:23:33Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295614',
                        'eventIncidentId': '295614',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295625',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43271',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2784',
                  'createDate': '2019-09-17T09:30:22Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295625',
                        'eventIncidentId': '295625',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295626',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'PENALTY_AWARDED',
                  'description': 'Penalty awarded',
                  'relativeTime': '2898',
                  'createDate': '2019-09-17T09:32:17Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295626',
                        'eventIncidentId': '295626',
                        'text': 'STAT_TYPE_PA',
                        'lang': 'en'
                      }
                    }
                  ]
                }
              },
              {
                'eventIncident': {
                  'id': '295627',
                  'eventId': '621399',
                  'eventPeriodId': '64827',
                  'eventParticipantId': '43272',
                  'incidentCode': 'SCORE',
                  'description': 'Scoring Incident',
                  'relativeTime': '2901',
                  'createDate': '2019-09-17T09:32:20Z',
                  'children': [
                    {
                      'eventIncidentComment': {
                        'id': '295627',
                        'eventIncidentId': '295627',
                        'text': 'SCORE_TYPE_PS',
                        'lang': 'en'
                      }
                    }
                  ]
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
      'id': '43271',
      'eventId': '621399',
      'name': 'Hearts',
      'type': 'T',
      'roleCode': 'HOME',
      'role': 'Home Team',
      'score': '2'
    }
  },
  {
    'eventParticipant': {
      'id': '43272',
      'eventId': '621399',
      'name': 'Paris FC',
      'type': 'T',
      'roleCode': 'AWAY',
      'role': 'Away Team',
      'score': '2'
    }
  }
];

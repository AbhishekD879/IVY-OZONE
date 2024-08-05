import { CommentsService } from './comments.service';
import { ITypedScoreData } from '@core/services/scoreParser/models/score-data.model';
import {
  footballCommentaryInitialExtraTime,
  footballCommentaryInitialPenalties
} from './comments.service.mock';

describe('CommentsService', () => {
  let service: CommentsService;
  let timeSync;
  let liveEventClock;
  let comments;

  beforeEach(() => {
    comments = [
      {
        eventParticipant: {
          roleCode: 'home',
          id: '12'
        },
      },
      {
        eventPeriod: {
          children: [
            {
              eventPeriod: {
                children: [
                  {
                    eventPeriodClockState: 'state',
                    eventPeriod: {
                      children: [
                        {
                          eventFact: {
                            factCode: 'SCORE',
                            fact: '78',
                            eventParticipantId: '13'
                          }
                        }
                      ],
                      periodCode: 'GAME',
                      periodIndex: 300
                    }
                  }
                ],
                periodCode: 'SET',
                periodIndex: 300
              },
              eventFact: {
                factCode: 'SCORE',
                fact: '77',
                eventParticipantId: '12'
              }
            }
          ]
        }
      }
    ];
    timeSync = {
      getTimeDelta: jasmine.createSpy()
    };
    liveEventClock = {
      create: jasmine.createSpy().and.returnValue({})
    };
    spyOn(console, 'warn');
    service = new CommentsService(timeSync, liveEventClock);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('reset comments', () => {
    it('should reset teams scores', () => {
      const parsedComments = {
        teams: {
          away: {
            score: 10
          },
          home: {
            score: 20
          }
        }
      };

      service.resetTeamsScores(parsedComments);
      expect(parsedComments.teams.away.score).toEqual(0);
      expect(parsedComments.teams.home.score).toEqual(0);
    });

    it('should not reset teams scores if there no game', () => {
      const parsedComments = {
        teams: {
          away: undefined,
          home: undefined
        }
      };

      service.resetTeamsScores(parsedComments);
      expect(parsedComments.teams.away).not.toEqual(jasmine.objectContaining({ score: 0 }));
      expect(parsedComments.teams.home).not.toEqual(jasmine.objectContaining({ score: 0 }));
    });
  });

  describe('badminton data', () => {
    let parsedComments;
    let gameData;

    beforeEach(() => {
      parsedComments = {
        teams: {
          away: {
            score: undefined,
            currentPoints: undefined
          },
          home: {
            score: undefined,
            currentPoints: undefined
          }
        }
      };
      gameData = {
        ALL: [
          { value: 30 },
          { value: 20 }
        ],
        SUBPERIOD: [
          { value: 1 },
          { value: 2 }
        ]
      };
    });

    it('should extend badminton data', () => {
      service.badmintonUpdateExtend(parsedComments, gameData);
      expect(parsedComments.teams.home.score).toEqual(30);
      expect(parsedComments.teams.away.score).toEqual(20);
      expect(parsedComments.teams.home.currentPoints).toEqual(1);
      expect(parsedComments.teams.away.currentPoints).toEqual(2);
    });

    it('should extend badminton data if CURRENT = []', () => {
      gameData = {
        ALL: [
          { value: 30 },
          { value: 20 }
        ],
        CURRENT: [],
        SUBPERIOD: [
          { value: 1 },
          { value: 2 }
        ]
      };
      service.badmintonUpdateExtend(parsedComments, gameData);
      expect(parsedComments.teams.home.score).toEqual(30);
      expect(parsedComments.teams.away.score).toEqual(20);
      expect(parsedComments.teams.home.currentPoints).toEqual(1);
      expect(parsedComments.teams.away.currentPoints).toEqual(2);
    });

    it('should extend badminton data if it has CURRENT points', () => {
      gameData = {
        ALL: [
          { value: 30 },
          { value: 20 },
        ],
        CURRENT: [
          { value: 3, is_active: 'true' },
          { value: 4, is_active: 'false' },
        ],
        SUBPERIOD: [
          { value: 1 },
          { value: 2 }
        ]
      };
      service.badmintonUpdateExtend(parsedComments, gameData);
      expect(parsedComments.teams.home.score).toEqual(30);
      expect(parsedComments.teams.away.score).toEqual(20);
      expect(parsedComments.teams.home.currentPoints).toEqual(3);
      expect(parsedComments.teams.away.currentPoints).toEqual(4);
      expect(parsedComments.teams.home.isActive).toBeTruthy();
      expect(parsedComments.teams.away.isActive).toBeFalsy();
    });

    it('should not extend badminton data if one game missing', () => {
      parsedComments.teams.home = undefined;
      service.badmintonUpdateExtend(parsedComments, gameData);
      expect(parsedComments.teams.away.score).toBeUndefined();
      expect(parsedComments.teams.away.currentPoints).toBeUndefined();
    });

    it('should not set currentPoints if CURRENT and SUBPERIOD are missed', () => {
      gameData = {
        ALL: [
          { value: 30 },
          { value: 20 },
        ]
      };
      service.badmintonUpdateExtend(parsedComments, gameData);
      expect(parsedComments.teams.home.currentPoints).toBeUndefined();
      expect(parsedComments.teams.away.currentPoints).toBeUndefined();
    });
  });

  describe('badminton data player_1 / player_2 format', () => {
    let parsedComments;
    let gameData;

    beforeEach(() => {
      parsedComments = {
        teams: {
          player_1: {
            score: undefined,
            currentPoints: undefined
          },
          player_2: {
            score: undefined,
            currentPoints: undefined
          }
        }
      };
      gameData = {
        ALL: [
          { value: 30 },
          { value: 20 }
        ],
        SUBPERIOD: [
          { value: 1 },
          { value: 2 }
        ]
      };
    });

    it('should extend badminton data', () => {
      service.badmintonUpdateExtend(parsedComments, gameData);
      expect(parsedComments.teams.player_1.score).toEqual(30);
      expect(parsedComments.teams.player_2.score).toEqual(20);
      expect(parsedComments.teams.player_1.currentPoints).toEqual(1);
      expect(parsedComments.teams.player_2.currentPoints).toEqual(2);
    });

    it('should extend badminton data if it has CURRENT points', () => {
      gameData = {
        ALL: [
          { value: 30 },
          { value: 20 },
        ],
        CURRENT: [
          { value: 3, is_active: 'true' },
          { value: 4, is_active: 'false' },
        ],
        SUBPERIOD: [
          { value: 1 },
          { value: 2 }
        ]
      };
      service.badmintonUpdateExtend(parsedComments, gameData);
      expect(parsedComments.teams.player_1.score).toEqual(30);
      expect(parsedComments.teams.player_2.score).toEqual(20);
      expect(parsedComments.teams.player_1.currentPoints).toEqual(3);
      expect(parsedComments.teams.player_2.currentPoints).toEqual(4);
      expect(parsedComments.teams.player_1.isActive).toBeTruthy();
      expect(parsedComments.teams.player_2.isActive).toBeFalsy();
    });

    it('should not set currentPoints if CURRENT and SUBPERIOD are missed', () => {
      gameData = {
        ALL: [
          { value: 30 },
          { value: 20 },
        ]
      };
      service.badmintonUpdateExtend(parsedComments, gameData);
      expect(parsedComments.teams.player_1.currentPoints).toBeUndefined();
      expect(parsedComments.teams.player_2.currentPoints).toBeUndefined();
    });
  });

  it('should update comments data for football and extend original event', () => {
    const parsedComments = {
      teams: {
        away: {
          score: 10
        },
        home: {
          score: 20
        }
      }
    };

    const gameData = {
      SUBPERIOD: [
        {
          period_code: 'PENALTIES',
          value: 20,
          role_code: 'home'
        },
        {
          period_code: 'test',
          value: 30,
          role_code: 'away'
        }
      ]
    };

    service.footballUpdateExtend(parsedComments, gameData);
    expect(parsedComments.teams.home['penaltyScore']).toEqual(20);
  });

  it('should parse initial comments', () => {
    expect(JSON.stringify(service.gameInitParse(comments))).toBe(JSON.stringify({
      teams: {
        [comments[0].eventParticipant.roleCode]: comments[0].eventParticipant
      }
    }));
  });

  it('should parse initial comments clock data for football', () => {
    expect(JSON.stringify(service.footballClockInitParse(
      comments,
      '12',
      '12',
      '12'
    ))).toBe(JSON.stringify({ clock: {} }));
  });

  it('should get clock data', () => {
    const period = {
      eventId: '12',
      periodCode: '10',
      children: [
        {
          eventPeriodClockState: {
            lastUpdate: 'test'
          }
        }
      ]
    };

    expect(service.getCLockData(period)).toEqual(jasmine.objectContaining(
      {
        ev_id: 12,
        period_code: '10',
        last_update: 'test'
      }
    ));
  });

  it('should extend game data', () => {
    const parsedComments = {
      teams: {
        footballRoleCode: {
          code: 'SCORE',
        },
        away: {
          eventId: '12',
          score: undefined
        }
      }
    };

    const gameData = {
      ALL: [{
        code: 'SCORE',
        role_code: 'away',
        value: 30,
        ev_id: '12'
      }]
    };
    service.gameUpdateExtend(parsedComments, gameData);
    expect(parsedComments.teams.away.score).toEqual(30);
  });

  it('should parse tennis data', () => {
    expect(service.tennisInitParse(comments).teams[comments[0].eventParticipant.roleCode]).toEqual(
      jasmine.objectContaining({ id: '12' })
    );
    expect(service.tennisInitParse(comments).runningSetIndex).toEqual(300);
    expect(service.tennisInitParse(comments).runningGameScores).toEqual(jasmine.objectContaining({ '13': '78' }));
  });

  it('should initial comments data for badminton events', () => {
    const parsedComments = {
      setsScores: {
        '300': {
          '20': '40',
          '10': '15'
        }
      },
      runningSetIndex: 300,
      teams: {
        player_1: {
          id: '10',
          score: 20,
          name: 'player_1'
        },
        player_2: {
          id: '20',
          score: 5,
          name: 'player_2'
        }
      }
    };

    expect(service.badmintonMSInitParse(parsedComments).home).toEqual(jasmine.objectContaining({
      id: '10',
      score: 20,
      name: 'player_1',
      currentPoints: '15'
    }));

    expect(service.badmintonMSInitParse(parsedComments).away).toEqual(jasmine.objectContaining({
      id: '20',
      score: 5,
      name: 'player_2',
      currentPoints: '40'
    }));
  });

  it('should get corrected code for football', () => {
    expect(service.getCorrectRoleCodeForFoolball('CODE')).toEqual('code');
  });

  it('should get corrected code for football', () => {
    const parsedComments = {
      teams: {
        away: {
          score: 10
        },
        home: {
          score: 20
        },
      }
    };

    const scores = {
      away: {
        score: 2,
        currentPoints: 4
      },
      home: {
        score: 3,
        currentPoints: 5
      }
    };
    service.sportUpdateExtend(parsedComments, scores);
    expect(parsedComments.teams.away['currentPoints']).toEqual(4);
    expect(parsedComments.teams.home['currentPoints']).toEqual(5);
  });

  describe('#tennisUpdateExtend', () => {
    it('should update event comments related to tennis live updates', () => {
      let data: any = {
        ALL: [{
          period_code: '',
          role_code: 'Player_1',
          value: '1'
        }],
        SUBPERIOD: [{
          period_code: '',
          period_index: '1set',
          participant_id: '123',
          value: '2'
        }],
        CURRENT: [{
          period_code: '',
          participant_id: '456',
          is_active: 'Y',
          role_code: 'player_1',
          value: '3'
        }]
      };
      const eventComments = {
        teams: {},
        setsScores: {},
        runningGameScores: {},
        runningSetIndex: ''
      };
      service.tennisUpdateExtend(eventComments, data);

      expect(eventComments).toEqual({
        teams: {},
        setsScores: {},
        runningGameScores: {},
        runningSetIndex: ''
      });

      data = {
        ALL: [{
          period_code: 'ALL',
          role_code: 'Player_1',
          value: '1'
        }],
        SUBPERIOD: [{
          period_code: 'SET',
          period_index: '1set',
          id: '123',
          value: '2'
        }],
        CURRENT: [{
          period_code: 'GAME',
          id: '123',
          is_active: 'true',
          role_code: 'player_1',
          value: '3'
        }]
      };
      eventComments.teams = {
        player_1: {
          score: '',
          isActive: false,
          id: '123'
        }
      };

      service.tennisUpdateExtend(eventComments, data);
      expect(eventComments.teams['player_1']['score']).toBe('1');

      expect(eventComments.setsScores['1']['123']).toBe('2');

      expect(eventComments.runningGameScores['123']).toBe('3');
      expect(eventComments.teams['player_1']['isActive']).toBe(true);

      data.SUBPERIOD[0].value = '10';
      service.tennisUpdateExtend(eventComments, data);
      expect(eventComments.setsScores['1']['123']).toBe('10');
    });

    it('should not update event comments', () => {
      const eventComments = {
        teams: {
          player_1: { id: '1', score: '2' },
          player_2: { id: '2', score: '3', isActive: true }
        },
        runningGameScores: {},
        runningSetIndex: ''
      };
      const data = {};
      service.tennisUpdateExtend(eventComments, data);
      expect(eventComments.teams.player_1.score).toEqual('2');
      expect(eventComments.teams.player_2.score).toEqual('3');
      expect(eventComments.teams.player_2.isActive).toEqual(true);
    });

    it('should add setsScores object in eventcomments object', () => {
      const data: any = {
        ALL: [{
          period_code: '',
          role_code: 'Player_1',
          value: '1'
        }],
        SUBPERIOD: [{
          period_code: '',
          period_index: '1set',
          participant_id: '123',
          value: '2'
        }],
        CURRENT: [{
          period_code: '',
          participant_id: '456',
          is_active: 'Y',
          role_code: 'player_1',
          value: '3'
        }]
      };
      const eventComments = {
        teams: { 
          player_1: { id: '1', score: '2' },
          player_2: { id: '2', score: '3', isActive: true }
        },
        runningGameScores: {},
        runningSetIndex: ''
      };
      service.tennisUpdateExtend(eventComments, data);

      expect(eventComments['setsScores']).toEqual({ 1 : {1:'2'} });
    });

    it(`should set latest set's score `, () => {
      const eventComments = {
        teams: {
          player_1: {
            id: '10',
            name: 'player_1'
          },
          player_2: {
            id: '20',
            name: 'player_2'
          }
        },
        setsScores: {},
        runningGameScores: {},
        runningSetIndex: ''
      };

      const data: any = {
        SUBPERIOD: [{ value: '1' }, { value: '2' }, { value: 3 }, { value: 4 }]
      };
      const setsScores = {
        '10': 3,
        '20': 4
      };

      service.tennisUpdateExtend(eventComments, data);

      expect(eventComments.setsScores[1]).toEqual(setsScores);
    });
  });

  describe('#badmintonMSInitParse', () => {
    it('should use first setScore if runningSetIndex is missed', () => {
      const parsedComments = {
        setsScores: {
          '1': {
            '20': '40',
            '10': '15'
          }
        },
        teams: {
          player_1: {
            id: '10',
            score: 20,
            name: 'player_1'
          },
          player_2: {
            id: '20',
            score: 5,
            name: 'player_2'
          }
        }
      };

      expect(service.badmintonMSInitParse(parsedComments).home).toEqual(jasmine.objectContaining({
        id: '10',
        score: 20,
        name: 'player_1',
        currentPoints: '15'
      }));

      expect(service.badmintonMSInitParse(parsedComments).away).toEqual(jasmine.objectContaining({
        id: '20',
        score: 5,
        name: 'player_2',
        currentPoints: '40'
      }));
    });
  });

  describe('#footballUpdateExtend', () => {
    it('should update comments data for football and extend original event', () => {
      const parsedComments = {
        teams: {
          away: {
            score: 10
          },
          home: {
            score: 20
          }
        }
      };

      const gameData = {
        SUBPERIOD: [
          {
            period_code: 'PENALTIES',
            value: 20,
            role_code: 'home'
          },
          {
            period_code: 'test',
            value: 30,
            role_code: 'away'
          }
        ]
      };

      service.footballUpdateExtend(parsedComments, gameData);
      expect(parsedComments.teams.home['penaltyScore']).toEqual(20);
    });

    it('should call updateSportScores if SUBPERIODS doesn\'t exist', () => {
      spyOn(service, 'updateSportScores');
      const parsedComments = {
        teams: {
          away: {
            score: 1
          },
          home: {
            score: 2
          }
        }
      };

      const gameData = {
        ALL: [
          {
            value: 20,
            role_code: 'home'
          },
          {
            value: 30,
            role_code: 'away'
          }
        ]
      };

      service.footballUpdateExtend(parsedComments, gameData);
      expect(service.updateSportScores).toHaveBeenCalledWith(parsedComments, gameData);
    });

    it('should call updateSportScores if SUBPERIODS exist but empty and with modified "role_code"', () => {
      spyOn(service, 'updateSportScores');
      const parsedComments = {
        teams: {
          away: {
            score: 1
          },
          home: {
            score: 2
          }
        }
      };

      const gameData = {
        SUBPERIOD: [],
        ALL: [
          {
            value: 20,
            role_code: 'TEAM_1'
          },
          {
            value: 30,
            role_code: 'TEAM_2'
          }
        ]
      };

      const gameDataCorrected = {
        SUBPERIOD: [],
        ALL: [
          {
            value: 20,
            role_code: 'home'
          },
          {
            value: 30,
            role_code: 'away'
          }
        ]
      };

      service.footballUpdateExtend(parsedComments, gameData);
      expect(service.updateSportScores).toHaveBeenCalledWith(parsedComments, gameDataCorrected);
    });
  });

  describe('updateSportScores', () => {
    it('should detect serving team', () => {
      const parsedComments = {
        teams: {
          away: {
            score: 1
          },
          home: {
            score: 2,
            isServing: true
          }
        }
      } as any;

      const gameData = {
        ALL: [
          {
            value: 20,
            role_code: 'home'
          },
          {
            value: 30,
            role_code: 'away'
          }
        ],
        CURRENT: [
          {
            role_code: 'home',
            value: 3,
          },
          {
            role_code: 'away',
            value: 1,
            is_active: 'true'
          }
        ]
      };
      service.updateSportScores(parsedComments, gameData);
      expect(parsedComments.teams.home.isServing).toBeUndefined();
      expect(parsedComments.teams.away.isActive).toEqual(true);
      expect(parsedComments.teams.home.currentPoints).toEqual(3);
      expect(parsedComments.teams.away.currentPoints).toEqual(1);
    });

  });

  describe('parseScoresFromName', () => {

    it('should split event to "home" and "away" teams', () => {
      const eventName = 'Volero Zurich Women (2) 12-5 (0) CS Volei Alba Blaj Women';

      const parsedEvent = service.parseScoresFromName(eventName);

      expect(parsedEvent.home).toBeTruthy();
      expect(parsedEvent.away).toBeTruthy();
    });

    describe('handball format', () => {
      let eventName = 'Team A 4-3 Team B';

      it('should define names of teams', () => {
        const eventObj = service.parseScoresFromName(eventName);

        expect(eventObj.home.name).toBe('Team A');
        expect(eventObj.away.name).toBe('Team B');
      });

      it('should define scores', () => {
        const eventObj = service.parseScoresFromName(eventName);

        expect(eventObj.home.score).toBe('4');
        expect(eventObj.away.score).toBe('3');
      });

      it('should define scores if name contain some word in brackets next to scores', () => {
        eventName = 'Team A (women) 4-3 (predators) Team B';

        const eventObj = service.parseScoresFromName(eventName);

        expect(eventObj.home.score).toBe('4');
        expect(eventObj.away.score).toBe('3');
      });

      it('should define currentPoints as null', () => {
        const eventObj = service.parseScoresFromName(eventName);

        expect(eventObj.home.currentPoints).toBeNull();
        expect(eventObj.away.currentPoints).toBeNull();
      });


    });

    describe('volleyball format', () => {
      const eventName = 'Volero Zurich Women (2) 12-5 (0) *CS Volei Alba Blaj Women';

      it('should define names teams if volleyball format', () => {

        const eventObj = service.parseScoresFromName(eventName);

        expect(eventObj.home.name).toBe('Volero Zurich Women');
        expect(eventObj.away.name).toBe('CS Volei Alba Blaj Women');
      });

      it('should define scores', () => {
        const eventObj = service.parseScoresFromName(eventName);

        expect(eventObj.home.score).toBe('2');
        expect(eventObj.away.score).toBe('0');
      });

      it('should define currentPoints', () => {
        const eventObj = service.parseScoresFromName(eventName);

        expect(eventObj.home.currentPoints).toBe('12');
        expect(eventObj.away.currentPoints).toBe('5');
      });

      it('should define isServing', () => {
        const eventObj = service.parseScoresFromName(eventName);

        expect(eventObj.home.isServing).toBeFalsy();
        expect(eventObj.away.isServing).toBeTruthy();
      });
    });


  });

  describe('@tennisTransformFallback', () => {
    it('should return comments in correct format', () => {
      const scoresFromName: ITypedScoreData = {
        home: {
          name: 'Team A',
          score: '1',
          periodScore: '2',
          currentPoints: '3',
          isServing: true,
        },
        away: {
          name: 'Team B',
          score: '4',
          periodScore: '5',
          currentPoints: '6',
          isServing: false,
        },
        type: 'SetsGamesPoints',
      };

      const commentsOutput = service.tennisTransformFallback(scoresFromName);

      expect(commentsOutput).toEqual({
        runningSetIndex: 1,
        setsScores: {
          1: {
            1: '2',
            2: '5',
          },
        },
        runningGameScores: {
          1: '3',
          2: '6',
        },
        teams: {
          player_1: {
            id: '1',
            score: '1',
            isActive: true,
          },
          player_2: {
            id: '2',
            score: '4',
            isActive: false,
          }
        }
      } as any);
    });
  });

  describe('@sportUpdateExtend', () => {
    let scores: any;
    let commentsObj: any;

    it('should call tennisTransformFallback if scores type is of SetsGamesPoints', () => {
      commentsObj = { teams: { player_1: {} } };
      scores = { type: 'SetsGamesPoints' };
      spyOn(service, 'tennisTransformFallback').and.returnValue({ foo: 'bar' } as any);

      service.sportUpdateExtend(commentsObj, scores);

      expect(commentsObj).toEqual({ teams: { player_1: {} }, foo: 'bar' } as any);
    });

    describe('update properties', () => {
      beforeEach(() => {
        commentsObj = {
          teams: {
            home: {
              score: 1,
              isServing: false,
              isActive: false,
            },
            away: {}
          }
        };

        scores = {
          home: {},
          away: {}
        };
      });

      it(`score`, () => {
        scores.home.score = 21;
        scores.away.score = 22;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.score).toEqual(21);
        expect(commentsObj.teams.away.score).toEqual(22);
      });

      it('should catch error', () => {
        commentsObj.teams = {
          player_1: { score: 1 },
          player_2: { score: 2 }
        };
        service.sportUpdateExtend(commentsObj, scores);
        expect(console.warn).toHaveBeenCalled();
      });

      it(`score update Hard`, () => {
        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.score).toBeUndefined();
        expect(commentsObj.teams.away.score).toBeUndefined();
      });

      it(`isServing`, () => {
        scores.home.isServing = false;
        scores.away.isServing = true;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.isServing).toBeFalsy();
        expect(commentsObj.teams.away.isServing).toBeTruthy();
      });

      it(`isServing update Hard`, () => {
        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.isServing).toBeUndefined();
        expect(commentsObj.teams.away.isServing).toBeUndefined();
      });

      it(`isActive`, () => {
        scores.home.isActive = false;
        scores.away.isActive = true;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.isActive).toBeFalsy();
        expect(commentsObj.teams.away.isActive).toBeTruthy();
      });

      it(`isActive update Hard`, () => {
        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.isActive).toBeUndefined();
        expect(commentsObj.teams.away.isActive).toBeUndefined();
      });

      it(`currentPoints`, () => {
        scores.home.currentPoints = false;
        scores.away.currentPoints = true;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.currentPoints).toBeFalsy();
        expect(commentsObj.teams.away.currentPoints).toBeTruthy();
      });

      it(`currentPoints should Not update Hard`, () => {
        commentsObj.teams.home.currentPoints = true;
        commentsObj.teams.away.currentPoints = false;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.currentPoints).toBeTruthy();
        expect(commentsObj.teams.away.currentPoints).toBeFalsy();
      });

      it(`periodScore`, () => {
        scores.home.periodScore = false;
        scores.away.periodScore = true;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.periodScore).toBeFalsy();
        expect(commentsObj.teams.away.periodScore).toBeTruthy();
      });

      it(`periodScore should Not update Hard`, () => {
        commentsObj.teams.home.periodScore = true;
        commentsObj.teams.away.periodScore = false;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.periodScore).toBeTruthy();
        expect(commentsObj.teams.away.periodScore).toBeFalsy();
      });

      it(`inn1`, () => {
        scores.home.inn1 = 21;
        scores.away.inn1 = 22;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.inn1).toEqual(21);
        expect(commentsObj.teams.away.inn1).toEqual(22);
      });


      it(`inn1 should Not update Hard`, () => {
        commentsObj.teams.home.inn1 = 1;
        commentsObj.teams.away.inn1 = 2;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.inn1).toEqual(1);
        expect(commentsObj.teams.away.inn1).toEqual(2);
      });

      it(`inn2`, () => {
        scores.home.inn2 = 21;
        scores.away.inn2 = 22;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.inn2).toEqual(21);
        expect(commentsObj.teams.away.inn2).toEqual(22);
      });


      it(`inn2 should Not update Hard`, () => {
        commentsObj.teams.home.inn2 = 1;
        commentsObj.teams.away.inn2 = 2;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.inn2).toEqual(1);
        expect(commentsObj.teams.away.inn2).toEqual(2);
      });

      it(`inn2 should Not update Hard if Not prop in score.home`, () => {
        scores.away.inn2 = 22;
        commentsObj.teams.home.inn2 = 1;
        commentsObj.teams.away.inn2 = 2;

        service.sportUpdateExtend(commentsObj, scores);

        expect(commentsObj.teams.home.inn2).toEqual(1);
        expect(commentsObj.teams.away.inn2).toEqual(2);
      });
    });
  });

  describe('footballInitParse', () => {
    it('should correctly parse football scores in extra time', () => {
      const commentary = JSON.parse(JSON.stringify(footballCommentaryInitialExtraTime));
      const result = service.footballInitParse(commentary);

      expect(result.teams.home).toEqual(jasmine.objectContaining({
        eventId: '623788',
        extraTimeScore: '3',
        id: '43277',
        name: 'Atom Men',
        penaltyScore: '0',
        role: 'Home Team',
        roleCode: 'HOME',
        score: '5',
        type: 'T'
      }));
      expect(result.teams.away).toEqual(jasmine.objectContaining({
        eventId: '623788',
        extraTimeScore: '3',
        id: '43278',
        name: 'Meadow Men',
        penaltyScore: '0',
        role: 'Away Team',
        roleCode: 'AWAY',
        score: '6',
        type: 'T'
      }));
    });

    it('should correctly parse football scores in penalties time', () => {
      const commentary = JSON.parse(JSON.stringify(footballCommentaryInitialPenalties));
      const result = service.footballInitParse(commentary);

      expect(result.teams.home).toEqual(jasmine.objectContaining({
        eventId: '621399',
        extraTimeScore: '1',
        id: '43271',
        name: 'Hearts',
        penaltyScore: '5',
        role: 'Home Team',
        roleCode: 'HOME',
        score: '3',
        type: 'T'
      }));
      expect(result.teams.away).toEqual(jasmine.objectContaining({
        eventId: '621399',
        extraTimeScore: '1',
        id: '43272',
        name: 'Paris FC',
        penaltyScore: '5',
        role: 'Away Team',
        roleCode: 'AWAY',
        score: '3',
        type: 'T'
      }));
    });
  });
  describe('getScoreTypeByCategory', () => {
    it('should return null if no category code passed', () => {
      expect(service['getScoreTypeByCategory'](undefined as any)).toBeNull();
    });
    it('should return null if category code not matched categories ' +
      'which support comments updates', () => {
      expect(service['getScoreTypeByCategory']('CRICKET')).toBeNull();
    });
    it('should return correct score type for provided category ' +
      'which support comments updates', () => {
      expect(service['getScoreTypeByCategory']('BADMINTON')).toEqual('SetsPoints');
      expect(service['getScoreTypeByCategory']('VOLLEYBALL')).toEqual('SetsPoints');
      expect(service['getScoreTypeByCategory']('HANDBALL')).toEqual('Simple');
      expect(service['getScoreTypeByCategory']('BEACH_VOLLEYBALL')).toEqual('SetsPoints');
      expect(service['getScoreTypeByCategory']('TENNIS')).toEqual('SetsGamesPoints');
      expect(service['getScoreTypeByCategory']('FOOTBALL')).toEqual('Simple');
      expect(service['getScoreTypeByCategory']('BASKETBALL')).toEqual('Simple');
    });
  });
  describe('extendWithScoreType', () => {
    it('should extend event with score type', () => {
      const event = {} as any;
      service['extendWithScoreInfo'](event as any, {
        scoreType: 'Simple',
        score: {}
      });
      expect(event.scoreType).toEqual('Simple');
    });
    it('shouldn`t fail if no event passed', () => {
      service['extendWithScoreType'](undefined as any, 'FOOTBALL');
    });
  });
  describe('extendWithScoreInfo', () => {
    it('should extend event with score info', () => {
      const event = {} as any;
      service['extendWithScoreInfo'](event as any, {
        scoreType: 'Simple',
        score: {}
      });
      expect(event.scoreType).toEqual('Simple');
      expect(event.comments.teams).toBeDefined();
    });
    it('shouldn`t fail if no scoreInfo passed', () => {
      service['extendWithScoreInfo'](undefined as any, 'FOOTBALL');
      service['extendWithScoreInfo']({} as any, undefined as any);
    });
  });
  it('isScoreboardTeamActive returns proper boolean', () => {
    expect(service['isScoreboardTeamActive']({is_active: 'N'})).toBe(false);
    expect(service['isScoreboardTeamActive']({is_active: 'Y'})).toBe(true);
    expect(service['isScoreboardTeamActive']({is_active: 'true'})).toBe(true);
  });
});

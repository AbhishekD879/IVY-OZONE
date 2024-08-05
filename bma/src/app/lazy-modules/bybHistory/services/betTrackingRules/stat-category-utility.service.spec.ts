import {
  StatCategoryUtilityService,
  TEAM_STATS
} from '@lazy-modules/bybHistory/services/betTrackingRules/stat-category-utility.service';
import {
  IScoreByPlayer,IScoreByTeams,
  IScoreboardStatsUpdate,
  ITeams,
  IPlayer, IPlayersSimple,
} from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';
import { scoreboardsStatsUpdate } from '@lazy-modules/bybHistory/services/bybSelectionsService/scoreboards-stats-update.mock';
import { DOUBLE_TEAMS } from '@lazy-modules/bybHistory/constants/byb-5aside-markets-config.constant';

describe('StatCategoryUtilityService', () => {
  let service: StatCategoryUtilityService;
  let statsDataMock;
  let expectedTeamsGoalsObj;
  const goal = {
    assistingPlayer: '25816',
    ownGoal: false,
    scorer: '25815',
    time: '20:00',
    timestamp: '2020-07-15T19:35:18Z'
  };

  beforeEach(() => {
    statsDataMock = JSON.parse(JSON.stringify(scoreboardsStatsUpdate));
    expectedTeamsGoalsObj = {
      score: {
        '1h': {
          home: 2,
          away: 1
        },
        '2h': {
          home: 0,
          away: 0
        },
        total: {
          home: 2,
          away: 1
        }
      },
      away: statsDataMock.away,
      home: statsDataMock.home
    };

    service = new StatCategoryUtilityService();
  });

  describe('getScore', () => {
   it('should get obj with teams scores', () => {
      const actualResult = service.getScore('teams', statsDataMock);

      expect(actualResult).toEqual(expectedTeamsGoalsObj as IScoreByTeams);
    });

    it('should get obj with team scores', () => {
      const actualResult = service.getScore('team', statsDataMock);

      expect(actualResult).toEqual(expectedTeamsGoalsObj as IScoreByTeams);
    });

    it('should get obj with player scores', () => {
      const expectedResult: IScoreByPlayer = {
        away: [
          {
            assistingPlayer: '25816',
            ownGoal: null,
            player: {
              assists: 0,
              cards: {
                red: 0,
                yellow: 0
              },
              chancesCreated: 4,
              fouls: 2,
              goals: 1,
              id: '25815',
              providerId: 'cotiiu6mjkfx5xa63nhfbdf4l',
              name: {
                firstName: 'Sadio',
                lastName: 'Mané',
                matchName: 'S. Mané'
              },
              passes: 34,
              goalConceded: 0,
              crosses: 0,
              offsides: 0,
              goalsInsideBox: 0,
              goalsOutsideBox: 0,
              shotsOutsideBox: 0,
              shotsWoodwork: 0,
              secondYellow: 0,
              shots: {
                blockedShot: 2,
                offTarget: 2,
                onTarget: 2,
                total: 6
              },
              tackles: 1
            },
            scorer: '25815',
            time: '20:00',
            timestamp: '2020-07-15T19:35:18Z'
          },
        ],
        home: [
          {
            assistingPlayer: null,
            ownGoal: null,
            player: {
              assists: 1,
              cards: {
                red: 0,
                yellow: 0
              },
              chancesCreated: 1,
              fouls: 2,
              goals: 1,
              id: '26324',
              providerId: 'f4cykd65su8xbme6xdc1iw7o5',
              name: {
                firstName: 'Alexandre',
                lastName: 'Lacazette',
                matchName: 'A. Lacazette'
              },
              passes: 11,
              goalConceded: 0,
              crosses: 0,
              offsides: 0,
              goalsInsideBox: 0,
              goalsOutsideBox: 0,
              shotsOutsideBox: 0,
              shotsWoodwork: 0,
              secondYellow: 0,
              shots: {
                blockedShot: 0,
                offTarget: 0,
                onTarget: 1,
                total: 1
              },
              tackles: 3
            },
            scorer: '26324',
            time: '32:00',
            timestamp: '2020-07-15T19:47:18Z'
          },
          {
            assistingPlayer: '26324',
            ownGoal: null,
            player: {
              assists: 0,
              cards: {
                red: 0,
                yellow: 0
              },
              chancesCreated: 0,
              providerId: 'bzummkjt2ya27kvolzmqn91wp',
              fouls: 0,
              goals: 1,
              id: '32166',
              name: {
                firstName: 'Reiss',
                lastName: 'Nelson',
                matchName: 'R. Nelson'
              },
              passes: 10,
              goalConceded: 0,
              crosses: 0,
              offsides: 0,
              goalsInsideBox: 0,
              goalsOutsideBox: 0,
              shotsOutsideBox: 0,
              shotsWoodwork: 0,
              secondYellow: 0,
              shots: {
                blockedShot: 0,
                offTarget: 0,
                onTarget: 1,
                total: 1
              },
              tackles: 2
            },
            scorer: '32166',
            time: '44:00',
            timestamp: '2020-07-15T19:59:18Z'
          }
        ]
      };
      const actualResult = service.getScore('player', statsDataMock);

      expect(actualResult).toEqual(expectedResult as IScoreByPlayer);
    });
  });

  describe('extendGoalWihPlayerInfo', () => {
    it('should extend goal object with player info(Home team)', () => {
      const update = {
        players: {
          home: {
            '25815': {
              goals: 1,
              id: '25815'
            }
          },
          away: {}
        }
      } as any;
      const goalsObj = {
        away: [],
        home: [goal]
      };
      service.extendGoalWihPlayerInfo(goal, update, goalsObj);

      expect(goalsObj).toEqual({
        away: [],
        home: [{
          player: {
            goals: 1,
            id: '25815'
          },
          ...goal
        }]
      } as IScoreByPlayer);
    });

    it('should extend goal object with player info(Away team)', () => {
      const update = {
        players: {
          home: {},
          away: {
            '25815': {
              goals: 1,
              id: '25815'
            }
          }
        }
      } as any;
      const goalsObj = {
        away: [goal],
        home: []
      };
      service.extendGoalWihPlayerInfo(goal, update, goalsObj);

      expect(goalsObj).toEqual({
        away: [
          {
            player: {
              goals: 1,
              id: '25815'
            },
            ...goal
          }
        ],
        home: []
      } as IScoreByPlayer);
    });
  });

  describe('getScoreByPlayer', () => {
    it('should get score obj by player', () => {
      const update = {
        players: {
          home: {
            '25815': {
              goals: 1,
              id: '25815'
            }
          },
          away: {}
        },
        goals: {
          home: [goal],
          away: []
        }
      } as any;
      const actualResult = service.getScoreByPlayer(update);

      expect(actualResult).toEqual({
        away: [],
        home: [{
          player: {
            goals: 1,
            id: '25815'
          },
          ...goal
        }]
      } as IScoreByPlayer);
    });
  });

  describe('getScoreByTeams', () => {
    it('should get score obj by teams', () => {
      const update = {
        score: {
          '1h': { home: 1, away: 2 },
          '2h': { home: 0, away: 0 },
          total: { home: 1, away: 2 }
        },
        home: statsDataMock.home,
        away: statsDataMock.away
      } as any;
      const actualResult = service.getScoreByTeams(update);

      expect(actualResult).toEqual({
        score: {
          '1h': { home: 1, away: 2 },
          '2h': { home: 0, away: 0 },
          total: { home: 1, away: 2 }
        },
        home: statsDataMock.home,
        away: statsDataMock.away
      } as IScoreByTeams);
    });
  });

  describe('getTeamStats', () => {
    it('should return empty obj if generalInformationRequired is wrong', () => {
      expect(service.getCorners('players', {} as IScoreboardStatsUpdate)).toEqual({} as ITeams);
    });

    it('should return obj by provided stat param', () => {
      const expected = {
        home: {
          '1h': { corners: 1, providerId: '4dsgumo7d4zupm2ugsvm4zm4d', id: '897' },
          total: { corners: 2, providerId: '4dsgumo7d4zupm2ugsvm4zm4d', id: '897' },
          ht: { corners: 0, providerId: '4dsgumo7d4zupm2ugsvm4zm4d', id: '897' },
          pre: { corners: 0, providerId: '4dsgumo7d4zupm2ugsvm4zm4d', id: '897' },
          '2h': { corners: 1, providerId: '4dsgumo7d4zupm2ugsvm4zm4d', id: '897' },
        },
        away: {
          '2h': { corners: 9, providerId: 'c8h9bw1l82s06h77xxrelzhur', id: '1394' },
          '1h': { corners: 4, providerId: 'c8h9bw1l82s06h77xxrelzhur', id: '1394' },
          ht: { corners: 0, providerId: 'c8h9bw1l82s06h77xxrelzhur', id: '1394' },
          pre: { corners: 0, providerId: 'c8h9bw1l82s06h77xxrelzhur', id: '1394' },
          total: { corners: 13, providerId: 'c8h9bw1l82s06h77xxrelzhur', id: '1394' },
        }
      } as ITeams;

      expect(service['getTeamStats']('team', statsDataMock, 'corners')).toEqual(expected);
    });
  });

  describe('Team Stats', () => {
    beforeEach(() => {
      service['getTeamStats'] = jasmine.createSpy('getTeamStats').and.callThrough();
      service['getPlayerStats'] = jasmine.createSpy('getPlayerStats').and.callThrough();
    });

    it('getCorners', () => {
      service.getCorners('teams', statsDataMock as IScoreboardStatsUpdate);

      expect(service['getTeamStats']).toHaveBeenCalledWith('teams', statsDataMock, 'corners');
    });

    it('getCardIndex', () => {
      service.getCardIndex('teams', statsDataMock as IScoreboardStatsUpdate);

      expect(service['getPlayerStats']).toHaveBeenCalledWith('player', statsDataMock, 'cards');
    });
  });

  describe('Player Stats', () => {
    beforeEach(() => {
      service.getPlayerStats = jasmine.createSpy('getPlayerStats').and.callThrough();
    });

    it('getShotsOnTarget', () => {
      service.getShotsOnTarget('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'shots');
    });

    it('getShots', () => {
      service.getShots('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'shots');
    });

    it('getAssists', () => {
      service.getAssists('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'assists');
    });

    it('getPasses', () => {
      service.getPasses('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'passes');
    });

    it('getCards', () => {
      service.getRedCards('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'cards');
    });

    it('getTackles', () => {
      service.getTackles('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'tackles');
    });

    it('getCrosses', () => {
      service.getCrosses('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'crosses');
    });

    it('getOffsides', () => {
      service.getOffsides('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'offsides');
    });

    it('GOALS_INSIDE_BOX', () => {
      service.getGoalsInsideBox('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'goalsInsideBox');
    });

    it('GOALS_OUTSIDE_BOX', () => {
      service.getGoalsOutsideBox('player', statsDataMock as IScoreboardStatsUpdate);

      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'goalsOutsideBox');
    });

    it('shotsWoodwork', () => {
      service.getShotsWoodwork('player', statsDataMock as IScoreboardStatsUpdate);
      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'shotsWoodwork');
    });

    it('getShotsOutsideBox', () => {
      service.getShotsOutsideBox('player', statsDataMock as IScoreboardStatsUpdate);
      expect(service.getPlayerStats).toHaveBeenCalledWith('player', statsDataMock, 'shotsOutsideBox');
    });
  });

  describe('getPlayerStats', () => {
    it('should return empty obj if generalInformationRequired is wrong', () => {
      expect(service.getPlayerStats('teams', statsDataMock as IScoreboardStatsUpdate, 'name')).toEqual({} as IPlayersSimple);
    });

    it('should return object by provided stat param', () => {
      const expected = {
        id: '33394',
        providerId: '3zl1q2gk6tdmzirsyfgm38no5',
        name: {
          firstName: 'Damián Emiliano',
          lastName: 'Martínez',
          matchName: 'E. Martínez'
        },
        team: 'home'
      };

      const result = service.getPlayerStats('player', statsDataMock as IScoreboardStatsUpdate, 'name');

      expect(result).toEqual(jasmine.any(Object));
      expect(result.home).toEqual(jasmine.any(Array));
      expect(result.away).toEqual(jasmine.any(Array));
      expect(result.home.find((player: IPlayer) => player.id === expected.id)).toEqual(expected as IPlayer);
    });
  });

  describe('getBooking', () => {
    let expectedObj;
    let actualResult;

    beforeEach(() => {
      expectedObj = {
        away: {
          '1h': {
            cards: { yellow: 0, red: 0 },
            id: '1394',
            providerId: 'c8h9bw1l82s06h77xxrelzhur'
          },
          '2h': {
            cards: { yellow: 1, red: 1 },
            id: '1394',
            providerId: 'c8h9bw1l82s06h77xxrelzhur'
          },
          'ht': {
            cards: { yellow: 0, red: 0 },
            id: '1394',
            providerId: 'c8h9bw1l82s06h77xxrelzhur'
          },
          'pre': {
            cards: { yellow: 0, red: 0 },
            id: '1394',
            providerId: 'c8h9bw1l82s06h77xxrelzhur'
          },
          'total': {
            cards: { yellow: 1, red: 1 },
            id: '1394',
            providerId: 'c8h9bw1l82s06h77xxrelzhur'
          }
        },
        home: {
          '1h': {
            cards: { yellow: 0, red: 1 },
            id: '897',
            providerId: '4dsgumo7d4zupm2ugsvm4zm4d'
          },
          '2h': {
            cards: { yellow: 3, red: 0 },
            id: '897',
            providerId: '4dsgumo7d4zupm2ugsvm4zm4d'
          },
          'ht': {
            cards: { yellow: 0, red: 0 },
            id: '897',
            providerId: '4dsgumo7d4zupm2ugsvm4zm4d'
          },
          'pre': {
            cards: { yellow: 0, red: 0 },
            id: '897',
            providerId: '4dsgumo7d4zupm2ugsvm4zm4d'
          },
          'total': {
            cards: { yellow: 3, red: 0 },
            id: '897',
            providerId: '4dsgumo7d4zupm2ugsvm4zm4d'
          }
        }
      };
    });

    it('should get obj with teams', () => {
      actualResult = service.getBooking('teams', statsDataMock);

      expect(actualResult).toEqual(expectedObj);
    });

    it('should get obj with team', () => {
      actualResult = service.getBooking('team', statsDataMock);

      expect(actualResult).toEqual(expectedObj);
    });

    it('should get obj with player', () => {
      expectedObj = {
        away: {
          id: '1394',
          providerId: 'c8h9bw1l82s06h77xxrelzhur'
        },
        home: {
          id: '897',
          providerId: '4dsgumo7d4zupm2ugsvm4zm4d'
        },
        cards: {
          away: [{
            player: '5537',
            time: '48:00',
            timestamp: '2020-07-15T21:05:59Z',
            type: 'yellow'
          }],
          home: [{
            player: '6048',
            time: '46:00',
            timestamp: '2020-07-15T21:03:59Z',
            type: 'yellow'
          }, {
            player: '5812',
            time: '81:00',
            timestamp: '2020-07-15T21:38:59Z',
            type: 'yellow'
          }, {
            player: '27849',
            time: '91:00',
            timestamp: '2020-07-15T21:48:59Z',
            type: 'yellow'
          }]
        }
      };
      actualResult = service.getBooking('player', statsDataMock);

      expect(actualResult).toEqual(expectedObj);
    });
  });

  it('redCards by teams', () => {
    const expectedResult = {
      away: {
        id: '1394',
        providerId: 'c8h9bw1l82s06h77xxrelzhur',
        periods: {
          '1h': { redCards: 0 },
          '2h': { redCards: 1 },
          'ht': { redCards: 0 },
          'pre': { redCards: 0 },
          total: { redCards: 1 }
        },
      },
      home: {
        id: '897',
        providerId: '4dsgumo7d4zupm2ugsvm4zm4d',
        periods: {
          '1h': { redCards: 1 },
          '2h': { redCards: 0 },
          'ht': { redCards: 0 },
          'pre': { redCards: 0 },
          total: { redCards: 0 }
        },
      }
    } as any;
    expect(service.getRedCards('teams', statsDataMock as IScoreboardStatsUpdate)).toEqual(expectedResult);
  });

  it('redCards by team', () => {
    const expectedResult = {
      away: {
        id: '1394',
        providerId: 'c8h9bw1l82s06h77xxrelzhur',
        periods: {
          '1h': { redCards: 0 },
          '2h': { redCards: 1 },
          'ht': { redCards: 0 },
          'pre': { redCards: 0 },
          total: { redCards: 1 }
        },
      },
      home: {
        id: '897',
        providerId: '4dsgumo7d4zupm2ugsvm4zm4d',
        periods: {
          '1h': { redCards: 1 },
          '2h': { redCards: 0 },
          'ht': { redCards: 0 },
          'pre': { redCards: 0 },
          total: { redCards: 0 }
        },
      }
    } as any;
    expect(service.getRedCards('team', statsDataMock as IScoreboardStatsUpdate)).toEqual(expectedResult);
  });

  describe('@getHomeAwayTeamByName', () => {
    let actualResult;
    let selection;

    beforeEach(() => {
      selection = {
        part: {
          outcome: [{
            name: 'Liverpool'
          }]
        }
      } as any;
    });
    it('should return team status(Away) by outcome name', () => {
      actualResult = service.getHomeAwayTeamByName(statsDataMock, selection);

      expect(actualResult).toEqual('Away');
    });

    it('should return team status(Home) by outcome name', () => {
      selection.part.outcome[0].name = 'Arsenal';
      actualResult = service.getHomeAwayTeamByName(statsDataMock, selection);

      expect(actualResult).toEqual('Home');
    });

    it('should also return team status(Home) by outcome name', () => {
      selection.part.outcome[0].name = 'FC Arsenal';
      actualResult = service.getHomeAwayTeamByName(statsDataMock, selection);
      expect(actualResult).toEqual('Home');
    });

    it('should return team status(Home) by outcome name', () => {
      selection.part.outcome[0].name = 'Draw';
      actualResult = service.getHomeAwayTeamByName(statsDataMock, selection);

      expect(actualResult).toEqual('Draw');
    });

    it('should not return team by outcome name if OPTA team name and OB team name are different', () => {
      selection.part.outcome[0].name = 'Arsnl';
      actualResult = service.getHomeAwayTeamByName(statsDataMock, selection);

      expect(actualResult).toEqual(null);
    });

    it('should not return team if no teams are available in the object', () => {
      selection.part.outcome[0].name = 'Arsnl';
      actualResult = service.getHomeAwayTeamByName({ } as any, selection);

      expect(actualResult).toEqual(null);
    });
  });

  describe('@getHomeAwayTeamByContestantId', () => {
    let actualResult;
    let selection;

    beforeEach(() => {
      selection = {
        part: {
          outcome: [{
            name: 'Liverpool',
            externalStatsLink: {
              'contestantId': 'c8h9bw1l82s06h77xxrelzhur',
              'statCategory': 'Score',
              'statValue': '0'
            }
          }]
        }
      } as any;
    });
    it('should return team status(Away) by outcome ContestantId', () => {
      actualResult = service.getHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual('Away');
    });

    it('should return team status(Home) by outcome ContestantId', () => {
      selection.part.outcome[0].name = 'Arsenal';
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      actualResult = service.getHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual('Home');
    });

    it('should return team status(Home) by outcome ContestantId case 1', () => {
      selection.part.outcome[0].name = 'Draw';
      delete selection.part.outcome[0].externalStatsLink;
      actualResult = service.getHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual('Draw');
    });
    it('should return team status(Home) by outcome ContestantId case 3', () => {
      selection.part.outcome[0].name = 'Draw';
      delete selection.part.outcome[0].externalStatsLink.contestantId;
      actualResult = service.getHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual('Draw');
    });

    it('should not return team by outcome name if OPTA team name and OB team name are different', () => {
      selection.part.outcome[0].name = 'Arsnl';
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zmijk';
      actualResult = service.getHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual(null);
    });

    it('should not return team if no teams are available in the object', () => {
      selection.part.outcome[0].name = 'Arsnl';
      actualResult = service.getHomeAwayTeamByContestantId({ } as any, selection);

      expect(actualResult).toEqual(null);
    });
  });

  describe('@getDoubleHomeAwayTeamByContestantId', () => {
    let actualResult;
    let selection;

    beforeEach(() => {
      selection = {
        part: {
          outcome: [{
            name: 'LIVERPOOL OR DRAW',
            externalStatsLink: {
              'contestantId': 'c8h9bw1l82s06h77xxrelzhur',
              'statCategory': 'Score',
              'statValue': '0'
            }
          }]
        }
      } as any;
    });

    it('should return double team status(away or draw) by outcome name', () => {
      actualResult = service.getDoubleHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual(DOUBLE_TEAMS.AWAY_OR_DRAW);
    });

    it('should return double team status(home or draw) by outcome name', () => {
      selection.part.outcome[0].name = 'ARSENAL OR DRAW';
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      actualResult = service.getDoubleHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual(DOUBLE_TEAMS.HOME_OR_DRAW);
    });

    it('should return double team status(home or away) by outcome name', () => {
      selection.part.outcome[0].name = 'ARSENAL OR LIVERPOOL';
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      actualResult = service.getDoubleHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual(DOUBLE_TEAMS.HOME_OR_AWAY);
    });

    it('should return double team status(home or away) by outcome name', () => {
      selection.part.outcome[0].name = 'LIVERPOOL or ARSENAL';
      selection.part.outcome[0].externalStatsLink.contestantId = 'c8h9bw1l82s06h77xxrelzhur';
      actualResult = service.getDoubleHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual(DOUBLE_TEAMS.HOME_OR_AWAY);
    });

    it('should return null', () => {
      selection.part.outcome[0].name = 'LIVERPOOL1 OR ARSENAL';
      selection.part.outcome[0].externalStatsLink.contestantId = 'c8h9bw1l82s06h77xxrelziop';
      actualResult = service.getDoubleHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual(null);
    });
    it('should return null for no conestastantId', () => {
      selection.part.outcome[0].name = 'LIVERPOOL1 OR ARSENAL';
      delete selection.part.outcome[0].externalStatsLink.contestantId;
      actualResult = service.getDoubleHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual(null);
    });
    it('should return null for no externalStatsLink', () => {
      selection.part.outcome[0].name = 'LIVERPOOL1 OR ARSENAL';
      delete selection.part.outcome[0].externalStatsLink;
      actualResult = service.getDoubleHomeAwayTeamByContestantId(statsDataMock, selection);

      expect(actualResult).toEqual(null);
    });
  });

  describe('@getCurrentPeriod', () => {
    it('should return current period(total)', () => {
      const actualResult = service.getCurrentPeriod('ert');

      expect(actualResult).toEqual('total');
    });

    it('should return current period(2h)', () => {
      const actualResult = service.getCurrentPeriod('ht');

      expect(actualResult).toEqual('2h');
    });

    it('should return current period(1h)', () => {
      const actualResult = service.getCurrentPeriod('1h');

      expect(actualResult).toEqual('1h');
    });
  });

  describe('findPlayerByIdAndTeam', () => {
    it('should return player by id', () => {
      const players = {
        home: [],
        away: [{ providerId: '1' }]
      } as IPlayersSimple;
      const actualResult = service['findPlayerByIdAndTeam'](players, '1', 'away');

      expect(actualResult).toEqual(jasmine.objectContaining({ providerId: '1' }));
    });

    it('should return undefined when no player by id found', () => {
      const players = {
        home: [],
        away: [{ providerId: '1' }]
      } as IPlayersSimple;
      const actualResult = service['findPlayerByIdAndTeam'](players, '1', 'home');

      expect(actualResult).toEqual(undefined);
    });
  });

  describe('getPlayerById', () => {
    it('should return player by id in away team', () => {
      const players = {
        home: [],
        away: [{ providerId: '1' }]
      } as IPlayersSimple;
      const actualResult = service['getPlayerById'](players, '1');

      expect(actualResult).toEqual(jasmine.objectContaining({ providerId: '1' }));
    });

    it('should return player by id in home team', () => {
      const players = {
        home: [{ providerId: '1' }],
        away: []
      } as IPlayersSimple;
      const actualResult = service['getPlayerById'](players, '1');

      expect(actualResult).toEqual(jasmine.objectContaining({ providerId: '1' }));
    });

    it('should return undefined when no player by id found', () => {
      const players = {
        home: [{ providerId: '1' }],
        away: [{ providerId: '2' }]
      } as IPlayersSimple;
      const actualResult = service['getPlayerById'](players, '3');

      expect(actualResult).toEqual(undefined);
    });
  });

  describe('getAllGoals', () => {
    let players;
    beforeEach(() => {
      players =  {
        home: {
          'Shevchenko': {
            id: 'Shevchenko'
          },
          'Rebrov': {
            id: 'Rebrov'
          }
        },
        away: {
          'Gusev': {
            id: 'Gusev'
          },
          'Voronin': {
            id: 'Voronin'
          },
          'Rotan': {
            id: 'Rotan'
          }
        }
      };
    });
    it('should return sorted array of goals', () => {
      const update = {
        players,
        goals: {
          home: [
            {
              scorer: 'Rebrov',
              timestamp: '2020-07-16T21:09:11Z'
            },
            {
              scorer: 'Shevchenko',
              timestamp: '2020-07-16T21:49:11Z'
            }
          ],
          away: [
            {
              scorer: 'Gusev',
              timestamp: '2020-07-16T21:39:11Z'
            },
            {
              scorer: 'Gusev',
              timestamp: '2020-07-16T22:10:11Z'
            }
          ]
        },
        score: {
          '1h': {
            home: 1,
            away: 0
          },
          '2h': {
            home: 1,
            away: 1
          },
          total: {
            home: 2,
            away: 2
          }
        }
      } as any;

      expect(service.getAllGoals(update as any)).toEqual([
        {
          scorer: 'Rebrov',
          timestamp: '2020-07-16T21:09:11Z',
          team: 'Home',
          period: '1h',
          player: {
            id: 'Rebrov'
          }
        },
        {
          scorer: 'Gusev',
          timestamp: '2020-07-16T21:39:11Z',
          team: 'Away',
          period: '2h',
          player: {
            id: 'Gusev'
          }
        },
        {
          scorer: 'Shevchenko',
          timestamp: '2020-07-16T21:49:11Z',
          team: 'Home',
          period: '2h',
          player: {
            id: 'Shevchenko'
          }
        },
        {
          scorer: 'Gusev',
          timestamp: '2020-07-16T22:10:11Z',
          team: 'Away',
          player: {
            id: 'Gusev'
          }
        }
      ] as any);

    });
    it('should return sorted array of goals in case if 2nd half not started yet', () => {
      const update = {
        players,
        goals: {
          home: [
            {
              scorer: 'Rebrov',
              timestamp: '2020-07-16T21:09:11Z'
            }
          ],
          away: [
            {
              scorer: 'Gusev',
              timestamp: '2020-07-16T21:11:11Z'
            },
            {
              scorer: 'Rotan',
              timestamp: '2020-07-16T21:15:11Z'
            }
          ]
        },
        score: {
          '1h': {
            home: 1,
            away: 2
          },
          total: {
            home: 1,
            away: 2
          }
        }
      } as any;

      expect(service.getAllGoals(update as any)).toEqual([
        {
          scorer: 'Rebrov',
          timestamp: '2020-07-16T21:09:11Z',
          team: 'Home',
          period: '1h',
          player: {
            id: 'Rebrov'
          }
        },
        {
          scorer: 'Gusev',
          timestamp: '2020-07-16T21:11:11Z',
          team: 'Away',
          period: '1h',
          player: {
            id: 'Gusev'
          }
        },
        {
          scorer: 'Rotan',
          timestamp: '2020-07-16T21:15:11Z',
          team: 'Away',
          period: '1h',
          player: {
            id: 'Rotan'
          }
        }
      ] as any);

    });
  });

  describe('getAllCards', () => {
    it('should return sorted array of all cards', () => {
      service['getBooking'] = jasmine.createSpy('getBooking').and.returnValue(statsDataMock);
      expect(service.getAllCards(statsDataMock as any)).toEqual([
        {
          player: '6048',
          time: '46:00',
          type: 'yellow',
          team: 'Home',
          timestamp: '2020-07-15T21:03:59Z'
        },
        {
          player: '5537',
          time: '48:00',
          type: 'yellow',
          team: 'Away',
          timestamp: '2020-07-15T21:05:59Z'
        },
        {
          player: '5812',
          time: '81:00',
          type: 'yellow',
          team: 'Home',
          timestamp: '2020-07-15T21:38:59Z'
        },
        {
          player: '27849',
          time: '91:00',
          type: 'yellow',
          team: 'Home',
          timestamp: '2020-07-15T21:48:59Z'
        }
      ] as any);
    });
  });

  describe('applyHandicapValue', () => {
    let expectedScore;

    beforeEach(() => {
      expectedScore = expectedTeamsGoalsObj.score;
    });

    it('should return goals with applied handicap value to proper team amount of goals(Home handicap)', () => {
      expectedScore['1h'].home = 3;
      const actualResult = service.applyHandicapValue(expectedTeamsGoalsObj, 'Home', 1, '1h');

      expect(actualResult.score).toEqual(expectedScore);
    });

    it('should return goals with applied handicap value to proper team amount of goals(Draw handicap)', () => {
      expectedScore['1h'].home = 1;
      const actualResult = service.applyHandicapValue(expectedTeamsGoalsObj, 'Draw', -1, '1h');

      expect(actualResult.score).toEqual(expectedScore);
    });

    it('should return goals without handicap value when no period were found', () => {
      expectedTeamsGoalsObj.score = expectedScore = {
        '1h': {
          home: 2,
          away: 1
        },
        total: {
          home: 2,
          away: 1
        }
      };
      const actualResult = service.applyHandicapValue(expectedTeamsGoalsObj, 'Draw', -1, '2h');

      expect(actualResult.score).toEqual(expectedScore);
    });
  });

  describe('calculateSumOfPlayersCards', () => {
    let cards;
    let players;

    beforeEach(() => {
      cards = {
        yellow: 0,
        red: 0
      };

      players = service.getPlayerStats('player', statsDataMock, TEAM_STATS.CARDS);
    });

    it('should calculate sum of all players cards from home team', () => {
      service['calculateSumOfPlayersCards'](cards, players, 'home');

      expect(cards).toEqual({ yellow: 3, red: 0 });
    });
  });


  describe('getPlayerByName', () => {
    const playersListObj = {
      home: {
        123: {name: { matchName: 'rty'}},
        345: {name: { matchName: 'qwe'}}},
      away: {
        123: {name: { matchName: 'ronaldo'}},
        345: {name: { matchName: 'messi'}}
      }
    } as any;

    it('should find a player in away team', () => {
      const player = {name: {matchName: 'messi'}, homeAwaySide: 'Away'} as any;
      expect(service.getPlayerByName('messi', playersListObj)).toEqual(player);
    });

    it('should find a player in home team', () => {
      playersListObj.home['123'].name.matchName = 'messi';
      playersListObj.away['123'].name.matchName = '123';
      const player = {name: {matchName: 'messi'}, homeAwaySide: 'Home'} as any;
      expect(service.getPlayerByName('messi', playersListObj)).toEqual(player);
    });
  });

  describe('getPlayerFromNameId', () => {
    const playersListObj = {
      home: {
        123: {name: { matchName: 'rty'}},
        345: {name: { matchName: 'qwe'}}},
      away: {
        123: {name: { matchName: 'ronaldo'}},
        345: {name: { matchName: 'messi'}}
      }
    } as any;

    it('should find a player in away team from id and name', () => {
      const player = {name: {matchName: 'messi'}, homeAwaySide: 'Away'} as any;
      expect(service.getPlayerFromNameId('messi', 'b2ak3yqqaexteldtl135erpx', playersListObj)).toEqual(player);
    });

    it('should find a player in home team from id and name', () => {
      playersListObj.home['123'].name.matchName = 'messi';
      playersListObj.away['123'].name.matchName = '123';
      const player = {name: {matchName: 'messi'}, homeAwaySide: 'Home'} as any;
      expect(service.getPlayerFromNameId('messi', 'b2ak3yqqaexteldtl135erpx', playersListObj)).toEqual(player);
    });
  });

  describe('getBookingPoints', () => {
    let cards;

    beforeEach(() => {
      cards = {
        yellow: 1,
        red: 2
      };
    });

    it('should calculate booking points', () => {
      expect(service.getBookingPoints(cards)).toEqual(60);
    });
  });
  describe('removeDiacritical', () => {
    it('should remove the Diacritical', () => {
      expect(service['removeDiacritical']('Córdoba')).toEqual('Cordoba');
    });
    it('should remove the Diacritical', () => {
      expect(service['removeDiacritical']('Córdoba'.toLowerCase())).toEqual('Cordoba'.toLowerCase());
    });
  });
  describe('getCardsFromPlayers', () => {
    let players;

    beforeEach(() => {
      players = service.getPlayerStats('player', statsDataMock, TEAM_STATS.CARDS);
    });

    it('should return cards(red and yellow) from all players according to Draw team', () => {
      const actualResult = service.getCardsFromPlayers(players, 'Draw');

      expect(actualResult).toEqual({ yellow: 4, red: 0 });
    });

    it('should return cards(red and yellow) from all players according to Away team', () => {
      const actualResult = service.getCardsFromPlayers(players, 'Away');

      expect(actualResult).toEqual({ yellow: 1, red: 0 });
    });

    it('should return cards(red and yellow) from all players according to Home team', () => {
      const actualResult = service.getCardsFromPlayers(players, 'Home');

      expect(actualResult).toEqual({ yellow: 3, red: 0 });
    });
  });

  describe('#getRedCardsByTeamWithYellowCardsWorkAround', () => {
    it('should return 0 red cards for both teams', () => {
      const result = service.getRedCardsByTeamWithYellowCardsWorkAround('', statsDataMock);

      expect(result).toEqual({
        away: { id: '1394', providerId: 'c8h9bw1l82s06h77xxrelzhur', periods: { total: { redCards: 0 } } },
        home: { id: '897', providerId: '4dsgumo7d4zupm2ugsvm4zm4d', periods: { total: { redCards: 0 } } }
      } as any);
    });

    it('should return 1 red card for home team when player has 1 red card', () => {
      statsDataMock.players.home['33394'].cards.red = 1;
      const result = service.getRedCardsByTeamWithYellowCardsWorkAround('', statsDataMock);

      expect(result).toEqual({
        away: { id: '1394', providerId: 'c8h9bw1l82s06h77xxrelzhur', periods: { total: { redCards: 0 } } },
        home: { id: '897', providerId: '4dsgumo7d4zupm2ugsvm4zm4d', periods: { total: { redCards: 1 } } }
      } as any);
    });

    it('should return 1 red card for away team when player has 1 red card', () => {
      statsDataMock.players.away['5352'].cards.red = 1;
      const result = service.getRedCardsByTeamWithYellowCardsWorkAround('', statsDataMock);

      expect(result).toEqual({
        away: { id: '1394', providerId: 'c8h9bw1l82s06h77xxrelzhur', periods: { total: { redCards: 1 } } },
        home: { id: '897', providerId: '4dsgumo7d4zupm2ugsvm4zm4d', periods: { total: { redCards: 0 } } }
      } as any);
    });

    it('should return 2 red cards for both teams when player has 1 red card in both team', () => {
      statsDataMock.players.away['5352'].cards.red = 1;
      statsDataMock.players.home['33394'].cards.red = 1;
      const result = service.getRedCardsByTeamWithYellowCardsWorkAround('', statsDataMock);

      expect(result).toEqual({
        away: { id: '1394', providerId: 'c8h9bw1l82s06h77xxrelzhur', periods: { total: { redCards: 1 } } },
        home: { id: '897', providerId: '4dsgumo7d4zupm2ugsvm4zm4d', periods: { total: { redCards: 1 } } }
      } as any);
    });

    it('should return 1 red card for away team when player has 2 yellow cards in away team', () => {
      statsDataMock.players.away['5352'].cards.yellow = 2;
      const result = service.getRedCardsByTeamWithYellowCardsWorkAround('', statsDataMock);

      expect(result).toEqual({
        away: { id: '1394', providerId: 'c8h9bw1l82s06h77xxrelzhur', periods: { total: { redCards: 1 } } },
        home: { id: '897', providerId: '4dsgumo7d4zupm2ugsvm4zm4d', periods: { total: { redCards: 0 } } }
      } as any);
    });

    it('should return 1 red card for home team when player has 2 yellow cards in home team', () => {
      statsDataMock.players.home['33394'].cards.yellow = 2;
      const result = service.getRedCardsByTeamWithYellowCardsWorkAround('', statsDataMock);

      expect(result).toEqual({
        away: { id: '1394', providerId: 'c8h9bw1l82s06h77xxrelzhur', periods: { total: { redCards: 0 } } },
        home: { id: '897', providerId: '4dsgumo7d4zupm2ugsvm4zm4d', periods: { total: { redCards: 1 } } }
      } as any);
    });

    it('should return 2 red cards for both teams when player has 2 yellow cards in both team', () => {
      statsDataMock.players.away['5352'].cards.yellow = 2;
      statsDataMock.players.home['33394'].cards.yellow = 2;
      const result = service.getRedCardsByTeamWithYellowCardsWorkAround('', statsDataMock);

      expect(result).toEqual({
        away: { id: '1394', providerId: 'c8h9bw1l82s06h77xxrelzhur', periods: { total: { redCards: 1 } } },
        home: { id: '897', providerId: '4dsgumo7d4zupm2ugsvm4zm4d', periods: { total: { redCards: 1 } } }
      } as any);
    });
  });
});

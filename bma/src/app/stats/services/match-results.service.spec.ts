import { MatchResultsService } from '@app/stats/services/match-results.service';
import { of as observableOf } from 'rxjs';
import { IStatsSeasons } from '@app/stats/models';

describe('MatchResultsService', () => {
  let service: MatchResultsService;
  let statsPointsProvider, timeService, commandService;
  let today: number;
  let currentPeriod;

  beforeEach(() => {
    today = Date.now();
    currentPeriod = {
      startDate: new Date(today - 1000),
      endDate: new Date(today + 1000)
    };

    statsPointsProvider = {
      leagueTableCompetitionSeason: jasmine.createSpy('leagueTableCompetitionSeason').and
        .returnValue(observableOf({
          sportId: '1',
          areaId: '2',
          competitionId: '3',
          ...currentPeriod
        } as any)),
      leagueTableSeasons: jasmine.createSpy('leagueTableSeasons').and
        .returnValue(observableOf([{
          startDate: new Date(today - 3000),
          endDate: new Date(today - 1000)
        } as any,
          currentPeriod])),
      seasonMatches: jasmine.createSpy('seasonMatches').and
        .returnValue(observableOf({})),
      statsCentrePlayers: jasmine.createSpy('statsCentrePlayers').and
        .returnValue(observableOf([{
          id: '2',
          'Last name': {
            value: 'Crawn'
          }
        } as any])),
      matchesByDate: jasmine.createSpy('matchesByDate').and.returnValue(observableOf([{ id: 1 }]))
    } as any;

    timeService = {
      getTodayTomorrowOrDate: jasmine.createSpy('getTodayTomorrowOrDate').and.returnValue('Today')
    } as any;

    commandService = {
      register: jasmine.createSpy('register').and.callFake((arg: string, cb: Function) => cb('1', 2, 3)),
      API: {
        GET_SEASON: 'get_season',
        GET_MATCHES_BY_SEASON: 'get_matches_by_season',
        GET_RESULTS_BY_PAGE: 'get_results_by_page',
        GET_MATCHES_BY_DATE: 'get_matches_by_date'
      }
    } as any;

    service = new MatchResultsService(statsPointsProvider, timeService, commandService);
  });

  it('static propetry check', () => {
    expect(MatchResultsService.STEP).toBe(7);
  });

  it('#registerCommand should set listeners to events', () => {
    service['getMatchesByDate'] = jasmine.createSpy('getMatchesByDate').and.returnValue(observableOf([]));
    service.registerCommand();
    expect(commandService.register).toHaveBeenCalledWith('get_season', jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith('get_matches_by_season', jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith('get_results_by_page', jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith('get_matches_by_date', jasmine.any(Function));
  });

  describe('#getSeason', () => {
    it('there is current season (startDate < today < endDate)', () => {
      service.getSeason('1', '2', '3').subscribe((data: IStatsSeasons | {}) => {
        expect(data).toEqual({
          startDate: new Date(today - 1000),
          endDate: new Date(today + 1000)
        } as any);
      });
    });

    it('there is no current season, the last should be chosen', () => {
      const season1 = {
        id: 1,
        startDate: 123,
        endDate: 321
      } as any;
      const season2 = {
        id: 2,
        startDate: 456,
        endDate: 654
      } as any;
      statsPointsProvider.leagueTableSeasons.and.returnValue(observableOf([season1, season2]));

      service.getSeason('1', '2', '3').subscribe((season: IStatsSeasons) => {
        expect(season).toEqual(season2);
      });
    });

    it('there is no season at all, null should be returned', () => {
      statsPointsProvider.leagueTableSeasons.and.returnValue(observableOf(undefined));
      service.getSeason('1', '2', '3').subscribe((season: IStatsSeasons) => {
        expect(season).toEqual(null);
      });
    });
    it('no competitionId', () => {
      (statsPointsProvider.leagueTableCompetitionSeason as jasmine.Spy).and
          .returnValue(observableOf({
            sportId: '1',
            areaId: '2',
            ...currentPeriod,
            status: 'failed'
          } as any));
      service.getSeason('1', '2', '3').subscribe(() => {}, err => {
        expect(err).toBe('failed');
      });
    });

    it('no areaId', () => {
      (statsPointsProvider.leagueTableCompetitionSeason as jasmine.Spy).and
        .returnValue(observableOf({
          sportId: '1',
          ...currentPeriod,
          status: 'failed'
        } as any));
      service.getSeason('1', '2', '3').subscribe(() => {}, err => {
        expect(err).toBe('failed');
      });
    });

    it('no sportId', () => {
      (statsPointsProvider.leagueTableCompetitionSeason as jasmine.Spy).and
        .returnValue(observableOf({
          ...currentPeriod,
          status: 'failed'
        } as any));
      service.getSeason('1', '2', '3').subscribe(() => {}, err => {
        expect(err).toBe('failed');
      });
    });
  });

  it('#getMatchesBySeasonByPage should form data from response', () => {
    const mockData = [{ id: 1 }, { id: 2 }] as any;
    service['getGoalScorersIds'] = jasmine.createSpy('getGoalScorersIds').and.returnValue(mockData);
    service['getPlayerDetails'] = jasmine.createSpy('getPlayerDetails').and.returnValue(mockData);
    service['createResultsFromGoalString'] = jasmine.createSpy('createResultsFromGoalString');
    service['groupByDate'] = jasmine.createSpy('groupByDate').and.callFake(res => res);

    service.getMatchesBySeasonByPage('1', 2, 2).subscribe(() => {
      expect(service['getGoalScorersIds']).toHaveBeenCalledWith({} as any);
      expect(service['getPlayerDetails']).toHaveBeenCalledWith(mockData);
      expect(service['createResultsFromGoalString']).toHaveBeenCalledTimes(2);
      expect(service['groupByDate']).toHaveBeenCalledWith({ showButton: true, matches: mockData });
    });
  });

  it('#getPage, private #getDateStrting, #create should create ui model for page due to STEP', () => {
    expect(service.getPage(3).length).toBe(MatchResultsService.STEP);
    expect(timeService.getTodayTomorrowOrDate).toHaveBeenCalledWith(jasmine.any(Date), false, false);
  });

  it('#getMatchesByDate should get array of matches results, private #sortByDisplayOrder', () => {
    service['getGoalScorersIds'] = jasmine.createSpy('getGoalScorersIds').and.callFake(res => res);
    service['getPlayerDetails'] = jasmine.createSpy('getPlayerDetails').and.returnValue([{
      id: 7, lastName: 'Wilson'
    }] as any);
    service['groupByCompetition'] = jasmine.createSpy('groupByCompetition').and.returnValue([{
      id: 1,
      displayOrder: 2
    }, {
      id: 2,
      displayOrder: 1
    }] as any);

    service.getMatchesByDate(new Date()).subscribe(res => {
      expect(statsPointsProvider.matchesByDate).toHaveBeenCalledWith({
        startdate: jasmine.any(String),
        enddate: jasmine.any(String)
      });
      expect(service['getGoalScorersIds']).toHaveBeenCalledWith([{ id: 1 }] as any);
      expect(service['getPlayerDetails']).toHaveBeenCalledWith([{ id: 1 }] as any);
      expect(service['groupByCompetition']).toHaveBeenCalledWith([{ id: 7, lastName: 'Wilson' }] as any);
      expect(res).toEqual([{
        id: 2,
        displayOrder: 1
      } as any, {
        id: 1,
        displayOrder: 2
      } as any]);
    });
  });

  describe('#getPlayerDetails should get player details', () => {
    beforeEach(() => {
      service['createGoalScorerStr'] = jasmine.createSpy('createGoalScorerStr').and
        .returnValue('PlayerName 11:30,12:44');
    });
    it('no goalScorerIds', () => {
      service['getPlayerDetails']({ matches: [{ id: '11' }] } as any);
      expect(service['createGoalScorerStr']).not.toHaveBeenCalled();
    });

    it('goalScorerIds empty', () => {
      service['getPlayerDetails']({ matches: [{ id: '11' }] } as any);
      expect(service['createGoalScorerStr']).not.toHaveBeenCalled();
    });

    it('goalScorerIds exist', () => {

      const matchesWithGoalScorers = {
        goalScorerIds: [ '1', '2' ],
        matches: [{
          id: 11,
          teamA: { goals: { playerID: '5' } },
          teamB: { goals: { playerID: '2' } }
        }]
      } as any;

      const result =  [{
        id: 11,
        teamA: { goals: { playerID: '5' }, goalScorers: 'PlayerName 11:30,12:44' },
        teamB: { goals: { playerID: '2' }, goalScorers: 'PlayerName 11:30,12:44' }
      }] as any;

      expect(service['getPlayerDetails'](matchesWithGoalScorers)).toEqual(result);
    });
  });

  it('#groupByDate should group matches by date, private #getDateStrting does formatting', () => {
    const matchesObj = {
      matches: [{ id: '1', date: today },
                { id: '4', date: today },
                { id: '6', date: today }]
    } as any;
    const result = {
        'Today': [{ id: '1', date: today, correctionDate: 'Today' },
                  { id: '4', date: today, correctionDate: 'Today' },
                  { id: '6', date: today, correctionDate: 'Today' }]
    } as any;
    expect(service['groupByDate'](matchesObj)).toEqual({ showButton: undefined, matches: result });
    expect(timeService.getTodayTomorrowOrDate).toHaveBeenCalledWith(jasmine.any(Date), false, false);

    // showButton exists
    matchesObj.showButton = true;
    result['Today'] = [{ id: '1', date: today, correctionDate: 'Today' },
                      { id: '4', date: today, correctionDate: 'Today' }];
    expect(service['groupByDate'](matchesObj)).toEqual({ showButton: true, matches: result });
  });

  it('#groupByCompetition & #createResultsFromGoalString grouping matches by competition', () => {
    const matches = [{
      teamA: {},
      teamB: {},
      competition: { id: '1', name: 'UEFA', displayOrder: 0 }
    } as any, {
      result: {},
      teamA: {},
      teamB: {},
      competition: { id: '2', name: 'Champ', displayOrder: 1 }
    } as any, {
      result: { fullTime: { value: '1:2' } },
      teamA: {},
      teamB: {},
      competition: { id: '1', name: 'UEFA', displayOrder: 0 }
    } as any];

    const result = [{
        id: '1',
        name: 'UEFA',
        displayOrder: 0,
        matches: [{
          result: { fullTime: { value: '0:0' } },
          teamA: { score: '0' },
          teamB: { score: '0' },
          competition: { id: '1', name: 'UEFA', displayOrder: 0 }
        } as any, {
          result: { fullTime: { value: '1:2' } },
          teamA: { score: '1' },
          teamB: { score: '2' },
          competition: { id: '1', name: 'UEFA', displayOrder: 0 }
        } as any],
        opened: false
      } as any, {
      id: '2',
      name: 'Champ',
      displayOrder: 1,
      matches: [{
        result: { fullTime: { value: '0:0' } },
        teamA: { score: '0' },
        teamB: { score: '0' },
        competition: { id: '2', name: 'Champ', displayOrder: 1 }
      } as any],
      opened: false
    }];

    expect(service['groupByCompetition'](matches)).toEqual(result);
  });

  it('#getGoalScorersIds should get player ids (#getTeamGoals, #getPlayerNameFromGoalString)', () => {
    service['getGoalsByTeamByScore'] = jasmine.createSpy('getGoalsByTeamByScore').and
      .returnValue({ teamA: [{ id: '1' }], teamB: [{ id: '2' }] });
    const matches = [{
      teamA: {},
      teamB: {}
    }, {
      goals: [],
      teamA: {},
      teamB: {}
    }, {
      goals: [{ playerID: '2', team: '1' }, { playerID: '3', team: '2' }],
      teamA: {},
      teamB: {}
    }, {
      result: {}
    }, {
      result: {
        goalsString: ''
      }
    }, {
      result: {
        goalsString: '1:0 12:45 Brown, 1:1 12:54 Orphan'
      },
      teamA: {},
      teamB: {}
    }] as any;
    const matchesResult = {
      matches: [{
        teamA: {},
        teamB: {}
      }, {
        goals: [],
        teamA: {},
        teamB: {}
      }, {
        goals: [{ playerID: '2', team: '1' }, { playerID: '3', team: '2' }],
        teamA: {
          goals: [{ playerID: '2', team: '1' }]
        },
        teamB: {
          goals: [{ playerID: '3', team: '2' }]
        }
      }, {
        result: {}
      }, {
        result: {
          goalsString: '',
        }
      }, {
        result: {
          goalsString: '1:0 12:45 Brown, 1:1 12:54 Orphan',
        },
        teamA: {
          goals: [{ id: '1' }]
        },
        teamB: {
          goals: [{ id: '2' }]
        }
      }],
    goalScorerIds: ['2', '3']} as any;

    expect(service['getGoalScorersIds'](matches)).toEqual(matchesResult);
  });

  it('#getGoalsByTeamByScore should gets goals for teams by score', () => {
    let goals = [{
      score: '1:2'
    }, {
      score: '0:4'
    }, {
      score: '4:0'
    }, {
      score: '2:2'
    }] as any;

    expect(service['getGoalsByTeamByScore'](goals)).toEqual({
      teamA: [{ score: '4:0' } ],
      teamB: [{ score: '1:2' }, { score: '0:4'}, { score: '2:2'}]
    } as any);

    goals = [{
      score: '2:1'
    }, {
      score: '3:0'
    }] as any;

    expect(service['getGoalsByTeamByScore'](goals)).toEqual({
      teamA: [{ score: '2:1' }, { score: '3:0' } ],
      teamB: []
    } as any);
  });

  it('#createGoalScorerStr should create goal scorer string', () => {
    const teamGoals = [{
      playerName: 'Petro',
      time: '04:45'
    }, {
      playerName: 'Petro',
      time: '20:34'
    }, {
      playerName: 'Ivan',
      time: '62:45'
    }, {
      playerName: 'Vasyl',
      time: '12:45'
    }] as any;

    expect(service['createGoalScorerStr'](teamGoals)).toBe('Petro 04:45\', 20:34\', Ivan 62:45\', Vasyl 12:45\'');
  });
});

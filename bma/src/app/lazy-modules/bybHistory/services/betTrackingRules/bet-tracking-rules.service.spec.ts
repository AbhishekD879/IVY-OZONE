import { BetTrackingRulesService } from '@lazy-modules/bybHistory/services/betTrackingRules/bet-tracking-rules.service';
import { IBybSelection } from '@lazy-modules/bybHistory/models/byb-selection.model';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';
import {
  IScoreboardStatsUpdate,
  IScoreByTeams,
} from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';
import {
  DOUBLE_TEAMS,
  TEAMS, STATUSES
} from '@lazy-modules/bybHistory/constants/byb-5aside-markets-config.constant';
import { PLAYER_STATS } from '@lazy-modules/bybHistory/services/betTrackingRules/stat-category-utility.service';
import { scoreboardsStatsUpdate } from '@lazy-modules/bybHistory/services/bybSelectionsService/scoreboards-stats-update.mock';

describe('BetTrackingRulesService', () => {
  let service: BetTrackingRulesService;
  let statCategoryUtilityService;
  let windowRefService;
  let statsDataMock, selection, update, goalsObj;

  beforeEach(() => {
    statCategoryUtilityService = {
      getScore: jasmine.createSpy('getScore').and.returnValue({ total: 1}),
      getCurrentPeriod: jasmine.createSpy('getCurrentPeriod').and.returnValue('1h'),
      getHomeAwayTeamByContestantId: jasmine.createSpy('getHomeAwayTeamByContestantId').and.returnValue('Home'),
      getPlayerById: jasmine.createSpy('getPlayerById'),
      getDoubleHomeAwayTeamByContestantId: jasmine.createSpy('getDoubleHomeAwayTeamByContestantId').
        and.returnValue(DOUBLE_TEAMS.HOME_OR_DRAW),
      getAllGoals: jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
      } as any]),
      getPlayerStats: jasmine.createSpy('getPlayerStats'),
      applyHandicapValue: jasmine.createSpy('applyHandicapValue'),
      getCardIndex: jasmine.createSpy('getCardIndex'),
      getCardsFromPlayers: jasmine.createSpy('getCardsFromPlayers'),
      getBookingPoints: jasmine.createSpy('getBookingPoints'),
      getPlayerByName: jasmine.createSpy('getPlayerByName'),
      getPlayerFromNameId: jasmine.createSpy('getPlayerFromNameId')
    };

    windowRefService = {
      nativeWindow: {
        localStorage: {
          getItem: jasmine.createSpy('getItem').and.returnValue({})
        }
      }
    };

    selection = {
      config: {
        period: 'total',
        generalInformationRequired: 'teams',
        statCategory: 'Corners'
      },
      part: {
        outcome: [{
          name: '', // Home | Away | Draw
          externalStatsLink: {
            statCategory: 'Corners',
            statValue: '' // > | >= | <
          }
        }]
      }
    };

    goalsObj = {
      score: {
        total: {
          home: 1,
          away: 2
        },
        '1h': {
          home: 0,
          away: 0
        },
        '2h': {
          home: 1,
          away: 2
        }
      },
      away: {
        id: '1',
        providerId: 'away'
      },
      home: {
        id: '1',
        providerId: 'home'
      }
    };

    update = {
      home: { id: 'Home', providerId: 'home', name: 'home' },
      away: { id: 'Away', providerId: 'away', name: 'away' },
      period: '1h',
      teams: {
        home: {
          total: { corners: 0 },
          '1h': { corners: 0 },
          '2h': { corners: 0 }
        },
        away: {
          total: { corners: 0 },
          '1h': { corners: 0 },
          '2h': { corners: 0 }
        }
      }
    };

    statsDataMock = JSON.parse(JSON.stringify(scoreboardsStatsUpdate));

    service = new BetTrackingRulesService(statCategoryUtilityService, windowRefService);
  });

  it('winHalvesStatusHandler - should not return any status in case no period were found', () => {
    const update_2 = JSON.parse(JSON.stringify(update));
    delete update_2.period;
    service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
    expect(service.winHalvesStatusHandler(selection, update_2)).toEqual({ status: '' });
  });

  it('winHalvesStatusHandler - should not return any status in case no 1st period data were found', () => {
    const update_2 = JSON.parse(JSON.stringify(update));
    service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue({ score: { total: {}}});
    expect(service.winHalvesStatusHandler(selection, update_2)).toEqual({ status: '' });
  });

  it('winHalvesStatusHandler - should not return any status in case no score data were found', () => {
    const update_2 = JSON.parse(JSON.stringify(update));
    service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue({ score: {}});
    expect(service.winHalvesStatusHandler(selection, update_2)).toEqual({ status: '' });
  });

  describe('winHalvesStatusHandler', () => {
    let status;
    let bet;
    beforeEach(() => {
      bet = { settled: 'N' } as any;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
    });

    it('should not return any status in case no team were found', () => {
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(null);
      status = '';
    });

    it(`should work even not data for 2h`, () => {
      status = 'Losing';

      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      delete goalsObj.score['2h'];
    });

    describe('WinBoth', () => {
      beforeEach(() => {
        selection.config.isBoth = true;
      });

      describe(`should return LOSE`, () => {
        beforeAll(() => {
          status = 'Lose';
        });

        it(`if period is '2h' and lose first half`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
        });

        it(`if period is 'total' and lose 1h`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('total');
        });

        it(`if period is 'total' and lose 2h`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('total');
          goalsObj.score['1h'].home = 3;
        });
      });

      describe(`should return Won`, () => {
        beforeAll(() => {
          status = 'Won';
        });

        beforeEach(() => {
          goalsObj.score['1h'].home = 3;
          goalsObj.score['2h'].home = 3;
        });

        it(`if period is 'total' and won 1h and 2h`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('total');
        });
      });

      describe('should return Losing', () => {
        beforeAll(() => {
          status = 'Losing';
        });

        it(`if period is '1h'`, () => {
          goalsObj.score['1h'].away = 3;
        });

        it(`if period is '2h' and won 1h and losing 2h`, () => {
          goalsObj.score['1h'].home = 3;
          goalsObj.score['2h'].away = 3;
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
        });
      });

      describe('should return Winning', () => {
        beforeAll(() => {
          status = 'Winning';
        });

        it(`if period is '2h' and Bet is Not Settled and winning 2h`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
          goalsObj.score['1h'].home = 3;
          goalsObj.score['2h'].home = 3;
        });
      });
    });

    describe('WinEitherHalf', () => {
      beforeEach(() => {
        selection.config.isBoth = false;
      });
      describe(`should return LOSE`, () => {
        beforeAll(() => {
          status = 'Lose';
        });

        it(`if period is 'total' and lose both half`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('total');
        });
      });

      describe(`should return Won`, () => {
        beforeAll(() => {
          status = 'Won';
        });

        it(`if period is '2h' and Won 1h`, () => {
          goalsObj.score['1h'].home = 3;
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
        });

        it(`if period is 'total' and won 1h`, () => {
          goalsObj.score['1h'].home = 3;
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('total');
        });

        it(`if period is 'total' and won 2h`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('total');
          goalsObj.score['2h'].home = 3;
        });
      });

      describe('should return Losing', () => {
        beforeAll(() => {
          status = 'Losing';
        });

        it(`if period is '1h' and is losing`, () => {
          goalsObj.score['1h'].away = 3;
        });

        it(`if period is '2h' and lose 1h and losing 2h`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
          goalsObj.score['1h'].away = 3;
          goalsObj.score['2h'].away = 3;
        });
      });

      describe('should return Winning', () => {
        beforeAll(() => {
          status = 'Winning';
        });

        it(`if period is '1h' and winning it`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
          goalsObj.score['1h'].home = 3;
        });

        it(`if period is '2h' and lose 1h Bet and winning 2h`, () => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
          goalsObj.score['1h'].away = 3;
          goalsObj.score['2h'].home = 3;
        });
      });
    });

    afterEach(() => {
      expect(service.winHalvesStatusHandler(selection, update)).toEqual({ status });
    });
  });

  describe('cleanSheetStatusHandler', () => {
    it('should handle cleanSheetStatusHandler market status', () => {
      goalsObj.score.total.away = 0;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
      service['getTeamByExternalStatsLink'] = jasmine.createSpy('getTeamByExternalStatsLin').and.returnValue('HOME');
      const bet = { settled: 'Y'} as any;
      expect(service.cleanSheetStatusHandler(selection, update)).toEqual({status: 'Winning'});

      goalsObj.score.total.away = 2;
      expect(service.cleanSheetStatusHandler(selection, update)).toEqual({status: 'Lose'});

      goalsObj.score.total.home = 0;
      service['getTeamByExternalStatsLink'] = jasmine.createSpy('getTeamByExternalStatsLin').and.returnValue('AWAY');
      bet.settled = '';
      expect(service.cleanSheetStatusHandler(selection, update)).toEqual({status: 'Winning'});

      goalsObj = {};
      service['getTeamByExternalStatsLink'] = jasmine.createSpy('getTeamByExternalStatsLin').and.returnValue('AWAY');
      bet.settled = '';
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
      expect(service.cleanSheetStatusHandler(selection, update)).toEqual({status: ''});
    });
  });

  describe('totalGoalsStatusHandler', () => {
    let bet, selectionObj;
    beforeEach(() => {
      bet = {
        settled: 'N'
      } as IBetHistoryBet;

      selectionObj = {
        config: {
          statCategory: 'Score',
          generalInformationRequired: 'teams',
          hasLine: true,
          period: 'total'
        },
        part: {
          outcome: [{
            externalStatsLink: {
              statValue: '>3.5',
              statCategory: 'Score',
              contestantId: 'away'
            }
          }]
        }
      } as any;

      statCategoryUtilityService.getScore.and.returnValue(goalsObj);
    });

    it('should return prePlay2h when 1st for 2nd half status', () => {
      selection.config.period = '2h';
      selection.betCompletion = false;
      statsDataMock.period = '1h';
      const actualResult = service.totalGoalsStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate, bet);
      expect(actualResult).toEqual({ status: 'prePlay2h' });
    });

    it('should handle PARTICIPANT_2 TOTAL GOALS market status when selection is OVER X.Y and period exists', () => {
      selectionObj.betCompletion = true;
      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Losing', progress: { current: 2, target: 4, desc: '2 of 4 Goals' }});
    });

    it('should handle return status empty if no current period in the update', () => {
      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, {} as any, bet);

      expect(actualResult).toEqual({ status: '' });
    });

    it('should handle PARTICIPANT_2 2ND HALF TOTAL GOALS market status when selection' +
      'is OVER X.Y and current period is 1h', () => {
      goalsObj.score = {
        total: {
          home: 1,
          away: 2
        },
        '1h': {
          home: 1,
          away: 2
        }
      } as any;
      selectionObj.config.period = '2h';
      statCategoryUtilityService.getScore.and.returnValue(goalsObj);
      update.period = '2h';

      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Losing', progress: { current: 0, target: 4, desc: '0 of 4 Goals' }});
    });

    it('should handle PARTICIPANT_2 TOTAL GOALS market status when selection is UNDER X.Y and period exists', () => {
      selectionObj.part.outcome[0].externalStatsLink.statValue = '<3.5';
      selectionObj.betCompletion = true;
      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Winning', progress: { current: 2, target: 3, desc: '2 of 3 Goals' }});
    });

    it('should handle 2ND HALF PARTICIPANT_1 TOTAL GOALS market status when selection is EQUAL X and period exists(2h)', () => {
      selectionObj.config.period = '2h';
      update.period = '2h';
      selectionObj.part.outcome[0].externalStatsLink.statValue = '=3';
      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Losing', progress: { current: 2, target: 3, desc: '2 of 3 Goals' }});
    });

    it('should handle 2ND HALF preplay during first half', () => {
      selectionObj.config.period = '2h';
      update.period = '1h';
      selectionObj.part.outcome[0].externalStatsLink.statValue = '=3';
      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'prePlay2h'});
    });

    it('should handle PARTICIPANT_2 2ND HALF TOTAL GOALS market status when selection' +
      'is OVER X.Y and period exists(2h)', () => {
      selectionObj.config.period = '2h';
      update.period = '2h';
      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Losing', progress: { current: 2, target: 4, desc: '2 of 4 Goals' }});
    });

    it('should handle PARTICIPANT_2 1ST HALF TOTAL GOALS market status when selection' +
      'is OVER X.Y and current period is 1h', () => {
      selectionObj.config.period = '1h';

      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Losing', progress: { current: 0, target: 4, desc: '0 of 4 Goals' }});
    });

    it('should handle PARTICIPANT_2 1ST HALF TOTAL GOALS market status when selection' +
      'is UNDER X.Y and current period is 1h', () => {
      selectionObj.config.period = '1h';
      selectionObj.part.outcome[0].externalStatsLink.statValue = '<3.5';

      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Winning', progress: { current: 0, target: 3, desc: '0 of 3 Goals' }});
    });

    it('should handle 1ST HALF PARTICIPANT_2 TOTAL GOALS market status when selection' +
      'is EQUAL X and current period is 1h', () => {
      selectionObj.config.period = '1h';
      selectionObj.betCompletion = true;
      selectionObj.part.outcome[0].externalStatsLink.statValue = '=3';

      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Losing', progress: { current: 0, target: 3, desc: '0 of 3 Goals' }});
    });

    it('should handle 1ST HALF PARTICIPANT_1 TOTAL GOALS market status when selection is EQUAL X and current period' +
      'is 1h and selection is home', () => {
      selectionObj.config.period = '1h';
      selectionObj.part.outcome[0].externalStatsLink.statValue = '=3';
      selectionObj.part.outcome[0].externalStatsLink.contestantId = 'home';

      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Losing', progress: { current: 0, target: 3, desc: '0 of 3 Goals' }});
    });

    it('should handle 2ND HALF TOTAL GOALS market status when selection is UNDER X.Y and current period' +
      'is 2h and selection is total', () => {
      selectionObj.config.period = '2h';
      update.period = '2h';
      selectionObj.part.outcome[0].externalStatsLink.statValue = '<3.5';
      selectionObj.part.outcome[0].externalStatsLink.contestantId = undefined;
      selectionObj.betCompletion = true;

      const actualResult = service.totalGoalsStatusHandler(selectionObj as IBybSelection, update as IScoreboardStatsUpdate, bet);

      expect(actualResult).toEqual({ status: 'Winning', progress: { current: 3, target: 3, desc: '3 of 3 Goals' }});
    });
  });

  describe('matchBettingStatusHandler', () => {
    it('should return empty status when no team were found', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(null);
      const actualResult = service.matchBettingStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return prePlay2h when 1st for 2nd half status', () => {
      selection.config.period = '2h';
      selection.betCompletion = false;
      statsDataMock.period = '1h';
      const actualResult = service.matchBettingStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );
      expect(actualResult).toEqual({ status: 'prePlay2h' });
    });

    it('should return empty status when no scores were found', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(null);
      const actualResult = service.matchBettingStatusHandler(
        selection,
        { score: {} } as any
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status when no current period was found', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(null);
      const actualResult = service.matchBettingStatusHandler(
        selection,
        { period: undefined } as any
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should handle matchBetting market status(Total period)', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
      selection = { config: { period: 'total' } } as IBybSelection;
      const actualResult = service.matchBettingStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle matchBetting market status(2nd half period)', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
      selection = { config: { period: '2h' } } as IBybSelection;
      const actualResult = service.matchBettingStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle matchBetting market status(1st half period)', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
      selection = { config: { period: '1h' } } as IBybSelection;
      const actualResult = service.matchBettingStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });
  });

  describe('bothTeamsToScoreStatusHandler', () => {
    let scoreObj;

    beforeEach(() => {
     scoreObj = { score: {
        '1h': { home: 0, away: 0 },
        '2h': { home: 0, away: 0 },
        total: { home: 0, away: 0 },
      }};
    });

    it('should return no status if no score data available', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue({ score: {} });

      expect(service['bothTeamsToScoreStatusHandler'](selection, update)).toEqual({status:''});
    });

    it('should return Loosing', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      expect(service['bothTeamsToScoreStatusHandler'](selection, update)).toEqual({status:'Losing'});
    });

    it('should return Winning', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service['bothTeamsToScoreStatusHandler'](selection, update)).toEqual({status:'Winning'});
    });

    it('should return WON if total > 0 for both teams', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      scoreObj.score.total.away = 1;
      scoreObj.score.total.home = 1;
      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      expect(service['bothTeamsToScoreStatusHandler'](selection, update)).toEqual({status:'Won'});
    });

    it('should return Lose if total > 0 for both teams', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      scoreObj.score.total.away = 1;
      scoreObj.score.total.home = 1;
      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service['bothTeamsToScoreStatusHandler'](selection, update)).toEqual({status:'Lose'});
    });
  });


  describe('bothTeamsToScoreByHalvesStatusHandler', () => {
    let scoreObj;

    beforeEach(() => {
     scoreObj = { score: {
        '1h': { home: 0, away: 0 },
        '2h': { home: 0, away: 0 },
        total: { home: 0, away: 0 },
      }};
    });

    it('should call bothTeamsHalfScoredStatus', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      selection.config.period = '1h';
      selection.betCompletion = true;
      service['bothTeamsHalfScoredStatus'] = jasmine.createSpy('bothTeamsHalfScoredStatus');

      service.bothTeamsToScoreByHalvesStatusHandler(selection, update);
      expect(service['getStatCategoryObj']).toHaveBeenCalledWith(selection, update);
      expect(service['bothTeamsHalfScoredStatus']).toHaveBeenCalledWith(scoreObj.score, update, selection);
    });

    it('should return prePlay2h when 1st for 2nd half status', () => {
      selection.config.period = '2h';
      selection.betCompletion = false;
      statsDataMock.period = '1h';
      const actualResult = service.bothTeamsToScoreByHalvesStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate);
      expect(actualResult).toEqual({ status: 'prePlay2h' });
    });

    it('should call bothTeamsBothHalves', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      selection.config.period = 'total';
      selection.betCompletion = true;
      service['bothTeamsBothHalves'] = jasmine.createSpy('bothTeamsBothHalves');

      service.bothTeamsToScoreByHalvesStatusHandler(selection, update);
      expect(service['getStatCategoryObj']).toHaveBeenCalledWith(selection, update);
      expect(service['bothTeamsBothHalves']).toHaveBeenCalledWith(scoreObj.score, update, selection);
    });
  });

  describe('redCardsStatusHandler', () => {
    it('should call getFullRedsStatus', () => {
      const cardsObj = {away: {periods: {total: {redCards: 2}}}, home: {periods: {total: {redCards: 1}}}};
      selection.part.outcome[0].name = 'YES';
      selection.config = {period: 'total'};
      update.period = 'ert';
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(cardsObj);
      service['getFullRedsStatus'] = jasmine.createSpy('getFullRedsStatus');
      service['getTotalRedCardsStatus'] = jasmine.createSpy('getTotalRedCardsStatus');

      service.redCardsStatusHandler(selection, update);
      expect(service['getFullRedsStatus']).toHaveBeenCalledWith('YES', cardsObj as any, 'total', 'ert');
    });

    it('should returrn empty status (no home periods)', () => {
      const cardsObj = {away: {periods: {total: {redCards: 2}}}, home: {}};
      update.period = 'ert';
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(cardsObj);
      const result = service.redCardsStatusHandler(selection, update);
      expect(result).toEqual({status: ''});
    });

    it('should returrn empty status (no away periods)', () => {
      const cardsObj = {away: {periods: {total: {redCards: 2}}}, home: {}};
      update.period = 'ert';
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(cardsObj);
      const result = service.redCardsStatusHandler(selection, update);
      expect(result).toEqual({status: ''});
    });

    it('should returrn empty status (no update periods)', () => {
      const cardsObj = {away: {periods: {total: {redCards: 2}}}, home: {periods: {total: {redCards: 1}}}};
      update.period = null;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(cardsObj);
      const result = service.redCardsStatusHandler(selection, update);
      expect(result).toEqual({status: ''});
    });
  });

  describe('redCardsParticipantStatusHandler', () => {
    it('should call getRedCardsParticipantStatus based on participant ID', () => {
      const cardsObj = {away: {periods: {total: {redCards : 2}}}, home: {periods: {total: {redCards : 1}}}};
      selection.part.outcome[0].name = 'YES';
      selection.part.outcome[0].externalStatsLink.contestantId = '123';
      update.away.providerId = '123';
      update.players = {
        home: {},
        away: {}
      };
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(cardsObj);
      service['getFullRedsStatus'] = jasmine.createSpy('getFullRedsStatus');
      service['getRedCardsParticipantStatus'] = jasmine.createSpy('getRedCardsParticipantStatus');

      service.redCardsParticipantStatusHandler(selection, update);
      expect(service['getRedCardsParticipantStatus']).toHaveBeenCalledWith(2, true);
    });

    it('should call getRedCardsParticipantStatus based on participant ID', () => {
      const cardsObj = {away: {periods: {total: {redCards : 2}}}, home: {periods: {total: {redCards : 1}}}};
      selection.part.outcome[0].name = 'YES';
      selection.part.outcome[0].externalStatsLink.contestantId = '456';
      update.home.providerId = '456';
      update.players = {
        home: {},
        away: {}
      };
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(cardsObj);
      service['getFullRedsStatus'] = jasmine.createSpy('getFullRedsStatus');
      service['getRedCardsParticipantStatus'] = jasmine.createSpy('getRedCardsParticipantStatus');

      service.redCardsParticipantStatusHandler(selection, update);
      expect(service['getRedCardsParticipantStatus']).toHaveBeenCalledWith(1, true);
    });

    it('should return empty status when update.players is not defined', () => {
      update.players = undefined;
      const bet = {} as any;
      const result = service.redCardsParticipantStatusHandler(selection, update);

      expect(result).toEqual({ status: '' });
    });


    it('should return empty status when update.players.home is not defined', () => {
      update.players = {
        home: undefined
      };
      const bet = {} as any;
      const result = service.redCardsParticipantStatusHandler(selection, update);

      expect(result).toEqual({ status: '' });
    });


    it('should return empty status when update.players.away is not defined', () => {
      update.players = {
        away: undefined
      };
      const bet = {} as any;
      const result = service.redCardsParticipantStatusHandler(selection, update);

      expect(result).toEqual({ status: '' });
    });
  });

  describe('cornersMatchBetStatusHandler', () => {
    beforeEach(() => {
      statCategoryUtilityService.getCorners = jasmine.createSpy('getCorners').and.callFake((info: string, upd: IScoreboardStatsUpdate) => {
       return  !info.includes('team') ? {} : {
          home: {
            total: { corners: upd.teams.home.total.corners },
            '1h': { corners: upd.teams.home['1h'].corners },
            '2h': { corners: upd.teams.home['2h'].corners }
          },
          away: {
            total: { corners: upd.teams.away.total.corners },
            '1h': { corners: upd.teams.away['1h'].corners },
            '2h': { corners: upd.teams.away['2h'].corners }
          }
        };
      });

      statCategoryUtilityService.getHomeAwayTeamByContestantId = jasmine.createSpy('getHomeAwayTeamByContestantId');
    });

    it('should not return any status in case no team were found', () => {
      selection.config.period = '1h';
      statCategoryUtilityService.getCurrentPeriod = jasmine.createSpy('getCurrentPeriod');
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(null);
      expect(service.cornersMatchBetStatusHandler(selection, update).status).toEqual('');
    });

    it('should handle return status empty if no current period in the update', () => {
      const update_2 = JSON.parse(JSON.stringify(update));
      delete update_2.period;
      const actualResult = service.cornersMatchBetStatusHandler(selection, update_2 as any);

      expect(actualResult).toEqual({ status: '' });
    });

    it('should handle return status empty if no stats for home team for market period', () => {
      statCategoryUtilityService.getCorners.and.callFake((info: string, upd: IScoreboardStatsUpdate) => {
        return  !info.includes('team') ? {} : {
          home: {
            '1h': { corners: upd.teams.home['1h'].corners },
            '2h': { corners: upd.teams.home['2h'].corners }
          },
          away: {
            total: { corners: upd.teams.away.total.corners },
            '1h': { corners: upd.teams.away['1h'].corners },
            '2h': { corners: upd.teams.away['2h'].corners }
          }
        };
      });
      const selection_2 = JSON.parse(JSON.stringify(selection));
      selection_2.config.period = 'total';
      const actualResult = service.cornersMatchBetStatusHandler(selection_2, update as any);

      expect(actualResult).toEqual({ status: '' });
    });

    it('should handle return status empty if no stats for away team for market period', () => {
      statCategoryUtilityService.getCorners.and.callFake((info: string, upd: IScoreboardStatsUpdate) => {
        return  !info.includes('team') ? {} : {
          home: {
            total: { corners: upd.teams.home.total.corners },
            '1h': { corners: upd.teams.home['1h'].corners },
            '2h': { corners: upd.teams.home['2h'].corners }
          },
          away: {
            '1h': { corners: upd.teams.away['1h'].corners },
            '2h': { corners: upd.teams.away['2h'].corners }
          }
        };
      });
      const selection_2 = JSON.parse(JSON.stringify(selection));
      selection_2.config.period = 'total';
      const actualResult = service.cornersMatchBetStatusHandler(selection_2, update as any);

      expect(actualResult).toEqual({ status: '' });
    });

    it('should handle return status empty if no stats for away team', () => {
      statCategoryUtilityService.getCorners.and.callFake((info: string, upd: IScoreboardStatsUpdate) => {
        return  !info.includes('team') ? {} : {
          home: {
            total: { corners: upd.teams.home.total.corners }
          }
        };
      });
      const actualResult = service.cornersMatchBetStatusHandler(selection, update as any);

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle return status empty if no stats for home team', () => {
      statCategoryUtilityService.getCorners.and.callFake((info: string, upd: IScoreboardStatsUpdate) => {
        return  !info.includes('team') ? {} : {
          away: {
            total: { corners: upd.teams.away.total.corners }
          }
        };
      });
      const actualResult = service.cornersMatchBetStatusHandler(selection, update as any);

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    describe('should process 1ST HALF', () => {
      beforeEach(() => {
        selection.config.period = '1h';
        statCategoryUtilityService.getCurrentPeriod = jasmine.createSpy('getCurrentPeriod');
      });

      describe('and return "Winning" in case', () => {
        beforeEach(() => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
        });

        it('is 1st Half and conditions match for Home Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Home');
          update.teams.home['1h'].corners = 1;
        });

        it('is 1st Half and conditions match for Away Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Away');
          update.teams.away['1h'].corners = 1;
        });

        it('is 1st Half and conditions match for Draw Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Draw');
        });

        afterEach(() => {
          expect(service.cornersMatchBetStatusHandler(selection, update).status).toEqual(STATUSES.WINNING);
        });
      });

      it('and return "Won" in case is 2nd Half and conditions match for Draw Team', () => {
        statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Draw');
        statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
        expect(service.cornersMatchBetStatusHandler(selection, update).status).toEqual(STATUSES.WON);
      });

      describe('and return "Losing" in case ', () => {
        beforeEach(() => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
        });

        it('is 1st Half and conditions do not match for Home Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Home');
        });

        it('is 1st Half and conditions do not match for Away Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Away');
        });

        it('is 1st Half and conditions do not match for Draw Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Draw');
          update.teams.away['1h'].corners = 1;
        });

        afterEach(() => {
          expect(service.cornersMatchBetStatusHandler(selection, update).status).toEqual(STATUSES.LOSING);
        });
      });

      describe('and return "Lose" in case', () => {
        it('2nd Half and conditions do not match for Away Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Away');
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
        });

        it('End Game and conditions do not match for Draw Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Draw');
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('total');
          update.teams.away['1h'].corners = 1;
        });

        afterEach(() => {
          expect(service.cornersMatchBetStatusHandler(selection, update).status).toEqual(STATUSES.LOSE);
        });
      });
    });

    describe('should process TOTAL | 2ND HALF', () => {
      describe('and return "Winning" in case', () => {
        it('conditions match for Home Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Home');
          update.teams.home.total.corners = 1;
        });

        it('conditions match for Away Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Away');
          update.teams.away.total.corners = 2;
        });

        it('conditions match for Draw Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Draw');
          selection.config.period = '2h';
        });

        afterEach(() => {
          expect(service.cornersMatchBetStatusHandler(selection, update).status).toEqual(STATUSES.WINNING);
        });
      });

      describe('and return "Losing" in case ', () => {
        it('conditions do not match for Home Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Home');
        });

        it('conditions do not match for Away Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Away');
        });

        it('conditions do not match for Draw Team', () => {
          statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Draw');
          update.teams.away.total.corners = 1;
        });

        afterEach(() => {
          expect(service.cornersMatchBetStatusHandler(selection, update).status).toEqual(STATUSES.LOSING);
        });
      });
    });

    it('should return "Loosing" in case no teams data', () => {
      selection.config.generalInformationRequired = 'player';
      expect(service.cornersMatchBetStatusHandler(selection, update).status).toEqual(STATUSES.LOSING);
    });
  });

  describe('totalCornersStatusHandler', () => {
    let bet: any;

    beforeEach(() => {
      bet = { settled: '' };

      statCategoryUtilityService.getCorners = jasmine.createSpy('getCorners').and.callFake((info: string, upd: IScoreboardStatsUpdate) => {
        return  !info.includes('team') ? {} : {
          home: {
            total: { corners: upd.teams.home.total.corners },
            '1h': { corners: upd.teams.home['1h'].corners },
            '2h': { corners: upd.teams.home['2h'].corners }
          },
          away: {
            total: { corners: upd.teams.away.total.corners },
            '1h': { corners: upd.teams.away['1h'].corners },
            '2h': { corners: upd.teams.away['2h'].corners }
          }
        };
      });
    });

    it('should return empty status if there is no update.period', () => {
      const update_2 = JSON.parse(JSON.stringify(update));
      delete update_2.period;
      const result = service.totalCornersStatusHandler(selection, update_2 as any, bet);
      expect(result).toEqual({ status: '' });
    });

    it('should return prePlay2h when 1st for 2nd half status', () => {
      selection.config.period = '2h';
      selection.betCompletion = false;
      statsDataMock.period = '1h';
      const actualResult = service.totalCornersStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate, bet);
      expect(actualResult).toEqual({ status: 'prePlay2h' });
    });

    it('should handle return status empty if no current period in the update', () => {
      const update_2 = JSON.parse(JSON.stringify(update));
      delete update_2.period;
      const actualResult = service.cornersMatchBetStatusHandler(selection, update_2 as any);

      expect(actualResult).toEqual({ status: '' });
    });

    describe('should process 1ST HALF', () => {
      beforeEach(() => {
        selection.config.period = '1h';
        statCategoryUtilityService.getCurrentPeriod = jasmine.createSpy('getCurrentPeriod');
      });

      describe('and return "Winning" in case', () => {
        beforeEach(() => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
        });

        it('bet not settled, is 1st Half and conditions match for Total case', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'draw';
          selection.part.outcome[0].externalStatsLink.statValue = '<5';
          update.teams.home['1h'].corners = 2;
          update.teams.away['1h'].corners = 2;
        });

        it('bet not settled, is 1st Half and conditions match for home case', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'home';
          selection.part.outcome[0].externalStatsLink.contestantId = 'home';
          selection.part.outcome[0].externalStatsLink.statValue = '<5';
          update.teams.home['1h'].corners = 2;
          update.teams.away['1h'].corners = 3;
        });

        it('bet not settled, is 1st Half and conditions match for away case', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'away';
          selection.part.outcome[0].externalStatsLink.contestantId = 'away';
          selection.part.outcome[0].externalStatsLink.statValue = '<5';
          update.teams.home['1h'].corners = 2;
          update.teams.away['1h'].corners = 3;
        });

        afterEach(() => {
          expect(service.totalCornersStatusHandler(selection, update, bet).status).toEqual(STATUSES.WINNING);
        });
      });

      describe('and return "Won" in case', () => {
        it('is 2nd Half and conditions match for Total case', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'draw';
          selection.part.outcome[0].externalStatsLink.statValue = '<5';
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
        });

        it('bet settled and conditions match for Draw Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'draw';
          selection.part.outcome[0].externalStatsLink.statValue = '>2';
          update.teams.home['1h'].corners = 2;
          update.teams.away['1h'].corners = 2;
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
          bet.settled = 'Y';
        });

        afterEach(() => {
          expect(service.totalCornersStatusHandler(selection, update, bet).status).toEqual(STATUSES.WON);
        });
      });

      describe('and return "Lose" in case', () => {
        it('bet settled, 2nd Half and conditions do not match for Away Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'away';
          selection.part.outcome[0].externalStatsLink.statValue = '>=2';
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
          bet.settled = 'Y';
        });

        it('bet not settled, 2nd Half and conditions do not match for Draw Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'draw';
          selection.part.outcome[0].externalStatsLink.statValue = '<0';
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
          update.teams.away['1h'].corners = 20;
        });

        afterEach(() => {
          expect(service.totalCornersStatusHandler(selection, update, bet).status).toEqual(STATUSES.LOSE);
        });
      });

      describe('and return "Losing" in case' , () => {
        beforeEach(() => {
          statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
        });

        it('bet not settled, is 1st Half and conditions match for Home Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'home';
          selection.part.outcome[0].externalStatsLink.statValue = '>5';
          update.teams.home['1h'].corners = 3;
        });

        it('bet not settled, is 1st Half and conditions match for Away Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'away';
          selection.part.outcome[0].externalStatsLink.statValue = '>=5';
          update.teams.away['1h'].corners = 2;
        });

        afterEach(() => {
          expect(service.totalCornersStatusHandler(selection, update, bet).status).toEqual(STATUSES.LOSING);
        });
      });
    });

    describe('should process TOTAL | 2ND HALF', () => {
      describe('and return "Winning" in case', () => {
        it('bet not settled and conditions match for Total case', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'draw';
          selection.part.outcome[0].externalStatsLink.statValue = '<5';
          update.teams.home.total.corners = 2;
          selection.betCompletion = true;
        });

        afterEach(() => {
          expect(service.totalCornersStatusHandler(selection, update, bet).status).toEqual(STATUSES.WINNING);
        });
      });

      describe('and return "Won" in case', () => {
        it('bet settled and conditions match for Home Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'home';
          selection.part.outcome[0].externalStatsLink.statValue = '>2';
          update.teams.home.total.corners = 3;
          selection.betCompletion = true;
        });

        it('bet settled and conditions match for Away Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'away';
          selection.part.outcome[0].externalStatsLink.statValue = '>=1';
          update.teams.away.total.corners = 3;
          selection.betCompletion = true;
        });

        it('bet settled and conditions do not match for Away Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'away';
          selection.part.outcome[0].externalStatsLink.statValue = '>=2';
          update.teams.away.total.corners = 2;
          selection.betCompletion = true;
        });

        afterEach(() => {
          expect(service.totalCornersStatusHandler(selection, update, bet).status).toEqual(STATUSES.WON);
        });
      });

      describe('and return "Losing" in case', () => {
        it('bet not settled and conditions match for Home Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'home';
          selection.part.outcome[0].externalStatsLink.statValue = '>5';
          update.teams.home.total.corners = 3;
          selection.betCompletion = true;
        });

        it('bet not settled and conditions match for Away Team', () => {
          selection.part.outcome[0].externalStatsLink.providerId = 'away';
          selection.part.outcome[0].externalStatsLink.statValue = '>=5';
          update.teams.away.total.corners = 2;
          selection.betCompletion = true;
        });
        afterEach(() => {
          expect(service.totalCornersStatusHandler(selection, update, bet).status).toEqual(STATUSES.LOSING);
        });
      });
    });
  });

  describe('StatusHandler', () => {
    beforeEach(() => {
      service['getPlayerStatusAndProgress'] = jasmine.createSpy('getPlayerStatusAndProgress');
    });

    it('totalTacklesStatusHandler', () => {
      let poorUpdate = {} as any;
      const bet = { settled: '' } as any;
      selection.config.statCategory = 'Tackles';
      selection.config.generalInformationRequired = 'player';
      (service['getPlayerStatusAndProgress'] as jasmine.Spy).and.returnValue({ status: STATUSES.WON });

      expect(service.totalTacklesStatusHandler(selection, poorUpdate, bet)).toEqual({ status: '' });
      poorUpdate = {
        players: {
          home: { '1': { id: 1, providerId: 1 } },
          away: { '2': { id: 2, providerId: 2 } }
        }
      } as any;
      expect(service.totalTacklesStatusHandler(selection, poorUpdate, bet)).toEqual({ status: STATUSES.WON });
    });

    it('totalShotsStatusHandler', () => {
      const poorUpdate = {} as any;
      const bet = { settled: '' } as any;
      selection.config.statCategory = 'Shots';
      selection.config.generalInformationRequired = 'player';
      (service['getPlayerStatusAndProgress'] as jasmine.Spy).and.returnValue({ status: STATUSES.WON });

      poorUpdate.players = {};
      expect(service.totalShotsStatusHandler(selection, poorUpdate, bet)).toEqual({ status: '' });

      poorUpdate.players.home = { '1': { id: 1, providerId: 1 } };
      poorUpdate.players.away = { '2': { id: 2, providerId: 2 } };
      expect(service.totalShotsStatusHandler(selection, poorUpdate, bet)).toEqual({ status: STATUSES.WON });
    });

    it('totalShotsOnTargetStatusHandler', () => {
      let poorUpdate = {} as any;
      const bet = { settled: '' } as any;
      selection.config.statCategory = 'ShotsOnTarget';
      selection.config.generalInformationRequired = 'player';
      (service['getPlayerStatusAndProgress'] as jasmine.Spy).and.returnValue({ status: STATUSES.WON });

      expect(service.totalShotsOnTargetStatusHandler(selection, poorUpdate, bet)).toEqual({ status: '' });
      poorUpdate = {
        players: {
          home: { '1': { id: 1, providerId: 1 } },
          away: { '2': { id: 2, providerId: 2 } }
        }
      } as any;
      expect(service.totalShotsOnTargetStatusHandler(selection, poorUpdate, bet))
        .toEqual({ status: STATUSES.WON });
    });

    it('totalAssistsStatusHandler', () => {
      service.totalAssistsStatusHandler({} as IBybSelection, {} as IScoreboardStatsUpdate, {} as IBetHistoryBet);

      expect(service['getPlayerStatusAndProgress']).toHaveBeenCalledWith(
        {} as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.ASSISTS
      );
    });

    it('totalPassesStatusHandler', () => {
      service.totalPassesStatusHandler({} as IBybSelection, {} as IScoreboardStatsUpdate, {} as IBetHistoryBet);

      expect(service['getPlayerStatusAndProgress']).toHaveBeenCalledWith(
        {} as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.PASSES
      );
    });

    it('goalsInsideBoxStatusHandler', () => {
      service.goalsInsideBoxStatusHandler({} as IBybSelection, {} as IScoreboardStatsUpdate, {} as IBetHistoryBet);

      expect(service['getPlayerStatusAndProgress']).toHaveBeenCalledWith(
        {} as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.GOALS_INSIDE_BOX
      );
    });

    it('goalsOutsideBoxStatusHandler', () => {
      service.goalsOutsideBoxStatusHandler({} as IBybSelection, {} as IScoreboardStatsUpdate, {} as IBetHistoryBet);

      expect(service['getPlayerStatusAndProgress']).toHaveBeenCalledWith(
        {} as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.GOALS_OUTSIDE_BOX
      );
    });

    it('shotsWoodworkStatusHandler', () => {
      service.shotsWoodworkStatusHandler({} as IBybSelection, {} as IScoreboardStatsUpdate, {} as IBetHistoryBet);

      expect(service['getPlayerStatusAndProgress']).toHaveBeenCalledWith(
        {} as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.SHOTS_WOODWORK
      );
    });

    it('totalCrossesStatusHandler', () => {
      service.totalCrossesStatusHandler({} as IBybSelection, {} as IScoreboardStatsUpdate, {} as IBetHistoryBet);

      expect(service['getPlayerStatusAndProgress']).toHaveBeenCalledWith(
        {} as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.CROSSES
      );
    });

    it('shotsOutsideBoxStatusHandler', () => {
      service.shotsOutsideBoxStatusHandler({} as IBybSelection, {} as IScoreboardStatsUpdate, {} as IBetHistoryBet);

      expect(service['getPlayerStatusAndProgress']).toHaveBeenCalledWith(
        {} as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.SHOTS_OUTSIDE_BOX
      );
    });

    it('totalOffsidesStatusHandler', () => {
      service.totalOffsidesStatusHandler({} as IBybSelection, {} as IScoreboardStatsUpdate, {} as IBetHistoryBet);

      expect(service['getPlayerStatusAndProgress']).toHaveBeenCalledWith(
        {} as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.OFFSIDES
      );
    });
  });

  describe('redCardsPlayerStatusHandler', () => {
    let cardsObj;
    let selectionObj;
    let player;

    beforeEach(() => {
      cardsObj = {
        home: [{ providerId: '1' }],
        away: []
      };
      selectionObj = {
        config: {
          name: 'Build Your Bet TO BE SENT OFF',
          hasLine: true,
          statCategory: 'RedCards',
          template: 'binary',
          period: 'total',
          generalInformationRequired: 'player',
          methodName: 'redCardsPlayerStatusHandler'
        },
        part: {
          outcome: [{
            name: 'PLAYER',
            externalStatsLink: {
              statCategory: 'Score',
              statValue: '',
              playerId: '1'
            }
          }]
        }
      };
      player = {
        providerId: '1',
        cards: {
          red: 1,
          yellow: 1
        }
      };

      statCategoryUtilityService.getRedCards = jasmine.createSpy('getRedCards').and.returnValue(cardsObj);
      statCategoryUtilityService.getPlayerById.and.returnValue(player);
    });

    it('should return Won status', () => {
      expect(service.redCardsPlayerStatusHandler(selectionObj, statsDataMock)).toEqual({ status: 'Won' });
    });

    it('should return Losing status', () => {
      player.cards.red = 0;
      expect(service.redCardsPlayerStatusHandler(selectionObj, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return Winning status when no player were found(No reds card selection)', () => {
      statCategoryUtilityService.getPlayerById.and.returnValue(undefined);
      selectionObj.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service.redCardsPlayerStatusHandler(selectionObj, statsDataMock)).toEqual({ status: 'Winning' });
    });

    it('should return Winning status when no player were found)', () => {
      statCategoryUtilityService.getPlayerById.and.returnValue(undefined);
      selectionObj.part.outcome[0].externalStatsLink.statValue = '>0.5';
      expect(service.redCardsPlayerStatusHandler(selectionObj, statsDataMock)).toEqual({ status: '' });
    });

    it('should return empty status when no home cards', () => {
      const updt = {cards:{away: []}};
      statCategoryUtilityService.getPlayerById.and.returnValue(undefined);
      selectionObj.part.outcome[0].externalStatsLink.statValue = '>0.5';

      expect(service.redCardsPlayerStatusHandler(selectionObj, updt as any)).toEqual({ status: '' });
    });

    it('should return empty status when no away cards', () => {
      const updt = {cards:{home: []}};
      statCategoryUtilityService.getPlayerById.and.returnValue(undefined);
      selectionObj.part.outcome[0].externalStatsLink.statValue = '>0.5';

      expect(service.redCardsPlayerStatusHandler(selectionObj, updt as any)).toEqual({ status: '' });
    });
  });

  describe('shownCardStatusHandler', () => {
    let cardsObj;
    let selectionObj;
    let player;

    beforeEach(() => {
      cardsObj = {
        home: [{ providerId: '1' }],
        away: []
      };
      selectionObj = {
        config: {
          name: 'Build Your Bet TO BE SHOWN A CARD',
          hasLine: true,
          statCategory: 'Booking',
          template: 'binary',
          period: 'total',
          generalInformationRequired: 'player',
          methodName: 'shownCardStatusHandler'
        },
        part: {
          outcome: [{
            name: 'PLAYER',
            externalStatsLink: {
              statCategory: 'Booking',
              statValue: '',
              playerId: '1'
            }
          }]
        }
      };
      player = {
        providerId: '1',
        cards: {
          red: 1,
          yellow: 1
        }
      };

      statCategoryUtilityService.getRedCards = jasmine.createSpy('getRedCards').and.returnValue(cardsObj);
      statCategoryUtilityService.getPlayerById.and.returnValue(player);
    });

    it('should return Won status', () => {
      expect(service.shownCardStatusHandler(selectionObj, statsDataMock)).toEqual({ status: 'Won' });
    });

    it('should return Losing status', () => {
      player.cards.red = 0;
      player.cards.yellow = 0;
      expect(service.shownCardStatusHandler(selectionObj, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return Winning status when no player were found)', () => {
      statCategoryUtilityService.getPlayerById.and.returnValue(undefined);
      expect(service.shownCardStatusHandler(selectionObj, statsDataMock)).toEqual({ status: '' });
    });

    it('should return empty status when update players is not defined', () => {
      statsDataMock.players = undefined;
      expect(service.shownCardStatusHandler(selectionObj, statsDataMock)).toEqual({ status: '' });
    });

    it('should return empty status when update players.home is not defined', () => {
      statsDataMock.players.home = undefined;
      expect(service.shownCardStatusHandler(selectionObj, statsDataMock)).toEqual({ status: '' });
    });

    it('should return empty status when update players.away is not defined', () => {
      statsDataMock.players.away = undefined;
      expect(service.shownCardStatusHandler(selectionObj, statsDataMock)).toEqual({ status: '' });
    });

    it('should return empty status when player don\'t have cards', () => {
      statCategoryUtilityService.getPlayerById.and.returnValue({});
      expect(service.shownCardStatusHandler(selectionObj, statsDataMock)).toEqual({ status: '' });
    });
  });

  describe('playerToOutscoreStatusHandler', () => {
    let scoreObj, playerObj, playersListObj;
    beforeEach(() => {
      scoreObj = { score: {
          '1h': { home: 0, away: 0 },
          '2h': { home: 0, away: 0 },
          total: { home: 0, away: 1 },
        }};
      playerObj = {
        goals: 1,
        homeAwaySide: 'away'
      };
      playersListObj = {
        123: {name: { matchName: 'ronaldo'}},
        345: {name: { matchName: 'messi'}}
      };
      selection = {
        config: {
          period: 'total',
          generalInformationRequired: 'teams',
        },
        part: {
          outcome: [
            {
              name: 'Messi'
            }
          ]
        }
      } as any;
      update = {
        ...update,
        score: {
          total: {}
        },
        players: {
          home: {},
          away: {}
        }
      };
      statCategoryUtilityService.getScoreByTeams = jasmine.createSpy('getScore').and.returnValue(scoreObj);
      statCategoryUtilityService.getPlayerByName = jasmine.createSpy('getPlayerByName').and.returnValue(playerObj);
      statCategoryUtilityService.getPlayerStats = jasmine.createSpy('getPlayerStats').and.returnValue(playersListObj);
    });
    it('should return Winning status', () => {
      expect(service.playerToOutscoreStatusHandler(selection, update)).toEqual({status: 'Winning'});
    });

    it('should return Losing status', () => {
      playerObj.homeAwaySide = 'home';
      scoreObj.score.total.home = 2;
      expect(service.playerToOutscoreStatusHandler(selection, update)).toEqual({status: 'Losing'});
    });

    it('should return empty status if player was not found status', () => {
      statCategoryUtilityService.getPlayerByName = jasmine.createSpy('getPlayerByName').and.returnValue('');
      scoreObj.score.total.away = 2;
      expect(service.playerToOutscoreStatusHandler(selection, update)).toEqual({status: ''});
    });

    it('should return empty status if player don\'t have goals', () => {
      statCategoryUtilityService.getPlayerByName = jasmine.createSpy('getPlayerByName').and.returnValue('');
      scoreObj.score.total.away = 2;
      expect(service.playerToOutscoreStatusHandler(selection, update)).toEqual({status: ''});
    });

    it('should return empty status if teamScore don\'t have score', () => {
      statCategoryUtilityService.getPlayerByName = jasmine.createSpy('getPlayerByName').and.returnValue({goals: 1});
      scoreObj.score = {};
      expect(service.playerToOutscoreStatusHandler(selection, update)).toEqual({status: ''});
    });

    it('should return empty status if update.players is undefined', () => {
      update.players = undefined;

      expect(service.playerToOutscoreStatusHandler(selection, update)).toEqual({status: ''});
    });

    it('should return empty status if update.players.home is undefined', () => {
      update.players.home = undefined;

      expect(service.playerToOutscoreStatusHandler(selection, update)).toEqual({status: ''});
    });

    it('should return empty status if update.players.away is undefined', () => {
      update.players.away = undefined;

      expect(service.playerToOutscoreStatusHandler(selection, update)).toEqual({status: ''});
    });
  });

  describe('totalGoalsOddsEvenStatusHandler', () => {
    beforeEach(() => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
    });

    it('should handle totalGoalsOddsEven market status - no period in update', () => {
      selection = { config: { period: 'total' }, title: 'Odd' } as IBybSelection;
      const update_2 = JSON.parse(JSON.stringify(statsDataMock));
      delete update_2.period;
      const actualResult = service.totalGoalsOddsEvenStatusHandler(
        selection,
        update_2 as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should handle totalGoalsOddsEven market status(Total period)', () => {
      selection = { config: { period: 'total' }, title: 'Odd' } as IBybSelection;
      const actualResult = service.totalGoalsOddsEvenStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Winning' });
    });

    it('should handle totalGoalsOddsEven market status(3nd half period in case it not started yet)', () => {
      selection = { config: { period: '3h' }, title: 'Odd' } as IBybSelection;
      const actualResult = service.totalGoalsOddsEvenStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle totalGoalsOddsEven market status(2nd half period in case it not started yet)', () => {
      selection = { config: { period: '2h' }, title: 'Odd' } as IBybSelection;
      goalsObj.score['2h'] = undefined;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
      const actualResult = service.totalGoalsOddsEvenStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle totalGoalsOddsEven market status(1st half period)', () => {
      selection = { config: { period: '1h' }, title: 'Even' } as IBybSelection;
      const actualResult = service.totalGoalsOddsEvenStatusHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Winning' });
    });
  });

  describe('doubleChanceStatusHandler', () => {
    let bybSelection;
    let actualResult;

    beforeEach(() => {
      bybSelection = {
        config: {
          period: 'total'
        },
        part: {
          outcome: [
            {
              name: 'ARSENAL OR DRAW'
            }
          ]
        }
      } as any;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
    });
    it('should handle double chance status(Total period)', () => {
      actualResult = service.doubleChanceStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle double chance status(1st half period)', () => {
      bybSelection.config.period = '1h';
      actualResult = service.doubleChanceStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Winning' });
    });

    it('should handle double chance status(2nd half period)', () => {
      bybSelection.config.period = '2h';
      actualResult = service.doubleChanceStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should return empty status (no team)', () => {
      statCategoryUtilityService.getDoubleHomeAwayTeamByContestantId.and.returnValue(null);
      bybSelection.part.outcome[0].name = 'LIVERPOOL1 OR ARSENAL';
      bybSelection.config.period = '2h';
      statsDataMock.period = null;
      actualResult = service.doubleChanceStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status when update.score is not defined', () => {
      statsDataMock.score = {};
      actualResult = service.doubleChanceStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status when update.period is not defined', () => {
      statsDataMock.period = undefined;
      bybSelection.config.period = '1h';
      actualResult = service.doubleChanceStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status when goalsObj.score is empty', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue({score: {}});
      statCategoryUtilityService.getDoubleHomeAwayTeamByContestantId.and.returnValue('HOME');
      bybSelection.part.outcome[0].name = 'LIVERPOOL1 OR ARSENAL';
      bybSelection.config.period = '2h';

      actualResult = service.doubleChanceStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status (no period)', () => {
      bybSelection.part.outcome[0].name = 'LIVERPOOL1 OR ARSENAL';
      bybSelection.config.period = '2h';
      statsDataMock.period = null;
      actualResult = service.doubleChanceStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });
  });

  describe('Ranged Market Status', () => {
    const goal = {
      scorer: 'Gusev',
      time: '05:00',
      team: 'Away',
      player: {
        id: 'Gusev'
      }
    };
    const goalStats = { Away: [goal], Home: [] };

    beforeEach(() => {
      selection = {
        config: {
          period: '15 mins',
          generalInformationRequired: 'teams',
          statCategory: 'Score'
        },
        part: {
          outcome: [{
            externalStatsLink: {
              statCategory: 'Score',
              contestantId: 'draw'
            }
          }]
        }
      };

      update = {
        ...update,
        time:'10:00'
      };

      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([goal]);

      service['getRangeMarketStatus'] = jasmine.createSpy('getRangeMarketStatus').and.returnValue(STATUSES.LOSE);
    });

    describe('should process market for', () => {
      it('getResultAfterNMinutes when time is within range', () => {
        expect(service.getResultAfterNMinutes(selection, update)).toEqual({ status: STATUSES.LOSE });
        expect(service['getRangeMarketStatus']).toHaveBeenCalledWith(goalStats as any, false, TEAMS.DRAW);
      });

      it('mostGoalsInRange when time is within range', () => {
        selection.config.period = '1h';
        expect(service.mostGoalsInRange(selection, update)).toEqual({ status: STATUSES.LOSE });
        expect(service['getRangeMarketStatus']).toHaveBeenCalledWith(goalStats as any, false, TEAMS.DRAW);
      });

      it('should return empty status when update.time is not define (getResultAfterNMinutes)', () => {
        update.time = undefined;
        expect(service.getResultAfterNMinutes(selection, update)).toEqual({ status: '' });
      });

      it('should return empty status when update.time is not define (mostGoalsInRange)', () => {
        update.time = undefined;
        expect(service.mostGoalsInRange(selection, update)).toEqual({ status: '' });
      });

      it('mostGoalsInRange when time is within range', () => {
        service['getTeamByExternalStatsLink'] = jasmine.createSpy('getTeamByExternalStatsLink').and.returnValue('');

        selection.config.period = '1h';
        expect(service.mostGoalsInRange(selection, update)).toEqual({ status: '' });
        expect(service.getResultAfterNMinutes(selection, update)).toEqual({ status: ''});
      });

    });

    describe('should process market for', () => {
      it('getResultAfterNMinutes when time is greater than range', () => {
        update.time = '30:00';
        expect(service.getResultAfterNMinutes(selection, update)).toEqual({ status: STATUSES.LOSE });
      });

      it('mostGoalsInRange when time is greater than range', () => {
        update.time = '75:00';
        selection.config.period = 'total';
        goalStats.Away = [];  // as goal scored at 05:00 is not in range of 30-60
        expect(service.mostGoalsInRange(selection, update)).toEqual({ status: STATUSES.LOSE });
      });

      afterEach(() => {
        expect(service['getRangeMarketStatus']).toHaveBeenCalledWith(goalStats as any, true, TEAMS.DRAW);
      });
    });
  });

  it('should not return any status in case no scores for specific half were found', () => {
    const selection_2 = JSON.parse(JSON.stringify(selection));
    selection_2.config.period = 'h2';
    service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue({ score: { 'h1': {} } });

    expect(service.toWinToNil(selection_2, update)).toEqual({ status: '' });
  });

  describe('toWinToNil', () => {
    let scoreStats: any;

    beforeEach(() => {
      selection.config.statCategory = 'Score';
      scoreStats = {
        score: {
          total: { home: 0, away: 0 }
        },
        away: undefined,
        home: undefined
      } as IScoreByTeams;

      statCategoryUtilityService.getHomeAwayTeamByContestantId = jasmine.createSpy('getHomeAwayTeamByContestantId');
    });

    it('should not return any status in case no team were found', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreStats);
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(null);

      expect(service.toWinToNil(selection, update)).toEqual({ status: '' });
    });

    it('should not return any status in case no scores were found', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue( { score: {} } );

      expect(service.toWinToNil(selection, update)).toEqual({ status: '' });
    });

    it('should get market status for Home Team', () => {
      scoreStats.score.total.home = 1;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreStats);
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(TEAMS.HOME);

      expect(service.toWinToNil(selection, update)).toEqual({ status: STATUSES.WINNING });
    });

    it('should get market status for Away Team', () => {
      scoreStats.score.total.away = 1;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreStats);
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(TEAMS.AWAY);

      expect(service.toWinToNil(selection, update)).toEqual({ status: STATUSES.WINNING });
    });

    it('should get market status when conditions do not match', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreStats);

      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(TEAMS.HOME);
      expect(service.toWinToNil(selection, update)).toEqual({ status: STATUSES.LOSING });

      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(TEAMS.AWAY);
      expect(service.toWinToNil(selection, update)).toEqual({ status: STATUSES.LOSING });
    });

    it('should get market status when opposite team scored', () => {
      scoreStats.score.total.home = 1;

      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreStats);
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue(TEAMS.AWAY);

      expect(service.toWinToNil(selection, update)).toEqual({ status: STATUSES.LOSE });
    });

    afterEach(() => {
      expect(service['getStatCategoryObj']).toHaveBeenCalledWith(selection, update);
      expect(statCategoryUtilityService.getHomeAwayTeamByContestantId).toHaveBeenCalledWith(update, selection);
    });
  });

  describe('firstTeamToScore', () => {
    beforeEach(() => {
      selection = {
        config: {
          period: 'total',
          generalInformationRequired: 'teams',
          statCategory: 'Score'
        },
        part: {
          outcome: [{
            externalStatsLink: {
              statCategory: 'Score',
              contestantId: ''
            }
          }]
        }
      };
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
    });
    it('should return prePlay2h when 1st for 2nd half status', () => {
      selection.config.period = '2h';
      selection.betCompletion = false;
      statsDataMock.period = '1h';
      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate);
      expect(actualResult).toEqual({ status: 'prePlay2h' });
    });
    it('should handle teamToScoreIn market status(Total period) won', () => {
      selection.config.period = 'total';
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Won' });
    });

    it('should handle teamToScoreIn market status(Total period) losing', () => {
      selection.config.period = '2h';
      selection.part.outcome[0].externalStatsLink.contestantId = 'c8h9bw1l82s06h77xxrelzhur';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([]);
      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle teamToScoreIn market status(Total period) lost', () => {
      selection.config.period = 'total';
      selection.part.outcome[0].externalStatsLink.contestantId = 'c8h9bw1l82s06h77xxrelzhur';
      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Lose' });
    });

    it('should handle FIRST TEAM TO SCORE IN 2ND HALF market status(2nd half period in case it not started yet)' +
      'when No Goals selection were chosen', () => {
      goalsObj.score['2h'] = undefined;
      selection.title = 'No Goal';
      selection.config.period = '2h';
      statsDataMock.score['2h'] = undefined;
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);

      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Winning' });
    });

    it('should handle FIRST TEAM TO SCORE IN 2ND HALF market status(2nd half period in case it not started yet)', () => {
      selection.config.period = '2h';
      statsDataMock.score['2h'] = undefined;
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);

      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle FIRST TEAM TO SCORE IN 2ND HALF market status(2nd half' +
      'period in case it not started yet)', () => {
      goalsObj.score['2h'] = undefined;
      selection.config.period = '2h';
      statsDataMock.score['2h'] = undefined;
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);

      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle teamToScoreIn market status(1st half period)', () => {
      selection.config.period = '1h';
      selection.part.outcome[0].externalStatsLink.contestantId = 'c8h9bw1l82s06h77xxrelzhur';
      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle teamToScoreIn NO GOAL market status for 1h period', () => {
      selection.config.period = '1h';
      selection.part.outcome[0].externalStatsLink.contestantId = 'c8h9bw1l82s06h77xxrelzhur';
      selection.title = 'No Goal';
      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Winning' });
    });

    it('should handle teamToScoreIn NO GOAL market status for 2h/total period', () => {
      selection.config.period = '2h';
      selection.part.outcome[0].externalStatsLink.contestantId = 'c8h9bw1l82s06h77xxrelzhur';
      selection.title = 'No Goal';
      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Lose' });
    });

    it('should return empty status when update.score is empty', () => {
      statsDataMock.score = {};
      const actualResult = service.firstTeamToScore(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });
  });

  describe('correctScoreStatusHandler', () => {
    let bybSelection;
    let actualResult;

    beforeEach(() => {
      bybSelection = {
        config: {
          period: 'total'
        },
        part: {
          outcome: [
            {
              name: 'ARSENAL 2-1',
              externalStatsLink: {
                contestantId: 'c8h9bw1l82s06h77xxrelzhur'
              }
            }
          ]
        }
      } as any;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
    });

    it('should handle correct score status(Total period)', () => {
      goalsObj.score = {
        total: {
          home: 2,
          away: 1
        },
        '1h': {
          home: 1,
          away: 2
        }
      } as any;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);

      actualResult = service.correctScoreStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WINNING });
    });

    it('should handle correct score status ', () => {
      goalsObj.score = {
        total: {
          home: 2,
          away: 1
        },
        '1h': {
          home: 1,
          away: 2
        }
      } as any;
      bybSelection.part.outcome[0].name = 'LIVERPOOL 2-1';
      bybSelection.config.period = '2h';
      statCategoryUtilityService.getHomeAwayTeamByContestantId.and.returnValue('Away');
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);

      actualResult = service.correctScoreStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate);

      expect(actualResult).toEqual({ status: STATUSES.LOSING });
    });

    it('should handle correct score status(Total period)', () => {
      bybSelection.part.outcome[0].name = 'ARSENAL 1-1';
      actualResult = service.correctScoreStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should handle correct score status(1st half period)', () => {
      bybSelection.config.period = '1h';
      actualResult = service.correctScoreStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSING });
    });

    it('should handle correct score status(2nd half period)', () => {
      bybSelection.config.period = '2h';
      bybSelection.part.outcome[0].name = 'LIVERPOOL 1-2';
      bybSelection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      actualResult = service.correctScoreStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WINNING });
    });

    it('should return empty string, if getTeamCorrectScores return null', () => {
      spyOn(service as any, 'getTeamCorrectScores').and.returnValue(null);
      bybSelection.config.period = '2h';
      bybSelection.part.outcome[0].name = 'LIVERPOOL 1-2';
      bybSelection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      actualResult = service.correctScoreStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );
      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status when update.score is empty', () => {
      statsDataMock.score = {};
      actualResult = service.correctScoreStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );
      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status when update.period is empty', () => {
      statsDataMock.period = undefined;
      bybSelection.config.period = '1h';
      actualResult = service.correctScoreStatusHandler(
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });
  });

  describe('participantToScoreNGoals', () => {
    let bet: any;

    beforeEach(() => {
      update.score = {
        'total': { home: 1, away: 2 }
      } as any;
      bet = { settled: '' };
      selection.config.statCategory = 'Score';
      selection.config.period = 'total';
      selection.part.outcome[0].externalStatsLink.statCategory = 'Score';
    });

    describe('when selection is "NO" for Home Team', () => {
      beforeEach(() => {
        selection.part.outcome[0].externalStatsLink.contestantId = 'home';
        statCategoryUtilityService.getScore = jasmine.createSpy('getScore').and.returnValue({
          score: {
            total: { home: 2, away: 0 }
          },
          away: undefined,
          home: undefined
        });
        service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue({
          score: {
            total: { home: 2, away: 0 }
          }
        });
      });

      it('should return status: "" if no period is set', () => {
        service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue({
          score: {}
        });

        expect(service.participantToScoreNGoals(selection, update, bet))
          .toEqual({ status: '' });
      });

      it('should return "WINNING" when bet not settled and conditions match', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '<4.5';

        expect(service.participantToScoreNGoals(selection, update, bet))
          .toEqual({ status: STATUSES.WINNING, progress: { current: 2, target: 4, desc: '2 of 4 Goals' } });
      });

      it('should return "WINNING" when bet not settled and conditions match', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '<2.5';

        expect(service.participantToScoreNGoals(selection, update, bet))
          .toEqual({ status: STATUSES.WINNING, progress: { current: 2, target: 2, desc: '2 of 2 Goals' } });
      });

      it('should return "LOSE" when bet not settled and conditions do not match', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '<1.5';

        expect(service.participantToScoreNGoals(selection, update, bet))
          .toEqual({ status: STATUSES.LOSE, progress: { current: 2, target: 1, desc: '2 of 1 Goal' } });
      });
    });

    describe('when selection is "YES" for Away Team', () => {
      beforeEach(() => {
        selection.part.outcome[0].externalStatsLink.contestantId = 'away';
        statCategoryUtilityService.getScore = jasmine.createSpy('getScore').and.returnValue({
          score: {
            total: { home: 0, away: 2 }
          },
          away: undefined,
          home: undefined
        });
      });

      it('should return "WON" when conditions match', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '>2';

        expect(service.participantToScoreNGoals(selection, update, bet))
          .toEqual({ status: STATUSES.WON, progress: { current: 2, target: 2, desc: '2 of 2 Goals' } });
      });

      it('should return "LOSING" when bet not settled and conditions do not match', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '>4';

        expect(service.participantToScoreNGoals(selection, update, bet))
          .toEqual({ status: STATUSES.LOSING, progress: { current: 2, target: 4, desc: '2 of 4 Goals' } });
      });
    });

    it('input data validation', () => {
      const poorUpdate = {
        home: {},
        away: {},
        score: {}
      } as any;
      expect(service.participantToScoreNGoals(selection, poorUpdate, bet)).toEqual({ status: '' });
      poorUpdate.score = {
        'total': { home: 1, away: 2 }
      } as any;
      (statCategoryUtilityService['getScore'] as jasmine.Spy).and.returnValue(poorUpdate);

      expect(service.participantToScoreNGoals(selection, poorUpdate, bet))
        .toEqual({ status: STATUSES.WON, progress: { current: 1, target: 0, desc: '1 of 0 Goals' } });
    });
  });

  describe('scoreAGoalInBothHalvesHandler', () => {
    beforeEach(() => {
      goalsObj = {
        score: {
          total: { home: 3, away: 2 },
          '1h': { home: 2, away: 0 },
          '2h': { home: 1, away: 2 }
        },
        away: { id: '1', providerId: 'away' },
        home: { id: '2', providerId: 'home' }
      };

      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      selection.config.statCategory = 'Score';
      selection.config.generalInformationRequired = 'teams';
      statCategoryUtilityService.getScore.and.returnValue(goalsObj);
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
    });

    it('should return prePlay2h when 1st for 2nd half status', () => {
      selection.config.period = '2h';
      selection.betCompletion = false;
      statsDataMock.period = '1h';
      const actualResult = service.scoreAGoalInBothHalvesHandler(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );
      expect(actualResult).toEqual({ status: 'prePlay2h' });
    });

    it('should return WON status for SCORE A GOAL IN BOTH HALVES market', () => {
      goalsObj = {
        score: {
          total: { home: 0, away: 0 },
          '1h': { home: 0, away: 0 },
          '2h': { home: 0, away: 0 }
        },
        away: { id: '1', providerId: 'away' },
        home: { id: '2', providerId: 'home' }
      };
      statsDataMock.period = '2h';
      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Won' });
    });

    it('should return WON status for SCORE A GOAL IN BOTH HALVES market', () => {
      goalsObj = {
        score: {
          total: { home: 0, away: 0 },
          '1h': { home: 0, away: 0 },
          '2h': { home: 0, away: 0 }
        },
        away: { id: '1', providerId: 'away' },
        home: { id: '2', providerId: 'home' }
      };
      statsDataMock.period = '2h';
      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Lose' });
    });

    it('should return WON status for SCORE A GOAL IN BOTH HALVES market', () => {
      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Won' });
    });

    it('should return LOSING status for SCORE A GOAL IN BOTH HALVES market when current time is First half', () => {
      goalsObj.score = {
        total: { home: 2, away: 0 },
        '1h': { home: 2, away: 0 }
      };
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');

      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return LOSING status for SCORE A GOAL IN BOTH HALVES market when current time is First half' +
      'and no goals were scored', () => {
      goalsObj.score = {
        total: { home: 0, away: 0 },
        '1h': { home: 0, away: 0 }
      };
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');

      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return LOSE status for SCORE A GOAL IN BOTH HALVES market when' +
      'both team scored in both halves and selection is NO', () => {
      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';

      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Lose' });
    });

    it('should return WINNING status for SCORE A GOAL IN BOTH HALVES market when' +
      'current time is First half and no goals were scored and selection is NO', () => {
      goalsObj.score = {
        total: { home: 0, away: 0 },
        '1h': { home: 0, away: 0 }
      };
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';

      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Winning' });
    });

    it('should return WINNING status for SCORE A GOAL IN BOTH HALVES market when' +
      'current time is Second half and no goals were scored and selection is NO', () => {
      goalsObj.score = {
        total: { home: 1, away: 0 },
        '1h': { home: 1, away: 0 },
        '2h': { home: 0, away: 0 }
      };
      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';

      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Winning' });
    });

    it('should return LOSING status for SCORE A GOAL IN BOTH HALVES market when' +
      'current time is Second half and no goals were scored and selection is YES', () => {
      goalsObj.score = {
        total: { home: 1, away: 0 },
        '1h': { home: 1, away: 0 },
        '2h': { home: 0, away: 0 }
      };
      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';

      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return Winning status for SCORE A GOAL IN BOTH HALVES market and selection is NO', () => {
      goalsObj.score = {
        total: { home: 1, away: 0 },
        '1h': { home: 1, away: 0 },
        '2h': { home: 0, away: 0 }
      };
      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';

      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Winning' });
    });

    it('should return Lose status for SCORE A GOAL IN BOTH HALVES market ' +
      'and no goals were scored in first half and selection is YES and current time is second', () => {
      goalsObj.score = {
        total: { home: 5, away: 0 },
        '1h': { home: 0, away: 0 },
        '2h': { home: 5, away: 0 }
      };
      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';

      expect(service.scoreAGoalInBothHalvesHandler(selection, statsDataMock)).toEqual({ status: 'Lose' });
    });

    it('input data validation', () => {
      const poorUpdate = {
        home: {},
        away: {},
        score: {}
      } as any;
      expect(service.scoreAGoalInBothHalvesHandler(selection, poorUpdate)).toEqual({ status: '' });

      poorUpdate.score = {
        '1h' : {
          home: 1,
          away: 2
        }
      };
      expect(service.scoreAGoalInBothHalvesHandler(selection, poorUpdate)).toEqual({ status: 'Won' });
    });
  });


  describe('halfToProduceFirstGoal', () => {
    beforeEach(() => {
      selection = {
        config: {
          period: 'total'
        },
        title: 'First Half'
      };
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
    });
    it('should handle teamToScoreIn market status(Total period)', () => {
      statsDataMock.period = '1h';
      statsDataMock.score['2h'] = undefined;
      const actualResult = service.halfToProduceFirstGoal(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Won' });
    });

    it('should handle teamToScoreIn market status(Total period) losing status', () => {
      statsDataMock.period = '1h';
      statsDataMock.score['1h'].home = 0;
      statsDataMock.score['1h'].away = 0;
      statsDataMock.score['2h'] = undefined;
      const actualResult = service.halfToProduceFirstGoal(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle teamToScoreIn market status(1st half period)', () => {
      statsDataMock.period  = '2h';
      selection.title = 'Second Half';
      const actualResult = service.halfToProduceFirstGoal(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Lose' });
    });

    it('should handle teamToScoreIn market status(2nd half period) winning', () => {
      statsDataMock.period  = '2h';
      selection.title = 'Second Half';
      statsDataMock.score['1h'].home = 0;
      statsDataMock.score['1h'].away = 0;
      statsDataMock.score['2h'].away = 1;
      const actualResult = service.halfToProduceFirstGoal(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Won' });
    });

    it('should handle teamToScoreIn market status(2nd half period) losing', () => {
      statsDataMock.period  = '2h';
      selection.title = 'Second Half';
      statsDataMock.score['1h'].home = 0;
      statsDataMock.score['1h'].away = 0;
      statsDataMock.score['2h'].away = 0;
      statsDataMock.score['2h'].home = 0;
      const actualResult = service.halfToProduceFirstGoal(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );
      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should handle teamToScoreIn NO GOAL market status for 1h period', () => {
      selection.title = 'No Goals';
      statsDataMock.score['total'].home = 1;
      statsDataMock.score['total'].away = 0;

      const actualResult = service.halfToProduceFirstGoal(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Lose' });
    });

    it('should handle teamToScoreIn NO GOAL market status for 2h/total period', () => {
      statsDataMock.score['total'].home = 0;
      statsDataMock.score['total'].away = 0;
      selection.title = 'No Goals';
      const actualResult = service.halfToProduceFirstGoal(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Winning' });
    });

    it('should return empty status when update.score is undefined', () => {
      statsDataMock.score = {};
      const actualResult = service.halfToProduceFirstGoal(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });
  });

  describe('teamToScoreInBothHalves', () => {
    beforeEach(() => {
      selection = {
        config: {
          period: 'total'
        },
        title: 'First Half',
        part: {
          outcome: [{
            externalStatsLink: {
              contestantId: 'home'
            }
          }]
        }
      };
      statsDataMock.home.providerId = 'home';
    });

    it('should return Losing if second half not started yet', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue({
        score: {
          '1h': {
            home: 1,
            away: 10
          }
        }
      });

      const actualResult = service.teamToScoreInBothHalves(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Losing' });
    });

    it('should return Won if team scored in both halves', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue({
        score: {
          '1h': {
            home: 1,
            away: 10
          },
          '2h': {
            home: 1,
            away: 10
          }
        }
      });
      const actualResult = service.teamToScoreInBothHalves(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: 'Won' });
    });

    it('should return empty status when update.score is undefined', () => {
      statsDataMock.score = {};
      const actualResult = service.teamToScoreInBothHalves(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });
  });

  describe('totalCards', () => {
    let bet, players;

    const progress = {
      target: 0,
      current: 10,
      desc: ''
    };

    beforeEach(() => {
      bet = { settled: '' } as IBetHistoryBet;
      players = {
        home: [{ cards: { yellow: 1, red: 2 } }],
        away: [{ cards: { yellow: 3, red: 4 } }]
      };
      update.players = players;
      selection.part.outcome[0].externalStatsLink.statCategory = 'Booking';
      statCategoryUtilityService.getCardIndex.and.returnValue(players);
      statCategoryUtilityService.getCardsFromPlayers.and.returnValue({ yellow: 4, red: 6 });
    });

    describe('should get status for under case and return', () => {
      it('status "Winning" if target count is greater equals cards count and bet not settled', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '<15';
        progress.target = 15;
        progress.desc = '10 of 15 Total Cards';

        expect(service.totalCards(selection, update, bet)).toEqual({ status: STATUSES.WINNING, progress });
      });

      it('status "Lose" if cards count is greater target count and bet not settled', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '<5';
        progress.target = 5;
        progress.desc = '10 of 5 Total Cards';

        expect(service.totalCards(selection, update, bet)).toEqual({ status: STATUSES.LOSE, progress });
      });

      it('input data validation', () => {
        const poorUpdate = {} as any;
        expect(service.totalCards(selection, poorUpdate, bet)).toEqual({ status: '' });

        poorUpdate.players = players as any;
        progress.target = 0;
        progress.desc = '10 of 0 Total Cards';
        expect(service.totalCards(selection, poorUpdate, bet))
          .toEqual({ status: STATUSES.WON, progress });
      });
    });

    describe('should get status for equal case and return', () => {
      it('status "Winning" if cards count equals target and bet not settled', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '=10';
        progress.target = 10;
        progress.desc = '10 of 10 Total Cards';

        expect(service.totalCards(selection, update, bet)).toEqual({ status: STATUSES.WINNING, progress });
      });

      it('status "Winning" if target count is greater than cards count and bet not settled', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '=11';
        progress.target = 11;
        progress.desc = '10 of 11 Total Cards';

        expect(service.totalCards(selection, update, bet)).toEqual({ status: STATUSES.LOSING, progress });
      });

      it('status "Lose" if cards count is greater than target count and bet settled', () => {
        bet.settled = 'Y';
        selection.part.outcome[0].externalStatsLink.statValue = '=8';
        progress.target = 8;
        progress.desc = '10 Total Cards';

        expect(service.totalCards(selection, update, bet)).toEqual({ status: STATUSES.LOSE, progress });
      });
    });

    describe('should get status for over case and return', () => {
      it('status "Losing" if cards count is less than target and bet no settled', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '>11';
        progress.target = 11;
        progress.desc = '10 of 11 Total Cards';

        expect(service.totalCards(selection, update, bet)).toEqual({ status: STATUSES.LOSING, progress });
      });

      it('status "Won" if cards count is greater than target', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '>5';
        progress.target = 5;
        progress.desc = '10 of 5 Total Cards';

        expect(service.totalCards(selection, update, bet)).toEqual({ status: STATUSES.WON, progress });
      });
    });
  });

  describe('totalGoalsByPlayerStatusHandler', () => {
    let bet, player, progress;
    beforeEach(() => {
      bet = {
        settled: 'N'
      } as IBetHistoryBet;

      player = {
        providerId: 'cotiiu6mjkfx5xa63nhfbdf4l',
        id: '123',
        goals: 1
      };

      selection.part.outcome[0].externalStatsLink.statValue = '>=1';
      selection.part.outcome[0].externalStatsLink.statCategory = 'Score';
      selection.config.statCategory = 'Score';
      selection.config.generalInformationRequired = 'player';
      selection.config.playerId = 'cotiiu6mjkfx5xa63nhfbdf4l';
      statCategoryUtilityService.getPlayerStats.and.returnValue({ away: [], home: []});
      statCategoryUtilityService.getPlayerById.and.returnValue(player);
      progress = {
        current: 1,
        desc: '1 of 1 Goal',
        target: 1
      };
    });

    it('should return WON status for TO SCORE N OR MORE GOALS market', () => {
      expect(service.totalGoalsByPlayerStatusHandler(selection, statsDataMock, bet)).toEqual({ status: 'Won', progress });
    });

    it('should return Losing status for TO SCORE EXACTLY GOALS market', () => {
      selection.part.outcome[0].externalStatsLink.statValue = '=2';
      progress.desc = '1 of 2 Goals';
      progress.target = 2;

      expect(service.totalGoalsByPlayerStatusHandler(selection, statsDataMock, bet)).toEqual({ status: 'Losing', progress });
    });

    it('should return Winning status for TO SCORE EXACTLY GOALS market', () => {
      player = {
        providerId: 'cotiiu6mjkfx5xa63nhfbdf4l',
        id: '123',
        goals: 2
      };
      statCategoryUtilityService.getPlayerById.and.returnValue(player);
      selection.part.outcome[0].externalStatsLink.statValue = '=2';
      progress = {
        current: 2,
        desc: '2 of 2 Goals',
        target: 2
      };

      expect(service.totalGoalsByPlayerStatusHandler(selection, statsDataMock, bet)).toEqual({ status: 'Winning', progress });
    });

    it('should Not return any status when no player were found', () => {
      statCategoryUtilityService.getPlayerById.and.returnValue(undefined);

      expect(service.totalGoalsByPlayerStatusHandler(selection, statsDataMock, bet)).toEqual({ status: '' });
    });

    it('input data validation', () => {
      const poorUpdate = {
        home: {}, away: {}, score: {}
      } as any;
      expect(service.totalGoalsByPlayerStatusHandler(selection, poorUpdate, bet)).toEqual({ status: '' });

      poorUpdate.players = {};
      expect(service.totalGoalsByPlayerStatusHandler(selection, poorUpdate, bet)).toEqual({ status: '' });

      poorUpdate.players = { home: {}, away: {} };
      progress = {
        current: 1,
        desc: '1 of 1 Goal',
        target: 1
      };
      expect(service.totalGoalsByPlayerStatusHandler(selection, poorUpdate, bet))
        .toEqual({ status: STATUSES.WON, progress });

    });
  });

  describe('playerToScoreInBothHalves', () => {
    beforeEach(() => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: {
              playerId: '1234',
              statValue: '=5',
              statCategory: 'Score'
            }
          }]
        },
        config: {}
      } as any;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
    });
    it('should return winning status if player scored goal in first half', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '1h',
        player: {
          providerId: '1234',
        }
      } as any]);
      statsDataMock.period  = '1h';

      const actualResult = service.playerToScoreInBothHalves(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({status: 'Losing'});
    });

    it('should return losing status if player did not score goal in first half', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '1h',
        player: {
          providerId: '0123'
        }
      } as any,
        {
          team: 'Home',
          period: '1h',
          player: {
            providerId: '5678',
          }
        } as any]);
      statsDataMock.period  = '1h';

      const actualResult = service.playerToScoreInBothHalves(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({status: 'Losing'});
    });

    it('should return won status if player scored goals in both halves', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '1h',
        player: {
          providerId: '1234'
        }
      } as any,
        {
          team: 'Home',
          period: '2h',
          player: {
            providerId: '1234',
          }
        } as any]);
      statsDataMock.period  = 'total';

      const actualResult = service.playerToScoreInBothHalves(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({status: 'Won'});
    });

    it('should return winning status if player did not score goal in first half', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '1h',
        player: {
          providerId: '1234'
        }
      } as any,
        {
          team: 'Home',
          period: '2h',
          player: {
            providerId: '1234',
          }
        } as any]);
      statsDataMock.period  = 'total';

      const actualResult = service.playerToScoreInBothHalves(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({status: 'Won'});
    });

    it('should return winning status if player scored goal in first half', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '1h',
        player: {
          providerId: '1234'
        }
      } as any,
        {
          team: 'Home',
          period: '2h',
          player: {
            providerId: '5678',
          }
        } as any]);
      statsDataMock.period  = 'total';

      const actualResult = service.playerToScoreInBothHalves(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({status: 'Losing'});
    });

    it('should return lose status if player not scored goal in first half', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '1h',
        player: {
          providerId: '56678'
        }
      } as any,
        {
          team: 'Home',
          period: '2h',
        } as any,
        {
          team: 'Home',
          period: '2h',
          player: {
            providerId: '1234'
          }
        } as any]);
      statsDataMock.period  = 'total';

      const actualResult = service.playerToScoreInBothHalves(
        selection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({status: 'Lose'});
    });

    it('input data validation', () => {
      const poorUpdate = {
        home: {},
        away: {},
        score: {}
      } as any;
      expect(service.playerToScoreInBothHalves(selection, poorUpdate)).toEqual({ status: '' });

      poorUpdate.goals = {};
      expect(service.playerToScoreInBothHalves(selection, poorUpdate)).toEqual({ status: '' });

      poorUpdate.goals = { home: [], away: [] };
      expect(service.playerToScoreInBothHalves(selection, poorUpdate)).toEqual({ status: STATUSES.LOSE });
    });
  });

  describe('playerToScoreInPeriod', () => {
    beforeEach(() => {
      selection = {
        config: {
          statCategory: 'Score',
          generalInformationRequired: 'player',
          period: '2h'
        },
        part: {
          outcome: [{
            externalStatsLink: {playerId: '1234', statValue: '1', statCategory: 'Score'}
          }]
        }
      } as any;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(goalsObj);
    });
    it('should return won status if player scored goal in first half', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '1h',
        player: {
          providerId: '1234',
        }
      } as any]);
      statsDataMock.period = '1h';
      selection.config.period = '1h';

      const actualResult = service.playerToScoreInPeriod(
        selection,
        statsDataMock as IScoreboardStatsUpdate,
        {} as IBetHistoryBet
      );

      expect(actualResult).toEqual({
        status: 'Won',
        progress: {
          current: 1,
          desc: '1 of 1 Goal',
          target: 1
        }
      });
    });

    it('should return won status if player scored goal in second half', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '2h',
        player: {
          providerId: '1234',
        }
      } as any]);
      statsDataMock.period = '2h';
      selection.config.period = '2h';

      const actualResult = service.playerToScoreInPeriod(
        selection,
        statsDataMock as IScoreboardStatsUpdate,
        {} as IBetHistoryBet
      );

      expect(actualResult).toEqual({
        status: 'Won',
        progress: {
          current: 1,
          desc: '1 of 1 Goal',
          target: 1
        }
      });
    });

    it('should return losing status if player not scored goal in second half', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '2h',
        player: {
          providerId: '123324123414',
        }
      } as any]);
      statsDataMock.period = '2h';
      selection.config.period = '2h';

      const actualResult = service.playerToScoreInPeriod(
        selection,
        statsDataMock as IScoreboardStatsUpdate,
        {} as IBetHistoryBet
      );

      expect(actualResult).toEqual({
        status: 'Losing',
        progress: {
          current: 0,
          desc: '0 of 1 Goal',
          target: 1
        }
      });
    });

    it('should return Losing status if player not scored goal in first half', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
        period: '2h',
        player: {
          providerId: '123324123414',
        }
      } as any]);
      statsDataMock.period = '2h';
      selection.config.period = '1h';

      const actualResult = service.playerToScoreInPeriod(
        selection,
        statsDataMock as IScoreboardStatsUpdate,
        {} as IBetHistoryBet
      );

      expect(actualResult).toEqual({
        status: 'Losing',
        progress: {
          current: 0,
          desc: '0 of 1 Goal',
          target: 1
        }
      });
    });

    it('input data validation', () => {
      const poorUpdate = {
        home: {},
        away: {},
        score: {}
      } as any;
      expect(service.playerToScoreInPeriod(selection, poorUpdate, {} as IBetHistoryBet)).toEqual({ status: '' });

      poorUpdate.goals = {};
      expect(service.playerToScoreInPeriod(selection, poorUpdate, {} as IBetHistoryBet)).toEqual({ status: '' });

      poorUpdate.goals = { home: [], away: [] };
      const progress = {
        current: 0,
        desc: '0 of 1 Goal',
        target: 1
      };
      expect(service.playerToScoreInPeriod(selection, poorUpdate, {} as IBetHistoryBet))
        .toEqual({ status: STATUSES.LOSING, progress });
    });
  });

  describe('handicapBettingStatusHandler', () => {
    let goalsWithHandicap;
    beforeEach(() => {
      goalsWithHandicap = goalsObj;

      selection.part.outcome[0].externalStatsLink.statValue = '1';
      selection.part.outcome[0].externalStatsLink.statCategory = 'Score';
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      selection.part.outcome[0].name = 'Arsenal (-1)';
      selection.config.statCategory = 'Score';
      selection.config.period = '1h';

      statCategoryUtilityService.getScore.and.returnValue(goalsObj);
    });

    it('should return Losing status for 1ST HALF HANDICAP BETTING market', () => {
      goalsWithHandicap.score['1h'].home = -1;
      statCategoryUtilityService.applyHandicapValue.and.returnValue(goalsWithHandicap);

      expect(service.handicapBettingStatusHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return Losing status for 2nd HALF HANDICAP BETTING market when current 1st half ', () => {
      goalsWithHandicap.score['2h'] = undefined;
      selection.config.period = '2h';
      statCategoryUtilityService.applyHandicapValue.and.returnValue(goalsWithHandicap);

      expect(service.handicapBettingStatusHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return Winning status for 2ND HALF HANDICAP BETTING market', () => {
      selection.part.outcome[0].externalStatsLink.statValue = '2';
      selection.part.outcome[0].name = 'Arsenal (+2)';
      selection.config.period = '2h';
      goalsWithHandicap.score['2h'].home = 3;
      statCategoryUtilityService.applyHandicapValue.and.returnValue(goalsWithHandicap);

      expect(service.handicapBettingStatusHandler(selection, statsDataMock)).toEqual({ status: 'Winning' });
    });

    it('should return Losing status for HANDICAP BETTING market', () => {
      selection.part.outcome[0].externalStatsLink.statValue = '1';
      selection.part.outcome[0].name = 'Arsenal (+1)';
      selection.config.period = 'total';
      goalsWithHandicap.score['total'].home = 2;
      statCategoryUtilityService.applyHandicapValue.and.returnValue(goalsWithHandicap);

      expect(service.handicapBettingStatusHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });

    describe('input data validation: ', () => {
      let poorUpdate;
      beforeEach(() => {
        statCategoryUtilityService.applyHandicapValue.and.callFake(arg => arg);
        selection.config.generalInformationRequired = 'teams';
        poorUpdate = {
          home: { providerId: 1 },
          away: { providerId: 2 },
          score: {}
        } as any;
      });

      it('no update.period', () => {
        expect(service.handicapBettingStatusHandler(selection, poorUpdate)).toEqual({ status: '' });
      });

      it('no update.score period', () => {
        poorUpdate.period = '1h';
        expect(service.handicapBettingStatusHandler(selection, poorUpdate)).toEqual({ status: '' });
      });

      it('data valid', () => {
        poorUpdate.period = '1h';
        poorUpdate.score = {
          '1h': { home: 1, away: 0 }
        };
        expect(service.handicapBettingStatusHandler(selection, poorUpdate)).toEqual({ status: 'Winning' });
      });
    });
  });

  describe('matchBookingPointsStatusHandler', () => {
    let bet, players, progress;
    beforeEach(() => {
      bet = {
        settled: 'N'
      } as IBetHistoryBet;
      players = {
        home: [{ cards: { yellow: 1, red: 0 }}],
        away: []
      };

      selection.part.outcome[0].externalStatsLink.statValue = '>25';
      selection.part.outcome[0].externalStatsLink.statCategory = 'CardIndex';
      selection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      selection.config.statCategory = 'CardIndex';
      selection.config.period = 'total';

      statCategoryUtilityService.getCardIndex.and.returnValue(players);
      statCategoryUtilityService.getCardsFromPlayers.and.returnValue({ yellow: 1, red: 0 });
      statCategoryUtilityService.getBookingPoints.and.returnValue(10);

      progress = { current: 10, target: 25, desc: '10 of 25 Booking Points' };
    });

    it('should return Losing status and progress for MATCH Booking Points market(Over selection)', () => {
      selection.part.outcome[0].externalStatsLink.contestantId = null;
      progress = { current: 10, target: 30, desc: '10 of 30 Booking Points' };
      expect(service.matchBookingPointsStatusHandler(selection, statsDataMock, bet)).toEqual({ status: 'Losing', progress });
    });

    it('should return Winning status and progress for PARTICIPANT_1 Booking Points market(Equal selection)', () => {
      selection.part.outcome[0].externalStatsLink.statValue = '<25';
      progress = { current: 10, target: 20, desc: '10 of 20 Booking Points' };
      expect(service.matchBookingPointsStatusHandler(selection, statsDataMock, bet)).toEqual({ status: 'Winning', progress });
    });

    it('should return Losing status and progress for PARTICIPANT_2 Booking Points market(Under selection)', () => {
      selection.part.outcome[0].externalStatsLink.statValue = '=25';
      selection.part.outcome[0].externalStatsLink.contestantId = 'c8h9bw1l82s06h77xxrelzhur';

      expect(service.matchBookingPointsStatusHandler(selection, statsDataMock, bet)).toEqual({ status: 'Losing', progress });
    });
  });

  describe('goalscorersStatusHandler', () => {
    let bet, player, allGoals;
    beforeEach(() => {
      bet = {
        settled: 'N'
      } as IBetHistoryBet;
      player = { id: '26324' };
      allGoals = [
        {
          team: 'Home',
          scorer: '26324'
        }
      ];

      selection.part.outcome[0].name = 'LACAZETTE';
      selection.part.outcome[0].externalStatsLink.playerId = 'b2ak3yqqaexteldtl135erpx';
      selection.config.period = 'total';

      statCategoryUtilityService.getPlayerFromNameId.and.returnValue(player);
      statCategoryUtilityService.getPlayerByName.and.returnValue(player);
      statCategoryUtilityService.getAllGoals.and.returnValue(allGoals);
    });

    it('should NOT return any status for ANYTIME GOALSCORER market when no playerId', () => {
      selection.part.outcome[0].externalStatsLink = '';
      statCategoryUtilityService.getPlayerByName.and.returnValue(undefined);

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: '' });
    });

    it('should NOT return any status for ANYTIME GOALSCORER market when there is playerId', () => {
      selection.part.outcome[0].externalStatsLink = '';
      statCategoryUtilityService.getPlayerByName.and.returnValue(player);

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Won' });
    });

    it('should NOT return any status for ANYTIME GOALSCORER market when no player were found', () => {
      statCategoryUtilityService.getPlayerFromNameId.and.returnValue(undefined);

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: '' });
    });

    it('should return Lose status for LAST GOALSCORER market when no player were found but' +
      'is it NO GOALSCORER selection selected', () => {
      statCategoryUtilityService.getPlayerFromNameId.and.returnValue(undefined);
      selection.part.outcome[0].name = 'NO GOALSCORER';

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Lose' });
    });

    it('should return Losing status for ANYTIME GOALSCORER market when no goals were found', () => {
      statCategoryUtilityService.getAllGoals.and.returnValue([]);

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return Won status for ANYTIME GOALSCORER market when' +
      'selected player has scored and bet is settled', () => {
      bet.settled = 'Y';

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Won' });
    });

    it('should return Lose status for ANYTIME GOALSCORER market when' +
      'selected player has not scored and bet is settled', () => {
      bet.settled = 'Y';
      player.id = '123555';
      statCategoryUtilityService.getPlayerFromNameId.and.returnValue(player);

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return Lose status for FIRST GOALSCORER market when' +
      'selected player has not scored first and game is in progress', () => {
      player.id = '123555';
      selection.config.period = 'first';
      statCategoryUtilityService.getPlayerFromNameId.and.returnValue(player);

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Lose' });
    });

    it('should return Won status for FIRST GOALSCORER market when' +
      'selected player has scored first and game is in progress', () => {
      selection.config.period = 'first';

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Won' });
    });

    it('should return Winning status for LAST GOALSCORER market when' +
      'selected player has scored last and game is in progress', () => {
      selection.config.period = 'last';

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Winning' });
    });

    it('should return Losing status for LAST GOALSCORER market when' +
      'selected player has not scored last and game is in progress', () => {
      selection.config.period = 'last';
      allGoals = [
        {
          team: 'home',
          scorer: '26324'
        },
        {
          team: 'away',
          scorer: '99999'
        }
      ];
      statCategoryUtilityService.getAllGoals.and.returnValue(allGoals);

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });

    it('should return Won status for ANYTIME GOALSCORER market when' +
      'selected player has scored and game is in progress', () => {
      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Won' });
    });

    it('should return Losing status for ANYTIME GOALSCORER market when' +
      'selected player has not scored yet and game is in progress', () => {
      player.id = '123555';

      expect(service.goalscorersStatusHandler(selection, statsDataMock)).toEqual({ status: 'Losing' });
    });
  });

  it('@teamToGetFirstGoal and @teamToGetSecondGoal', () => {
    service['teamToGetFirstOrSecondGoalStatus'] = jasmine.createSpy('teamToGetFirstOrSecondGoalStatus')
      .and.returnValue({ status: STATUSES.LOSING });
    selection.config.generalInformationRequired = 'team';
    selection.config.statCategory = 'Score';
    const poorUpdate = {
      home: {},
      away: {},
      score: {},
    } as any;

    expect(service.teamToGetFirstGoal(selection, poorUpdate)).toEqual({ status: '' });
    expect(service.teamToGetSecondGoal(selection, poorUpdate)).toEqual({ status: '' });

    poorUpdate.goals = {};
    expect(service.teamToGetFirstGoal(selection, poorUpdate)).toEqual({ status: '' });
    expect(service.teamToGetSecondGoal(selection, poorUpdate)).toEqual({ status: '' });

    poorUpdate.goals = {
      home: [],
      away: []
    };
    expect(service.teamToGetFirstGoal(selection, poorUpdate)).toEqual({ status: STATUSES.LOSING });
    expect(service.teamToGetSecondGoal(selection, poorUpdate)).toEqual({ status: STATUSES.LOSING });
  });

  describe('playerToGetFirstBooking', () => {
    let bybSelection;
    let actualResult;

    beforeEach(() => {
      bybSelection = {
        config: {
          period: 'total'
        },
        part: {
          outcome: [
            {
              name: 'ARSENAL'
            }
          ]
        }
      } as any;
      statCategoryUtilityService.getPlayerByName.and.returnValue({ id: '26324' });
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([{ team: 'Away', player: '26324' }]);
    });

    it('should process first card and return "WON" in case conditions match for AWAY Team', () => {
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WON });
    });

    it('should return empty status', () => {
      statCategoryUtilityService.getPlayerByName.and.returnValue();
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status', () => {
      statCategoryUtilityService.getPlayerByName.and.returnValue();
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return STATUSES.LOSING', () => {
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([]);
      statCategoryUtilityService.getPlayerByName.and.returnValue({ id: '26324' });
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSING });
    });

    it('should return STATUSES.LOSE', () => {
      statCategoryUtilityService.getPlayerByName.and.returnValue({ id: '26323' });
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should return status empty when update.players is undefined', () => {
      statsDataMock.players = undefined;
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return status empty when update.players.home is undefined', () => {
      statsDataMock.players.home = undefined;
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return status empty when update.players.away is undefined', () => {
      statsDataMock.players.away = undefined;
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return status empty when update.teams is undefined', () => {
      statsDataMock.teams = undefined;
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return status empty when update.teams.home is undefined', () => {
      statsDataMock.teams.home = undefined;
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return status empty when update.teams.away is undefined', () => {
      statsDataMock.teams.away = undefined;
      actualResult = service['playerToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });
  });

  describe('teamToGetFirstBooking', () => {
    let bybSelection;
    let actualResult;

    beforeEach(() => {
      bybSelection = {
        config: {
          period: 'total'
        },
        title: 'First Half',
        part: {
          outcome: [{
            name: TEAMS.HOME,
            externalStatsLink: {
              contestantId: 'home'
            }
          }]
        }
      };
      statsDataMock.home.providerId = 'home';
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([{ team: TEAMS.HOME }]);
    });

    it('should return "STATUSES.WON" in case bet not settled and conditions match for HOME Team', () => {
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WON });
    });

    it('should return "LOSING" in case bet not settled and conditions not match for HOME Team', () => {
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([]);
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSING });
    });

    it('should return "WINNING" in case bet not settled and conditions not match for HOME Team', () => {
      bybSelection.title = 'No cards';
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([]);
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WINNING });
    });

    it('should return "LOSE" in case bet not settled and conditions not match for HOME Team', () => {
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([{ team: TEAMS.AWAY }]);
      bybSelection.title = 'No cards';
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should return "LOSE" in case bet not settled and conditions match for AWAY Team', () => {
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([{ team: TEAMS.AWAY }]);
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should return "LOSING" in case bet not settled and conditions not match for AWAY Team', () => {
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([]);
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSING });
    });

    it('should return "WINNING" in case conditions not match for AWAY Team', () => {
      bybSelection.title = 'No cards';
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([]);
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WINNING });
    });

    it('should return "LOSE" in case bet not settled and conditions not match for AWAY Team', () => {
      statCategoryUtilityService.getAllCards = jasmine.createSpy('getAllCards').and.returnValue([{ team: TEAMS.HOME }]);
      bybSelection.title = 'No cards';
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should return empty status when update.teams is undefined', () => {
      statsDataMock.teams = undefined;
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status when update.teams.home is undefined', () => {
      statsDataMock.teams.home = undefined;
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return empty status when update.teams.away is undefined', () => {
      statsDataMock.teams.away = undefined;
      actualResult = service['teamToGetFirstBooking'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: '' });
    });
  });

  describe('goalsConcededStatusHandler', () => {
    let bet, player, actualResult, preMatchStats, progress;
    beforeEach(() => {
      bet = {
        settled: 'N'
      } as IBetHistoryBet;
      player = { id: '26324', team: 'home', goalConceded: 0 };
      preMatchStats = JSON.stringify({
        'data': {
          'participants': {
            'home': {
              'lineup': [ { 'id': '26324', 'substitute': false }]
            },
            'away': {}
          }
        }
      });

      selection.config.period = 'total';
      selection.config.generalInformationRequired = 'player';
      selection.part.outcome[0].externalStatsLink.statValue = '>=2';
      selection.part.outcome[0].externalStatsLink.statCategory = 'GoalConceded';
      selection.part.outcome[0].externalStatsLink.playerId = '3zl1q2gk6tdmzirsyfgm38no5';

      statCategoryUtilityService.getPlayerStats.and.returnValue([{}]);
      statCategoryUtilityService.getPlayerById.and.returnValue(player);

      windowRefService.nativeWindow.localStorage.getItem.and.returnValue(preMatchStats);
      progress = {
        current: 0,
        desc: '0 of 2 Goals Conceded',
        target: 2
      };
    });

    it('should check for player playing if both preMatchOptaStats and player have data', () => {
      player = { id: '26324', team: 'home', goalConceded: 0 };
      preMatchStats = JSON.stringify({
        'data': {
          'participants': {
            'home': {
              'lineup': [{ 'id': '26324', 'substitute': false }]
            },
            'away': {}
          }
        }
      });
      windowRefService.nativeWindow.localStorage.getItem.and.returnValue(preMatchStats);
      statCategoryUtilityService.getPlayerById.and.returnValue(player);
      actualResult = service.goalsConcededStatusHandler(selection, statsDataMock, bet);
      expect(actualResult).toEqual({ status: 'Losing', progress });
    });

    it('should return status and progress if  preMatchOptaStats is false  and player have data', () => {
      windowRefService.nativeWindow.localStorage.getItem.and.returnValue(null);
      statCategoryUtilityService.getPlayerById.and.returnValue(player);
      actualResult = service.goalsConcededStatusHandler(selection, statsDataMock, bet);
      expect(actualResult).toEqual({ status: 'Losing', progress });
    });

    it('should return status and progress if  preMatchOptaStats is true  and player false', () => {
      windowRefService.nativeWindow.localStorage.getItem.and.returnValue(preMatchStats);
      statCategoryUtilityService.getPlayerById.and.returnValue(null);
      actualResult = service.goalsConcededStatusHandler(selection, statsDataMock, bet);
      expect(actualResult).toEqual({ status: 'Losing', progress });
    });

    it('should not return status if no prematch stats and no player were found', () => {
      windowRefService.nativeWindow.localStorage.getItem.and.returnValue(null);
      statCategoryUtilityService.getPlayerById.and.returnValue(null);
      actualResult = service.goalsConcededStatusHandler(selection, statsDataMock, bet);

      expect(actualResult).toEqual({ status: '' });
    });

    it('should not return status if player doesnt play in the match ', () => {
      preMatchStats = JSON.stringify({
        'data': {
          'participants': {
            'home': {
              'lineup': [ { 'id': '26324', 'substitute': true }]
            },
            'away': {}
          }
        }
      });
      windowRefService.nativeWindow.localStorage.getItem.and.returnValue(preMatchStats);

      actualResult = service.goalsConcededStatusHandler(selection, statsDataMock, bet);

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return Losing status for PLAYER TOTAL GOALS CONCEDED market', () => {
      actualResult = service.goalsConcededStatusHandler(selection, statsDataMock, bet);

      expect(actualResult).toEqual({ status: 'Losing', progress });
    });

    it('should return Winning status for PLAYER TO KEEP A CLEAN SHEET market', () => {
      progress = {
        current: 0,
        desc: '0 of 0 Goals Conceded',
        target: 0
      };
      selection.part.outcome[0].externalStatsLink.statValue = '=0';
      actualResult = service.goalsConcededStatusHandler(selection, statsDataMock, bet);

      expect(actualResult).toEqual({ status: 'Winning', progress });
    });
  });

  it('isUpdatePlayersDataValid', () => {
    const upd = {} as any;
    expect(service['isUpdatePlayersDataValid'](upd)).toBe(false);

    upd.players = {};
    expect(service['isUpdatePlayersDataValid'](upd)).toBe(false);

    upd.players.home = {};
    expect(service['isUpdatePlayersDataValid'](upd)).toBe(false);

    upd.players.away = {};
    expect(service['isUpdatePlayersDataValid'](upd)).toBe(true);
  });

  describe('#validateGoalCase', () => {
    it('should return no goal', () => {
      const response = service['validateGoalCase'](true, 'team');
      expect(response).toBe('No Goal');
    });
    it('should return team', () => {
      const response = service['validateGoalCase'](false, 'team');
      expect(response).toBe('team');
    });
  });
});

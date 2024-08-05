import { BetTrackingRulesHelperService } from '@bybHistoryModule/services/betTrackingRules/bet-tracking-rules-helper.service';
import { IBybSelection } from '@lazy-modules/bybHistory/models/byb-selection.model';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';
import {
  IScoreboardStatsUpdate,
  ITeams
} from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';
import {
  DOUBLE_TEAMS,
  TEAMS,
  STATUSES,
  PLAYER_SHOTS
} from '@lazy-modules/bybHistory/constants/byb-5aside-markets-config.constant';
import { TEAM_STATS, PLAYER_STATS } from '@lazy-modules/bybHistory/services/betTrackingRules/stat-category-utility.service';
import { scoreboardsStatsUpdate } from '@lazy-modules/bybHistory/services/bybSelectionsService/scoreboards-stats-update.mock';

describe('BetTrackingRulesHelperService', () => {
  let service: BetTrackingRulesHelperService;
  let statCategoryUtilityService;
  let statsDataMock, selection, update, goalsObj;

  beforeEach(() => {
    statCategoryUtilityService = {
      getScore: jasmine.createSpy('getScore').and.returnValue({ total: 1}),
      getCurrentPeriod: jasmine.createSpy('getCurrentPeriod').and.returnValue('1h'),
      getHomeAwayTeamByName: jasmine.createSpy('getHomeAwayTeamByName').and.returnValue('Home'),
      getPlayerById: jasmine.createSpy('getPlayerById'),
      getDoubleHomeAwayTeamByName: jasmine.createSpy('getDoubleHomeAwayTeamByName').and.returnValue(DOUBLE_TEAMS.HOME_OR_DRAW),
      getAllGoals: jasmine.createSpy('getAllGoals').and.returnValue([{
        team: 'Home',
      } as any]),
      getPlayerStats: jasmine.createSpy('getPlayerStats'),
      applyHandicapValue: jasmine.createSpy('applyHandicapValue'),
      getCardIndex: jasmine.createSpy('getCardIndex'),
      getCardsFromPlayers: jasmine.createSpy('getCardsFromPlayers'),
      getBookingPoints: jasmine.createSpy('getBookingPoints'),
      getPlayerByName: jasmine.createSpy('getPlayerByName')
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
      period: '',
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

    service = new BetTrackingRulesHelperService(statCategoryUtilityService);
  });

  describe('getSelectionProgress', () => {
    it('should return null', () => {
      selection = {
        part: { outcome: [{}] }
      } as any;
      expect(service['getSelectionProgress'](selection, {} as any, 1)).toBe(null);
    });

    it('should return progress', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '3', statCategory: 'Score' }
          }]
        }
      } as any;
      expect(service['getSelectionProgress'](selection, {} as any, 2)).toEqual({
        current: 2, target: 3, desc: '2 of 3 Goals'
      });
    });

    it('should return progress (settled bet)', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '3', statCategory: 'Score', currentValue: '2' }
          }]
        }
      } as any;
      const bet: any = { settled: 'Y' };
      expect(service['getSelectionProgress'](selection, bet, 2)).toEqual({
        current: 2, target: 3, desc: '2 Goals'
      });
    });

    it('should return progress (settled bet) with singular category', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '3', statCategory: 'Score', currentValue: '2' }
          }]
        }
      } as any;
      const bet: any = { settled: 'Y' };
      expect(service['getSelectionProgress'](selection, bet, 1)).toEqual({
        current: 1, target: 3, desc: '1 Goal'
      });
    });

    it('should return desc for singular catedoties', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '1', statCategory: 'Score', currentValue: '2' }
          }]
        }
      } as any;
      expect(service['getSelectionProgress'](selection, {} as any, 2)).toEqual({
        current: 2, target: 1, desc: '2 of 1 Goal'
      });
    });
  });

  describe('getBookingSelectionProgress', () => {
    it('should return null', () => {
      selection = {
        part: { outcome: [{}] }
      } as any;
      expect(service['getBookingSelectionProgress'](selection, {} as any, 10)).toBe(null);
    });

    it('should return progress Over', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '>25', statCategory: 'CardIndex' }
          }]
        }
      } as any;
      expect(service['getBookingSelectionProgress'](selection, {} as any, 10)).toEqual({
        current: 10, target: 30, desc: '10 of 30 Booking Points'
      });
    });

    it('should return progress Under', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '<40', statCategory: 'CardIndex' }
          }]
        }
      } as any;
      expect(service['getBookingSelectionProgress'](selection, {} as any, 25)).toEqual({
        current: 25, target: 35, desc: '25 of 35 Booking Points'
      });
    });

    it('should return progress Equal', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '=25', statCategory: 'CardIndex' }
          }]
        }
      } as any;
      expect(service['getBookingSelectionProgress'](selection, {} as any, 10)).toEqual({
        current: 10, target: 25, desc: '10 of 25 Booking Points'
      });
    });

    it('should return progress (settled bet)', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '>25', statCategory: 'CardIndex', currentValue: '10' }
          }]
        }
      } as any;
      const bet: any = { settled: 'Y' };
      expect(service['getBookingSelectionProgress'](selection, bet, 10)).toEqual({
        current: 10, target: 30, desc: '10 Booking Points'
      });
    });

    it('should return progress (unsettled bet)', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '>25', statCategory: 'CardIndex', currentValue: '10' }
          }]
        }
      } as any;
      const bet: any = { settled: 'N' };
      expect(service['getBookingSelectionProgress'](selection, bet, 10)).toEqual({
        current: 10, target: 30, desc: '10 of 30 Booking Points'
      });
    });

    it('should return progress Over 10 selection', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '>10', statCategory: 'CardIndex' }
          }]
        }
      } as any;
      expect(service['getBookingSelectionProgress'](selection, {} as any, 10)).toEqual({
        current: 10, target: 20, desc: '10 of 20 Booking Points'
      });
    });

    it('should return progress Over 10 selection Fail', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '>20', statCategory: 'CardIndex' }
          }]
        }
      } as any;
      expect(service['getBookingSelectionProgress'](selection, {} as any, 10)).toEqual({
        current: 10, target: 25, desc: '10 of 25 Booking Points'
      });
    });

    it('should return progress Under 10 selection', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '<10', statCategory: 'CardIndex' }
          }]
        }
      } as any;
      expect(service['getBookingSelectionProgress'](selection, {} as any, 10)).toEqual({
        current: 10, target: 0, desc: '10 of 0 Booking Points'
      });
    });

    it('should return progress Under 10 selection fail', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '<25', statCategory: 'CardIndex' }
          }]
        }
      } as any;
      expect(service['getBookingSelectionProgress'](selection, {} as any, 10)).toEqual({
        current: 10, target: 20, desc: '10 of 20 Booking Points'
      });
    });

    it('should return progress (settled bet)', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '>25', statCategory: 'CardIndex', currentValue: '10' }
          }]
        }
      } as any;
      const bet: any = { settled: 'Y' };
      expect(service['getBookingSelectionProgress'](selection, bet, 1)).toEqual({
        current: 1, target: 30, desc: '1 Booking Point'
      });
    });

    it('should return progress (unsettled bet)', () => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '>25', statCategory: 'CardIndex', currentValue: '10' }
          }]
        }
      } as any;
      const bet: any = { settled: 'N' };
      expect(service['getBookingSelectionProgress'](selection, bet, 1)).toEqual({
        current: 1, target: 30, desc: '1 of 30 Booking Points'
      });
    });

  });

  describe('getStatCategoryObj', () => {
    it('should trigger particular method of statCategoryUtilityService', () => {
      selection = {
        config: {
          statCategory: 'Score',
          generalInformationRequired: 'teams'
        }
      };
      const actualResult = service['getStatCategoryObj'](selection as IBybSelection, {} as IScoreboardStatsUpdate);

      expect(actualResult).toEqual({total: 1});
    });

    it('should Not trigger method of statCategoryUtilityService if no handler were found', () => {
      selection = {
        config: {
          statCategory: 'Assist',
          generalInformationRequired: 'player'
        }
      };
      const actualResult = service['getStatCategoryObj'](selection as IBybSelection, {} as IScoreboardStatsUpdate);

      expect(actualResult).toEqual({});
    });
  });

  describe('getTotalRedCardsStatus', () => {
    it('should return Winning if isRedCard true, isYesOutcome true', () => {
      expect(service['getTotalRedCardsStatus'](true, true)).toEqual('Winning');
    });

    it('should return Loosing if isRedCard true, isYesOutcome false', () => {
      expect(service['getTotalRedCardsStatus'](true, false)).toEqual('Losing');
    });

    it('should return Losing if isRedCard false, isYesOutcome false', () => {
      expect(service['getTotalRedCardsStatus'](false, true)).toEqual('Losing');
    });

    it('should return Winning if isRedCard false, isYesOutcome false', () => {
      expect(service['getTotalRedCardsStatus'](false, false)).toEqual('Winning');
    });
  });

  describe('getFirstHalfRedCardsStatus', () => {
    it('should return Winning if isRedCard true, isYesOutcome true, isBetSettled false, isFirstHalf true', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getFirstHalfRedCardsStatus'](true, true, '1h')).toEqual('Winning');
    });

    it('should return Losing if isRedCard true, isYesOutcome false, isBetSettled false, isFirstHalf true', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getFirstHalfRedCardsStatus'](true, false, '1h')).toEqual('Losing');
    });

    it('should return Losing if isRedCard true, isYesOutcome true, isSecondOrTotal true', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      expect(service['getFirstHalfRedCardsStatus'](true, true, '2h')).toEqual('Won');
    });

    it('should return Losing if isRedCard true, isYesOutcome false, isSecondOrTotal true', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      expect(service['getFirstHalfRedCardsStatus'](true, false, '2h')).toEqual('Lose');
    });

    it('should return Losing if isRedCard false, isYesOutcome false, isBetSettled false, isFirstHalf true', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getFirstHalfRedCardsStatus'](false, true, '1h')).toEqual('Losing');
    });

    it('should return Winning if isRedCard false, isYesOutcome false, isBetSettled false, isFirstHalf true', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getFirstHalfRedCardsStatus'](false, false, '1h')).toEqual('Winning');
    });

    it('should return Losing if isRedCard false, isYesOutcome true, isSecondOrTotal true', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      expect(service['getFirstHalfRedCardsStatus'](false, true, '2h')).toEqual('Lose');
    });

    it('should return Winning if isRedCard false, isYesOutcome false, isSecondOrTotal true', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      expect(service['getFirstHalfRedCardsStatus'](false, false, '2h')).toEqual('Won');
    });
  });

  describe('bothTeamsHalfScoredStatus', () => {
    let scoreObj;

    beforeEach(() => {
     scoreObj = { score: {
        '1h': { home: 1, away: 1 },
        '2h': { home: 1, away: 1 },
        total: { home: 2, away: 2 },
      }};
    });

    it('should call bothTeamsHalfScoredStatus and return status based on selection name yes/no', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      selection.config.period = '1h';
      expect(service['bothTeamsHalfScoredStatus'](scoreObj.score, update, selection)).toEqual('Won');

      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service['bothTeamsHalfScoredStatus'](scoreObj.score, update, selection)).toEqual('Lose');

      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      scoreObj.score['1h'].away = 0;
      selection.config.period = '1h';
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');

      expect(service['bothTeamsHalfScoredStatus'](scoreObj.score, update, selection)).toEqual('Won');

      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['bothTeamsHalfScoredStatus'](scoreObj.score, update, selection)).toEqual('Winning');

      scoreObj.score['2h'].home = 0;
      selection.config.period = '2h';
      expect(service['bothTeamsHalfScoredStatus'](scoreObj.score, update, selection)).toEqual('Winning');

      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      expect(service['bothTeamsHalfScoredStatus'](scoreObj.score, update, selection)).toEqual('Losing');

      scoreObj.score['2h'] = undefined;
      selection.config.period = '2h';
      expect(service['bothTeamsHalfScoredStatus'](scoreObj.score, update, selection)).toEqual('Losing');

      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service['bothTeamsHalfScoredStatus'](scoreObj.score, update, selection)).toEqual('Winning');

      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      expect(service['bothTeamsHalfScoredStatus'](scoreObj.score, update, selection)).toEqual('Losing');
    });
  });

  describe('bothTeamsBothHalves', () => {
    let scoreObj;
    beforeEach(() => {
     scoreObj = { score: {
        '1h': { home: 1, away: 1 },
        '2h': { home: 1, away: 1 },
        total: { home: 2, away: 2 },
      }};
    });

    it('should call bothTeamsBothHalves and return Won or Lose based on selection name yes/no - SCORE 1h:(1:1) 2h:(1:1)', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      selection.config.period = 'total';
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Won');

      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Lose');
    });

    it('should call bothTeamsBothHalves and return Won or Lose based on selection name yes/no - SCORE 1h:(1:1) 2h:(1:1)', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      selection.config.period = 'total';
      update.period = '2h';
      scoreObj.score['1h'].home = 0;
      // 1h:(0:1) 2h:(0:0)
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Lose');

      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Won');

      // 1h:(1:1) 2h:(2:0)
      scoreObj.score['1h'].home = 2;
      scoreObj.score['2h'].home = 0;
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Winning');

      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Losing');

      scoreObj.score['1h'].home = 2;
      scoreObj.score['2h'].home = 2;
      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Lose');

      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Won');
    });
    it('should call bothTeamsBothHalves and return Won or Lose based on selection name yes/no - SCORE 1h:(1:1) 2h:(1:1) (Case: 2)', () => {
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(scoreObj);
      selection.part.outcome[0].externalStatsLink.statValue = '>0.5';
      selection.config.period = 'total';
      update.period = '2h';
      scoreObj.score['1h'].home = 0;
      spyOn(service as any, 'validateTeamsBothHalves').and.returnValue(false);
      // 1h:(0:1) 2h:(0:0)
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Losing');

      selection.part.outcome[0].externalStatsLink.statValue = '<0.5';
      expect(service['bothTeamsBothHalves'](scoreObj.score, update, selection)).toEqual('Winning');
    });
  });

  describe('getRedCardsParticipantStatus', () => {
    it('should call getTotalRedCardsStatus', () => {
      service['getTotalRedCardsStatus'] = jasmine.createSpy('getTotalRedCardsStatus');

      service['getRedCardsParticipantStatus'](2, true);
      expect(service['getTotalRedCardsStatus']).toHaveBeenCalledWith(true, true);
    });
  });

  describe('getFullRedsStatus', () => {
    it('should call getTotalRedCardsStatus', () => {
      service['getTotalRedCardsStatus'] = jasmine.createSpy('getTotalRedCardsStatus');
      let cardsObj = {away: {periods: {total: {redCards: 2}}}, home: {periods: {total: {redCards: 1}}}};
      service['getFullRedsStatus']('YES', cardsObj as any, 'total', 'ert');
      expect(service['getTotalRedCardsStatus']).toHaveBeenCalledWith(true, true);

      cardsObj.away.periods.total = undefined;
      cardsObj.home.periods.total = undefined;
      service['getFullRedsStatus']('YES', cardsObj as any, 'total', 'ert');
      expect(service['getTotalRedCardsStatus']).toHaveBeenCalledWith(false, true);

      cardsObj = {away: {periods: {total: undefined}}, home: {periods: {total: {redCards: 1}}}};
      service['getFullRedsStatus']('YES', cardsObj as any, 'total', 'ert');
      expect(service['getTotalRedCardsStatus']).toHaveBeenCalledWith(false, true);
    });

    it('should call getFirstHalfRedCardsStatus', () => {
      service['getFirstHalfRedCardsStatus'] = jasmine.createSpy('getFirstHalfRedCardsStatus');
      const bet = { settled: 'Y' };
      const cardsObj = {
        away: {
          periods: { '1h': { redCards: 2 } }
        },
        home: {
          periods: { '1h': { redCards: 1 } }
        }
      };
      service['getFullRedsStatus']('YES', cardsObj as any, '1h', '1h');
      expect(service['getFirstHalfRedCardsStatus']).toHaveBeenCalledWith(true, true, '1h');
    });
  });

  describe('getFirstHalfBettingStatus', () => {
    const conditions = {
      [ TEAMS.DRAW ]: true,
      [ TEAMS.AWAY ]: false,
      [ TEAMS.HOME ]: false
    };
    it('should get status for first half betting markets(Winning status)', () => {
      const actualResult = service['getFirstHalfBettingStatus'](
        conditions,
        'Draw',
        '1h'
      );

      expect(actualResult).toEqual('Winning');
    });

    // it('should get status for first half betting markets(Won status)', () => {
    //   const actualResult = service['getFirstHalfBettingStatus'](
    //     conditions,
    //     'Draw',
    //     '1h'
    //   );
    //
    //   expect(actualResult).toEqual('Won');
    // });

    it('should get status for first half betting markets(Won status - current time - 2h)', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      const actualResult = service['getFirstHalfBettingStatus'](
        conditions,
        'Draw',
        '2h'
      );

      expect(actualResult).toEqual('Won');
    });

    it('should get status for first half betting markets(Losing status)', () => {
      const actualResult = service['getFirstHalfBettingStatus'](
        conditions,
        'Home',
        '1h'
      );

      expect(actualResult).toEqual('Losing');
    });
  });

  describe('getFullMatchStatus', () => {
    const conditions = {
      [ TEAMS.DRAW ]: true,
      [ TEAMS.AWAY ]: false,
      [ TEAMS.HOME ]: false
    };
    it('should get full match status(Winning status)', () => {
      const actualResult = service['getFullMatchStatus'](
        conditions,
        'Draw'
      );

      expect(actualResult).toEqual('Winning');
    });

    it('should get full match status(Losing status)', () => {
      const actualResult = service['getFullMatchStatus'](
        conditions,
        'Home'
      );

      expect(actualResult).toEqual('Losing');
    });
  });

  describe('getMatchBettingStatus', () => {
    it('should get status for MATCH BETTING 1st HALF market(Winning status)', () => {
      const actualResult = service['getMatchBettingStatus'](
        goalsObj,
        'Draw',
        '1h',
        '1h'
      );

      expect(actualResult).toEqual('Winning');
    });

    it('should get status for MATCH BETTING 2nd HALF market(Winning status)', () => {
      const actualResult = service['getMatchBettingStatus'](
        goalsObj,
        'Away',
        '2h',
        '2h'
      );

      expect(actualResult).toEqual('Winning');
    });

    it('should get status for MATCH BETTING 2nd HALF market(Losing status) when current period is 1h', () => {
      goalsObj.score['2h'] = undefined;
      const actualResult = service['getMatchBettingStatus'](
        goalsObj,
        'Away',
        '2h',
        '1h'
      );

      expect(actualResult).toEqual('Losing');
    });

    it('should get status for MATCH BETTING 2nd HALF market(Losing status) when no current period', () => {
      goalsObj.score['2h'] = undefined;
      const actualResult = service['getMatchBettingStatus'](
        goalsObj,
        'Away',
        '2h'
      );

      expect(actualResult).toEqual('Losing');
    });
  });

  describe('parseStatValue', () => {
    beforeEach(() => {
      selection = {
        part: {
          outcome: [{
            externalStatsLink: {
              statValue: undefined,
              statCategory: 'Score'
            }
          }]
        }
      } as any;

      it('should parse ">0.5" as 1', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '>0.5';

        expect(service['getSelectionProgress'](selection as IBybSelection, {} as IBetHistoryBet, 0))
          .toEqual({current: 0, target: 1, desc: '0 of 1 Goals'});
      });

      it('should parse "<0.5" as 0', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '<0.5';

        expect(service['getSelectionProgress'](selection as IBybSelection, {} as IBetHistoryBet, 0))
          .toEqual({current: 0, target: 0, desc: '0 of 0 Goals'});
      });

      it('should parse ">=1" as 1', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '>=1';

        expect(service['getSelectionProgress'](selection as IBybSelection, {} as IBetHistoryBet, 0))
          .toEqual({current: 0, target: 1, desc: '0 of 1 Goals'});
      });

      it('should parse "1" as 1', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '1';

        expect(service['getSelectionProgress'](selection as IBybSelection, {} as IBetHistoryBet, 0))
          .toEqual({current: 0, target: 1, desc: '0 of 1 Goals'});
      });

      it('should parse "=1" as 1', () => {
        selection.part.outcome[0].externalStatsLink.statValue = '=1';

        expect(service['getSelectionProgress'](selection as IBybSelection, {} as IBetHistoryBet, 0))
          .toEqual({current: 0, target: 1, desc: '0 of 1 Goals'});
      });
    });
  });

  describe('getPlayerStatusAndProgress', () => {
    it('should handle player status', () => {
      selection = {
        config: {
          statCategory: 'Assist',
          generalInformationRequired: 'player',
          hasLine: true
        },
        part: {
          outcome: [{
            externalStatsLink: {
              statValue: '1',
              statCategory: 'Assists',
              playerId: '26324'
            }
          }]
        }
      } as any;
      const objGoals = {
        home: [{ id: '26324', assists: 3 }],
        away: [{ id: '26323' }]
      };
      const optaStatValue = 3;
      service['getStatCategoryObj'] = jasmine.createSpy('getStatCategoryObj').and.returnValue(objGoals);
      service['getOptaStatValue'] = jasmine.createSpy('getOptaStatValue').and.returnValue(optaStatValue);
      service['getOverTotalMarketsStatus'] = jasmine.createSpy('getOverTotalMarketsStatus').and.returnValue('Lose');
      service['parseStatValue'] = jasmine.createSpy('parseStatValue').and.returnValue(1);
      service['getSelectionProgress'] = jasmine.createSpy('getSelectionProgress').and.returnValue({
        current: 1,
        target: 3,
        desc: '0 of 3 Assists'
      });

      const actualResult = service['getPlayerStatusAndProgress'](
        selection as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.ASSISTS,
        PLAYER_SHOTS.TOTAL
      );

      expect(service['getStatCategoryObj']).toHaveBeenCalledWith(
        selection as IBybSelection,
        {} as IScoreboardStatsUpdate
      );
      expect(service['getOptaStatValue']).toHaveBeenCalledWith(
        objGoals as any,
        selection.part.outcome[0].externalStatsLink.playerId,
        PLAYER_STATS.ASSISTS,
        PLAYER_SHOTS.TOTAL
      );
      expect(service['getOverTotalMarketsStatus']).toHaveBeenCalledWith(optaStatValue, 1);
      expect(service['parseStatValue']).toHaveBeenCalledWith(selection.part.outcome[0].externalStatsLink.statValue);
      expect(service['getSelectionProgress']).toHaveBeenCalledWith(
        selection as IBybSelection,
        {} as IBetHistoryBet,
        optaStatValue
      );
      expect(actualResult).toEqual({ status: 'Lose', progress: { current: 1, target: 3, desc: '0 of 3 Assists' }});
    });

    it('should return no status if no player provided (no opta stat value)', () => {
      service['getOptaStatValue'] = jasmine.createSpy('getOptaStatValue').and.returnValue(null);

      const actualResult = service['getPlayerStatusAndProgress'](
        selection as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.ASSISTS
      );

      expect(actualResult).toEqual({ status: '' });
    });

    it('should return Won status if player achieved stats', () => {
      service['getOptaStatValue'] = jasmine.createSpy('getOptaStatValue').and.returnValue(3);
      selection.part.outcome[0].externalStatsLink.statValue = '>=3';
      selection.part.outcome[0].externalStatsLink.statCategory = 'Assists';

      const actualResult = service['getPlayerStatusAndProgress'](
        selection as IBybSelection,
        {} as IScoreboardStatsUpdate,
        {} as IBetHistoryBet,
        PLAYER_STATS.ASSISTS
      );

      expect(actualResult).toEqual({ status: 'Won', progress: { current: 3, target: 3, desc: '3 of 3 Assists' }});
    });
  });

  describe('getOptaStatValue', () => {
    let objGoals;
    let playerId;

    beforeEach(() => {
      objGoals = {
        home: [{ providerId: '26324', assists: 3 }],
        away: [{ providerId: '26323' }]
      } as any;
      playerId = '26324';
    });
    it('should return 3', () => {
      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.ASSISTS)).toBe(objGoals.home[0].assists);
    });

    it('should return null', () => {
      playerId = '26327';
      objGoals = null;

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.ASSISTS)).toBeNull();
    });

    it('should return null', () => {
      objGoals = {} as any;

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.ASSISTS)).toBeNull();
    });

    it('should return null', () => {
      objGoals = {
        home: [],
        away: []
      } as any;

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.ASSISTS)).toBeNull();
    });

    it('should return null', () => {
      objGoals = {
        home: [],
        away: [{}]
      } as any;

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.ASSISTS)).toBeNull();
    });

    it('should return null', () => {
      objGoals = {
        home: [{}],
        away: []
      } as any;

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.ASSISTS)).toBeNull();
    });

    it('should return null', () => {
      objGoals = {
        home: [{}],
        away: [{}]
      } as any;

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.ASSISTS)).toBeNull();
    });

    it('should return undefined', () => {
      objGoals = {
        home: [{}],
        away: [{ providerId: '26324', shots: { total: 3, onTarget: 1 } }]
      } as any;

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.ASSISTS, PLAYER_SHOTS.TOTAL)).toBeUndefined();
    });

    it('should return null', () => {
      objGoals = {
        home: [{}],
        away: [{ providerId: '26324', shots: { total: 3, onTarget: 1 } }]
      } as any;
      playerId = '26325';

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.SHOTS, PLAYER_SHOTS.TOTAL)).toBeNull();
    });

    it('should return 5', () => {
      objGoals = {
        home: [{}],
        away: [{ providerId: '26324', shots: { total: 5, onTarget: 1 } }]
      } as any;

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.SHOTS, PLAYER_SHOTS.TOTAL)).toBe(5);
    });

    it('should return 1', () => {
      objGoals = {
        home: [{}],
        away: [{ providerId: '26324', shots: { total: 3, onTarget: 1 } }]
      } as any;

      expect(service['getOptaStatValue'](objGoals, playerId, PLAYER_STATS.SHOTS, PLAYER_SHOTS.ON_TARGET)).toBe(1);
    });
  });

  describe('getTeamByExternalStatsLink', () => {
    selection = {
      part: {
        outcome: [{
          externalStatsLink: {
            contestantId: ''
          }
        }]
      }
    } as any;

    it('should return "Home" if providerId matches', () => {
      selection.part.outcome[0].externalStatsLink.contestantId = 'home';

      expect(service['getTeamByExternalStatsLink'](selection, update)).toEqual('Home');
    });

    it('should return "Away" if providerId matches', () => {
      selection.part.outcome[0].externalStatsLink.contestantId = 'away';

      expect(service['getTeamByExternalStatsLink'](selection, update)).toEqual('Away');
    });

    it('should return "Draw" if providerId does not match', () => {
      selection.part.outcome[0].externalStatsLink.contestantId = 'draw';

      expect(service['getTeamByExternalStatsLink'](selection, update)).toEqual('Draw');
    });

  });

  describe('getGoalsByTeamAndPeriod', () => {
    const periodStart = '30:00',
      periodEnd = '60:00';

    const goals = [{
      time: '05:00',
      team: 'Home'
    } as any, {
      time: '06:00',
      team: 'Away'
    } as any, {
      time: '35:00',
      team: 'Home'
    } as any, {
      time: '36:00',
      team: 'Away'
    } as any];

    it('should get home and away goals within 0-30 range', () => {
      expect(service['getGoalsByTeamAndPeriod'](goals, periodStart))
        .toEqual({ [TEAMS.HOME]: [goals[0]], [TEAMS.AWAY]: [goals[1]] });
    });

    it('should get home and away goals within 30-60 range', () => {
      expect(service['getGoalsByTeamAndPeriod'](goals, periodEnd, periodStart))
        .toEqual({ [TEAMS.HOME]: [goals[2]], [TEAMS.AWAY]: [goals[3]] });
    });

    it('should get no goals if team is not home nor away', () => {
      expect(service['getGoalsByTeamAndPeriod']([], periodStart))
        .toEqual({ [TEAMS.HOME]: [], [TEAMS.AWAY]: [] });
    });
  });

  describe('getTeamStatsByPeriod', () => {
    const stat = TEAM_STATS.CORNERS;
    let statsCategoryObj = {
      home: {
        total: { corners: 5 },
        '1h': { corners: 10 },
        '2h': { corners: 15 }
      },
      away: {
        total: { corners: 20 },
        '1h': { corners: 25 },
        '2h': { corners: 30 }
      }
    } as ITeams;

    it('should return home and away total corners', () => {
      expect(service['getTeamStatsByPeriod']('total', statsCategoryObj, stat)).toEqual({ home: 5, away: 20 });
    });

    it('should return home and away corners from 1st half', () => {
      expect(service['getTeamStatsByPeriod']('1h', statsCategoryObj, stat)).toEqual({ home: 10, away: 25 });
    });

    it('should return home and away corners from 2nd half', () => {
      expect(service['getTeamStatsByPeriod']('2h', statsCategoryObj, stat)).toEqual({ home: 15, away: 30 });
    });

    it('should return home and away corners as a zero, because 2nd half is not started yet and' +
      'current period is 1st half or half time' +
      '(2ND HALF CORNERS MATCH BET, PARTICIPANT_1|PARTICIPANT_2 2ND HALF TOTAL CORNERS)', () => {
      statsCategoryObj = {
        home: {
          total: { corners: 5 },
          '1h': { corners: 10 }
        },
        away: {
          total: { corners: 20 },
          '1h': { corners: 25 }
        }
      } as ITeams;
      expect(service['getTeamStatsByPeriod']('2h', statsCategoryObj, stat)).toEqual({ home: 0, away: 0 });
    });

    it('should return empty object if period does not match', () => {
      expect(service['getTeamStatsByPeriod']('custom', statsCategoryObj, stat)).toEqual({});
    });
  });

  describe('isUnder', () => {
    let statValue: string;

    it('should return true if statValue equals UNDER X.Y', () => {
      statValue = '<';
      expect(service['isUnder'](statValue)).toBeTruthy();
    });

    it('should return false if statValue equals OVER X.Y', () => {
      statValue = '>';
      expect(service['isUnder'](statValue)).toBeFalsy();

      statValue = '>=';
      expect(service['isUnder'](statValue)).toBeFalsy();
    });
  });

  describe('isOver', () => {
    let statValue: string;

    it('should return true if statValue equals OVER X.Y', () => {
      statValue = '>';
      expect(service['isOver'](statValue)).toBeTruthy();

      statValue = '>=';
      expect(service['isOver'](statValue)).toBeTruthy();
    });

    it('should return false if statValue equals UNDER X.Y', () => {
      statValue = '<';
      expect(service['isOver'](statValue)).toBeFalsy();
    });
  });

  describe('getUnderTotalMarketsStatus', () => {
    it('should return total under market status(Winning status)', () => {
      expect(service['getUnderTotalMarketsStatus'](1, 2)).toEqual('Winning');
    });

    it('should return total under market status(Lose status) when strict conditions', () => {
      expect(service['getUnderTotalMarketsStatus'](5, 5,true)).toEqual('Lose');
    });

    it('should return total under market status(Winning status) when strict conditions', () => {
      expect(service['getUnderTotalMarketsStatus'](2, 5, true)).toEqual('Winning');
    });
  });

  describe('getUnderBookingStatus', () => {
    it('should return total under market status(Lose status)', () => {
      expect(service['getUnderBookingStatus'](40, 35)).toEqual('Lose');
    });

    it('should return total under market status(Winning status) when strict conditions', () => {
      expect(service['getUnderBookingStatus'](25, 35)).toEqual('Winning');
    });

    it('should return total under market status(Winnings status) when strict conditions', () => {
      expect(service['getUnderBookingStatus'](0, 25)).toEqual('Winning');
    });

    it('should return total under market status(Winnins status) when strict conditions', () => {
      expect(service['getUnderBookingStatus'](0, 0)).toEqual('Winning');
    });

  });

  describe('getUnderFirstHalfMarketsStatus', () => {
    it('should return 1st half under market status(Winning status)', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getUnderFirstHalfMarketsStatus'](1, 2, '1h')).toEqual('Winning');
    });

    it('should return 1st half under market status(Winning status)', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getUnderFirstHalfMarketsStatus'](2, 2, '1h')).toEqual('Winning');
    });

    it('should return 1st half under market status(Won status) when currentValue < target and there is second half', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      expect(service['getUnderFirstHalfMarketsStatus'](1, 2, '2h')).toEqual('Won');
    });

    it('should return 1st half under market status(Won status) when currentValue < target and there is second half', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      expect(service['getUnderFirstHalfMarketsStatus'](2, 2, '2h')).toEqual('Won');
    });

    it('should return 1st half under market status(Lose status)', () => {
      expect(service['getUnderFirstHalfMarketsStatus'](5, 2, '1h')).toEqual('Lose');
    });
  });

  describe('getOverTotalMarketsStatus', () => {
    it('should return TOTAL OVER market status(Losing status)', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getOverTotalMarketsStatus'](1, 2)).toEqual('Losing');
    });

    it('should return TOTAL OVER market status(Won status)', () => {
      expect(service['getOverTotalMarketsStatus'](6, 2)).toEqual('Won');
    });

    it('should return Losing status for OVER markets when strict conditions', () => {
      expect(service['getOverTotalMarketsStatus'](2, 2, true)).toEqual('Losing');
    });

    it('should return Won status for OVER markets when strict conditions', () => {
      expect(service['getOverTotalMarketsStatus'](3, 2, true)).toEqual('Won');
    });

    it('should return WON status for OVER markets when strict conditions', () => {
      expect(service['getOverTotalMarketsStatus'](3, 3, false)).toEqual('Won');
    });

    it('should return Lose status for OVER markets when strict conditions', () => {
      expect(service['getOverTotalMarketsStatus'](undefined, undefined)).toEqual('Lose');
    });
  });

  describe('getOverFirstHalfMarketsStatus', () => {
    it('should return 1st half over market status(Losing status)', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getOverFirstHalfMarketsStatus'](1, 2, '1h')).toEqual('Losing');
    });

    it('should return 1st half over market status(Won status)', () => {
      expect(service['getOverFirstHalfMarketsStatus'](5, 2, '2h')).toEqual('Won');
    });

    it('should return 1st half over market status(Losing status)', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      expect(service['getOverFirstHalfMarketsStatus'](1, 2, '2h')).toEqual('Lose');
    });
  });

  describe('isFirstHalf', () => {
    it('should check if it first half', () => {
      expect(service['isFirstHalf']('1h')).toBeTruthy();
    });
  });

  describe('isSecondHalfOrTotal', () => {
    it('should check if it second half', () => {
      expect(service['isSecondHalfOrTotal']('2h')).toBeTruthy();
    });

    it('should check if it total time', () => {
      expect(service['isSecondHalfOrTotal']('total')).toBeTruthy();
    });
  });

  describe('getNoRedCardsSelectionStatus', () => {
    it('should return Winning status', () => {
      expect(service['getNoRedCardsSelectionStatus'](statsDataMock)).toEqual('Winning');
    });

    it('should return Lose status if Home team has red card', () => {
      statsDataMock.cards = {
        home: [{type: 'red'}],
        away: []
      };
      expect(service['getNoRedCardsSelectionStatus'](statsDataMock)).toEqual('Lose');
    });

    it('should return Lose status if Away team has red card', () => {
      statsDataMock.cards = {
        home: [],
        away: [{type: 'red'}]
      };
      expect(service['getNoRedCardsSelectionStatus'](statsDataMock)).toEqual('Lose');
    });

    it('should return Lose status if both team have red cards', () => {
      statsDataMock.cards = {
        home: [{type: 'red'}],
        away: [{type: 'red'}]
      };
      expect(service['getNoRedCardsSelectionStatus'](statsDataMock)).toEqual('Lose');
    });
  });

  describe('isPeriodReached', () => {
    it('should return true if match time and period are equal', () => {
      expect(service['isPeriodReached']('15:00', '15:00')).toBeTruthy();
    });

    it('should return true if match time is greater than period', () => {
      expect(service['isPeriodReached']('16:00', '15:00')).toBeTruthy();
      expect(service['isPeriodReached']('15:01', '15:00')).toBeTruthy();
    });

    it('should return true if match time is lower than period', () => {
      expect(service['isPeriodReached']('14:59', '15:00')).toBeFalsy();
      expect(service['isPeriodReached']('14:58', '14:59')).toBeFalsy();
    });
  });

  describe('getDoubleChanceStatus', () => {
    let actualResult;

    it('should get status for Double Chance 1st HALF market(Winning status) when current period is 1h', () => {
      actualResult = service['getDoubleChanceStatus'](
        goalsObj,
        DOUBLE_TEAMS.HOME_OR_DRAW,
        '1h',
        '1h'
      );

      expect(actualResult).toEqual(STATUSES.WINNING);
    });

    it('should get status for Double Chance 1st HALF market(Losing status) when current period is 1h', () => {
      goalsObj.score['1h'] = {
        home: 2,
        away: 3
      };
      actualResult = service['getDoubleChanceStatus'](
        goalsObj,
        DOUBLE_TEAMS.HOME_OR_DRAW,
        '1h',
        '1h'
      );

      expect(actualResult).toEqual(STATUSES.LOSING);
    });

    it('should get status for Double Chance 2nd HALF market(Winning status)', () => {
      actualResult = service['getDoubleChanceStatus'](
        goalsObj,
        DOUBLE_TEAMS.AWAY_OR_DRAW,
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.WINNING);
    });

    it('should get status for Double Chance 2nd HALF market(Winning status) when current period is 1h', () => {
      goalsObj.score['2h'] = {
        home: 2,
        away: 3
      };

      actualResult = service['getDoubleChanceStatus'](
        goalsObj,
        DOUBLE_TEAMS.AWAY_OR_DRAW,
        '2h',
        '1h'
      );

      expect(actualResult).toEqual(STATUSES.WINNING);
    });

    it('should get status for Double Chance 2nd HALF market(Losing status) when no current period', () => {
      goalsObj.score['2h'] = {
        home: 2,
        away: 2
      };

      actualResult = service['getDoubleChanceStatus'](
        goalsObj,
        DOUBLE_TEAMS.HOME_OR_AWAY,
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.LOSING);
    });

    it('should get status for Double Chance 2nd HALF market(Winning status) when no current period', () => {
      goalsObj.score['2h'] = {
        home: 2,
        away: 1
      };

      actualResult = service['getDoubleChanceStatus'](
        goalsObj,
        DOUBLE_TEAMS.HOME_OR_AWAY,
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.WINNING);
    });

    it('should get status for Double Chance market(Losing status)', () => {
      actualResult = service['getDoubleChanceStatus'](
        goalsObj,
        DOUBLE_TEAMS.HOME_OR_AWAY,
        '3h'
      );

      expect(actualResult).toEqual(STATUSES.LOSING);
    });

    it('should get status for Double Chance market(LOSE status)', () => {
      actualResult = service['getDoubleChanceStatus'](
        goalsObj,
        DOUBLE_TEAMS.HOME_OR_AWAY,
        '3h'
      );

      expect(actualResult).toEqual(STATUSES.LOSING);
    });
  });

  describe('getRangeMarketStatus', () => {
    let goalsStat: any;

    beforeEach(() => {
      goalsStat = {
        [TEAMS.HOME]: [],
        [TEAMS.AWAY]: []
      };
    });

    describe('should return "Winning" in case', () => {
      it('match time is within period and conditions match for Home team', () => {
        goalsStat[TEAMS.HOME].push({
          scorer: 'Rebrov',
          time: '00:00',
          team: 'Home',
          player: { id: 'Rebrov' }
        });

        expect(service['getRangeMarketStatus'](goalsStat, false, TEAMS.HOME)).toEqual( STATUSES.WINNING);
      });

      it('match time is within period and conditions match for Away team', () => {
        goalsStat[TEAMS.AWAY].push({
          scorer: 'Gusev',
          time: '00:00',
          team: 'Away',
          player: { id: 'Gusev' }
        });

        expect(service['getRangeMarketStatus'](goalsStat, false, TEAMS.AWAY)).toEqual( STATUSES.WINNING);
      });

      it('match time is within period and conditions match for Draw', () => {
        expect(service['getRangeMarketStatus'](goalsStat, false, TEAMS.DRAW)).toEqual( STATUSES.WINNING);
      });
    });

    describe('should return "Won" in case', () => {
      it('match time is greater than period and conditions match', () => {
        expect(service['getRangeMarketStatus'](goalsStat, true, TEAMS.DRAW)).toEqual( STATUSES.WON);
      });
    });

    describe('should return "Losing" in case', () => {
      it('match time is within period and conditions do not match for Home team', () => {
        expect(service['getRangeMarketStatus'](goalsStat, false, TEAMS.HOME)).toEqual( STATUSES.LOSING);
      });

      it('match time is within period and conditions do not match for Away team', () => {
        expect(service['getRangeMarketStatus'](goalsStat, false, TEAMS.AWAY)).toEqual( STATUSES.LOSING);
      });

      it('bet not settled, match time is within period and conditions do not match for Draw', () => {
        goalsStat[TEAMS.HOME].push({
          scorer: 'Rebrov',
          time: '00:00',
          team: 'Home',
          player: { id: 'Rebrov' }
        });

        expect(service['getRangeMarketStatus'](goalsStat, false, TEAMS.DRAW)).toEqual( STATUSES.LOSING);
      });
    });

    describe('should return "Lose" in case', () => {
      beforeEach(() => {
        goalsStat[TEAMS.HOME].push({
          scorer: 'Rebrov',
          time: '00:00',
          team: 'Home',
          player: { id: 'Rebrov' }
        });
      });

      it('bet not settled, match time is greater than period and conditions do not match', () => {
        expect(service['getRangeMarketStatus'](goalsStat, true, TEAMS.DRAW)).toEqual( STATUSES.LOSE);
      });
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

    let bet: any;

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

      bet = { settled: '' };

      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([goal]);

      service['getRangeMarketStatus'] = jasmine.createSpy('getRangeMarketStatus').and.returnValue(STATUSES.LOSE);
    });

    describe('should process market for', () => {
      afterEach(() => {
        expect(service['getRangeMarketStatus']).toHaveBeenCalledWith(goalStats as any, false, TEAMS.DRAW);
      });
    });

    describe('should process market for', () => {
      afterEach(() => {
        expect(service['getRangeMarketStatus']).toHaveBeenCalledWith(goalStats as any, true, TEAMS.DRAW);
      });
    });
  });

  describe('getCorrectScoreStatus', () => {
    let actualResult;

    it('should get status for Correct Score 1st HALF market(Losing status) when current period is 1h', () => {
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 2, away: 3 },
        '1h',
        '1h'
      );

      expect(actualResult).toEqual(STATUSES.LOSING);
    });

    it('should get status for Correct Score 1st HALF market(Losing status) when current period is 1h', () => {
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 1, away: 2},
        '1h',
        '1h'
      );

      expect(actualResult).toEqual(STATUSES.LOSING);
    });

    it('should get status for Correct Score 2nd HALF market(Winning status)', () => {
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 1, away: 2 },
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.WINNING);
    });

    it('should get status for Correct Score 2nd HALF market(Winning status) when current period is 1h', () => {
      goalsObj.score['2h'] = {
        home: 2,
        away: 3
      };

      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 2, away: 3},
        '2h',
        '1h'
      );

      expect(actualResult).toEqual(STATUSES.WINNING);
    });

    it('should get status for Correct Score 2nd HALF market(Losing status) when no current period', () => {
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 1, away: 1 },
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.LOSE);
    });

    it('should get status for Correct Score 2nd HALF market(Winning status) when no current period', () => {
      goalsObj.score['2h'] = {
        home: 2,
        away: 2
      };
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 2, away: 2 },
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.WINNING);
    });

    it('should get status for Correct Score 2nd HALF market(WON status)', () => {
      goalsObj.score['2h'] = {
        home: 2,
        away: 3
      };
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 2, away: 3 },
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.WINNING);
    });

    it('should get status for Correct Score 2nd HALF market(LOSE status)', () => {
      goalsObj.score['2h'] = {
        home: 3,
        away: 3
      };
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 2, away: 3 },
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.LOSE);
    });

    it('should get status for Correct Score 2nd HALF market(LOSE status)', () => {
      goalsObj.score['2h'] = {
        home: 3,
        away: 3
      };
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 2, away: 3 },
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.LOSE);
    });

    it('should get status for Correct Score 2nd HALF market(LOSE status)', () => {
      goalsObj.score['2h'] = {
        home: 3,
        away: 3
      };
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 3, away: 2 },
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.LOSE);
    });

    it('should get status for Correct Score 2nd HALF market(LOSING status)', () => {
      goalsObj.score['2h'] = {
        home: 1,
        away: 2
      };
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 3, away: 2 },
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.LOSING);
    });

    it('should get status for Correct Score 2nd HALF market(LOSE status)', () => {
      goalsObj.score['2h'] = {
        home: 3,
        away: 3
      };
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 3, away: 2 },
        '2h'
      );

      expect(actualResult).toEqual(STATUSES.LOSE);
    });

    it('should get status for Correct Score(Losing status)', () => {
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 1, away: 2 },
        '3h'
      );

      expect(actualResult).toEqual(STATUSES.LOSING);
    });

    it('should get status for Correct Score(LOSE status)', () => {
      actualResult = service['getCorrectScoreStatus'](
        goalsObj,
        { home: 1, away: 2 },
        '3h'
      );

      expect(actualResult).toEqual(STATUSES.LOSING);
    });
  });

  describe('getEqualFirstHalfMarketsStatus', () => {
    beforeEach(() => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
    });

    it('should return 1ST HALF EXACT Markets status as Won when current period is second half', () => {
      expect(service['getEqualFirstHalfMarketsStatus'](1, 1, '2h')).toEqual('Won');
    });

    it('should return 1ST HALF EXACT Markets status as Winning when current period is first half', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getEqualFirstHalfMarketsStatus'](1, 1, '1h')).toEqual('Winning');
    });

    it('should return 1ST HALF EXACT Markets status as Losing when current period is first half', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getEqualFirstHalfMarketsStatus'](0, 1, '1h')).toEqual('Losing');
    });

    it('should return 1ST HALF EXACT Markets status as Lose when current period is first half', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('1h');
      expect(service['getEqualFirstHalfMarketsStatus'](5, 1, '1h')).toEqual('Lose');
    });

    it('should return 1ST HALF EXACT Markets status as Lose when current period is second half', () => {
      expect(service['getEqualFirstHalfMarketsStatus'](0, 1, '2h')).toEqual('Lose');
    });
  });

  describe('getEqualTotalMarketsStatus', () => {
    it('should return TOTAL/2nd HALF EXACT Markets status as Winning when bet is not settled', () => {
      expect(service['getEqualTotalMarketsStatus'](1, 1)).toEqual('Winning');
    });

    it('should return TOTAL/2nd HALF EXACT Markets status as Losing when bet is not settled', () => {
      expect(service['getEqualTotalMarketsStatus'](0, 1)).toEqual('Losing');
    });

    it('should return TOTAL/2nd HALF EXACT Markets status as Lose', () => {
      expect(service['getEqualTotalMarketsStatus'](5, 1)).toEqual('Lose');
    });
  });

  describe('isEqual', () => {
    it('should check if selection is EQUAL', () => {
      expect(service['isEqual']('=2')).toBeTruthy();
    });
  });

  describe('teamToGetFirstOrSecondGoalStatus', () => {
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
              name: 'ARSENAL',
              externalStatsLink: {
                contestantId: 'c8h9bw1l82s06h77xxrelzhur'
              }
            }
          ]
        }
      } as any;
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{ team: TEAMS.AWAY }]);
    });

    it('should process first goal and return "Winning" in case bet not settled and conditions match for AWAY Team', () => {
      statCategoryUtilityService.getHomeAwayTeamByName.and.returnValue(TEAMS.AWAY);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate,
        true
      );

      expect(actualResult).toEqual({ status: STATUSES.WON });
    });

    it('should process first goal and return "Losing" in case bet not settled and conditions match for AWAY Team', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{ team: TEAMS.HOME }]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate,
        true
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should process first goal and return "Losing" in case bet not settled and conditions match for HOME Team', () => {
      bybSelection.part.outcome[0].name = 'LIVERPOOL';
      bybSelection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{ team: TEAMS.AWAY }]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate,
        true
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should process first goal and return "Winning" in case bet not settled and conditions match for HOME Team', () => {
      bybSelection.part.outcome[0].name = 'LIVERPOOL';
      bybSelection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([{ team: TEAMS.HOME }]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate,
        true
      );

      expect(actualResult).toEqual({ status: STATUSES.WON });
    });

    it('should process first goal and return "Winning" in case bet not settled and conditions match for No Goals', () => {
      bybSelection.title = 'No Goal';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate,
        true
      );

      expect(actualResult).toEqual({ status: STATUSES.WINNING });
    });

    it('should process first goal and return "Losing" in case bet not settled and conditions match for No Goals', () => {
      bybSelection.title = 'No Goal';
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate,
        true
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should process Second goal and return "Winning" in case bet not settled and conditions match for AWAY Team', () => {
      bybSelection.title = '';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([
        { team: TEAMS.AWAY },
        { team: TEAMS.AWAY }
      ]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WON });
    });

    it('should process Second goal and return "Winning" in case bet not settled and conditions match for AWAY Team', () => {
      bybSelection.title = '';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([
        { team: TEAMS.HOME },
        { team: TEAMS.AWAY }
      ]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WON });
    });

    it('should process Second goal and return "Losing" in case bet not settled and conditions match for AWAY Team', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([
        { team: TEAMS.AWAY },
        { team: TEAMS.HOME }
      ]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should process Second goal and return "Losing" in case bet not settled and conditions match for AWAY Team', () => {
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSING });
    });

    it('should process Second goal and return "Losing" in case bet not settled and conditions match for HOME Team', () => {
      bybSelection.part.outcome[0].name = 'LIVERPOOL';
      bybSelection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([
        { team: TEAMS.HOME },
        { team: TEAMS.AWAY }
      ]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSE });
    });

    it('should process Second goal and return "Losing" in case bet not settled and conditions match for HOME Team', () => {
      bybSelection.part.outcome[0].name = 'LIVERPOOL';
      bybSelection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.LOSING });
    });

    it('should process Second goal and return "Winning" in case bet not settled and conditions match for HOME Team', () => {
      bybSelection.part.outcome[0].name = 'LIVERPOOL';
      bybSelection.part.outcome[0].externalStatsLink.contestantId = '4dsgumo7d4zupm2ugsvm4zm4d';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([
        { team: TEAMS.HOME },
        { team: TEAMS.HOME }
      ]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WON });
    });

    it('should process Second goal and return "Winning" in case bet not settled and conditions match for No Goals', () => {
      bybSelection.title = 'No Goal';
      statCategoryUtilityService.getAllGoals = jasmine.createSpy('getAllGoals').and.returnValue([]);
      actualResult = service['teamToGetFirstOrSecondGoalStatus'](
        bybSelection,
        statsDataMock as IScoreboardStatsUpdate
      );

      expect(actualResult).toEqual({ status: STATUSES.WINNING });
    });
  });

  describe('getNoStatsCategorySelectionStatus', () => {
    it('should return Winning for no Stats Category selection when bet is not settled', () => {
      expect(service['getNoStatsCategorySelectionStatus'](true)).toEqual('Winning');
    });

    it('should return Lose for no Stats Category selection when bet is settled', () => {
      expect(service['getNoStatsCategorySelectionStatus'](false)).toEqual('Lose');
    });

    it('should return Lose for no Stats Category selection when bet is not settled', () => {
      expect(service['getNoStatsCategorySelectionStatus'](false)).toEqual('Lose');
    });
  });

  describe('getFirstHalfCorrectScoreStatus', () => {
    let conditions = {
      forWining: true,
      forLosing: false
    };
    it('should get status for first half (Winning status)', () => {
      const actualResult = service['getFirstHalfCorrectScoreStatus'](
        conditions,
        '1h'
      );

      expect(actualResult).toEqual('Winning');
    });

    it('should get status for half time (Winning status)', () => {
      const actualResult = service['getFirstHalfCorrectScoreStatus'](
        conditions,
        'ht'
      );

      expect(actualResult).toEqual('Winning');
    });

    it('should get status for first half (Won status)', () => {
      const actualResult = service['getFirstHalfCorrectScoreStatus'](
        conditions,
        '1h'
      );

      expect(actualResult).toEqual('Winning');
    });

    it('should get status for second half (Won status)', () => {
      statCategoryUtilityService.getCurrentPeriod.and.returnValue('2h');
      const actualResult = service['getFirstHalfCorrectScoreStatus'](
        conditions,
        '2h'
      );

      expect(actualResult).toEqual('Won');
    });

    it('should get status for first half(Lose status)', () => {
      conditions = {
        forWining: false,
        forLosing: true
      };
      const actualResult = service['getFirstHalfCorrectScoreStatus'](
        conditions,
        '1h'
      );

      expect(actualResult).toEqual('Lose');
    });

    it('should get status for first half(Losing status)', () => {
      conditions = {
        forWining: false,
        forLosing: false
      };
      const actualResult = service['getFirstHalfCorrectScoreStatus'](
        conditions,
        '1h'
      );

      expect(actualResult).toEqual('Losing');
    });
  });

  describe('getTotalCorrectScoreStatus', () => {
    let conditions = {
      forWining: true,
      forLosing: false
    };

    it('should get status for first half (Winning status)', () => {
      const actualResult = service['getTotalCorrectScoreStatus'](
        conditions
      );

      expect(actualResult).toEqual('Winning');
    });

    it('should get status for first half(Losing status)', () => {
      conditions = {
        forWining: false,
        forLosing: false
      };
      const actualResult = service['getTotalCorrectScoreStatus'](
        conditions
      );

      expect(actualResult).toEqual('Losing');
    });

    it('should get status for first half betting markets(Lose status)', () => {
      conditions = {
        forWining: false,
        forLosing: true
      };
      const actualResult = service['getTotalCorrectScoreStatus'](
        conditions
      );

      expect(actualResult).toEqual('Lose');
    });
  });

  describe('#validateTeamsBothHalves', () => {
    it('should return false if false|false|false(case: 1)', () => {
      const updateMock = {
        period: '1h'
      } as any;
      const scored = {
        '1h': true,
        '2h': true
      } as any;
      const response = service['validateTeamsBothHalves'](updateMock, scored);
      expect(response).toBe(false);
    });
    it('should return false if true|false|false(case: 2)', () => {
      const updateMock = {
        period: '2h'
      } as any;
      const scored = {
        '1h': true,
        '2h': true
      } as any;
      const response = service['validateTeamsBothHalves'](updateMock, scored);
      expect(response).toBe(false);
    });
    it('should return true if true|true|false(case: 3)', () => {
      const updateMock = {
        period: '2h'
      } as any;
      const scored = {
        '1h': false,
        '2h': true
      } as any;
      const response = service['validateTeamsBothHalves'](updateMock, scored);
      expect(response).toBe(true);
    });
    it('should return true if false|false|true(case: 4)', () => {
      const updateMock = {
        period: '1h'
      } as any;
      const scored = {
        '1h': true,
        '2h': false
      } as any;
      const response = service['validateTeamsBothHalves'](updateMock, scored);
      expect(response).toBe(false);
    });
  });
});

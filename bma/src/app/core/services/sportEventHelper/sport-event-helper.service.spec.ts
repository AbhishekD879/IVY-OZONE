import { SportEventHelperService } from './sport-event-helper.service';

describe('SportEventHelperService', () => {
  let service: SportEventHelperService;
  let locale;
  let coreTools;
  let filterService;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy()
    };
    coreTools = {
      hasOwnDeepProperty: jasmine.createSpy()
    };
    filterService = {
      getTeamName: jasmine.createSpy(),
      numberSuffix: jasmine.createSpy()
    };

    service = new SportEventHelperService(locale, coreTools, filterService);
  });

  describe('#isOutrightEvent', () => {
    it('isOutrightEvent: false', () => {
      expect(service.isOutrightEvent({ eventSortCode: 'TEST' } as any)).toEqual(false);
    });
    it('isOutrightEvent: true', () => {
      expect(service.isOutrightEvent({ eventSortCode: 'TNMT' } as any)).toEqual(true);
    });
    it('isOutrightEvent: true', () => {
      expect(service.isOutrightEvent({ eventSortCode: 'TR01' } as any)).toEqual(true);
    });
    it('isOutrightEvent: false for golf event', () => {
      expect(service.isOutrightEvent({ eventSortCode: 'MTCH', categoryCode: 'GOLF' } as any)).toBeFalsy();
    });
    it('isOutrightEvent: false for football event', () => {
      expect(service.isOutrightEvent({ eventSortCode: 'MTCH', categoryCode: 'FOOTBALL' } as any)).toBeFalsy();
    });
    it('should log error', () => {
      spyOn(console, 'warn');

      service.isOutrightEvent({ categoryCode: 'FOOTBALL' } as any);

      expect(console.warn).toHaveBeenCalled();
    });
  });

  describe('#isClockAllowed', () => {
    it('isClockAllowed: false', () => {
      expect(service.isClockAllowed({} as any)).toEqual(false);
    });
    it('isClockAllowed: true', () => {
      expect(service.isClockAllowed({ clock: true } as any)).toEqual(true);
    });
  });

  describe('#isHalfTime', () => {
    it('isHalfTime: false', () => {
      expect(service.isHalfTime({ clock: { matchTime: 'FT' } } as any)).toEqual(false);
    });
    it('isHalfTime: true', () => {
      expect(service.isHalfTime({ clock: { matchTime: 'HT' } } as any)).toEqual(true);
    });
  });

  describe('#isPenalties', () => {
    it('isPenalties: false', () => {
      expect(service.isPenalties({ clock: { matchTime: 'FT' } } as any)).toEqual(false);
    });
    it('isPenalties: true', () => {
      expect(service.isPenalties({ clock: { matchTime: 'PENS' } } as any)).toEqual(true);
    });
  });

  describe('#isFullTime', () => {
    it('isFullTime: false', () => {
      expect(service.isFullTime({ clock: { matchTime: 'HT' } } as any)).toEqual(false);
    });
    it('isFullTime: true', () => {
      expect(service.isFullTime({ clock: { matchTime: 'FT' } } as any)).toEqual(true);
    });
  });

  describe('#isCashOutEnabled', () => {
    it('isCashOutEnabled: true', () => {
      expect(service.isCashOutEnabled({ cashoutAvail: 'Y', markets: []} as any)).toEqual(true);
    });
    it('isCashOutEnabled: false', () => {
      expect(service.isCashOutEnabled({ cashoutAvail: 'N', markets: []} as any)).toEqual(false);
    });
    it('isCashOutEnabled: false', () => {
      expect(service.isCashOutEnabled({ markets: [{}] } as any)).toEqual(false);
    });
    it('isCashOutEnabled: false', () => {
      expect(service.isCashOutEnabled({ markets: [{ cashoutAvail: 'N' }] } as any)).toEqual(false);
    });
    it('isCashOutEnabled: true', () => {
      expect(service.isCashOutEnabled({ markets: [{ cashoutAvail: 'Y' }] } as any)).toEqual(true);
    });
  });

  describe('#isEventSecondNameAvailable', () => {
    it('isEventSecondNameAvailable: false', () => {
      expect(service.isEventSecondNameAvailable({
        nameOverride: 'Liverpool'
      } as any)).toBe(false);
    });
    it('isEventSecondNameAvailable: false', () => {
      expect(service.isEventSecondNameAvailable({
        name: 'Liverpool'
      } as any)).toBe(false);
    });
    it('isEventSecondNameAvailable: true', () => {
      filterService.getTeamName.and.returnValue('Man City');
      expect(service.isEventSecondNameAvailable({
        name: 'Liverpool vs Man Ciry'
      } as any)).toBe(true);
    });
  });

  describe('#getEventNames', () => {
    it('getEventNames: no names', () => {
      expect(service.getEventNames({} as any)).toEqual({
        eventFirstName: null,
        eventSecondName: null
      });
    });

    it('getEventNames: no names', () => {
      filterService.getTeamName.and.returnValue('Man City');
      expect(service.getEventNames({
        nameOverride: 'Liverpool vs Man City'
      } as any)).toEqual({
        eventFirstName: 'Man City',
        eventSecondName: 'Man City'
      });
    });
    it('getEventNames: no names', () => {
      filterService.getTeamName.and.returnValue('Man City');
      expect(service.getEventNames({
        name: 'Liverpool vs Man City'
      } as any)).toEqual({
        eventFirstName: 'Man City',
        eventSecondName: 'Man City'
      });
    });
  });

  describe('#isTennis', () => {
    it('isTennis: false', () => {
      expect(service.isTennis({
        categoryName: 'Football'
      } as any)).toEqual(false);
    });

    it('isTennis: true', () => {
      expect(service.isTennis({
        categoryName: 'Tennis'
      } as any)).toEqual(true);
    });
  });

  describe('#isFootball', () => {
    it('isFootball: true', () => {
      expect(service.isFootball({
        categoryName: 'Football'
      } as any)).toEqual(true);
    });

    it('isFootball: false', () => {
      expect(service.isTennis({
        categoryName: 'false'
      } as any)).toEqual(false);
    });
  });

  it('isEventHasCurrentPoints', () => {
    service.isEventHasCurrentPoints('test' as any);
    expect(coreTools.hasOwnDeepProperty).toHaveBeenCalledTimes(1);
    expect(coreTools.hasOwnDeepProperty).toHaveBeenCalledWith('test', 'comments.teams.home.currentPoints');
  });

  it('isEventHasOddsScores', () => {
    service.isEventHasOddsScores('test' as any);
    expect(coreTools.hasOwnDeepProperty).toHaveBeenCalledTimes(1);
    expect(coreTools.hasOwnDeepProperty).toHaveBeenCalledWith('test', 'comments.teams.home');
  });

  describe('#isCashoutAvailable', () => {
    it('isCashoutAvailable: false', () => {
      expect(service.isCashOutEnabled({} as any)).toEqual(false);
    });
    it('isCashoutAvailable: false', () => {
      expect(service.isCashOutEnabled({ markets: [{}] } as any)).toEqual(false);
    });
    it('isCashoutAvailable: false', () => {
      expect(service.isCashOutEnabled({ markets: [{ cashoutAvail: 'N' }] } as any)).toEqual(false);
    });
    it('isCashoutAvailable: true', () => {
      expect(service.isCashOutEnabled({ markets: [{ cashoutAvail: 'Y' }] } as any)).toEqual(true);
    });
  });

  describe('#isLive', () => {
    it('isLive: false', () => {
      expect(service.isLive({} as any)).toEqual(undefined);
    });

    it('isLive: false', () => {
      expect(service.isLive({
        isStarted: false
      } as any)).toEqual(undefined);
    });

    it('isLive: false', () => {
      expect(service.isLive({
        eventIsLive: false
      } as any)).toEqual(false);
    });

    it('isLive: true', () => {
      expect(service.isLive({
        eventIsLive: true
      } as any)).toEqual(true);
    });

    it('isLive: true', () => {
      expect(service.isLive({
        isStarted: true
      } as any)).toEqual(true);
    });
  });

  describe('#isHomeDrawAwayType', () => {
    const event = {
      oddsCardHeaderType: 'homeDrawAwayType'
    } as any,
    sportConfig = {
      config: {
        oddsCardHeaderType: 'type'
      }
    } as any;
    it('check is HomeDrawAwayType and return true', () => {
      expect(service.isHomeDrawAwayType(event, sportConfig)).toEqual(true);
    });
    it('check is HomeDrawAwayType and return false', () => {
      const event1 = {} as any;
      expect(service.isHomeDrawAwayType(event1, sportConfig)).toEqual(false);
    });
    it('check is HomeDrawAwayType and return true', () => {
      const event2 = {} as any,
        sportConfig2 = {
        config: {
          oddsCardHeaderType: 'homeDrawAwayType'
        }
      } as any;
      expect(service.isHomeDrawAwayType(event2, sportConfig2)).toEqual(true);
    });
    it('check is HomeDrawAwayType and return true', () => {
      const event3 = {} as any,
        sportConfig3 = {
          config: {
            oddsCardHeaderType: {
              outcomesTemplateType1: 'homeDrawAwayType'
            }
          }
        } as any;
      expect(service.isHomeDrawAwayType(event3, sportConfig3)).toEqual(true);
    });
    it('check is HomeDrawAwayType and return true', () => {
      const event3 = {
          oddsCardHeaderType: 'oneThreeType'
        } as any;
      expect(service.isHomeDrawAwayType(event3, sportConfig)).toEqual(true);
    });
  });

  describe('#isOutrightSport', () => {
    it('should check if event belongs to specific sports which has sortCode "MTCH" as outright', () => {
      expect(service['isOutrightSport']('CYCLING')).toBeTruthy();
    });
  });

  describe('isSpecialEvent', () => {

    it('should detect special based on event flags (flag is the first one)', () => {
      expect(service.isSpecialEvent({drilldownTagNames: 'EVFLAG_SP,FOO_FLAG', markets: [{}]} as any, false)).toBe(true);
    });

    it('should detect special based on event flags (flag is not the first one)', () => {
      expect(service.isSpecialEvent({drilldownTagNames: 'FOO_FLAG,EVFLAG_SP', markets: [{}]} as any, false)).toBe(true);
    });

    it('should detect special based on market flags', () => {
      expect(service.isSpecialEvent(
        {
          drilldownTagNames: 'FOO_FLAG',
          markets: [{
            drilldownTagNames: 'MKTFLAG_SP'
          }]
        } as any,
        true)
      ).toBe(true);
    });

    it('should not detect special based on event flags only', () => {
      expect(service.isSpecialEvent({drilldownTagNames: 'FOO_FLAG,FOO_FLAG2', markets: [{}]} as any, false)).toBe(false);
    });

    it('should set event as not special if markets are not available ', () => {
      expect(service.isSpecialEvent({drilldownTagNames: 'EVFLAG_SP', markets: []} as any, false)).toBe(false);
    });

    it('should handle empty drilldownTagNames property', () => {
      expect(service.isSpecialEvent({markets: [{}]} as any, false)).toBeFalsy();
    });
  });

  describe('getOddsScore', () => {
    it('getOddsScore isPenalty = false', () => {
      const event = <any>{
        isUS: false,
        comments: {
          teams: {
            home: {
              score: 2
            },
            away: {
              score: 1
            }
          }
        }
      };
      expect(service.getOddsScore(event, 'teamA', false)).toBe(2);
      expect(service.getOddsScore(event, 'teamB', false)).toBe(1);
    });

    it('getOddsScore isPenalty = true', () => {
      const event = <any>{
        isUS: false,
        comments: {
          teams: {
            home: {
              penaltyScore: 2
            },
            away: {
              penaltyScore: 1
            }
          }
        }
      };
      expect(service.getOddsScore(event, 'teamA', true)).toBe(2);
      expect(service.getOddsScore(event, 'teamB', true)).toBe(1);
    });

    it('getOddsScore isUS = true', () => {
      const event = <any>{
        isUS: true,
        comments: {
          teams: {
            home: {
              score: 1
            },
            away: {
              score: 2
            }
          }
        }
      };
      expect(service.getOddsScore(event, 'teamA')).toBe(2);
    });
  });

  it('getEventCurrentPoints', () => {
    const event = <any>{
      isUS: true,
      comments: {
        teams: {
          home: {
            currentPoints: 1
          },
          away: {
            currentPoints: 2
          }
        }
      }
    };

    expect(service.getEventCurrentPoints(event, 'teamA')).toBe(1);
  });

  describe('getTennisSetScores', () => {
    it('getTennisSetScores', () => {
      const event = <any>{
        isUS: true,
        comments: {
          setsScores: {}
        }
      };

      coreTools.hasOwnDeepProperty.and.returnValue(false);
      expect(service.getTennisSetScores(event)).toEqual([]);
    });

    it('getTennisSetScores setsScores', () => {
      const event = <any>{
        isUS: true,
        comments: {
          setsScores: {
            a: 1
          }
        }
      };

      coreTools.hasOwnDeepProperty.and.returnValue(true);
      expect(service.getTennisSetScores(event).length).toEqual(1);
    });
  });

  it('getTennisScoreForPlayer', () => {
    const event = <any>{
      isUS: true,
      comments: {
        teams: {
          player_1: {
            id: 5
          }
        }
      }
    };

    expect(service.getTennisScoreForPlayer(event, 'playerA')).toEqual(5);
  });

  it('isStreamAvailable', () => {
    expect(service.isStreamAvailable(<any>{ liveStreamAvailable: true })).toEqual(false);
  });

  it('showMarketsCount', () => {
    expect(service.showMarketsCount(<any>{ marketsCount: 2 })).toEqual(true);
  });

  describe('getTennisSetScores', () => {
    it('getTennisSetIndex', () => {
      expect(service.getTennisSetIndex(<any>{})).toEqual('');
    });

    it('getTennisSetIndex runningSetIndex', () => {
      const event = <any>{
        comments: {
          runningSetIndex: 5
        }
      };
      coreTools.hasOwnDeepProperty.and.returnValue(true);
      locale.getString.and.returnValue('test');

      expect(service.getTennisSetIndex(event)).toEqual('5test test');
    });
  });

  describe('getMarketsCount', () => {
    it('getMarketsCount marketsCount', () => {
      expect(service.getMarketsCount(<any>{ marketsCount: 2 })).toEqual(1);
    });

    it('getMarketsCount', () => {
      expect(service.getMarketsCount(<any>{} )).toEqual(0);
    });
  });

  it('isEachWayTermsAvailable', () => {
    expect(service.isEachWayTermsAvailable(<any>{eachWayPlaces: true, eachWayFactorDen: '1', eachWayFactorNum: '1'} )).toEqual(true);
  });

  describe('isCashoutAvailable', () => {
    it('isCashoutAvailable Y', () => {
      expect(service.isCashoutAvailable(<any>{cashoutAvail: 'Y'} )).toEqual(true);
    });

    it('isCashoutAvailable N', () => {
      expect(service.isCashoutAvailable(<any>{cashoutAvail: 'N'} )).toEqual(false);
    });
  });

  describe('showStreamIcon', () => {
    it('showStreamIcon', () => {
      expect(service['showStreamIcon'](<any>{ drilldownTagNames: 'a,b,c' })).toEqual(false);
    });

    it('showStreamIcon true', () => {
      expect(service['showStreamIcon'](<any>{ drilldownTagNames: 'EVFLAG_AVA,b,c' })).toEqual(true);
    });
  });
});

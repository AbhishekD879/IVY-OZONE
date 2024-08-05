import { OddsCardHeaderService } from './odds-card-header.service';
import { ISportEvent } from '@core/models/sport-event.model';
import * as _ from 'underscore';
describe('OddsCardHeaderService', () => {
  let service: OddsCardHeaderService;

  let locale, coreTools, marketTypeService: any;

  beforeEach(() => {
    locale = {
      getString: (key: string) => {
        return key !== 'sb.' ? key : 'KEY_NOT_FOUND';
      }
    };
    coreTools = {
      hasOwnDeepProperty: jasmine.createSpy('hasOwnDeepProperty'),
    };
    marketTypeService = {
      getDisplayMarketConfig: jasmine.createSpy('getDisplayMarketConfig').and.returnValue({}),
      extractMarketNameFromEvents: (events: ISportEvent[], isFilterByTemplateMarketName?: boolean): string[] => {
        const marketNames = _.reduce(events, (accumulator, event) => {
          const eventMarketNames = (event.markets || []).map(market => {
            if (isFilterByTemplateMarketName) {
              if (market.templateMarketName === 'Match Betting') {
                market.templateMarketName = 'Match Result';
              }
              return market.templateMarketName;
            }
    
            return market.name;
          });
    
          accumulator.push(...eventMarketNames);
    
          return accumulator;
        }, []);
        return marketNames;
      }
    };
    service = new OddsCardHeaderService(
      locale,
      coreTools,
      marketTypeService
    );
  });

  it('isSpecialSection', () => {
    const res: boolean = service.isSpecialSection(<any>[
      {
        categoryCode: 'Football',
        categoryName: 'football',
        typeId: '8',
        eventSortCode: 'TNMT'
      }
    ], <any>{
      football: [{
        specialsTypeIds: ['8']
      }],
      config: {
        request: {
          marketTemplateMarketNameIntersects: ''
        }
      }
    });

    expect(res).toBeTruthy();
  });

  it('isSpecialSection: outright', () => {
    const res: boolean = service.isSpecialSection(<any>[
      {
        categoryCode: 'golf',
        categoryName: 'football',
        typeId: '8',
        eventSortCode: 'TNMT'
      }
    ], <any>{
      football: [{
        specialsTypeIds: ['7']
      }],
      config: {
        request: {
          marketTemplateMarketNameIntersects: ''
        }
      }
    });

    expect(res).toBeTruthy();
  });

  it('isHomeDrawAwayMarketType: true', () => {
    expect(service.isHomeDrawAwayMarketType('Match Betting')).toBeTruthy();
  });

  it('isHomeDrawAwayMarketType: false', () => {
    expect(service.isHomeDrawAwayMarketType('Unkown')).toBeFalsy();
  });

  it('isRacing: true', () => {
    expect(service.isRacing('21')).toBeTruthy();
  });

  it('isRacing: false', () => {
    expect(service.isRacing('16')).toBeFalsy();
  });

  it('getLocale', () => {
    spyOn(locale, 'getString');
    service.getLocale('locale,locale');
    expect(locale.getString).toHaveBeenCalledTimes(2);
    expect(locale.getString).toHaveBeenCalledWith('sb.locale');
  });

  it('getLocale', () => {
    expect(service.getLocale('')).toEqual('');
  });

  it('showComponent', () => {
    const res: boolean = service.showComponent(<any>[
      'selectedMarket'
    ], 'selectedMarket');
    expect(res).toBeTruthy();
  });

  it('showComponent', () => {
    const res: boolean = service.showComponent(<any>[{
      markets: []
    }], 'selectedMarket');

    expect(res).toBeFalsy();
  });
  it('showComponent with 0 length', () => {
    const res: boolean = service.showComponent([], 'selectedMarket');
    expect(res).toBeFalsy();
  });
  it('showComponent with no selected market', () => {
    const res: boolean = service.showComponent(['match Betting'], '');
    expect(res).toBeTrue();
  });
  it('showComponent with market and selected market', () => {
    const res: boolean = service.showComponent(['match Betting','Total Points'], 'match Betting');
    expect(res).toBeTrue();
  });
  it('getSportName', () => {
    const res = service.getSportName({categoryName: 'categoryName'} as any);
    expect(res).toEqual('categoryname');
  });

  describe('@getHeaderByMarketName', () => {
    it('it should set homeAwayType header', () => {
      const market = {
        templateMarketName: 'To Win to Nil'
      } as any;
      const result = service.getHeaderByMarketName(true, market);
      expect(result).toEqual('homeAwayType');
    });

    it('it should set homeDrawAwayType header', () => {
      const market = {
        templateMarketName: 'Match Betting'
      } as any;
      const result = service.getHeaderByMarketName(true, market);
      expect(result).toEqual('homeDrawAwayType');
    });

    it('it should set yesNoType header', () => {
      const market = {
        templateMarketName: 'Score Goal in Both Halves'
      } as any;
      const result = service.getHeaderByMarketName(true, market);
      expect(result).toEqual('yesNoType');
    });

    it('it should not set header', () => {
      const market = {
        templateMarketName: 'Score Goal in Both Halves'
      } as any;
      const result = service.getHeaderByMarketName(true, market);
      expect(result).toEqual('yesNoType');
    });
  });

  describe('isEventsHaveScores', () => {
    beforeEach(() => {
      coreTools.hasOwnDeepProperty = jasmine.createSpy('hasOwnDeepProperty').and.callFake((obj, path) => {
        if (path === 'comments.teams.home.score' && obj.comments.teams.home.score) {
          return true;
        }
      });
    });

    it('should return true if event comments has player_1', () => {
      coreTools.hasOwnDeepProperty = jasmine.createSpy('hasOwnDeepProperty').and.callFake((obj, path) => {
        if (path === 'comments.teams.player_1' && obj.comments.teams.player_1) {
          return true;
        }
      });
      const event = {
        comments: {
          teams: {
            player_1: { }
          }
        }
      };
      expect(service.isEventsHaveScores([event] as any)).toBeTruthy();
    });

    it('should return true if event comments have scores', () => {
      const event = {
        comments: {
          teams: {
            home: {
              score: '0'
            }
          }
        }
      };
      expect(service.isEventsHaveScores([event] as any)).toBeTruthy();
    });

    it('should not return true if event comments have no scores', () => {
      const event = {
        comments: {
          teams: {
            home: {}
          }
        }
      };
      expect(service.isEventsHaveScores([event] as any)).toBeFalsy();
    });
  });

  describe('sortEventsByScores', () => {
    let eventA, eventB, events;

    beforeEach(() => {
      coreTools.hasOwnDeepProperty = jasmine.createSpy('hasOwnDeepProperty').and.callFake((obj, path) => {
        if (path === 'comments.teams.home.score' && obj.comments.home.score) {
          return true;
        }
      });
      eventA = { comments: { home: { } } };
      eventB = { comments: { home: { } } };
      events = [eventA, eventB];
    });

    describe('should correctly sort events when', () => {
      it('both events have no scores', () => {
        service.sortEventsByScores(events);
        expect(events).toEqual([eventA, eventB]);
      });

      it('A has scores and B has no scores', () => {
        eventA.comments.home.score = '0';
        service.sortEventsByScores(events);
        expect(events).toEqual([eventA, eventB]);
      });

      it('A has no scores and B has scores', () => {
        eventB.comments.home.score = '0';
        service.sortEventsByScores(events);
        expect(events).toEqual([eventB, eventA]);
      });

      it('both events have scores', () => {
        eventA.comments.home.score = '0';
        eventB.comments.home.score = '0';
        service.sortEventsByScores(events);
        expect(events).toEqual([eventA, eventB]);
      });
    });
  });

  describe('isSpecialEvent', () => {
    it('should return false (no sport config)', () => {
      expect(service.isSpecialEvent({} as any, null)).toBeFalsy();
    });

    it('should return true (outright sport)', () => {
      const event: any = { categoryCode: 'MOTOR_CARS', eventSortCode: 'TNMT'  };
      const sportConfig: any = {
      config: {
        request: {
          marketTemplateMarketNameIntersects: ''
        }
      }};
      expect(service.isSpecialEvent(event, sportConfig)).toBeTruthy();
    });

    it('should return true (enhance multiples)', () => {
      const event: any = { typeId: 1, categoryCode: 'MOTOR_CARS' };
      const sportConfig: any = { specialsTypeIds: [1],
      config: {
        request: {
          marketTemplateMarketNameIntersects: ''
        }
      } };
      expect(service.isSpecialEvent(event, sportConfig)).toBeTruthy();
    });

    it('should return false (not special event)', () => {
      const event: any = { typeId: 1, categoryCode: 'MOTOR_CARS' };
      const sportConfig: any = { specialsTypeIds: [2],
      config: {
        request: {
          marketTemplateMarketNameIntersects: ''
        }
      } };
      expect(service.isSpecialEvent(event, sportConfig)).toBeFalsy();
    });
    it('should return false (not special event)', () => {
      const event: any = { typeId: 1, categoryId: '16', categoryCode: 'golf' };
      const sportConfig: any = {
        specialsTypeIds: [2],
        config: {
          request: {
            marketTemplateMarketNameIntersects: ''
          }
        }
      };
      expect(service.isSpecialEvent(event, sportConfig)).toBeFalsy();
    });
    it('should return true (special outright golf event)', () => {
      const event: any = { typeId: 1, categoryId: '16', categoryCode: 'golf', typeName: '#Yourcall' };
      const sportConfig: any = {
        specialsTypeIds: [2],
        config: {
          request: {
            marketTemplateMarketNameIntersects: ''
          }
        }
      };
      expect(service.isSpecialEvent(event, sportConfig)).toBeFalsy();
    });
    it('should return true (special drilldownTagNames code)', () => {
      const event: any = { typeId: 1, categoryId: '16', categoryCode: 'golf', typeName: '#Yourcall' , drilldownTagNames: 'EVFLAG_SP' };
      const sportConfig: any = {
        specialsTypeIds: [2],
        config: {
          request: {
            marketTemplateMarketNameIntersects: ''
          }
        }
      };
      expect(service.isSpecialEvent(event, sportConfig)).toBeFalsy();
    });
    it('should return true (special market and not drilldownTagNames code)', () => {
      const event: any = { typeId: 1, categoryId: '16', categoryCode: 'golf', typeName: '#Yourcall' , drilldownTagNames: '1234' };
      const sportConfig: any = {
        specialsTypeIds: [2],
        config: {
          request: {
            marketTemplateMarketNameIntersects: ''
          }
        }
      };
      expect(service.isSpecialEvent(event, sportConfig)).toBeFalsy();
    });
    it('should return true (not special market but drilldownTagNames code)', () => {
      const event: any = { typeId: 1, categoryId: '16', categoryCode: 'golf', typeName: '#abcd' , drilldownTagNames: 'EVFLAG_SP' };
      const sportConfig: any = {
        specialsTypeIds: [2],
        config: {
          request: {
            marketTemplateMarketNameIntersects: ''
          }
        }
      };
      expect(service.isSpecialEvent(event, sportConfig)).toBeFalsy();
    });
  });

  describe('#isOutrightSport', () => {
    let sportConfig;

    beforeEach(() => {
      sportConfig = { config: { isOutrightSport: false } };
    });

    it('should return true when categoryCode available in outrightsSports', () => {
      const result = service['isOutrightSport']('GOLF', sportConfig);
      expect(result).toEqual(false);
    });

    it('should return false when categoryCode not available in outrightsSports', () => {
      const result = service['isOutrightSport']('GOLF1', sportConfig);
      expect(result).toEqual(false);
    });

    it('should return true when isOutrightSport is true', () => {
      sportConfig.config.isOutrightSport = true;
      const result = service['isOutrightSport']('GOLF1', sportConfig);
      expect(result).toEqual(true);
    });

    it('should return false when isOutrightSport = false', () => {
      const result = service['isOutrightSport']('GOLF1', sportConfig);
      expect(result).toEqual(false);
    });
  });

  describe('#getHeaderByViewType', () => {

    it('should return oneThreeType', () => {
      const result = service['getHeaderByViewType']('Scorer', 1, 'golf');
      expect(result).toEqual('oneThreeType');
    });
    it('should return homeDrawAwayType', () => {
      const result = service['getHeaderByViewType']('WDW', 1, 'not');
      expect(result).toEqual('homeDrawAwayType');
    });
    it('should return homeDrawAwayType when length is 3', () => {
      const result = service['getHeaderByViewType']('WW', 3, 'not');
      expect(result).toEqual('homeDrawAwayType');
    });
  });
  describe('#getMarketByTemplateMarketName', () => {
    it('getMarketByTemplateMarketName with isFilterByTemplateMarketName true', () => {
      let markets = [{ name: 'Match Result', templateMarketName: 'Match Betting' }] as any;
      let market = service['getMarketByTemplateMarketName'](markets, 'Match Result', true);
      expect(market).toEqual(markets[0]);
      markets = [{ name: 'Match Result', templateMarketName: 'Match Betting' }] as any;
      market = service['getMarketByTemplateMarketName'](markets, 'Match Betting', true);
      expect(market).toEqual(markets[0]);
    });
    it('getMarketByTemplateMarketName with isFilterByTemplateMarketName false', () => {
      const markets = [{ name: 'Match Result', templateMarketName: 'Match Result' }] as any;
      const market = service['getMarketByTemplateMarketName'](markets, 'Match Result', false);
      expect(market).toEqual(markets[0]);
    });
  });
  it('should call getMultiTemplateHeader', () => {
    expect(service.getMultiTemplateHeader('60 Minute Betting')).toEqual('60 Min');
    expect(service.getMultiTemplateHeader('Match Betting')).toEqual('sb.matchbetting');
    expect(service.getMultiTemplateHeader('')).toEqual('');
  });
});

import { TemplateService } from '@shared/services/template/template.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IQuickbetReceiptLegPartsModel } from '@app/quickbet/models/quickbet-receipt.model';
import { IMarket } from '@app/core/models/market.model';
import { IBetDetailLegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { fakeAsync, flush, tick } from '@angular/core/testing';
import { of } from 'rxjs';
import { IOutcome } from '@core/models/outcome.model';

describe('#TemplateService', () => {
  let templateService, filter, timeService, locale, cmsProvider, windowRef;

  const testStr = 'TestString';
  let outcomes = [];

  beforeEach(() => {
    filter = {
      date: jasmine.createSpy('filter.date').and.callFake((date, format) => format)
    };
    timeService = {
      determineDay: jasmine.createSpy()
    };
    locale = {
      getString: jasmine.createSpy('getString').and.callFake(s => s)
    };
    cmsProvider = {
      getMenuItems: jasmine.createSpy('getMenuItems').and.returnValue(of([]))
    };
    windowRef = {
      nativeWindow: {
        location: {
         href:  'football'
        }
      }
    };
    templateService = new TemplateService(
      filter,
      timeService,
      locale,
      cmsProvider,
      windowRef
    );
    
  });

  it('should be created', () => {
    expect(templateService).toBeTruthy();
  });

  it('should call isListTemplate', () => {
    expect(templateService.isListTemplate('Round Betting')).toBeTruthy();
  });

  it('should call isListTemplate when selected market undefined', () => {
    expect(templateService.isListTemplate('')).toBeFalse();
  });

  describe('#genTerms', () => {
    it('should generate terms', () => {
      const result = templateService.genTerms({ name: 'market' });
      expect(result).toEqual('sb.oddsAPlaces');
      expect(locale.getString).toHaveBeenCalled();
    });

    it('should generate new terms', () => {
      locale.getString.and.returnValue('new odds string');
      const result = templateService.genTerms({ name: 'market' }, 'sb.newOddsAPlaces');

      expect(result).toEqual('new odds string');
      expect(locale.getString).toHaveBeenCalled();
    });
  });

  describe('setCorrectPriceType(): ', () => {
    let eventsArray;

    beforeEach(() => {
      eventsArray = [
        {
          id: 'id1',
          markets: [{ id: 'id1' }],
          startTime: '12'
        },
        {
          id: 'id2',
          markets: [{ id: 'id2' }],
          startTime: '2'
        },
        {
          id: 'id3',
        },
        {
          id: 'id4',
          markets: [{ isSpAvailable: true, outcomes: [{}] }]
        },
        {
          id: 'id5',
          markets: [{ isSpAvailable: true, isLpAvailable: true, outcomes: [{ prices: [{}] }] }]
        }
      ];

      spyOn(templateService, 'genTerms');
    });

    it('should call this.genTerms()', () => {
      templateService.setCorrectPriceType(eventsArray, false, false);

      expect(templateService.genTerms).toHaveBeenCalled();
    });

    it('should call this.genTerms() with new OddsAPlaces', () => {
      templateService.setCorrectPriceType(eventsArray, false, true);

      expect(templateService.genTerms).toHaveBeenCalledWith(eventsArray[0].markets[0], 'sb.newOddsAPlaces');
    });

    it('should sort current array', () => {
      templateService.setCorrectPriceType(eventsArray, false);

      expect(eventsArray[0].id).toBe('id2');
    });
  });

  describe('groupEventsByTypeName', () => {
    const sportEventsStub = [
      { typeName: '1', country: testStr },
      { typeName: '1', country: testStr },
      { typeName: '2', country: testStr }
    ] as ISportEvent[];

    it('should group Events By Type Name', () => {
      expect(templateService.groupEventsByTypeName(sportEventsStub))
        .toEqual({ '1': [sportEventsStub[0], sportEventsStub[1]], '2': [sportEventsStub[2]] });
    });

    it('should group Events By Type Name with adding contry to group name if isTote', () => {
      expect(templateService.groupEventsByTypeName(sportEventsStub, true))
        .toEqual({ [`1 ${testStr}`]: [sportEventsStub[0], sportEventsStub[1]], [`2 ${testStr}`]: [sportEventsStub[2]] });
    });
  });

  it('isOutrightSport', () => {
    expect(templateService.isOutrightSport('MOTOR_CARS')).toBeTruthy();
    expect(templateService.isOutrightSport('RUGBY')).toBeFalsy();
  });
    it('should set popularscore', () => {
    templateService.popularScorer=true;
    expect(templateService.getPopularScorer()).toEqual(true);
    });


    it('should set otherscore', () => {
    templateService.otherScorer=true;
    expect(templateService.getOtherScorer()).toEqual(true);
    });

  describe('getTemplate', () => {
    let event: any;

    it('should return template with name "Regular for fanzone page"', () => {
      event = { typeName: 'Enhanced Multiples' };
      windowRef.nativeWindow.location.href = 'fanzone';
      expect(templateService.getTemplate(event)).toEqual({
        type: 1, name: 'Regular',
      });
    });

    it('should return template with name "Enhanced Multiples"', () => {
      event = { typeName: 'Enhanced Multiples' };
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'Enhanced Multiples',
      });
    });

    it('should return template with name "Outrights"', () => {
      event = { markets: [] };
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'Outrights',
      });
    });

    it('should return template with name "outrightsWithSelection"', () => {
      event = { eventSortCode: 'TNMT', outcomeId: '1', markets: [{}] };
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'outrightsWithSelection',
      });
    });
    it('should return "Outrights" when sport golf, eventsortcode MTCH, special market', () => {
      event = { eventSortCode: 'MTCH', outcomeId: '', markets: [{}], typeName: '#Yourcall', categoryCode: 'golf', categoryId: '' };
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'Outrights',
      });
      templateService.switcher = true;
      event = { eventSortCode: 'MTCH', outcomeId: '', markets: [{}], typeName: '#Yourcall', categoryCode: 'golf', categoryId: '18' };
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'Regular',
      });

      templateService.switcher = true;
      event = { eventSortCode: 'MTCH', outcomeId: '', markets: [{}], typeName: '#Yourcall', categoryCode: 'golf', categoryId: '' };
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'Outrights',
      });
    });

    it('should return "Regular" when sport is golf, eventsortcode MTCH, not special market', () => {
      event = {
        eventSortCode: 'MTCH', outcomeId: '',
        markets: [{ outcomes: [{}, {}], marketMeaningMinorCode: 'HH' }], typeName: '#Standard', categoryCode: 'golf'
      };
      expect(templateService.getTemplate(event)).toEqual({
        type: 1, name: 'Regular',
      });
    });
    it('should return "Regular" when sport is golf, eventsortcode MTCH, drilldownTagNames and markets are not special', () => {
      event = {
        eventSortCode: 'MTCH', outcomeId: '', drilldownTagNames: '12434',
        markets: [{ outcomes: [{}, {}], marketMeaningMinorCode: 'HH' }], typeName: '3 Ball Betting', categoryCode: 'golf'
      };
      expect(templateService.getTemplate(event)).toEqual({
        type: 1, name: 'Regular',
      });
    });
    it('should return "Outrights" when golf, eventsortcode MTCH and drilldownTagNames is not special', () => {
      event = {
        eventSortCode: 'MTCH', outcomeId: '', drilldownTagNames: '12434',
        markets: [{ outcomes: [{}, {}], marketMeaningMinorCode: 'HH' }], typeName: '#Yourcall', categoryCode: 'golf'
      };
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'Outrights',
      });
    });
    it('should return "Outrights" when golf, eventsortcode MTCH and drilldownTagNames is special', () => {
      event = {
        eventSortCode: 'MTCH', outcomeId: '', drilldownTagNames: 'EVFLAG_SP',
        markets: [{ outcomes: [{}, {}], marketMeaningMinorCode: 'HH' }], typeName: 'abcd', categoryCode: 'golf'
      };
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'Outrights',
      });
    });

    it('should return template with name "Outrights"', () => {
      event = { eventSortCode: 'MTCH', outcomeId: '', markets: [{}] };
      templateService.isOutrightSport = () => true;
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'Outrights',
      });
    });

    it('should return template with name "Regular"', () => {
      event = {
        eventSortCode: 'MTCH123',
        markets: [{
          outcomes: [{}, {}],
          marketMeaningMinorCode: 'HH'
        }]
      };
      expect(templateService.getTemplate(event)).toEqual({
        type: 1, name: 'Regular',
      });
    });

    it('should return template with name "Two or three ways"', () => {
      event = {
        eventSortCode: 'MTCH123',
        markets: [{
          outcomes: [{}, {}]
        }]
      };
      expect(templateService.getTemplate(event)).toEqual({
        type: 1, name: 'Two or three ways',
      });
    });

    it('should return template with name "One way"', () => {
      event = {
        eventSortCode: 'MTCH123',
        markets: [{
          outcomes: [{}]
        }]
      };
      expect(templateService.getTemplate(event)).toEqual({
        type: 2, name: 'One way',
      });
    });
  });

  describe('#genEachWayPlaces', () => {
    let type: IQuickbetReceiptLegPartsModel | IMarket | IBetDetailLegPart;
    beforeEach(() => {
      type = { eachWayPlaces: 5 } as any;
    });

    it('should have been called with default newTerms argument', () => {
      const result = templateService.genEachWayPlaces(type);
      expect(result).toBe('1,2,3,4,5');
    });

    it('should have been called with newTerms true arguments', () => {
      const result = templateService.genEachWayPlaces(type, true);
      expect(result).toBe('1-2-3-4-5');
    });
  });

  describe('#getMarketViewType', () => {
    it('when ViewType template is present in undefined templates', () => {
      const market = { marketMeaningMinorCode: '3W', outcomes: [{}, {}, {}] } as any;
      const result = templateService.getMarketViewType(market);
      expect(result).toBe('WDW');
    });

    it('when ViewType template is not present in undefined templates', () => {
      const market = { marketMeaningMinorCode: 'GT', outcomes: [{}, {}, {}, {}, {}] } as any;
      const result = templateService.getMarketViewType(market);
      expect(result).toBe('List');
    });

    it('should set correct ViewType template for markets group in Football sport', () => {
      const market = { marketMeaningMinorCode: '--', templateMarketName: 'Double Chance', outcomes: [{}, {}, {}, {}, {}] } as any;
      const result = templateService.getMarketViewType(market, 'football');
      expect(result).toBe('marketsGroup');
    });

    it('should return "Correct Score"', () => {
      const market = { marketMeaningMinorCode: 'CS' } as IMarket;
      expect(templateService.getMarketViewType(market)).toEqual('Correct Score');
    });
    it('should return "List"', () => {
      const market = { marketMeaningMinorCode: '--' , templateMarketName: 'Outright'} as IMarket;
      expect(templateService.getMarketViewType(market)).toEqual('List');
    });
    it('should return "List"', () => {
      const market = { marketMeaningMinorCode: '--' , templateMarketName: 'Price Boost'} as IMarket;
      expect(templateService.getMarketViewType(market)).toEqual('List');
    });
    it('should return "List"', () => {
      const market = { marketMeaningMinorCode: '--' , templateMarketName: 'Odds Boosters'} as IMarket;
      expect(templateService.getMarketViewType(market)).toEqual('List');
    });
    it('should return "List"', () => {
      const market = { marketMeaningMinorCode: '--' , templateMarketName: 'Smart Boost'} as IMarket;
      expect(templateService.getMarketViewType(market)).toEqual('List');
    });
    it('should return "List"', () => {
      spyOn(templateService, 'isGetAPriceMarket').and.callThrough();
      const market = { marketMeaningMinorCode: '--' , templateMarketName: '#GetAPrice'} as IMarket;
      expect(templateService.getMarketViewType(market)).toEqual('List');
    });
    it('when ViewType template is not present', () => {
      const market = { outcomes: [{}] } as IMarket;
      expect(templateService.getMarketViewType(market, 'boxing')).toEqual('List');
    });
  });

  describe('sortOutcomesByPrice', () => {
    beforeEach(() => {
      outcomes = [
        {
          prices: [
            {
              priceDec: 1.2
            }
          ]
        },
        {
          prices: [
            {
              priceDec: 0.12
            }
          ]
        },
        {
          prices: [
            {
              priceDec: 11.3
            }
          ]
        }
      ];
    });

    it('should sort outcomes', () => {
      const result = templateService.sortOutcomesByPrice(outcomes);
      expect(result).toEqual([
        {
          prices: [
            {
              priceDec: 0.12
            }
          ]
        },
        {
          prices: [
            {
              priceDec: 1.2
            }
          ]
        },
        {
          prices: [
            {
              priceDec: 11.3
            }
          ]
        },
      ] as any);
    });
  });

  describe('sortByMeaningMinorCode', () => {
    it('should sort by outcomeMeaningMinorCode if isUS flag is set', () => {
      const outcomesArray = [
        { isUS: true, outcomeMeaningMinorCode: '3', id: 1 },
        { isUS: true, outcomeMeaningMinorCode: '2', id: 2 },
        { isUS: true, outcomeMeaningMinorCode: '1', id: 3 }
      ];
      const result = templateService.sortByMeaningMinorCode(outcomesArray as any);
      expect(result[0].id).toEqual(3);
    });

    it('should not sort if isUS flag is not set', () => {
      const outcomesArray = [
        { outcomeMeaningMinorCode: '3', id: 1 },
        { outcomeMeaningMinorCode: '2', id: 2 },
        { outcomeMeaningMinorCode: '1', id: 3 }
      ];
      const result = templateService.sortByMeaningMinorCode(outcomesArray as any);
      expect(result[0].id).toEqual(1);
    });
  });

  describe('addOutcomeMeaningMinorCode', () => {
    it('should add Outcome Meaning Minor Code to outcomes', () => {
      const outcomesArray = [
        {}, {}, {}, {}
      ];
      const result = templateService.addOutcomeMeaningMinorCode(3, outcomesArray as any);
      expect(result[0].outcomeMeaningMinorCode).toEqual(1);
      expect(result[2].outcomeMeaningMinorCode).toEqual(3);
      expect(result[3].outcomeMeaningMinorCode).toEqual(1);
    });
  });

  describe('sortCS', () => {
    it('should sort outcomes array by name', () => {
      const outcomesArray = [
        { name: 'C', csOutcomeOrder:3, outcomeMeaningScores: '3,1,' },
        { name: 'A', csOutcomeOrder:1, outcomeMeaningScores: '1,0,' },
        { name: 'B', csOutcomeOrder:2, outcomeMeaningScores: '2,1,' },
      ];
      const result = templateService.sortCS(outcomesArray as any);
      expect(result[0].name).toEqual('A');
    });

    it('add outcomeMeaningMinorCode if outcomeMeaningScores is present', () => {
      const outcomesArray = [
        { name: 'C', outcomeMeaningScores: '3,1,', csOutcomeOrder:3 },
        { name: 'A', outcomeMeaningScores: '1,0,', csOutcomeOrder:1 },
        { name: 'B', outcomeMeaningScores: '2,2,', csOutcomeOrder:2 },
      ];
      const result = templateService.sortCS(outcomesArray as any);
      expect(result[0].name).toEqual('A');
      expect(result[0].outcomeMeaningMinorCode).toEqual(1);
      expect(result[1].outcomeMeaningMinorCode).toEqual(2);
    });
    it('add outcomeMeaningMinorCode if outcomeMeaningScores is present', () => {
      const outcomesArray = [
        { name: 'C', outcomeMeaningScores: '0,1,', csOutcomeOrder:3 },
        { name: 'A', outcomeMeaningScores: '2,4,', csOutcomeOrder:1 },
        { name: 'B', outcomeMeaningScores: '2,2,', csOutcomeOrder:2 },
      ] as any;
      const result = templateService.sortCS(outcomesArray as any);
      expect(result[1].outcomeMeaningMinorCode).toEqual(2);
    });
  });

  describe('getMarketsColumnsNumberForExceptions', () => {
    it('should return list', () => {
      expect(templateService.getMarketsColumnsNumberForExceptions(1)).toEqual('List');
      expect(templateService.getMarketsColumnsNumberForExceptions(6)).toEqual('List');
    });
    it('should return Win Win', () => {
      expect(templateService.getMarketsColumnsNumberForExceptions(2)).toEqual('WW');
    });
    it('should return Win Draw Win', () => {
      expect(templateService.getMarketsColumnsNumberForExceptions(3)).toEqual('WDW');
    });
  });

  describe('setOutcomeMeaningMinorCodeForExceptions', () => {
    it('should populate outcomeMeaningMinorCode', () => {
      const outcomesArray = [
        { name: 'C' },
        { name: 'A' },
        { name: 'B' },
      ];
      const markets = [
        {
          outcomes: [
            { outcomeMeaningMinorCode: 2, name: 'B' },
            { outcomeMeaningMinorCode: 3, name: 'A' },
          ]
        }
      ];
      const result = templateService.setOutcomeMeaningMinorCodeForExceptions(outcomesArray as any, markets as any);
      expect(result[0].outcomeMeaningMinorCode).toEqual(1);
      expect(result[1].outcomeMeaningMinorCode).toEqual(3);
    });
  });

  describe('sortOutcomesByPriceAndName', () => {
    it('should sort outcomes', () => {
      const outcomesArray = [
        { name: 'C' },
        { name: 'A', prices: [{ priceDec: 0.3 }] },
        { name: 'B' },
        { name: 'A' },
        { name: 'A', prices: [{ priceDec: 0.1 }] },
      ];
      const result = templateService.sortOutcomesByPriceAndName(outcomesArray as any);
      expect(result[0]).toEqual({ name: 'A', prices: [{ priceDec: 0.3 }] });
    });
  });

  describe('sortOutcomesByPriceAndDisplayOrder', () => {
    it('should sort outcomes', () => {
      const outcomesArray = [
        { displayOrder: 'C' },
        { displayOrder: 'A', prices: [{ priceDec: 0.3 }] },
        { displayOrder: 'B' },
        { displayOrder: 'A' },
        { displayOrder: 'A', prices: [{ priceDec: 0.1 }] },
      ];
      spyOn(templateService, 'sortOutcomesByPrice').and.callThrough();
      const result = templateService.sortOutcomesByPriceAndDisplayOrder(outcomesArray as any);
      expect(templateService.sortOutcomesByPrice).toHaveBeenCalled();
    });
  });

  describe('getMarketWithSortedOutcomes', () => {
    beforeEach(() => {
      templateService['getMarketViewType'] = jasmine.createSpy().and.returnValue('CS');
      templateService['isGetAPriceMarket'] = jasmine.createSpy().and.returnValue(false);
    });
    it('should return market with sorted outcomes by displayOrder', () => {
      const market = {
        marketMeaningMinorCode: 'FS',
        outcomes: [
          { name: 'B', displayOrder: 2 },
          { outcomeMeaningMinorCode: 1, name: 'A' },
          { name: 'C', displayOrder: 1 },
        ]
      };
      const result = templateService.getMarketWithSortedOutcomes(market as any);
      expect(result[0].name).toEqual('C');
    });

    it('should return market with sorted outcomes by outcomeMeaningMinorCode', () => {
      const market = {
        marketMeaningMinorCode: 'FS',
        outcomes: [
          { outcomeMeaningMinorCode: 2, name: 'A' },
          { outcomeMeaningMinorCode: 3, name: 'B' },
          { outcomeMeaningMinorCode: 1, name: 'C' },
        ]
      };
      const result = templateService.getMarketWithSortedOutcomes(market as any);
      expect(result[0].name).toEqual('C');
      expect(result[0].originalOutcomeMeaningMinorCode).toEqual(1);
    });

    it('should add 3W outcomeMeaningMinorCode', () => {
      const market = {
        marketMeaningMinorCode: 'FS',
        dispSortName: '3W',
        outcomes: [
          { outcomeMeaningMinorCode: 2, name: 'A' },
          { outcomeMeaningMinorCode: 3, name: 'B' },
          { outcomeMeaningMinorCode: 1, name: 'C' },
        ]
      };
      spyOn(templateService, 'addOutcomeMeaningMinorCode').and.callThrough();
      templateService.getMarketWithSortedOutcomes(market as any);
      expect(templateService.addOutcomeMeaningMinorCode).toHaveBeenCalled();
    });
    it('should not add 3W outcomeMeaningMinorCode', () => {
      const market = {
        marketMeaningMinorCode: 'FS',
        dispSortName: 'LS',
        outcomes: [
          { outcomeMeaningMinorCode: 2, name: 'A' },
          { outcomeMeaningMinorCode: 3, name: 'B' },
          { outcomeMeaningMinorCode: 1, name: 'C' },
        ]
      };
      spyOn(templateService, 'addOutcomeMeaningMinorCode').and.callThrough();
      templateService.getMarketWithSortedOutcomes(market as any);
      expect(templateService.addOutcomeMeaningMinorCode).not.toHaveBeenCalled();
    });
    it('should add 2W outcomeMeaningMinorCode', () => {
      const market = {
        marketMeaningMinorCode: 'FS',
        dispSortName: '2W',
        outcomes: [
          { outcomeMeaningMinorCode: 2, name: 'A' },
          { outcomeMeaningMinorCode: 3, name: 'B' },
          { outcomeMeaningMinorCode: 1, name: 'C' },
        ]
      };
      spyOn(templateService, 'addOutcomeMeaningMinorCode').and.callThrough();
      templateService.getMarketWithSortedOutcomes(market as any);
      expect(templateService.addOutcomeMeaningMinorCode).toHaveBeenCalled();
    });
    it('should return market with sorted outcomes using sortOutcomesByPriceAndName when marketMeaningMinorCode is --', () => {
      const market = {
        marketMeaningMinorCode: '--',
        dispSortName: 'MR',
        outcomes: [
          { outcomeMeaningMinorCode: 2, name: 'A' },
          { outcomeMeaningMinorCode: 3, name: 'B' },
          { outcomeMeaningMinorCode: 1, name: 'C' },
        ]
      };
      spyOn(templateService, 'sortOutcomesByPriceAndName').and.callThrough();
      templateService.getMarketWithSortedOutcomes(market as any);
      expect(templateService.sortOutcomesByPriceAndName).toHaveBeenCalled();
    });
    it('should not return market with sorted outcomes using sortOutcomesByPriceAndName when marketMeaningMinorCode is --', () => {
      const market = {
        marketMeaningMinorCode: '--',
        dispSortName: '3W',
        outcomes: [
          { outcomeMeaningMinorCode: 2, name: 'A' },
          { outcomeMeaningMinorCode: 3, name: 'B' },
          { outcomeMeaningMinorCode: 1, name: 'C' },
        ]
      };
      templateService['getMarketViewType'] = jasmine.createSpy().and.returnValue('List');
      templateService['isGetAPriceMarket'] = jasmine.createSpy().and.returnValue(true);
      spyOn(templateService, 'sortOutcomesByPriceAndDisplayOrder').and.callThrough();
      spyOn(templateService, 'sortOutcomesByPriceAndName').and.callThrough();
      templateService.getMarketWithSortedOutcomes(market as any);
      expect(templateService.sortOutcomesByPriceAndName).not.toHaveBeenCalled();
      expect(templateService.sortOutcomesByPriceAndDisplayOrder).toHaveBeenCalled();
    });
    it('should not return market with sorted outcomes using sortOutcomesByPriceAndName when undefinedFlag is true', () => {
      const market = {
        marketMeaningMinorCode: 'MR',
        dispSortName: '3W',
        outcomes: [
          { outcomeMeaningMinorCode: 2, name: 'A' },
          { outcomeMeaningMinorCode: 3, name: 'B' },
          { outcomeMeaningMinorCode: 1, name: 'C' },
        ]
      };
      templateService.undefinedFlag = true;
      spyOn(templateService, 'sortOutcomesByPriceAndName').and.callThrough();
      templateService.getMarketWithSortedOutcomes(market as any);
      expect(templateService.sortOutcomesByPriceAndName).not.toHaveBeenCalled();
    });
    it('should return market with sorted outcomes using sortOutcomesByPriceAndName marketMeaningMinorCode is undefined-2', () => {
      const market = {
        dispSortName: 'MR',
        outcomes: [
          { outcomeMeaningMinorCode: 2, name: 'A' },
          { outcomeMeaningMinorCode: 3, name: 'B' },
          { outcomeMeaningMinorCode: 1, name: 'C' },
        ]
      };
      templateService.undefinedFlag = true;
      spyOn(templateService, 'sortOutcomesByPriceAndName').and.callThrough();
      templateService.getMarketWithSortedOutcomes(market as any);
      expect(templateService.sortOutcomesByPriceAndName).toHaveBeenCalled();
    });
    it('should return market with sorted outcomes using sortOutcomesByPriceAndName', () => {
      const market = {
        outcomes: [
          { outcomeMeaningMinorCode: 2, name: 'A' },
          { outcomeMeaningMinorCode: 3, name: 'B' },
          { outcomeMeaningMinorCode: 1, name: 'C' },
        ]
      };
      spyOn(templateService, 'sortOutcomesByPriceAndName').and.callThrough();
      templateService.getMarketWithSortedOutcomes(market as any);
      expect(templateService.sortOutcomesByPriceAndName).toHaveBeenCalled();
    });
  });

  describe('getSportViewTypes', () => {
    it('should return ISportViewTypes', () => {
      expect(templateService.getSportViewTypes('football')).toEqual({ className: true, outrights: false });
      expect(templateService.getSportViewTypes('motorsports')).toEqual({ className: true, outrights: true });
      expect(templateService.getSportViewTypes('golf')).toEqual({ className: false, outrights: false });
    });
  });

  const sportCategories = [
    { categoryId: 1, svgId: 'svgId-1', svg: 'svg-1' },
    { categoryId: 2, svgId: 'svgId-2', svg: 'svg-2' },
    { categoryId: 3, svgId: 'svgId-3', svg: 'svg-3' },
  ];

  describe('addIconsToEvents', () => {
    it('should add icons to events', fakeAsync(() => {
      templateService.cmsProvider.getMenuItems = jasmine.createSpy().and.returnValue(of(sportCategories));
      const events = [
        { id: '1', categoryId: '1' },
        { id: '2', categoryId: '5' }
      ];
      templateService.addIconsToEvents(events as any).subscribe(() => {
        expect(events).toEqual([
          { id: '1', categoryId: '1', svgId: 'svgId-2' },
          { id: '2', categoryId: '5' }
        ] as any);
      });
      flush();
    }));
  });

  describe('getIconSport', () => {
    it('should return icon', fakeAsync(() => {
      templateService.cmsProvider.getMenuItems = jasmine.createSpy().and.returnValue(of(sportCategories));
      templateService.getIconSport(2).subscribe(result => {
        expect(result).toEqual({ categoryId: 3, svgId: 'svgId-3', svg: 'svg-3' });
      });
      tick();
    }));
  });

  describe('getEventCorrectedDay', () => {
    const startTime = (new Date('2020-03-20')).toISOString();

    it('should return "sb.today"', () => {
      timeService.determineDay = jasmine.createSpy().and.returnValue('today');
      expect(templateService.getEventCorectedDay(startTime)).toEqual('sb.today');
    });

    it('should return "EEE"', () => {
      timeService.determineDay = jasmine.createSpy().and.returnValue('tomorrow');
      expect(templateService.getEventCorectedDay(startTime)).toEqual('EEE');
    });

    it('should return "d MMM"', () => {
      timeService.determineDay = jasmine.createSpy().and.returnValue('');
      templateService.getEventCorectedDay(startTime);
      expect(templateService.filter.date).toHaveBeenCalledWith('2020-03-20T00:00:00.000Z', 'd MMM');
    });
  });

  describe('getEventCorectedDays', () => {
    const startTime = (new Date('2020-03-20')).toISOString();

    it('should return "sb.today"', () => {
      timeService.determineDay = jasmine.createSpy().and.returnValue('today');
      expect(templateService.getEventCorectedDays(startTime)).toEqual('sb.today');
    });

    it('should return "sb.tomorrow"', () => {
      timeService.determineDay = jasmine.createSpy().and.returnValue('tomorrow');
      expect(templateService.getEventCorectedDays(startTime)).toEqual('sb.tomorrow');
    });

    it('should return "d MMM"', () => {
      timeService.determineDay = jasmine.createSpy().and.returnValue('');
      templateService.getEventCorectedDays(startTime);
      expect(templateService.filter.date).toHaveBeenCalledWith('2020-03-20T00:00:00.000Z', 'd MMM');
    });
  });

  describe('isMultiplesEvent', () => {
    it('should return true', () => {
      const eventEntity = { typeName: 'Enhanced Multiples' } as ISportEvent;
      expect(templateService.isMultiplesEvent(eventEntity)).toBeTruthy();
    });

    it('should return false', () => {
      const eventEntity = { typeName: 'Whatever' } as ISportEvent;
      expect(templateService.isMultiplesEvent(eventEntity)).toBeFalsy();
    });
  });

  describe('filterMultiplesEvents', () => {
    it('should return array of events without Enhanced Multiples', () => {
      const events = [
        { typeName: 'Enhanced Multiples' },
        { typeName: 'Whatever' }
      ] as ISportEvent[];
      expect(templateService.filterMultiplesEvents(events).length).toEqual(1);
    });

    it('should return array', () => {
      expect(templateService.filterMultiplesEvents()).toEqual([]);
    });
  });

  describe('getCorrectedOutcomeMeaningMinorCode', () => {
    it('should return 1 (H)', () => {
      const outcomeEntity = { outcomeMeaningMinorCode: 'H' } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(1);
    });
    it('should return 2 (O)', () => {
      const outcomeEntity = { outcomeMeaningMinorCode: 'O' } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(2);
    });
    it('should return 3 (H)', () => {
      const outcomeEntity = { outcomeMeaningMinorCode: 'H', isUS: true } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(3);
    });
    ['D', 'N', 'L'].forEach(code => {
      it(`should return 2 (${code})`, () => {
        const outcomeEntity = { outcomeMeaningMinorCode: code } as IOutcome;
        expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(2);
      });
    });
    it('should return 3 (A)', () => {
      const outcomeEntity = { outcomeMeaningMinorCode: 'A' } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(3);
    });
    it('should return 1 (A)', () => {
      const outcomeEntity = { outcomeMeaningMinorCode: 'A', isUS: true } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(1);
    });
    it('should return 3 (L)', () => {
      const outcomeEntity = { outcomeMeaningMinorCode: 'L', outcomeMeaningMajorCode: 'HL' } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(3);
    });
    it('should return 1 (Yes)', () => {
      const outcomeEntity = { outcomeMeaningMajorCode: '--', name: 'Yes' } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(1);
    });
    it('should return 3 (No)', () => {
      const outcomeEntity = { outcomeMeaningMajorCode: '--', name: 'No' } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(3);
    });
    it('should return 1 (No) if isUs is true', () => {
      const outcomeEntity = { outcomeMeaningMinorCode: 'L', outcomeMeaningMajorCode: 'HL', isUS: true } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(1);
    });
    it('should return number', () => {
      const outcomeEntity = { outcomeMeaningMinorCode: 123 } as IOutcome;
      expect(templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity)).toEqual(123);
    });
  });

  describe('filterEventsWithoutMarketsAndOutcomes', () => {
    it('should return array', () => {
      const events = [
        { markets: [{ outcomes: [{}] }] },
        { markets: [] }
      ] as ISportEvent[];
      expect(templateService.filterEventsWithoutMarketsAndOutcomes(events).length).toEqual(1);
    });
  });



  describe('filterBetInRunMarkets', () => {
    it('should return array', () => {
      const events = [
        { isStarted: true, markets: [{ isMarketBetInRun: true }] },
        { markets: [{ outcomes: [] }] }
      ] as ISportEvent[];
      expect(templateService.filterBetInRunMarkets(events).length).toEqual(2);
    });
    it('should return array', () => {
      const events = [
        { isStarted: true, markets: [{ isMarketBetInRun: true }] },
        { isStarted: false, markets: [{ outcomes: [] }] }
      ] as ISportEvent[];
      expect(templateService.filterBetInRunMarkets(events).length).toEqual(1);
    });
  });


  describe('genClass', () => {
    it('should return empty string', () => {
      const eventEntity = {} as ISportEvent;
      expect(templateService.genClass(eventEntity)).toEqual('');
    });
    it('should return string', () => {
      const eventEntity = { racingFormEvent: { class: 'some-class' } } as ISportEvent;
      expect(templateService.genClass(eventEntity)).toEqual('sb.class');
    });
  });
  describe('isGetAPriceMarket', () => {
    it('should return true', () => {
      const market = { templateMarketName: '#GetAPrice' };
      templateService['isGetAPriceMarket'](market);
      expect(templateService['isGetAPriceMarket']).toBeTruthy();
    });
    it('should return false', () => {
      const market = { templateMarketName: 'Teams' };
      expect(templateService['isGetAPriceMarket'](market)).toBeFalsy();
    });
  });
  describe('checkGoalScorerMarket', () => {
    it('popularScorer should return true', () => {
      templateService.marketList= [{templateMarketName:'Outright'},{templateMarketName:'First Goalscorer'}, {templateMarketName:'Anytime Goalscorer'}, {templateMarketName:'Goalscorer - 2 Or More'}];
      templateService['checkGoalScorerMarket']();
      expect(templateService.popularScorer).toBe(true);
      expect(templateService.otherScorer).toBe(false);
    });
    it('otherMarkets should return true', () => {
      templateService.marketList= [{templateMarketName:'Outright'},{templateMarketName:'Last Goalscorer'}, {templateMarketName:'Hat trick'}];
      templateService['checkGoalScorerMarket']();
      expect(templateService.popularScorer).toBe(false);
      expect(templateService.otherScorer).toBe(true);
    });
    it('marketList is empty', () => {
      templateService.marketList= [];
      templateService['checkGoalScorerMarket']();
      expect(templateService.popularScorer).toBe(false);
      expect(templateService.otherScorer).toBe(false);
    });
    it('marketList is undefined', () => {
      templateService.marketList= undefined;
      templateService['checkGoalScorerMarket']();
      expect(templateService.popularScorer).toBe(false);
      expect(templateService.otherScorer).toBe(false);
    });
    it('marketList is null', () => {
      templateService.marketList= null;
      templateService['checkGoalScorerMarket']();
      expect(templateService.popularScorer).toBe(false);
      expect(templateService.otherScorer).toBe(false);
    });
    it('marketList is undefined-2', () => {
      templateService['checkGoalScorerMarket']();
      expect(templateService.popularScorer).toBe(false);
      expect(templateService.otherScorer).toBe(false);
    });
  });
});

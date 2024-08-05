import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';

describe('MarketTypeService', () => {
  let service: MarketTypeService;

  beforeEach(() => {
    service = new MarketTypeService();
  });

  describe('@isHeader2Columns', () => {
    it('it should set correct header - isOverUnderType = true', () => {
      const market = {} as any;
      service.isHomeDrawAwayType = jasmine.createSpy('isHomeDrawAwayType').and.returnValue(false);
      service.isMatchResultType = jasmine.createSpy('isMatchResultType').and.returnValue(false);
      service.isYesNoType = jasmine.createSpy('isYesNoType').and.returnValue(false);
      service.isOverUnderType = jasmine.createSpy('isOverUnderType').and.returnValue(true);
      expect(service.isHeader2Columns(market)).toBe(true);
    });

    it('it should set correct header - isYesNoType = true', () => {
      const market = {} as any;
      service.isHomeDrawAwayType = jasmine.createSpy('isHomeDrawAwayType').and.returnValue(false);
      service.isMatchResultType = jasmine.createSpy('isMatchResultType').and.returnValue(false);
      service.isYesNoType = jasmine.createSpy('isYesNoType').and.returnValue(true);
      service.isOverUnderType = jasmine.createSpy('isOverUnderType').and.returnValue(false);
      expect(service.isHeader2Columns(market)).toBe(true);
    });

    it('it should set correct header - isHomeDrawAwayType = true', () => {
      const market = {} as any;
      service.isHomeDrawAwayType = jasmine.createSpy('isHomeDrawAwayType').and.returnValue(true);
      service.isMatchResultType = jasmine.createSpy('isMatchResultType').and.returnValue(false);
      service.isYesNoType = jasmine.createSpy('isYesNoType').and.returnValue(false);
      service.isOverUnderType = jasmine.createSpy('isOverUnderType').and.returnValue(false);
      expect(service.isHeader2Columns(market)).toBe(false);
    });

    it('it should set correct header - isMatchResultType = true', () => {
      const market = { } as any;
      service.isHomeDrawAwayType = jasmine.createSpy('isHomeDrawAwayType').and.returnValue(false);
      service.isMatchResultType = jasmine.createSpy('isMatchResultType').and.returnValue(true);
      service.isYesNoType = jasmine.createSpy('isYesNoType').and.returnValue(false);
      service.isOverUnderType = jasmine.createSpy('isOverUnderType').and.returnValue(false);
      expect(service.isHeader2Columns(market)).toBe(false);
    });

    it('it should set correct header - invalid market', () => {
      const market = null;
      service.isHomeDrawAwayType = jasmine.createSpy('isHomeDrawAwayType').and.returnValue(false);
      service.isMatchResultType = jasmine.createSpy('isMatchResultType').and.returnValue(false);
      service.isYesNoType = jasmine.createSpy('isYesNoType').and.returnValue(false);
      service.isOverUnderType = jasmine.createSpy('isOverUnderType').and.returnValue(false);
      expect(service.isHeader2Columns(market)).toBe(false);
    });
  });

  describe('@isHomeDrawAwayType', () => {
    it('it should set correct header for market "Extra-Time Result"', () => {
      const market = { templateMarketName: 'Extra-Time Result' } as any;
      expect(service.isHomeDrawAwayType(market)).toBe(true);
    });

    it('it should set correct header for market "Next Team to Score"', () => {
      const market = { templateMarketName: 'Next Team to Score' } as any;
      expect(service.isHomeDrawAwayType(market)).toBe(true);
    });

    it('it should set correct header for other market with 3 outcomes', () => {
      const market = { templateMarketName: 'Other Market', outcomes: [ {}, {}, {} ] } as any;
      expect(service.isHomeDrawAwayType(market)).toBe(true);
    });

    it('it should set correct header for other market', () => {
      const market = { templateMarketName: 'Other Market', outcomes: [{}] } as any;
      expect(service.isHomeDrawAwayType(market)).toBe(false);
    });

    it('it should set correct header for other market without outcomes', () => {
      const market = { templateMarketName: 'Other Market' } as any;
      expect(service.isHomeDrawAwayType(market)).toBe(undefined);
    });

    it('it should set correct header for event without market', () => {
      const market = undefined;
      expect(service.isHomeDrawAwayType(market)).toBe(undefined);
    });
  });

  describe('@isOneTieTwoType', () => {
    it('marketentity with outcomes 3 & 60 Minute Betting should be true', () => {
      const market = {
        templateMarketName: '60 Minute Betting',
        outcomes: [{ id: '1' }, { id: '2' }, { id: '3' }]
      } as any;
      const categoryId = '1';
      service['OneTieTwoMarketNames']=['60 Minute Betting', '2 Ball Betting'];
      expect(service.isOneTieTwoType(market, categoryId)).toBe(true);

    });
    it('marketentity with outcomes 2 & 60 Minute Betting should be false', () => {
      const market = {
        templateMarketName: '60 Minute Betting',
        outcomes: [{ id: '1' }, { id: '2' }]
      } as any;
      const categoryId = '1';
      service['OneTieTwoMarketNames']=['60 Minute Betting', '2 Ball Betting'];
      expect(service.isOneTieTwoType(market, categoryId)).toBe(false);

    });
    it('marketentity with outcomes 3 & Test Betting should be false', () => {
      const market = {
        templateMarketName: 'Test Betting',
        outcomes: [{ id: '1' }, { id: '2' }, { id: '3' }]
      } as any;
      const categoryId = '1';
      service['OneTieTwoMarketNames']=['60 Minute Betting', '2 Ball Betting'];
      expect(service.isOneTieTwoType(market, categoryId)).toBe(false);

    });
    it('marketentity with outcomes 2 & Test Betting should be false', () => {
      const market = {
        templateMarketName: 'Test Betting',
        outcomes: [{ id: '1' }, { id: '2' }]
      } as any;
      const categoryId = '1';
      service['OneTieTwoMarketNames']=['60 Minute Betting', '2 Ball Betting'];
      expect(service.isOneTieTwoType(market, categoryId)).toBe(false);
    });
    it('marketentity with outcomes 3 & Match Betting & For Darts(13) should be true', () => {
      const market = {
        templateMarketName: 'Match Betting',
        outcomes: [{ id: '1' }, { id: '2' }, { id: '3' }]
      } as any;
      const categoryId = '13';
      service['OneTieTwoMarketNames']=['60 Minute Betting', '2 Ball Betting'];
      expect(service.isOneTieTwoType(market, categoryId)).toBe(true);
    });
    it('marketentity with outcomes 2 & Match Betting & For Football(16) should be false', () => {
      const market = {
        templateMarketName: 'Match Betting',
        outcomes: [{ id: '1' }, { id: '2' }, { id: '3' }]
      } as any;
      const categoryId = '16';
      service['OneTieTwoMarketNames']=['60 Minute Betting', '2 Ball Betting'];
      expect(service.isOneTieTwoType(market, categoryId)).toBe(false);
    });
  });

  describe('#isOneDrawTwoType', () => {
    it('marketentity with outcomes 3 & Fight Betting should be true', () => {
      const market = {
        templateMarketName: 'Fight Betting',
        outcomes: [{ id: '1' }, { id: 'draw' }, { id: '2' }]
      } as any;
      const categoryId = '9';
      service['oneDrawTwoTemplateMarketNames']=['Fight Betting'];
      expect(service.isOneDrawTwoType(market, categoryId)).toBe(true);
    });
    
    it('marketentity with outcomes 2 & Fight Betting should be false', () => {
      const market = {
        templateMarketName: 'Fight Betting',
        outcomes: [{ id: '1' }, { id: '2' }]
      } as any;
      const categoryId = '9';
      service['oneDrawTwoTemplateMarketNames']=['Fight Betting'];
      expect(service.isOneDrawTwoType(market, categoryId)).toBe(false);
    });
  });

  describe('#getDisplayMarketConfig', () => {
    it('should return empty object', () => {
      const result = service.getDisplayMarketConfig('', [] as any);

      expect(result).toEqual({} as any);
    });

    it('should return eventMarketConfig', () => {
      const markets = [{
        templateMarketName: 'market1'
      }];
      const result = service.getDisplayMarketConfig('market1,market2', markets as any);

      expect(result).toEqual({
        displayMarketName: 'market1',
        displayMarket: { templateMarketName: 'market1' }
      } as any);
    });

    it('should return eventMarketConfig with typeof markets[0] = string', () => {
      const markets = ['market1'];
      const result = service.getDisplayMarketConfig('market1', markets as any);

      expect(result).toEqual({
        displayMarketName: 'market1',
        displayMarket: 0
      } as any);
    });
    it('should check match Betting and Match result', () => {
      const markets = ['Match Result'];
      const result = service.getDisplayMarketConfig('Match Betting', markets as any);

      expect(result).toEqual({
        displayMarketName: 'Match Betting',
        displayMarket: 0
      } as any);
    });
  });

  describe('combineMeaningCode', () => {
    it('should return particular string', () => {
      const marketEntity = { marketMeaningMajorCode: 'A', marketMeaningMinorCode: 'B' } as IMarket;
      expect(service.combineMeaningCode(marketEntity)).toEqual('A|B');
    });
  });

  describe('isOverUnderType', () => {
    it('should return true', () => {
      const marketEntity = { marketMeaningMajorCode: 'L', marketMeaningMinorCode: 'I' } as IMarket;
      expect(service.isOverUnderType(marketEntity)).toBe(true);
    });
  });

  describe('isYesNoType', () => {
    it('should return true', () => {
      const marketEntity = { dispSortName: 'BO', marketMeaningMinorCode: 'GB' } as IMarket;
      expect(service.isYesNoType(marketEntity)).toBe(true);
    });
  });

  describe('isMatchResultType', () => {
    [ 'MR', 'H1', 'H2'].forEach(minorCode => {
      it(`should return true for "${minorCode}"`, () => {
        const marketEntity = { marketMeaningMajorCode: '-', marketMeaningMinorCode: minorCode } as IMarket;
        expect(service.isMatchResultType(marketEntity)).toEqual(true);
      });
    });
    it('should return false', () => {
      const marketEntity = { marketMeaningMinorCode: 'whatever'} as IMarket;
      expect(service.isMatchResultType(marketEntity)).toEqual(false);
    });
  });

  describe('someEventsAreMatchResultType', () => {
    it('should return true #1', () => {
      const events = [
        { markets: [ { marketMeaningMajorCode: '-', marketMeaningMinorCode: 'MR' } ] },
        { markets: [] }
      ] as ISportEvent[];
      expect(service.someEventsAreMatchResultType(events, '', false)).toEqual(true);
    });
    it('should return true #2', () => {
      const events = [
        { markets: [ { templateMarketName: 'market name', marketMeaningMajorCode: '-', marketMeaningMinorCode: 'MR' } ] },
        { markets: [] }
      ] as ISportEvent[];
      expect(service.someEventsAreMatchResultType(events, 'market name', true)).toEqual(true);
    });
    it('should return true #3', () => {
      const events = [
        { markets: [ { name: 'market name', marketMeaningMajorCode: '-', marketMeaningMinorCode: 'MR' } ] },
        { markets: [] }
      ] as ISportEvent[];
      expect(service.someEventsAreMatchResultType(events, 'market name', false)).toEqual(true);
    });
  });

  describe('#extractMarketNameFromEvents', () => {
    it('should return market names', () => {
      const events = [{
        categoryCode: 16,
        categoryName: 'football',
        typeId: '8',
        markets: [{
          templateMarketName: 'templateMarketName'
        }],
      }];
      const result = service.extractMarketNameFromEvents(events as any, true);

      expect(result).toEqual(['templateMarketName'] as any);
    });
    it('should return Match Result for market names which has templateMarketName as Match Betting', () => {
      const events = [{
        categoryCode: 16,
        categoryName: 'rugby-league',
        typeId: '8',
        markets: [{ templateMarketName: 'Match Betting', name: 'Match Betting' }],
      }];
      const result = service.extractMarketNameFromEvents(events as any, true);

      expect(result).toEqual(['Match Result'] as any);
      const result1 = service.extractMarketNameFromEvents(events as any, false);

      expect(result1).toEqual(['Match Betting'] as any);

      const events1 = [{
        categoryCode: 16,
        categoryName: 'rugby-league',
        typeId: '8'
      }]; 

      const result2 = service.extractMarketNameFromEvents(events1 as any, false);

      expect(result2).toEqual([] as any);
    });
  });
});

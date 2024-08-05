import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import { IBetslipBetData } from '@betslip/models/betslip-bet-data.model';
import { IOutcome } from '@core/models/outcome.model';

describe('BetslipBetDataUtils', () => {
  describe('isFreeBetUsed', () => {
    it('should return true if freebet property exist', () => {
      const betData = { Bet: { freeBet: { id: '1234' } } } as IBetslipBetData;

      expect(BetslipBetDataUtils.isFreeBetUsed(betData)).toBe(true);
    });

    it('should return true if freebet was used', () => {
      const betData = { Bet: {}, tokenValue: 5 } as IBetslipBetData;

      expect(BetslipBetDataUtils.isFreeBetUsed(betData)).toBe(true);
    });

    it('should return false if freebet property does not exist', () => {
      const betData = { Bet: {} } as IBetslipBetData;

      expect(BetslipBetDataUtils.isFreeBetUsed(betData)).toBe(false);
    });

    it('should return false if freebet property does not contain id', () => {
      const betData = { Bet: { freeBet: {} } } as IBetslipBetData;

      expect(BetslipBetDataUtils.isFreeBetUsed(betData)).toBe(false);
    });
  });

  describe('areFreeBetsAvailable', () => {
    it('should return true if freebets contains some numbers', () => {
      const betData = { Bet: { freeBets: [1, 2] as any } } as IBetslipBetData;

      expect(BetslipBetDataUtils.areFreeBetsAvailable(betData)).toBe(true);
    });
    it('should return false if freebets are empty', () => {
      const betData = { Bet: { freeBets: [] as any } } as IBetslipBetData;

      expect(BetslipBetDataUtils.areFreeBetsAvailable(betData)).toBe(false);
    });
    it('should return false if freebets does not exist', () => {
      const betData = { Bet: {} } as IBetslipBetData;

      expect(BetslipBetDataUtils.areFreeBetsAvailable(betData)).toBe(false);
    });
    it('should return false if bet is disabled', () => {
      const betData = { Bet: { disabled: true } as any } as IBetslipBetData;

      expect(BetslipBetDataUtils.areFreeBetsAvailable(betData)).toBe(false);
    });
  });

  describe('estReturnsAvalibale', () => {
    it('should return false if no bet', () => {
      expect(BetslipBetDataUtils.estReturnsAvalibale(null)).toEqual(false);
    });

    it('should return false if bet has no price', () => {
      expect(BetslipBetDataUtils.estReturnsAvalibale({} as any)).toEqual(false);
    });

    it('should return false if bet has no priceType', () => {
      expect(BetslipBetDataUtils.estReturnsAvalibale({price: {}} as any)).toEqual(false);
    });

    it('should return false if priceType is SP', () => {
      expect(BetslipBetDataUtils.estReturnsAvalibale({price: {priceType: 'SP'}} as any)).toEqual(false);
    });

    it('should return true', () => {
      expect(BetslipBetDataUtils.estReturnsAvalibale({price: {priceType: 'LP'}} as any)).toEqual(true);
      expect(BetslipBetDataUtils.estReturnsAvalibale({price: {priceType: 'GP'}} as any)).toEqual(true);
      expect(BetslipBetDataUtils.estReturnsAvalibale({price: {priceType: 'GUARANTEED'}} as any)).toEqual(true);
    });
  });

  describe('isSPLP', () => {
    let market;
    let outcome;

    beforeEach(() => {
      market = {
        isLpAvailable: true,
        isSpAvailable: true
      };
      outcome = {
        outcomeMeaningMinorCode: '0'
      };
    });

    it('should return true', () => {
      expect(BetslipBetDataUtils.isSPLP(market, outcome)).toEqual(true);
    });

    it('should return false if market has no isLpAvailable', () => {
      market.isLpAvailable = false;
      expect(BetslipBetDataUtils.isSPLP(market, outcome)).toEqual(false);
    });

    it('should return false if market has no isSpAvailable', () => {
      market.isSpAvailable = false;
      expect(BetslipBetDataUtils.isSPLP(market, outcome)).toEqual(false);
    });

    it('should return false if outcomeMeaningMinorCode is 1', () => {
      outcome.outcomeMeaningMinorCode = '1';
      expect(BetslipBetDataUtils.isSPLP(market, outcome)).toEqual(false);

      market.outcomeMeaningMinorCode = '1';
      expect(BetslipBetDataUtils.isSPLP(market)).toEqual(false);
    });

    it('should return false if outcomeMeaningMinorCode is 2', () => {
      outcome.outcomeMeaningMinorCode = '2';
      expect(BetslipBetDataUtils.isSPLP(market, outcome)).toEqual(false);

      market.outcomeMeaningMinorCode = '2';
      expect(BetslipBetDataUtils.isSPLP(market)).toEqual(false);
    });
  });

  describe('outcomeDetails', () => {
    let event, market, outcome;

    beforeEach(() => {
      event = {
        drilldownTagNames: 'event drilldownTagNames',
        liveServChannels: 'event liveServChannels',
        isAvailable: false,
        cashoutAvail: false,
        sportId: 100,
        startTime: '00:00',
        isStarted: false
      };
      market = {
        drilldownTagNames: 'market drilldownTagNames',
        liveServChannels: 'market liveServChannels',
        isMarketBetInRun: false,
        isGpAvailable: false,
        isEachWayAvailable: false,
        cashoutAvail: false,
        priceTypeCodes: 'priceTypeCodes'
      };
      outcome = {
        liveServChannels: 'outcome liveServChannels',
        outcomeMeaningMinorCode: 'H'
      };
    });
    it('should return undefined', () => {
      expect(BetslipBetDataUtils.outcomeDetails(undefined, {} as any, {} as any)).toEqual(undefined);
      expect(BetslipBetDataUtils.outcomeDetails({} as any, undefined, {} as any)).toEqual(undefined);
      expect(BetslipBetDataUtils.outcomeDetails({} as any, {} as any, undefined, )).toEqual(undefined);
    });


    it('should return outcome detail data', () => {
      expect(BetslipBetDataUtils.outcomeDetails(event as any, market as any, outcome as any)).toEqual({
        eventDrilldownTagNames: 'event drilldownTagNames',
        marketDrilldownTagNames: 'market drilldownTagNames',
        isAvailable: false,
        cashoutAvail: false,
        marketCashoutAvail: false,
        isMarketBetInRun: false,
        eventliveServChannels: 'event liveServChannels',
        marketliveServChannels: 'market liveServChannels',
        outcomeliveServChannels: 'outcome liveServChannels',
        isSPLP: false,
        isGpAvailable: false,
        isEachWayAvailable: false,
        marketPriceTypeCodes: 'priceTypeCodes',
        outcomeMeaningMinorCode: 'H',
        info: {
          sportId: 100,
          time: '00:00',
          isStarted: false
        }
      } as any);
    });

    it('should return outcome detail data with marketliveServChannels on market level', () => {
      market.marketliveServChannels = 'marketliveServChannels';

      expect(BetslipBetDataUtils.outcomeDetails(event as any, market as any, outcome as any)).toEqual({
        eventDrilldownTagNames: 'event drilldownTagNames',
        marketDrilldownTagNames: 'market drilldownTagNames',
        isAvailable: false,
        cashoutAvail: false,
        marketCashoutAvail: false,
        isMarketBetInRun: false,
        eventliveServChannels: 'event liveServChannels',
        marketliveServChannels: 'marketliveServChannels',
        outcomeliveServChannels: 'outcome liveServChannels',
        isSPLP: false,
        isGpAvailable: false,
        isEachWayAvailable: false,
        marketPriceTypeCodes: 'priceTypeCodes',
        outcomeMeaningMinorCode: 'H',
        info: {
          sportId: 100,
          time: '00:00',
          isStarted: false
        }
      } as any);
    });
  });

  describe('getOutcomeMeaningMinorCode', () => {
    it('should return outcomeMeaningMinorCode', () => {
      const result = BetslipBetDataUtils.getOutcomeMeaningMinorCode({outcomeMeaningMinorCode: 'H'} as IOutcome);

      expect(result).toEqual('H');
    });

    it('should return originalOutcomeMeaningMinorCode', () => {
      const result = BetslipBetDataUtils.getOutcomeMeaningMinorCode(
        {outcomeMeaningMinorCode: 1, originalOutcomeMeaningMinorCode: '1'} as any
      );

      expect(result).toEqual('1');
    });
  });
});

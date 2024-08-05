import { Observable } from 'rxjs';

import { CacheEventsService } from './cache-events.service';
import { Cached } from './cached';

describe('CacheEventsService', () => {
  let service: CacheEventsService;
  let timeService;
  let pubSubService;

  beforeEach(() => {
    timeService = {
      getCurrentTime: jasmine.createSpy(),
      apiDataCacheInterval: {
        event: 1
      }
    };
    pubSubService = {
      publish: jasmine.createSpy()
    };

    service = new CacheEventsService(
      timeService,
      pubSubService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('store', () => {
    service['pack'] = jasmine.createSpy();
    service.addToIndex = jasmine.createSpy();
    service['merge'] = jasmine.createSpy();
    service.stored = jasmine.createSpy();

    const args = ['/', 'home', 1];

    service.store(...args);

    expect(service['pack']).toHaveBeenCalledWith(args);
    expect(service.addToIndex).toHaveBeenCalled();
    expect(service['merge']).toHaveBeenCalled();
    expect(service.stored).toHaveBeenCalledWith(...args.slice(0, -1) as any);
  });

  it('clearByName', () => {
    service.clearByName('event');
    expect(service.storedData.event).toBeUndefined();
  });

  it('async', () => {
    expect(service.async(null, true)).toEqual(jasmine.any(Promise));
    expect(service.async(null, false)).toEqual(jasmine.any(Observable));
  });

  it('storeNewMarketOrOutcome', () => {
    service['storeNewMarket'] = jasmine.createSpy();
    service['storeNewOutcome'] = jasmine.createSpy();
    let update;

    update = { eventId: 'EID' };
    service.storeNewMarketOrOutcome(update);
    expect(service['storeNewMarket']).toHaveBeenCalledWith(update);

    update = {};
    service.storeNewMarketOrOutcome(update);
    expect(service['storeNewOutcome']).toHaveBeenCalledWith(update);
  });

  it('stored', () => {
    const cached = new Cached(null, timeService);
    const intervalId = 1;

    service['dive'] = jasmine.createSpy().and.returnValue(cached);
    service['isDataOutdated'] = jasmine.createSpy();
    service['interval'] = jasmine.createSpy().and.returnValue(intervalId);

    const args = ['a', 'b'];
    service.stored(...args);

    expect(service['dive']).toHaveBeenCalledWith(args, service.storedData);
    expect(service['interval']).toHaveBeenCalledWith(args[0]);
    expect(service['isDataOutdated']).toHaveBeenCalledWith(cached as any, intervalId);
  });

  it('addToIndex', () => {
    service['getStoredDataPath'] = jasmine.createSpy().and.returnValue(['event1']);
    service['cleanIndex'] = jasmine.createSpy();
    service['addToIndexWithDeepnessLevel1'] = service['addToIndexWithDeepnessLevel2'] = () => {};

    const data: any = {
      index: [], marketsIndex: [], outcomesIndex: []
    };
    const sourceData: any = {
      event1: {
        updated: 1540991989051,
        data: [{}]
      }
    };
    service.addToIndex(data, sourceData);

    expect(service['getStoredDataPath']).toHaveBeenCalledWith(sourceData);
    expect(service['cleanIndex']).toHaveBeenCalledWith(
      data.index, data.marketsIndex, data.outcomesIndex,
    );
  });

  it('cleanIndex', () => {
    const eventsIndex: any = {
      event1: {
        ref1: { expire: 1140982644667 }
      }
    };
    const marketsIndex: any = {
      market1: 'event1'
    };
    const outcomesIndex: any = {
      outcome1: 'event1'
    };
    service['indexConfig'].addToIndexCounter = 99;
    timeService.getCurrentTime.and.returnValue(1540982644667);

    service['cleanIndex'](eventsIndex, marketsIndex, outcomesIndex);

    expect(timeService.getCurrentTime).toHaveBeenCalled();
    expect(eventsIndex.event1).toBeUndefined();
    expect(marketsIndex.market1).toBeUndefined();
    expect(outcomesIndex.outcome1).toBeUndefined();
  });

  it('getStoredDataPath', () => {
    expect(service['getStoredDataPath']({ home: '/' })).toEqual(['home']);
    expect(service['getStoredDataPath']({ home: '/', inplay: '/inplay' })).toEqual([]);
  });

  it('addToIndexWithDeepnessLevel1', () => {
    const eventsIndex: any = {};
    const marketsIndex: any = {};
    const outcomesIndex: any = {};
    const path: any[] = ['/', 'inplay'];
    const reference: any[] = [
      {
        id: 'event1',
        markets: [
          {
            id: 'market1',
            outcomes: [
              { id: 'outcome1' }
            ]
          }
        ]
      }
    ];
    const expireTimestamp = 1540983949804;

    service['addToIndexWithDeepnessLevel1'](
      eventsIndex, marketsIndex, outcomesIndex, path, reference, expireTimestamp
    );

    expect(eventsIndex.event1).toBeDefined();
    expect(marketsIndex.market1).toBe('event1');
    expect(outcomesIndex.outcome1).toBe('event1');
    expect(eventsIndex.event1['/inplay']).toEqual({
      path: path.concat(0),
      expire: expireTimestamp,
      reference: reference[0]
    });
  });

  it('addToIndexWithDeepnessLevel2', () => {
    const eventsIndex: any = {};
    const marketsIndex: any = {};
    const outcomesIndex: any = {};
    const path: any[] = ['/', 'inplay'];
    const reference: any[] = [
      { ref1: {} }
    ];
    const expireTimestamp = 1540983949804;

    const context = {
      fn: jasmine.createSpy(),
      key: 'ref1'
    };

    service['addToIndexWithDeepnessLevel2'].call(
      context, eventsIndex, marketsIndex, outcomesIndex, path, reference, expireTimestamp
    );

    expect(context.fn).toHaveBeenCalledWith(
      eventsIndex, marketsIndex, outcomesIndex, ['/', 'inplay', 0, 'ref1'], reference[0].ref1, expireTimestamp
    );
  });

  it('pack', () => {
    let result;

    result = service['pack'](['a', 'b', 'c']);
    expect(result.a.b).toEqual(jasmine.any(Cached));

    result = service['pack'](['a', 'b']);
    expect(result.a).toEqual(jasmine.any(Cached));

    result = service['pack'](['a']);
    expect(result).toEqual(jasmine.any(Cached));
  });

  it('merge', () => {
    const target: any = {};
    const source: any = { x: 1, y: { z: 2 } };

    service['merge'](target, source);
    expect(target).toEqual(source);
  });

  it('isDataOutdated', () => {
    let cached: any;

    cached = { updated: 1540985035842, data: {} };
    timeService.getCurrentTime.and.returnValue(1540985035899);
    expect(service['isDataOutdated'](cached, 2)).toBeFalsy();
    expect(timeService.getCurrentTime).toHaveBeenCalled();

    cached = { updated: 1540985035899, data: {} };
    timeService.getCurrentTime.and.returnValue(1540985035842);
    expect(service['isDataOutdated'](cached, 2)).toBeTruthy();
    expect(timeService.getCurrentTime).toHaveBeenCalled();
  });

  it('dive', () => {
    let fullPath: any;
    let obj: any;

    fullPath = [];
    obj = null;
    expect(service['dive'](fullPath, obj)).toBeUndefined();

    fullPath = ['a'];
    obj = { a: 1 };
    expect(service['dive'](fullPath, obj)).toBe(obj.a);

    fullPath = ['a', 'b'];
    obj = { a: { b: 1 } };
    expect(service['dive'](fullPath, obj)).toBe(obj.a.b);
  });

  it('interval', () => {
    expect(service['interval']('event')).toBe(timeService.apiDataCacheInterval.event);
  });

  it('storeNewMarket', () => {
    service.storedData.event.data = [{
      id: '1',
      markets: []
    }] as any[];
    const market: any = { id: '2', eventId: '1' };

    expect(service['storeNewMarket'](market)).toBe(service.storedData.event.data[0].markets[0]);
    expect(market.new).toBeTruthy();
    expect(service.storedData.marketsIndex['2']).toBe('1');
    expect(service.storedData.event.data[0].markets[0]).toBe(market);
  });

  it('storeNewMarket (no event)', () => {
    service.storedData.event.data = [] as any[];
    const market: any = {};

    expect(service['storeNewMarket'](market)).toBeFalsy();
    expect(market.new).toBeTruthy();
  });

  it('storeNewOutcome', () => {
    service['extendHandicapOutcome'] = jasmine.createSpy();
    service['removeFakeOutcomes'] = jasmine.createSpy().and.returnValue([]);

    const event: any = {
      id: '1',
      markets: [
        {
          id: '10',
          outcomes: []
        }
      ]
    };

    service.storedData.event.data = [event];

    const outcome: any = {
      id: '30',
      marketId: '10'
    };

    expect(service['storeNewOutcome'](outcome)).toBe(event.markets[0]);
    expect(service['extendHandicapOutcome']).toHaveBeenCalledWith(event.markets[0], outcome);
    expect(service['removeFakeOutcomes']).toHaveBeenCalled();
    expect(service.storedData.outcomesIndex[outcome.id]).toBe(event.id);
    expect(pubSubService.publish).toHaveBeenCalledWith(
      'UPDATE_OUTCOMES_FOR_MARKET', event.markets[0]
    );
  });

  it('storeNewOutcome (no event)', () => {
    service['storedData'].event.data = [];
    expect(service['storeNewOutcome']({} as any)).toBeFalsy();
  });

  it('removeFakeOutcomes', () => {
    const outcomes: any[] = [
      {}, { fakeOutcome: true }
    ];
    expect(service['removeFakeOutcomes'](outcomes).length).toBe(1);
  });

  describe('extendHandicapOutcome', () => {
    it('when outcomeMeaningMinorCode is string', () => {
      const handicapMarket: any = {
        handicapValues: ['V1'],
        marketMeaningMinorCode: 'abc'
      };
      const handicapOutcome: any = {
        outcomeMeaningMinorCode: '0',
        prices: [{}]
      };

      service['extendHandicapOutcome'](handicapMarket, handicapOutcome);

      expect(handicapOutcome.prices[0].handicapValueDec).toBe('V1,');
      expect(handicapOutcome.outcomeMeaningMajorCode).toBe(handicapMarket.marketMeaningMinorCode);
    });

    it('when outcomeMeaningMinorCode is number', () => {
      const handicapMarket: any = { handicapValues: ['V1'], marketMeaningMinorCode: 'abc' };
      const handicapOutcome: any = { outcomeMeaningMinorCode: 0, prices: [{}] };
      service['extendHandicapOutcome'](handicapMarket, handicapOutcome);
      expect(handicapOutcome.prices[0].handicapValueDec).toBe('V1,');
      expect(handicapOutcome.outcomeMeaningMajorCode).toBe(handicapMarket.marketMeaningMinorCode);
    });

    it('when outcomeMeaningMinorCode is []string', () => {
      const handicapMarket: any = { handicapValues: ['V1'], marketMeaningMinorCode: 'abc' };
      const handicapOutcome: any = { outcomeMeaningMinorCode: ['0'], prices: [{}] };
      service['extendHandicapOutcome'](handicapMarket, handicapOutcome);
      expect(handicapOutcome.prices[0].handicapValueDec).toBe('V1,');
      expect(handicapOutcome.outcomeMeaningMajorCode).toBe(handicapMarket.marketMeaningMinorCode);
    });
  });

  describe('storeNewOutcomes', () => {
    it('market with outcomes', () => {
      service.storedData.event.data = [{
        markets: [{
          outcomes: [{}]
        }]
      }] as any;
      service.storeNewOutcomes([{}] as any);
      expect(pubSubService.publish).toHaveBeenCalledTimes(1);
    });

    it('market without outcomes', () => {
      service.storedData.event.data = [{
        markets: [{}]
      }] as any;
      service.storeNewOutcomes([{}] as any);
      expect(pubSubService.publish).toHaveBeenCalledTimes(1);
    });
  });
});

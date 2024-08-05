import { of as observableOf } from 'rxjs';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';

describe('UkToteService', () => {
  let ukToteService: UkToteService;

  let siteServerPoolService, siteServerService, sbFilter, ukToteEventsLinkingService, routingHelperService, locale;
  const eventEntityTest: any = {
    cashoutAvail: 'cashoutAvail',
    categoryCode: 'categoryCode',
    externalKeys: {
      OBEvLinkScoop6: '1',
      OBEvLinkNonTote: '2'
    },
    poolTypes: ['poolType1', 'poolType2']
  };

  beforeEach(() => {
    siteServerPoolService = {
      getPoolsForEvent: jasmine.createSpy('getPoolsForEvent').and.returnValue(observableOf([])),
      getPoolToPoolValue: jasmine.createSpy('getPoolToPoolValue').and.returnValue(observableOf([]))
    };

    siteServerService = {
      getEventsByMarkets: jasmine.createSpy('getEventsByMarkets'),
      getEvent: jasmine.createSpy('getEvent'),
      getEventsToMarketsByEvents: jasmine.createSpy('getEventsToMarketsByEvents')
    };

    sbFilter = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities')
    };

    ukToteEventsLinkingService = {
      extendToteEvents: jasmine.createSpy('extendToteEvents'),
      extendToteEventInfo: jasmine.createSpy('extendToteEventInfo')
    };

    routingHelperService = {
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl')
    };

    locale = {
      getString: jasmine.createSpy('getString')
    };

    ukToteService = new UkToteService(siteServerPoolService, siteServerService, sbFilter, ukToteEventsLinkingService,
      routingHelperService, locale);
  });

  it('Tests if UkToteService Service Created', () => {
    expect(ukToteService).toBeTruthy();
  });

  it('#getPoolsForEvent', () => {
    ukToteService.getPoolsForEvent({});

    expect(siteServerPoolService.getPoolsForEvent).toHaveBeenCalled();
  });

  it('#getGuidesData', () => {
    ukToteService.getGuidesData({});

    expect(siteServerPoolService.getPoolToPoolValue).toHaveBeenCalled();
  });

  it('#loadEventsByMarketIds', () => {
    ukToteService.loadEventsByMarketIds([]);

    expect(siteServerService.getEventsByMarkets).toHaveBeenCalled();
  });

  it('#loadEventsByEventIds', () => {
    ukToteService.loadEventsByEventIds(['1', '2', '3']);

    expect(siteServerService.getEvent).toHaveBeenCalledWith('1,2,3', { racingFormOutcome: true }, false);
  });

  describe('addAvailablePoolTypes', () => {
    it('toteEvents and pools', (done) => {
      const events = [{ id: '3241' }] as any;
      const toteEvents = [];
      const pools = [];
      const toteEventIds = ['3241'];
      siteServerService.getEventsToMarketsByEvents = jasmine.createSpy().and.returnValue(Promise.resolve(toteEvents));
      siteServerPoolService.getPoolsForEvent = jasmine.createSpy().and.returnValue(observableOf(pools));
      ukToteService.getTotePoolEventIds = jasmine.createSpy().and.callFake(event => event.id);
      ukToteService['mapEventsWithPoolTypes'] = jasmine.createSpy();
      ukToteService.addAvailablePoolTypes(events).then((data) => {
        expect(siteServerService.getEventsToMarketsByEvents).toHaveBeenCalledWith(toteEventIds);
        expect(siteServerPoolService.getPoolsForEvent).toHaveBeenCalledWith({
          eventsIds: toteEventIds,
          poolTypes: 'UPLP,UQDP,UJKP,USC6,UPP7'
        });
        expect(ukToteService['mapEventsWithPoolTypes']).toHaveBeenCalledWith(events, toteEvents, pools);
        expect(data).toBe(events);
        done();
      });
    });

    it('toteEvents and no pools', (done) => {
      const events = [{ id: '3241' }] as any;
      const toteEvents = [];
      const toteEventIds = ['3241'];
      siteServerService.getEventsToMarketsByEvents = jasmine.createSpy().and.returnValue(Promise.resolve(toteEvents));
      siteServerPoolService.getPoolsForEvent = jasmine.createSpy().and.returnValue(observableOf(null));
      ukToteService.getTotePoolEventIds = jasmine.createSpy().and.callFake(event => event.id);
      ukToteService['mapEventsWithPoolTypes'] = jasmine.createSpy();
      ukToteService.addAvailablePoolTypes(events).then((data) => {
        expect(siteServerService.getEventsToMarketsByEvents).toHaveBeenCalledWith(toteEventIds);
        expect(siteServerPoolService.getPoolsForEvent).toHaveBeenCalledWith({
          eventsIds: toteEventIds,
          poolTypes: 'UPLP,UQDP,UJKP,USC6,UPP7'
        });
        expect(ukToteService['mapEventsWithPoolTypes']).not.toHaveBeenCalled();
        expect(data).toBe(events);
        done();
      });
    });

    it('pools and no toteEvents', (done) => {
      const events = [{ id: '3241' }] as any;
      const pools = [];
      const toteEventIds = ['3241'];
      siteServerService.getEventsToMarketsByEvents = jasmine.createSpy().and.returnValue(Promise.resolve(null));
      siteServerPoolService.getPoolsForEvent = jasmine.createSpy().and.returnValue(observableOf(pools));
      ukToteService.getTotePoolEventIds = jasmine.createSpy().and.callFake(event => event.id);
      ukToteService['mapEventsWithPoolTypes'] = jasmine.createSpy();
      ukToteService.addAvailablePoolTypes(events).then((data) => {
        expect(siteServerService.getEventsToMarketsByEvents).toHaveBeenCalledWith(toteEventIds);
        expect(siteServerPoolService.getPoolsForEvent).toHaveBeenCalledWith({
          eventsIds: toteEventIds,
          poolTypes: 'UPLP,UQDP,UJKP,USC6,UPP7'
        });
        expect(ukToteService['mapEventsWithPoolTypes']).not.toHaveBeenCalled();
        expect(data).toBe(events);
        done();
      });
    });
  });

  it('#getTotePoolEventIds when there is no eventEntity', () => {
    const actualResult = ukToteService.getTotePoolEventIds({} as ISportEvent);

    expect(actualResult).toEqual([]);
  });

  it('#getTotePoolEventIds when there is eventEntity and it has externalKeys', () => {
    const actualResult = ukToteService.getTotePoolEventIds(eventEntityTest);

    expect(actualResult).toEqual(['1']);
  });

  it('getPoolIndicators', () => {
    const events = [
      {
        isStarted: false,
        isResulted: false,
        isFinished: false,
        poolTypes: ['UWIN'],
        startTime: '10',
        id: '1'
      },
      {
        isStarted: false,
        isResulted: false,
        isFinished: false,
        poolTypes: ['UWIN', 'UPLC'],
        startTime: '8',
        id: '2'
      },
      {
        isStarted: false,
        isResulted: false,
        isFinished: false,
        poolTypes: ['UWIN'],
        startTime: '6',
        id: '3'
      },
      {
        isStarted: true,
        isResulted: false,
        isFinished: false,
        poolTypes: ['UWIN'],
        startTime: '10',
        id: '4'
      },
      {
        isStarted: false,
        isResulted: true,
        isFinished: false,
        poolTypes: ['UWIN'],
        startTime: '10',
        id: '5'
      },
      {
        isStarted: false,
        isResulted: false,
        isFinished: true,
        poolTypes: ['UWIN'],
        startTime: '10',
        id: '6'
      }
    ] as any;
    const expectedResult = [
      {
        id: '1',
        startTime: '10',
        poolType: 'uktote.UWIN',
        link: '/totepool/win'
      },
      {
        id: '2',
        startTime: '8',
        poolType: 'uktote.UPLC',
        link: '/totepool/place'
      }
    ] as any;
    locale.getString = jasmine.createSpy().and.callFake((str) => str);
    ukToteService['generateLinkToEvent'] = jasmine.createSpy().and.returnValue('');
    const result = ukToteService.getPoolIndicators(events);
    expect(locale.getString).toHaveBeenCalledTimes(2);
    expect(ukToteService['generateLinkToEvent']).toHaveBeenCalledTimes(2);
    expect(result).toEqual(expectedResult);
  });

  it('#isOutcomeSuspended when outcome has suspended status', () => {
    const actualResult = ukToteService.isOutcomeSuspended({outcomeStatusCode: 'S'} as IOutcome);

    expect(actualResult).toEqual(true);
  });

  it('#isOutcomeSuspended when outcome has not suspended status', () => {
    const actualResult = ukToteService.isOutcomeSuspended({outcomeStatusCode: 'test'} as IOutcome);

    expect(actualResult).toEqual(false);
  });

  it('#isEventSuspended when event has suspended status', () => {
    const actualResult = ukToteService.isEventSuspended({eventStatusCode: 'S'} as ISportEvent);

    expect(actualResult).toEqual(true);
  });

  it('#isEventSuspended when event has not suspended status', () => {
    const actualResult = ukToteService.isEventSuspended({eventStatusCode: 'test'} as ISportEvent);

    expect(actualResult).toEqual(false);
  });

  it('#isMarketSuspended when market of provided event has suspended status', () => {
    const actualResult = ukToteService.isMarketSuspended({
      markets: [{ marketStatusCode: 'S' }]
    } as ISportEvent);

    expect(actualResult).toEqual(true);
  });

  it('#isMarketSuspended when market of provided event has not suspended status', () => {
    const actualResult = ukToteService.isMarketSuspended({
      markets: [{ marketStatusCode: 'test' }]
    } as ISportEvent);

    expect(actualResult).toEqual(false);
  });

  it('#isMultipleLegsToteBet when bet is multiple legs tote bet', () => {
    const actualResult = ukToteService.isMultipleLegsToteBet('UPLP');

    expect(actualResult).toEqual(true);
  });

  it('#isMultipleLegsToteBet when bet is not multiple legs tote bet', () => {
    const actualResult = ukToteService.isMultipleLegsToteBet('test');

    expect(actualResult).toEqual(false);
  });

  describe('#sortOutcomes', () => {
    const outcomes = [
      { outcomeMeaningMinorCode: 1 },
      { outcomeMeaningMinorCode: 0 }] as any;

    it('should exclude favourites', () => {
      const extendedOutcomes = [
        {
          outcomeMeaningMinorCode: 0,
          isFavourite: false
        }
      ];
      ukToteService.sortOutcomes(outcomes, true);

      expect(sbFilter.orderOutcomeEntities).toHaveBeenCalledWith(extendedOutcomes, false, true, true);
    });

    it('should not exclude favourites', () => {
      const extendedOutcomes = [
        {
          outcomeMeaningMinorCode: 1,
          isFavourite: true
        },
        {
          outcomeMeaningMinorCode: 0,
          isFavourite: false
        }
      ];
      ukToteService.sortOutcomes(outcomes, false);

      expect(sbFilter.orderOutcomeEntities).toHaveBeenCalledWith(extendedOutcomes, false, true, true);
    });
  });

  it('#extendToteEvents', () => {
    ukToteService.extendToteEvents([], true);

    expect(ukToteEventsLinkingService.extendToteEvents).toHaveBeenCalledWith([], true, jasmine.any(Object));
  });

  it('#extendToteEventInfo', () => {
    ukToteService.extendToteEventInfo({} as ISportEvent, {} as ISportEvent);

    expect(ukToteEventsLinkingService.extendToteEventInfo).toHaveBeenCalledWith({}, {}, jasmine.any(Object));
  });

  it('#getRaceTitle when there is no event', () => {
    const actualResult = ukToteService.getRaceTitle(null as ISportEvent);

    expect(actualResult).toEqual('');
  });

  it('#getRaceTitle when there is event', () => {
    const actualResult = ukToteService.getRaceTitle({localTime: 'localTime', typeName: 'typeName'} as ISportEvent);

    expect(actualResult).toEqual('localTime typeName');
  });

  describe('#getAllIdsForEvents', () => {
    const eventEntities = [
      {
        markets: [{
          name: 'market1',
          linkedMarketId: 'linkedMarketId1',
          outcomes: [{
            linkedOutcomeId: 'linkedOutcomeId1'
          }]
        }],
        linkedEventId: 'linkedEventId1'
      },
      {
        markets: [{
          name: 'market2',
          linkedMarketId: 'linkedMarketId2',
          outcomes: [{
            linkedOutcomeId: 'linkedOutcomeId2'
          }]
        }],
        linkedEventId: 'linkedEventId2'
      }
    ] as any;

    it('check markets ids', () => {
      const expectedMarketsIds = ['linkedMarketId1', 'linkedMarketId2'];
      const actualResult = ukToteService.getAllIdsForEvents(eventEntities);

      expect(actualResult['market']).toEqual(expectedMarketsIds);
    });

    it('check events ids', () => {
      const expectedEventIds = ['linkedEventId1', 'linkedEventId2'] as any;
      const actualResult = ukToteService.getAllIdsForEvents(eventEntities);

      expect(actualResult['event']).toEqual(expectedEventIds);
    });

    it('check outcomes ids', () => {
      const expectedOutcomesIds = ['linkedOutcomeId1', 'linkedOutcomeId2'];
      const actualResult = ukToteService.getAllIdsForEvents(eventEntities);

      expect(actualResult['outcome']).toEqual(expectedOutcomesIds);
    });
  });

  it('extendEvent', () => {
    const mainEvent = {} as any;
    const extendingEvent = {
      id: '3422',
      eventStatusCode: 'A',
      isResulted: false,
      localTime: '874379',
      typeName: 'typeName',
      isUKorIRE: true
    } as any;
    const expectedEvent = {
      linkedEventId: extendingEvent.id,
      eventStatusCode: extendingEvent.eventStatusCode,
      isResulted: extendingEvent.isResulted,
      localTime: extendingEvent.localTime,
      typeName: extendingEvent.typeName,
      isUKorIRE: extendingEvent.isUKorIRE
    } as any;
    ukToteService['extendEvent'](mainEvent, extendingEvent);
    expect(mainEvent).toEqual(expectedEvent);
  });

  it('extendMarket', () => {
    const mainMarket = {} as any;
    const extendingMarket = {
      id: '324',
      marketStatusCode: 'A'
    } as any;
    const expectedMarket = {
      linkedMarketId: extendingMarket.id,
      marketStatusCode: extendingMarket.marketStatusCode
    } as any;
    ukToteService['extendMarket'](mainMarket, extendingMarket);
    expect(mainMarket).toEqual(expectedMarket);
  });

  describe('normalizeRunnerName', () => {
    it('should normalize runner name if it is in Upper Case', () => {
      const outcome: any = {
        name: 'LUNAR TUNES'
      } as any;
      ukToteService['normalizeRunnerName'](outcome);
      expect(outcome.name).toEqual('Lunar Tunes');
    });

    it('should normalize non runner name if it is in Upper Case', () => {
      const outcome: any = {
        name: 'LUNAR TUNES N/R'
      } as any;
      ukToteService['normalizeRunnerName'](outcome);
      expect(outcome.name).toEqual('Lunar Tunes N/R');
    });

    it('shouldn\'t change runner name if it not in upper case', () => {
      const outcome: any = {
        name: 'Lunar Tunes'
      } as any;
      ukToteService['normalizeRunnerName']({
        name: 'Lunar Tunes'
      } as any);
      expect(outcome.name).toEqual('Lunar Tunes');
    });
    it('should pass edge cases without errors', () => {
      ukToteService['normalizeRunnerName'](undefined);
      ukToteService['normalizeRunnerName']({} as any);
    });
  });

  it('extendOutcome', () => {
    const mainOutcome: any = {};
    const extendingOutcome: any = {
      id: '32423',
      outcomeStatusCode: 'code'
    };
    const expectedOutcome: any = {
      linkedOutcomeId: extendingOutcome.id,
      outcomeStatusCode: extendingOutcome.outcomeStatusCode
    };
    ukToteService['normalizeRunnerName'] = jasmine.createSpy('normalizeRunnerName');
    ukToteService['markNonRunners'] = jasmine.createSpy();
    ukToteService['extendOutcome'](mainOutcome, extendingOutcome);

    expect(ukToteService['normalizeRunnerName']).toHaveBeenCalledWith(mainOutcome);
    expect(ukToteService['markNonRunners']).toHaveBeenCalledWith(mainOutcome, extendingOutcome);
    expect(mainOutcome).toEqual(expectedOutcome);
  });

  it('extendOutcome no extendingOutcome', () => {
    const mainOutcome: any = {};
    const extendingOutcome = null;
    ukToteService['normalizeRunnerName'] = jasmine.createSpy();
    ukToteService['markNonRunners'] = jasmine.createSpy();
    ukToteService['extendOutcome'](mainOutcome, extendingOutcome);
    expect(ukToteService['normalizeRunnerName']).not.toHaveBeenCalled();
    expect(ukToteService['markNonRunners']).not.toHaveBeenCalled();
  });

  it('extendOutcome with racingFormOutcome', () => {
    const mainOutcome: any = {};
    const extendingOutcome: any = {
      id: '32423',
      outcomeStatusCode: 'code',
      racingFormOutcome: 'racingFormOutcome'
    };
    const expectedOutcome: any = {
      linkedOutcomeId: extendingOutcome.id,
      outcomeStatusCode: extendingOutcome.outcomeStatusCode,
      racingFormOutcome: extendingOutcome.racingFormOutcome
    };
    ukToteService['normalizeRunnerName'] = jasmine.createSpy();
    ukToteService['markNonRunners'] = jasmine.createSpy();
    ukToteService['extendOutcome'](mainOutcome, extendingOutcome);

    expect(ukToteService['normalizeRunnerName']).toHaveBeenCalledWith(mainOutcome);
    expect(ukToteService['markNonRunners']).toHaveBeenCalledWith(mainOutcome, extendingOutcome);
    expect(mainOutcome).toEqual(expectedOutcome);
  });

  describe('markNonRunners', () => {
    it('name does not matche RegExp', () => {
      const outcome = {} as any;
      const extendingOutcomeMatch = { name: 'NR' };
      ukToteService['markNonRunners'](outcome, extendingOutcomeMatch);
      expect(outcome).toEqual({});
    });

    it('name matches RegExp', () => {
      const outcome = {
        name: '  name N/R'
      } as any;
      const extendingOutcomeMatch = { name: 'N/R' };
      const expectedOutcome = {
        name: 'name N/R',
        nonRunner: true
      } as any;
      ukToteService['markNonRunners'](outcome, extendingOutcomeMatch);
      expect(outcome).toEqual(expectedOutcome);
    });
  });

  it('generateLinkToEvent', () => {
    const link = 'link';
    const event = {} as any;
    routingHelperService.formResultedEdpUrl = jasmine.createSpy().and.returnValue(link);
    const result = ukToteService['generateLinkToEvent'](event);
    expect(result).toBe(link);
    expect(routingHelperService.formResultedEdpUrl).toHaveBeenCalledWith(event);
  });

  it('mapEventsWithPoolTypes', () => {
    const events = [
      {
        id: '0921',
        poolTypes: ['poolType4']
      },
      {
        id: '2376',
        poolTypes: null
      },
      {
        id: '1421',
        poolTypes: []
      }
    ] as any;
    const toteEvents = [
      {
        markets: null
      },
      {
        markets: []
      },
      {
        markets: [null]
      },
      {
        markets: [{}]
      },
      {
        id: '0921',
        markets: [{ id: '8279' }]
      },
      {
        id: '2376',
        markets: [{ id: '3242' }]
      }
    ] as any;
    const pools = [
      {
        marketIds: ['8279'],
        type: 'poolType1'
      },
      {
        marketIds: ['3242', '8279'],
        type: 'poolType2'
      }
    ] as any;
    const updatedEvents = [
      {
        id: '0921',
        poolTypes: [ 'poolType4', 'poolType1', 'poolType2' ]
      },
      {
        id: '2376',
        poolTypes: ['poolType2']
      },
      {
        id: '1421',
        poolTypes: []
      }
    ] as any;
    ukToteService['getTotePoolEventIds'] = jasmine.createSpy().and.callFake((event) => [event.id]);
    ukToteService['mapEventsWithPoolTypes'](events, toteEvents, pools);
    expect(ukToteService['getTotePoolEventIds']).toHaveBeenCalledTimes(3);
    expect(events).toEqual(updatedEvents);
  });
});

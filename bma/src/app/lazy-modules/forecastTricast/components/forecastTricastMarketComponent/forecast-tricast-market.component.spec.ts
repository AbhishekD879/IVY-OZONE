import {
  ForecastTricastMarketComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastMarketComponent/forecast-tricast-market.component';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('ForecastTricastMarketComponent', () => {
  let component: ForecastTricastMarketComponent;
  let locale;
  let betBuilderService;
  let pubSubService;
  let ukTotesHandleLiveServeUpdatesService;
  let ukToteLiveUpdatesService;
  let ukToteService;
  let gtmService;
  const outcomeObj = [
    { id:'1450161413' },
    { id:'1450161403' }
  ];
  const eventObj = {
    categoryId: 16,
    id: 0,
    localTime: '13:55',
    originalName: '13:55 Exeter',
    typeId: 34404
  }

  beforeEach(() => {
    const data = 
      {bets:[{storeId: 'FORECAST_COM|1450161413|1450161403'},{betComplexName: 'FORECAST'}]};
    locale = {
      getString: jasmine.createSpy().and.returnValue('Please add another selection')
    };
    betBuilderService = {
      clear: jasmine.createSpy()
    };
    pubSubService = {
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb(data)),
      API: pubSubApi,
      publish: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    ukTotesHandleLiveServeUpdatesService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy()
    };
    ukToteLiveUpdatesService = {
      getAllChannels: jasmine.createSpy().and.returnValue([]),
      updateEventWithLiveUpdate: jasmine.createSpy()
    };
    ukToteService = {
      getAllIdsForEvents: jasmine.createSpy()
    };
    gtmService = {
      push: jasmine.createSpy('push'),
    };

    createComponent();
  });

  function createComponent() {
    component = new ForecastTricastMarketComponent(
      locale,
      betBuilderService,
      ukTotesHandleLiveServeUpdatesService,
      ukToteLiveUpdatesService,
      ukToteService,
      pubSubService,
      gtmService
    );
  }

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    spyOn<any>(component as any, 'setBetProperties');
    spyOn<any>(component as any, 'getBetBuilderWarning').and.returnValue(null);
    spyOn<any>(component as any, 'updateEvent').and.returnValue({});
    spyOn<any>(component as any, 'setMarketDescriptionClass');
    component.selectedPoolType = 'Forecast';
    component.event = {} as any;
    component.marketEntity = {
      outcomes: []
    } as any;
    component.ngOnInit();

    expect(ukToteService.getAllIdsForEvents).toHaveBeenCalledWith([component.event]);
    expect(ukToteLiveUpdatesService.getAllChannels).toHaveBeenCalled();
    expect(ukTotesHandleLiveServeUpdatesService.subscribe).toHaveBeenCalledWith([], jasmine.any(Function));

    expect(component.betFilter).toEqual('FC');
    expect(component['setBetProperties']).toHaveBeenCalledWith('FC');
    expect(component.betBuilderMsg.warning).toEqual(null);
  });
  it('ngOnChanges', () => {
    spyOn<any>(component as any, 'updateFCTCmarkets').and.callThrough();
    component.marketEntity = {
      fcMktAvailable: 'Y',
      tcMktAvailable: 'Y'
    } as any;
    component.event = {
      id: 555
    } as any;
    component.ngOnChanges(
      {
        delta: {
          currentValue: {
            updateEventId:'555',
            fcMktAvailable: 'N',
            tcMktAvailable: 'N'
          }
        }
      } as any);
    expect(component.marketEntity.fcMktAvailable).toBe('N');
    expect(component.marketEntity.tcMktAvailable).toBe('N');
  });
  it('ngOnDestroy', () => {
    component.channels = [];
    component.ngOnDestroy();
    expect(ukTotesHandleLiveServeUpdatesService.unsubscribe).toHaveBeenCalledWith([]);
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  });

  it('isSuspended', () => {
    component.event = {
      eventStatusCode: 'S',
    } as any;
    component.marketEntity = {
      marketStatusCode: 'S',
    } as any;
    expect(component.isSuspended({} as any)).toBeTruthy();
    component.event.eventStatusCode = 'A';
    expect(component.isSuspended({} as any)).toBeTruthy();
    component.marketEntity.marketStatusCode = 'A';
    expect(component.isSuspended({ outcomeStatusCode: 'S' } as any)).toBeTruthy();
    expect(component.isSuspended({ outcomeStatusCode: 'A' } as any)).toBeFalsy();
    component.betFilter = 'FC';
    component.marketEntity.fcMktAvailable = 'Y';
    expect(component.isSuspended({ outcomeStatusCode: 'A' } as any)).toBeFalsy();
    component.betFilter = 'TC';
    component.marketEntity.tcMktAvailable = 'N';
    expect(component.isSuspended({ outcomeStatusCode: 'A' } as any)).toBeTruthy();
  });

  it('trackByOutcomes', () => {
    const outcome = {
      isDisplayed: true,
      id: '532178415',
      name: 'Decadent',
      marketId: '142153564'
    } as any;

    expect(component.trackByOutcomes(0, outcome)).toEqual('0true532178415Decadent142153564');
  });

  it('onMapUpdate', () => {
    component.betFilter = 'FC';
    spyOn<any>(component as any, 'checkMap');
    const map = {
      532178415: {
        '1st': 'checked',
        '2nd': 'disabled',
        'any': 'disabled'
      },
      532178416: {
        '1st': 'disabled',
        '2nd': 'disabled',
        'any': 'disabled'
      }
    } as any;
    component.onMapUpdate(map);

    expect(component.betBuilderMsg.warning).toEqual('Please add another selection');
    expect(component['checkMap']).toHaveBeenCalledWith(1);
  });

  it('addToBetslip', () => {
    const outcomes = [
      { id:'1450161413' },
      { id:'1450161403' }
    ];    
    component['getCastType'] = jasmine.createSpy().and.returnValue('FORECAST_COM');
    component['getCheckedOutcomes'] = jasmine.createSpy().and.returnValue(outcomes);
    component['sendGTMData'] = jasmine.createSpy();
    component['resetMap'] = jasmine.createSpy();
    component.event = {localTime: "12:45"} as any;
    component.addToBetslip();

    expect(component['getCastType']).toHaveBeenCalledTimes(1);
    expect(component['getCheckedOutcomes']).toHaveBeenCalledTimes(1);
    expect(pubSubService.publish).toHaveBeenCalledTimes(1);
    expect(pubSubService.subscribe).toHaveBeenCalledTimes(1);
    expect(component['sendGTMData']).toHaveBeenCalled();
    expect(component['resetMap']).toHaveBeenCalledTimes(1);
  });

  it('should set the brandName', () => {
    spyOn<any>(component as any, 'sendGTMData');
    const outcomes = [
      { id:'1450161413' },
      { id:'1450161403' }
    ];
    component['getCastType'] = jasmine.createSpy().and.returnValue('FORECAST_COM');
    component['getCheckedOutcomes'] = jasmine.createSpy().and.returnValue(outcomes);
    component.event = {localTime: "12:45"} as any;
    component.addToBetslip();
    expect(component['sendGTMData']).toHaveBeenCalled();
  });

  it('checkMap', () => {
    component.betFilter = 'FC';
    component['checkMap'](1);
    expect(component.isBetAvailable).toEqual(false);

    component['checkMap'](2);
    expect(component.isBetAvailable).toEqual(true);

    component['checkMap'](3);
    expect(component.isBetAvailable).toEqual(true);

    component.betFilter = 'TC';
    component['checkMap'](4);
    expect(component.isBetAvailable).toEqual(true);
  });

  it('prepareIdsForLiveUpdates', () => {
    const event = {
      id: 111,
      markets: [{
        id: 222,
        outcomes: [{
          id: 333
        }]
      }]
    } as any;
    component['prepareIdsForLiveUpdates'](event);

    expect(event.linkedEventId).toBe(111);
    expect(event.markets[0].linkedMarketId).toBe(222);
    expect(event.markets[0].outcomes[0].linkedOutcomeId).toBe(333);
  });

  it('updateEvent (status: A)', () => {
    spyOn<any>(component as any, 'resetMap');
    spyOn<any>(component as any, 'onMapUpdate');

    const liveUpdate = {
      id: 111,
      payload: {
        status: 'A'
      },
      type: 'sSELCN'
    } as any;

    component['updateEvent'](liveUpdate);

    expect(component['resetMap']).not.toHaveBeenCalled();
    expect(component['onMapUpdate']).not.toHaveBeenCalled();
  });

  it('updateEvent (status: S)', () => {
    spyOn<any>(component as any, 'resetMap');
    spyOn<any>(component as any, 'onMapUpdate');

    const liveUpdate = {
      id: 111,
      payload: {
        status: 'S'
      },
      type: 'sSELCN'
    } as any;

    component['updateEvent'](liveUpdate);

    expect(component['resetMap']).toHaveBeenCalled();
    expect(component['onMapUpdate']).toHaveBeenCalled();
  });

  describe('getBetBuilderWarning', () => {
    it ('should return warning if not enough selections selected for forecast', () => {
      component.betFilter = 'FC';
      component['getBetBuilderWarning'](1);

      expect(locale.getString).toHaveBeenCalledWith('racing.addSelection');
    });
    it ('should return warning if not enough selections selected for tricast', () => {
      component.betFilter = 'TR';
      component['getBetBuilderWarning'](2);

      expect(locale.getString).toHaveBeenCalledWith('racing.addSelection');
    });

    it ('should', () => {
      component.betFilter = 'TR';
      const actualResult = component['getBetBuilderWarning'](3);

      expect(locale.getString).not.toHaveBeenCalledWith('Please add another selection');
      expect(actualResult).toEqual(null);
    });
  });

  describe('getPoolCssClass', () => {
    it ('should return Execta class for forecast market', () => {
      component.betFilter = 'FC';
      expect(component['getPoolCssClass']()).toEqual('execta-pool');
    });
    it ('should return Trifecta class for tricast market', () => {
      component.betFilter = 'TC';
      expect(component['getPoolCssClass']()).toEqual('trifecta-pool');
    });
  });

  describe('@verifyPoolType', () => {
    it ('should return FC market', () => {
      expect(component['verifyPoolType']('Forecast')).toEqual('FC');
    });
    it ('should return TC market', () => {
      expect(component['verifyPoolType']('Tricast')).toEqual('TC');
    });
  });

  describe('@setBetProperties', () => {
    it ('it should set FC Market', () => {
      component['event'] = <any>{categoryId: '39'};
      component.marketEntity = {
        outcomes: [
          {id: '532178415'},
          {id: '532178416'}
        ]
      } as any;
      const checkboxesMap = {
        532178415: {
          '1st': 'open',
          '2nd': 'open',
          'any': 'open'
        },
        532178416: {
          '1st': 'open',
          '2nd': 'open',
          'any': 'open'
        }
      };
      component.isMultipleLegsToteBet = false;
      component['setBetProperties']('FC');

      expect(component.checkboxesMap).toEqual(checkboxesMap);
      expect(locale.getString).toHaveBeenCalledWith('racing.forTriMsg', { num: 'two'});
      expect(betBuilderService.clear).toHaveBeenCalledWith(null);
    });

    it ('it should set TC Market', () => {
      component['event'] = <any>{categoryId: '39'};
      component.marketEntity = undefined as any;
      component.isMultipleLegsToteBet = true;
      component['setBetProperties']('TC');

      expect(component.checkboxesMap).toEqual(undefined as any);
      expect(locale.getString).toHaveBeenCalledWith('racing.forTriMsg', { num: 'three'});
      expect(betBuilderService.clear).toHaveBeenCalledWith(null);
    });

    it ('it should not set Market if it is not correct ', () => {
      component['event'] = <any>{categoryId: '39'};
      component.marketEntity = undefined as any;
      component.isMultipleLegsToteBet = false;
      component['setBetProperties']('ST');

      expect(component.checkboxesMap).toEqual({} as any);
      expect(locale.getString).toHaveBeenCalled();
      expect(betBuilderService.clear).toHaveBeenCalledWith(null);
    });
  });

  it('getCastType', () => {
    component.selectedPoolType = 'Forecast';

    component.checkboxesMap = {
      'outcome1': { '1st': 'checked' }
    } as any;
    expect(component['getCastType']()).toBe('FORECAST');

    component.checkboxesMap = {
      'outcome1': { 'any': 'checked' }
    } as any;
    expect(component['getCastType']()).toBe('FORECAST_COM');
  });

  it('getCheckedOutcomes', () => {
    component['getOutcomesByPlace'] = jasmine.createSpy();
    component.outcomesMap = {
      'outcome1': {}, 'outcome2': {}
    } as any;
    component.checkboxesMap = {
      'outcome1': { '1st': 'checked' },
      'outcome2': { 'any': 'checked' }
    } as any;

    component['getCheckedOutcomes']('FORECAST');
    component['getCheckedOutcomes']('TRICAST');
    component['getCheckedOutcomes']('TRICAST_COM');

    expect(component['getOutcomesByPlace']).toHaveBeenCalledTimes(2);
  });

  it('getOutcomesByPlace', () => {
    component.checkboxesMap = {
      'outcome1': { '1st': 'checked' },
      'outcome2': { '1st': 'disabled' },
      'outcome3': { '2nd': 'checked' },
    } as any;
    component.outcomesMap = { 'outcome1': {}, 'outcome2': {}, 'outcome3': {} } as any;

    expect(
      component['getOutcomesByPlace'](['1st', '2nd'])
    ).toEqual([
      component.outcomesMap['outcome1'], component.outcomesMap['outcome2']
    ]);
  });

  it('sendGTMData for Forecast', () => {
    component['sendGTMData']('FORECAST', outcomeObj, eventObj);
    const type = 'FORECAST';
    expect(type).toBe('FORECAST');
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('sendGTMData for Tricast', () => {
    const type = 'TRICAST';
    component['sendGTMData']('TRICAST', outcomeObj, eventObj);
    expect(type).toBe('TRICAST');
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('sendGTMData for Forecast_com', () => {
    component['sendGTMData']('FORECAST_COM', outcomeObj, eventObj);
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('sendGTMData for Tricast_com', () => {
    component['sendGTMData']('TRICAST_COM', outcomeObj, eventObj);
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('resetMap', () => {
    component.checkboxesMap = {
      '111': { '1st': 'checked', '2nd': 'disabled', 'any': 'disabled' },
      '222': { '1st': 'disabled', '2nd': 'checked', 'any': 'disabled' },
      '333': { '1st': 'disabled', '2nd': 'disabled', 'any': 'open' }
    } as any;

    component['resetMap']();

    expect(component.checkboxesMap).toEqual({
      '111': { '1st': 'open', '2nd': 'open', 'any': 'open' },
      '222': { '1st': 'open', '2nd': 'open', 'any': 'open' },
      '333': { '1st': 'open', '2nd': 'open', 'any': 'open' }
    });
  });

  describe('@sortMarketOutcomes', () => {
    it('it should sort outcomes by runnerNumber', () => {
      component.event = <any>{
        categoryCode: 'HORSES'
      };
      component.marketEntity = {
        outcomes: [
          { runnerNumber: 2, name: 'A' },
          { runnerNumber: 1, name: 'B' },
          { runnerNumber: 3, name: 'C' }]
      } as any;

      component['sortMarketOutcomes']();
      expect(component.outcomes).toEqual([
        { runnerNumber: 1, name: 'B' },
        { runnerNumber: 2, name: 'A' },
        { runnerNumber: 3, name: 'C' }] as any);
    });

    it('it should sort outcomes by trapNumber', () => {
      component.event = <any>{
        categoryCode: 'GREYHOUNDS'
      };
      component.marketEntity = {
        outcomes: [
          { trapNumber: 2, name: 'A' },
          { trapNumber: 1, name: 'B' },
          { trapNumber: 3, name: 'C' }]
      } as any;

      component['sortMarketOutcomes']();
      expect(component.outcomes).toEqual([
        { trapNumber: 1, name: 'B' },
        { trapNumber: 2, name: 'A' },
        { trapNumber: 3, name: 'C' }] as any);
    });

    it('it should sort outcomes by displayOrder', () => {
      component.event = <any>{
        categoryCode: 'HORSES'
      };
      component.marketEntity = {
        outcomes: [
          { displayOrder: 2, name: 'A' },
          { displayOrder: 1, name: 'C' },
          { displayOrder: 3, name: 'B' }]
      } as any;

      component['sortMarketOutcomes']();
      expect(component.outcomes).toEqual([
        { displayOrder: 1, name: 'C' },
        { displayOrder: 2, name: 'A' },
        { displayOrder: 3, name: 'B' }] as any);
    });

    it('it should sort outcomes by name', () => {
      component.event = <any>{
        categoryCode: 'HORSES'
      };
      component.marketEntity = {
        outcomes: [
          { displayOrder: 0, name: 'C' },
          { displayOrder: 0, name: 'A' },
          { displayOrder: 0, name: 'B' }]
      } as any;

      component['sortMarketOutcomes']();
      expect(component.outcomes).toEqual([
        { displayOrder: 0, name: 'A' },
        { displayOrder: 0, name: 'B' },
        { displayOrder: 0, name: 'C' }] as any);
    });
  });

  describe('#setMarketDescriptionClass', () => {
    it ('should add class, if marketDescription is enabled', () => {
      component.event = {
        sortedMarkets: [
          {
            label: 'Forecast',
            description: 'Welcome'
          }
        ]
      } as any;
      component.isMarketDescriptionEnabled = true;
      component.selectedPoolType = 'Forecast';
      component['setMarketDescriptionClass']();
      expect(component.marketDescriptionClass).toBe('has-market-description');
    });
    it ('should not add class, if marketDescription is not available', () => {
      component.event = {
        sortedMarkets: [
          {
            label: 'Tricast',
            description: ''
          }
        ]
      } as any;
      component.selectedPoolType = 'Tricast';
      component.isMarketDescriptionEnabled = true;
      component['setMarketDescriptionClass']();
      expect(component.marketDescriptionClass).toBe('');
    });
  });
});

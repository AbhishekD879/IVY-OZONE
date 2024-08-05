import { of as observableOf } from 'rxjs';
import {
  CompetitionOutrightsComponent
} from '@app/bigCompetitions/components/competitionOutrights/competition-outrights.component';
import {
  ICompetitionMarket,
  ICompetitionModules
} from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('CompetitionOutrightsComponent', () => {

  let component: CompetitionOutrightsComponent;

  let pubsubService;
  let liveUpdatesService;
  let bigCompetitionsFactory;

  let moduleConfig;

  beforeEach(() => {
    moduleConfig = {
      id: 'id',
      type: 'type',
      name: 'name',
      maxDisplay: 10,
      viewType: 'card',
      markets: [
        {
          collapsed: false,
          marketId: '1',
          maxDisplay: 5,
          nameOverride: '',
          viewType: 'card',
          data: {
            id: '5',
            markets: [
              {
                outcomes: [{}, null, {}]
              }
            ]
          }
        },
        {
          collapsed: true,
          marketId: '2',
          maxDisplay: 7,
          nameOverride: '',
          viewType: 'list',
          data: {
            id: '7',
            markets: [
              {
                outcomes: [null, {}]
              }
            ]
          }
        }
      ],
      results: []
    };

    pubsubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((arg1, arg2, callback) => callback()),
      unsubscribe: jasmine.createSpy()
    };
    liveUpdatesService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy()
    };
    bigCompetitionsFactory = {
      getModule: jasmine.createSpy().and.returnValue(observableOf(moduleConfig))
    };

    component = new CompetitionOutrightsComponent(
      pubsubService,
      liveUpdatesService,
      bigCompetitionsFactory
    );
    component.moduleConfig = moduleConfig;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.ngOnInit();

    expect(pubsubService.subscribe)
    .toHaveBeenCalledWith(`OutrightCtrl${component.id}`, pubsubService.API.DELETE_MARKET_FROM_CACHE, jasmine.any(Function));

    expect(pubsubService.subscribe.calls.allArgs()[1]).toEqual(
      [`OutrightCtrl${component.id}`, pubsubService.API.DELETE_EVENT_FROM_CACHE, jasmine.any(Function)]
    );

    expect(pubsubService.subscribe)
      .toHaveBeenCalledWith(`OutrightCtrl${component.id}`, pubsubService.API.SUSPENDED_EVENT, jasmine.any(Function));
  });

  describe('#ngAfterViewInit', () => {
    it('call ngAfterViewInit', () => {
      component['loadData'] = jasmine.createSpy();
      component['ngAfterViewInit']();
      expect(component['loadData']).toHaveBeenCalled();
    });
  });

  it('#ngOnDestroy', () => {
    component.id = 'id';
    component.ngOnDestroy();
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith(`OutrightCtrl${component.id}`);
  });

  it('should return correct result', () => {
    const item = { marketId: 'id' } as ICompetitionMarket;
    const index = 3;
    expect(component.trackByFn(index, item)).toBe('3id');
  });

  it('should call correct method', () => {
    const index = 5;
    component.loadIndexData = jasmine.createSpy();
    component.loadData(index);
    expect(component.loadIndexData).toHaveBeenCalledWith(index);
  });

  it('should call correct method and set property', () => {
    const events = [];
    component.isExpanded = true;
    component.getEvents = jasmine.createSpy().and.returnValue(events);
    component['unsubscribeOnExpand'] = jasmine.createSpy();
    component.loadData();
    expect(component.getEvents).toHaveBeenCalledWith(component.moduleConfig.markets);
    expect(component['unsubscribeOnExpand']).toHaveBeenCalledWith(events);
    expect(component.isExpanded).toBeFalsy();
  });

  it('should call correct method and set property', () => {
    const events = [];
    component.moduleConfig = { id: 'id' } as ICompetitionModules;
    component.isExpanded = false;
    component['subscribeOnExpand'] = jasmine.createSpy();
    component.getEvents = jasmine.createSpy().and.returnValue(events);
    component.loadData();
    expect(bigCompetitionsFactory.getModule).toHaveBeenCalledWith(component.moduleConfig.id);
    expect(component.moduleConfig.markets).toBe(moduleConfig.markets);
    expect(component.getEvents).toHaveBeenCalledWith(component.moduleConfig.markets);
    expect(component['subscribeOnExpand']).toHaveBeenCalledWith(events);
    expect(component.isExpanded).toBeTruthy();
    expect(component.loadingData).toEqual(false);
  });

  it('should return correct result', () => {
    const markets = [
      {
        collapsed: false,
        marketId: '1',
        maxDisplay: 5,
        nameOverride: '',
        viewType: 'card',
        data: {}
      },
      {
        collapsed: true,
        marketId: '2',
        maxDisplay: 7,
        nameOverride: '',
        viewType: 'list',
        data: {}
      }
    ];
    const events = component.getEvents(markets);
    expect(events.length).toBe(2);
    expect(events[0]).toBe(markets[0].data as ISportEvent);
    expect(events[1]).toBe(markets[1].data as ISportEvent);
  });

  it('should call correct methods and set properties', () => {
    const index = 0;
    component['unsubscribeOnExpand'] = jasmine.createSpy();
    component.loadIndexData(index);
    expect(component['unsubscribeOnExpand'])
      .toHaveBeenCalledWith(jasmine.arrayContaining([component.moduleConfig.markets[index].data]));
    expect(component.moduleConfig.markets[index].isExpanded).toBeFalsy();
  });

  it('should call correct methods and set properties', () => {
    const index = 0;
    moduleConfig.markets[index].isExpanded = false;
    component['subscribeOnExpand'] = jasmine.createSpy();
    component.loadIndexData(index);
    expect(component['subscribeOnExpand'])
      .toHaveBeenCalledWith(jasmine.arrayContaining([component.moduleConfig.markets[index].data]));
    expect(component.moduleConfig.markets[index].isExpanded).toBeTruthy();
  });

  it('should return correct result', () => {
    expect(component.checkForData()).toBe(3);
  });

  it('should return true', () => {
    const market = {
      collapsed: false,
      marketId: '1',
      maxDisplay: 5,
      nameOverride: '',
      viewType: 'card',
      data: {
        markets: [
          {
            id: '1',
            outcomes: [{}, null, {}]
          }
        ]
      }
    } as ICompetitionMarket;
    expect(component.checkForInnerData(market)).toBeTruthy();
  });

  it('should return undefined when markets is empty', () => {
    const market = {
      collapsed: false,
      marketId: '1',
      maxDisplay: 5,
      nameOverride: '',
      viewType: 'card',
      data: {
        markets: []
      }
    } as ICompetitionMarket;
    expect(component.checkForInnerData(market)).toBeUndefined();
  });

  it('should call correct method', () => {
    const events = [];
    component['subscribeOnExpand'](events);
    expect(liveUpdatesService.subscribe).toHaveBeenCalledWith(events);
  });

  it('should call correct method', () => {
    const events = [];
    component['unsubscribeOnExpand'](events);
    expect(liveUpdatesService.unsubscribe).toHaveBeenCalledWith(events);
  });

  describe('applyDelta', () => {
    it('should extend object and handle falsy markets data values', () => {
      const delta = { newProp: 'value' };
      const id = 5;

      component.moduleConfig.markets[1].data = null;
      component['applyDelta'](delta, id);

      expect(component.moduleConfig.markets[0].data['newProp']).toBe('value');
    });
  });

  it('should call getHeaderClass', () => {
    component.moduleConfig = {
      brand: {
        brand: 'Coral',
        device: 'Mobile'
      }
    } as any;
    expect(component.getHeaderClass()).toEqual('forced-chevron-up-and-styles');
    component.moduleConfig = {
      brand: {
        brand: 'Lads',
        device: 'Mobile'
      }
    } as any;
    expect(component.getHeaderClass()).toEqual('');
  });
});

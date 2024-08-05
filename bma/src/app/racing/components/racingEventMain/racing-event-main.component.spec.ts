import { of as observableOf, of, Subject } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { RacingEventMainComponent } from '@racing/components/racingEventMain/racing-event-main.component';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import {
  filteredEventsDataMock,
  sportEventMock
} from '@racing/components/racingEventMain/racing-event-main.component.mock';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('RacingEventMainComponent', () => {
  let component: RacingEventMainComponent;
  let router;
  let route;
  let timeService;
  let command;
  let nativeBridge;
  let deviceService;
  let routesDataSharingService;
  let windowRef;
  let horseRacingService;
  let greyhoundService;
  let routingState;
  let smartBoostsService;
  let cmsService;
  let nextRacesService;
  let eventService;
  let templateService;
  let extraPlaceService;
  let changeDetectorRef;
  let pubSubService;
  let unsavedEmaHandler;
  let routingHelperService;
  let eventVideoStreamProviderService;
  let sessionStorageService;

  const testStr = 'TestString';
  const wasPriceStub = 'TestWasPrice';
  const event = {
    cashoutAvail: 'cashoutAvail',
    categoryCode: 'categoryCode',
    categoryId: 'categoryId',
    categoryName: 'categoryName',
    displayOrder: 12,
    drilldownTagNames: 'drilldownTagNames',
    eventIsLive: false,
    eventSortCode: 'eventSortCode',
    eventStatusCode: 'eventStatusCode',
    id: 123
  };
  const navigationItems = [
    {
      flag: 'UK',
      data: [
        {
          meeting: 'meeting',
          events: event
        }
      ]
    }
  ] as any[];
  const sportEvents = [event];

  beforeEach(() => {
    templateService = {
      genTerms: jasmine.createSpy().and.returnValue('')
    };
    command = {
      API: commandApi
    };
    nativeBridge = {onEventDetailsStreamAvailable: jasmine.createSpy('onEventDetailsStreamAvailable')};
    windowRef = {
      document: {
      removeEventListener: jasmine.createSpy('removeEventListener'),
      addEventListener: jasmine.createSpy('addEventListener')
    }};
    router = {
      events: jasmine.createSpyObj(['subscribe', 'unsubscribe']),
      navigateByUrl: jasmine.createSpy('router.navigateByUrl')
    };
    extraPlaceService = {
      getEvents: jasmine.createSpy('getEvents').and.returnValue(Promise.resolve(sportEvents))
    };
    cmsService = { getSystemConfig: jasmine.createSpy().and.returnValue({ subscribe: () => {} }) };
    nextRacesService = { getNextRacesModuleConfig: jasmine.createSpy().and.returnValue({}) };
    eventService = {hrEventSubscription:{subscribe:jasmine.createSpy().and.returnValue(false), next:jasmine.createSpy('next')} , getNextEvents: jasmine.createSpy().and.returnValue( new Promise((resolve) =>  resolve([]) )) };

    route = {
      queryParams : new Subject(),
      params: observableOf({
        market: 'Win or Each Way',
        marketType: 'UEXA'
      }),
      snapshot: {
        params: { id: '1' },
        paramMap: { get: jasmine.createSpy() },
        queryParams: {}
      }
    };

    deviceService = {
      isDesktop: true
    };

    routingState = {
      getCurrentSegment: jasmine.createSpy().and.returnValue(''),
    };
    horseRacingService = {
      unSubscribeEDPForUpdates: jasmine.createSpy(),
      subscribeEDPForUpdates: jasmine.createSpy(),
      getTypeNamesEvents: jasmine.createSpy().and.returnValue(Promise.resolve(filteredEventsDataMock)),
      getAntepostEventsByFlag: jasmine.createSpy().and.returnValue(Promise.resolve(navigationItems)),
      getConfig: jasmine.createSpy().and.returnValue({ name: 'horseracing' }),
      getById: jasmine.createSpy().and.returnValue(Promise.resolve([{ id: '1' }])),
      getGeneralConfig: jasmine.createSpy().and.returnValue({ PRESIM_STOP_TRACK_INTERVAL: '' }),
      sortMarketsName: jasmine.createSpy()
        .and.returnValue({ typeName: testStr, markets: [{ outcomes: [{ name: '' }] }] as IMarket[] }),
      sortRacingMarketsByTabs: jasmine.createSpy().and.returnValue('123321123'),
      navMenuGroupEnhancedRaces: jasmine.createSpy().and.returnValue(filteredEventsDataMock)
    };
    greyhoundService = {
      unSubscribeEDPForUpdates: jasmine.createSpy(),
      subscribeEDPForUpdates: jasmine.createSpy(),
      sortRacingMarketsByTabs: jasmine.createSpy().and.returnValue('123321123'),
      getTypeNamesEvents: jasmine.createSpy().and.returnValue(Promise.resolve({})),
      getConfig: jasmine.createSpy().and.returnValue({ name: 'greyhound' }),
      getGreyhoundEvent: jasmine.createSpy().and.returnValue(Promise.resolve([{ id: '1' }])),
      getGeneralConfig: jasmine.createSpy().and.returnValue({ PRESIM_STOP_TRACK_INTERVAL: '' }),
      sortMarketsName: jasmine.createSpy()
        .and.returnValue({ typeName: testStr, markets: [{ outcomes: [{ name: '' }] }] as IMarket[] }),
    };

    routesDataSharingService = jasmine.createSpyObj(['updatedHasSubHeader']);

    timeService = jasmine.createSpyObj(['determineDay']);

    smartBoostsService = {
      isSmartBoosts: jasmine.createSpy().and.returnValue(true),
      parseName: jasmine.createSpy().and.returnValue({ name: testStr, wasPrice: wasPriceStub })
    };


    templateService = {
      genTerms: jasmine.createSpy('templateService.genTerms')
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a: string, param: string[] | string, fn: Function) => {
        switch (param) {
          case 'CHANGE_MARKET':
            fn('testMarket');
            break;
          case 'CHANGE_BET_FILTER':
            fn('testFilter');
            break;
          case pubSubApi.RELOAD_COMPONENTS :
            break;
          case 'EMA_UNSAVED_ON_EDP' :
            unsavedEmaHandler = fn;
            break;
          default:
            fn();
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish:jasmine.createSpy('publish'),
      API: pubSubApi
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy().and.returnValue('EDPpath')
    };
    eventVideoStreamProviderService = {
      getStreamBetCmsConfig: jasmine.createSpy('getStreamBetCmsConfig').and.returnValue(of({})),
      isStreamBetAvailable: jasmine.createSpy('isStreamBetAvailable')
    };
    sessionStorageService = {};
    component = new RacingEventMainComponent(router, route, timeService, templateService, command, nativeBridge,
      deviceService, routesDataSharingService, windowRef, horseRacingService, greyhoundService,
      routingState, smartBoostsService, cmsService, nextRacesService, eventService,
      extraPlaceService, pubSubService, changeDetectorRef, routingHelperService, eventVideoStreamProviderService, sessionStorageService);
  });

  it('#ngOninit should run addConnectListeners in happy path', fakeAsync(() => {
    const cbMap = {};
    spyOn(component, 'reloadComponent');
    pubSubService.subscribe.and.callFake((n, ch, cb) => cbMap[ch] = cb);
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing');
    component.ngOnInit();
    tick();

    expect(pubSubService.subscribe)
      .toHaveBeenCalledWith('racingEventMain', pubSubService.API.DEVICE_VIEW_TYPE_CHANGED_NEW, jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('racingEventMain', 'RELOAD_COMPONENTS', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('racingEventMain', pubSubService.API.SUCCESSFUL_LOGIN, jasmine.any(Function));
    expect(component.eventEntity.isVirtual).toBeFalsy();
    expect(component['state'].error).toBeFalsy();
    expect(component['state'].loading).toBeFalsy();
    cbMap['RELOAD_COMPONENTS']();
    expect(component.reloadComponent).toHaveBeenCalled();
  }));

  it('should handle EMA_UNSAVED_ON_EDP event', () => {
    component.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component['tagName'], pubSubService.API.EMA_UNSAVED_ON_EDP, jasmine.any(Function));
  });

  it('unsavedEmaHandler', () => {
    component.ngOnInit();
    unsavedEmaHandler(true);
    expect(component['editMyAccaUnsavedOnEdp']).toEqual(true);
  });

  it('#ngOninit should run addConnectListeners in error path with inner observables', fakeAsync(() => {
    horseRacingService.sortMarketsName.and.returnValue(sportEventMock);
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing');
    component['horseRacingService'].getTypeNamesEvents = () => Promise.reject('err');
    spyOn(component, 'reloadComponent');
    eventService.hrEventSubscription.subscribe.and.callFake(cb => cb & cb(true));
    component.ngOnInit();
    tick();
    expect(component.eventEntity.isVirtual).toBeFalsy();
    expect(component['state'].error).toBeTruthy();
    expect(component['state'].loading).toBeFalsy();
  }));
  describe('oninit empty response path', () => {
    beforeEach(() => {
      component['greyhoundService'].getGreyhoundEvent = jasmine.createSpy().and.returnValue(Promise.resolve(
        []
      ));
    });
    it('#ngOninit should finish load of edp and hide spinner', fakeAsync(() => {
      component['hideSpinner'] = jasmine.createSpy();
      component.ngOnInit();
      tick();

      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component.racingEdpReady).toBeTruthy();
    }));
  });

  describe('canChangeRoute', () => {
    it('should not when editMyAccaUnsavedOnEdp is true', () => {
      component['editMyAccaUnsavedOnEdp'] = false;
      expect(component.canChangeRoute()).toEqual(true);
    });

    it('should when editMyAccaUnsavedOnEdp is false', () => {
      component['editMyAccaUnsavedOnEdp'] = true;
      expect(component.canChangeRoute()).toEqual(false);
    });
  });

  it('onChangeRoute', () => {
    component.onChangeRoute();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
  });

  it('#ngOninit should run addConnectListeners in error path ', fakeAsync(() => {
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing');
    component['horseRacingService'].getById = jasmine.createSpy().and.returnValue(Promise.reject({ error: 'some error' }));
    const cbMap = {};
    pubSubService.subscribe.and.callFake((n, ch, cb) => cbMap[ch] = cb);
    spyOn(component, 'reloadComponent');

    component.ngOnInit();
    tick();

    expect(pubSubService.subscribe)
      .toHaveBeenCalledWith('racingEventMain', pubSubService.API.DEVICE_VIEW_TYPE_CHANGED_NEW, jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('racingEventMain', 'RELOAD_COMPONENTS', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('racingEventMain', pubSubService.API.SUCCESSFUL_LOGIN, jasmine.any(Function));
    expect(component['state'].error).toBeTruthy();
    expect(component['state'].loading).toBeFalsy();
    cbMap['RELOAD_COMPONENTS']();
    expect(component.reloadComponent).toHaveBeenCalled();
  }));

  it('#ngOninit should transform SmartBoosts markets', fakeAsync(() => {
    const virtualSportEvent = {...sportEventMock, typeFlagCodes: 'VR,'};
    eventVideoStreamProviderService.isStreamBetAvailable.and.returnValue(true);
    horseRacingService.sortMarketsName.and.returnValue(virtualSportEvent);
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing');
    component['transformSmartBoostsMarkets'] = jasmine.createSpy();
    component['racingService'].navMenuGroupEnhancedRaces = jasmine.createSpy().and.returnValue(filteredEventsDataMock);
    component.eventEntity = sportEventMock as any;
    component.eventEntity.liveStreamAvailable = true;
    component.ngOnInit();
    tick();
    expect(component.isStreambetAvailable).toBeTrue();
    expect(component.eventEntity.isVirtual).toBeTruthy();
    expect(component.isHorseRacingScreen).toEqual(true);
    expect(component['routingState'].getCurrentSegment).toHaveBeenCalled();
    expect(component.quickNavigationItems).toBeDefined();
    expect(component.quickNavigationItems).toEqual(filteredEventsDataMock.groupedByFlagAndData as any);
  }));

  it('#ngOninit should set loadFloatingMsgComp as true', fakeAsync(() => {
    const virtualSportEvent = {...sportEventMock, typeFlagCodes: 'VR,', drilldownTagNames: "'EVFLAG_AP', 'EVFLAG_IHR'"};
    horseRacingService.sortMarketsName.and.returnValue(virtualSportEvent);
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing');
    component['transformSmartBoostsMarkets'] = jasmine.createSpy();
    component['racingService'].navMenuGroupEnhancedRaces = jasmine.createSpy().and.returnValue(filteredEventsDataMock);
    component.eventEntity = sportEventMock as any;
    component['deviceService'].isDesktop = false;
    component['deviceService'].isWrapper = true;
    component.eventEntity.liveStreamAvailable = true;
    component.ngOnInit();
    tick();
    expect(nativeBridge.onEventDetailsStreamAvailable).toHaveBeenCalled();
    expect(component.loadFloatingMsgComp).toBe(true);
  }));

  describe('#ngOninit racingService', () => {
    let enhancedEvents;
    let response;

    beforeEach(() => {
      enhancedEvents = {
        groupedByFlagAndData: [
          {
            flag: 'ENHRCS',
            data: [{
              events: {
                id: 12197298,
                name: 'Kempton'
              },
              meeting: 'Kempton'
            }]
          }
        ]
      };
      response = {
        groupedByFlagAndData: [
          {
            flag: 'UK',
            data: [
              { meeting: 'Newcastle', events: {} },
              { meeting: 'Market Rasen', events: {} }
            ]
          },
          {
            flag: 'INT', data: [
              { meeting: 'Newcastle2', events: {} },
              { meeting: 'Market Rasen2', events: {} }
            ]
          },
          {
            flag: 'VR', data: [
              { meeting: 'Newcastle3', events: {} },
              { meeting: 'Market Rasen3', events: {} }
            ]
          }
        ],
        groupedByMeetings: {
          Cagnessurmer: {
            id: 9458938,
            isResulted: false
          },
          TestString: {
            id: 9458938,
            isResulted: false
          }
        },
        sportEventsData: [sportEventMock] as any
      } as any;

      spyOn<any>(component, 'edpReady');
      component['racingService'].navMenuGroupEnhancedRaces = jasmine.createSpy().and.returnValue(enhancedEvents);
      component['racingService'].getTypeNamesEvents = jasmine.createSpy().and.returnValue(Promise.resolve(response));
    });

    it('general flow', fakeAsync(() => {
      component.ngOnInit();
      tick();

      expect(enhancedEvents.groupedByFlagAndData[0].data[0].events.name).toEqual('Kempton');
      expect(component.quickNavigationItems).toEqual(response.groupedByFlagAndData);
      expect(component.racingsMap).toEqual(response.groupedByMeetings);
      expect(component['edpReady']).toHaveBeenCalledWith(response.groupedByMeetings.TestString);
    }));

    it('racingEdpReady should be false when route params are changing till event will be loaded from SiteServ', () => {
      component['racingEdpReady'] = true;

      component.ngOnInit();
      expect(component['changeDetectorRef'].detectChanges).toHaveBeenCalledTimes(1);
      expect(component['racingEdpReady']).toBeFalsy();
    });

    it('should pass full System Config to nextRacesService.getNextRacesModuleConfig (hello, coverage!)', fakeAsync(() => {
      routingState.getCurrentSegment.and.returnValue('horseracing');
      component['route'].snapshot.queryParams.origin = 'next-races';
      cmsService.getSystemConfig.and.returnValue(observableOf({ NextRaces: {}, RacingHubData: {} }));
      component.ngOnInit();
      tick();
      expect(nextRacesService.getNextRacesModuleConfig).toHaveBeenCalledWith('horseracing', { NextRaces: {}, RacingHubData: {} });
    }));

    it('should check if the event available in nextraces data', fakeAsync(() => {
      routingState.getCurrentSegment.and.returnValue('horseracing');
      component['route'].snapshot.queryParams.origin = 'next-races';
      cmsService.getSystemConfig.and.returnValue(observableOf({ NextRaces: {}, RacingHubData: {} }));
      eventService.getNextEvents.and.returnValue(of([{...sportEventMock}] as any));
      component.ngOnInit();
      tick();
      expect(router.navigateByUrl).toHaveBeenCalled();
    }));

    it('should pass full System Config to getEventsByTimeAndStatus', fakeAsync(() => {
      routingState.getCurrentSegment.and.returnValue('horseracing');
      component['route'].snapshot.queryParams.origin = 'offers-and-featured';
      spyOn(component, 'getEventsByTimeAndStatus');
      component.ngOnInit();
      tick();
      expect(component.origin).toEqual('offers-and-featured');
      expect(component.getEventsByTimeAndStatus).toHaveBeenCalled();
    }));

    it('should call getEvents for quick navigation items on horce racing screen', fakeAsync(() => {
      routingState.getCurrentSegment.and.returnValue('horseracing');
      component.ngOnInit();
      tick();
      expect(extraPlaceService.getEvents).toHaveBeenCalledTimes(1);
      expect(horseRacingService.navMenuGroupEnhancedRaces).toHaveBeenCalledTimes(1);
    }));
    it('should call racingAutoseoData', fakeAsync(() => {
      spyOn(component as any, 'racingAutoseoData').and.callThrough();
      component.ngOnInit();
      tick();
      expect(component['racingAutoseoData']).toHaveBeenCalled();
    }));
  });

  it('should transform SmartBoosts markets zzzz', () => {
    component.racingEdpReady = false;
    // @ts-ignore
    const events = [ { id: 2, startTime: 2 }, { id: 1, startTime: 1 } ] as ISportEvent[];

    component['edpReady'](events);
    // @ts-ignore
    expect(component.racingInMeeting).toEqual([ { id: 1, startTime: 1 }, { id: 2, startTime: 2 } ]);
    expect(component.racingEdpReady).toEqual(true);
  });

  describe('transformSmartBoostsMarkets', () => {
    let markets;

    beforeEach(() => {
      markets = [{ outcomes: [{ name: '' }] }] as IMarket[];
    });

    it(`isSmartBoosts property should equal true if market is SmartBoosts`, () => {
      component['transformSmartBoostsMarkets'](markets);
      expect(markets[0].isSmartBoosts).toBeTruthy();
    });

    it(`isSmartBoosts property should equal false if market is SmartBoosts`, () => {
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component['transformSmartBoostsMarkets'](markets);
      expect(markets[0].isSmartBoosts).toBeFalsy();
    });

    it(`should change outcomes 'name' if market is SmartBoosts`, () => {
      markets[0].outcomes[0].name = '';
      component['transformSmartBoostsMarkets'](markets);

      expect(markets[0].outcomes[0].name).toEqual(testStr);
    });

    it(`should set outcomes 'wasPrice' if market is SmartBoosts`, () => {
      delete markets[0].outcomes[0].wasPrice;
      component['transformSmartBoostsMarkets'](markets);

      expect(markets[0].outcomes[0].wasPrice).toEqual(wasPriceStub);
    });

    it(`should Not change outcomes 'name' if market is Not SmartBoosts`, () => {
      markets[0].outcomes[0].name = '';
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component['transformSmartBoostsMarkets'](markets);

      expect(markets[0].outcomes[0].name).toEqual('');
    });

    it(`should Not set outcomes 'wasPrice' if market is Not SmartBoosts`, () => {
      delete markets[0].outcomes[0].wasPrice;
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component['transformSmartBoostsMarkets'](markets);
      expect(markets[0].outcomes[0].wasPrice).toBeUndefined();
    });

    it(`should Not set outcomes 'wasPrice' if parsedName has Not 'wasPrice'`, () => {
      component['smartBoostsService'].parseName = jasmine.createSpy().and.returnValue({ name: '' });

      component['transformSmartBoostsMarkets'](markets);
      expect(markets[0].outcomes[0].wasPrice).toBeUndefined();
    });
  });

  describe('ngOnDestroy', () => {
    it(`should unsubscribe of 'paramsSubscriber'`, () => {
      component['paramsSubscriber'] = jasmine.createSpyObj(['unsubscribe']);
      component['eventSubscription'] = jasmine.createSpyObj (['unsubscribe'])
      component.ngOnDestroy();

      expect(component['paramsSubscriber'].unsubscribe).toHaveBeenCalled();
      expect(component['eventSubscription'].unsubscribe).toHaveBeenCalled();
    });
    it(`should unsubscribe of 'getEventsSubscription' and pubsub events`, () => {
      component['getEventsSubscription'] = jasmine.createSpyObj(['unsubscribe']);
      component['eventSubscription'] = jasmine.createSpyObj (['unsubscribe']);
      component.ngOnDestroy();
      expect(component['getEventsSubscription'].unsubscribe).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('racingEventMain');
    });
  });

  it('should define racingService when it is horseRacingService', () => {
    component.isHorseRacingScreen = true;
    const actualResult = component['racingService'];

    expect(actualResult).toEqual(component['horseRacingService']);
  });

  it('should define racingService when it is greyhoundService', () => {
    component.isHorseRacingScreen = false;
    const actualResult = component['racingService'];

    expect(actualResult).toEqual(component['greyhoundService']);
  });

  it('should not set selectedMarketPath on ReInit', () => {
    component.selectedMarketPath = 'testMarket';
    component.ngOnInit(true);

    expect(component.selectedMarketPath).toEqual('testMarket');
  });

  it('should set selectedMarketPath on Init', () => {
    pubSubService.subscribe = jasmine.createSpy('subscribe');
    component.ngOnInit();

    expect(component.selectedMarketPath).toEqual('Win or Each Way');
  });

  it('should set selectedMarketPath on first Init', () => {
    pubSubService.subscribe = jasmine.createSpy('subscribe');
    component.ngOnInit(false);

    expect(component.selectedMarketPath).toEqual('Win or Each Way');
  });

  it('should not set selectedMarketTypePath on ReInit', () => {
    component.selectedMarketTypePath = 'testMarket';
    component.ngOnInit(true);

    expect(component.selectedMarketTypePath).toEqual('testFilter');
  });

  it('should set selectedMarketTypePath on Init', () => {
    pubSubService.subscribe = jasmine.createSpy('subscribe');
    component.ngOnInit();

    expect(component.selectedMarketTypePath).toEqual('UEXA');
  });

  it('should not set selectedMarketTypePath on Init', () => {
    pubSubService.subscribe = jasmine.createSpy('subscribe');
    component['route'].params = observableOf({
        market: null,
        marketType: null
    }) as any;
    component.ngOnInit(true);

    expect(component.selectedMarketPath).not.toBeDefined();
    expect(component.selectedMarketTypePath).not.toBeDefined();
  });

  it('should define racingService when it is greyhoundService', () => {
    component.isHorseRacingScreen = false;
    const actualResult = component['racingService'];

    expect(actualResult).toEqual(component['greyhoundService']);
  });

  it('should check isNextRaceEvent information to show right racepanel', () => {
    const startedEventMock: any = {...sportEventMock};
    startedEventMock.isStarted = 'true';

    component.origin = 'next-races';
    component.eventEntity = startedEventMock;

    const isNextRaceEvent = component['isNextRaceEvent']();
    expect(isNextRaceEvent).toBeTruthy;
  });

  it('origin true and includes offers', () => {

    cmsService.getSystemConfig.and.returnValue(of({}));
    component['origin'] = 'offers';
    expect(component.getEventsByTimeAndStatus).toBeTrue
    expect(component.origin).toBeTrue;
  })

  it('@reloadComponent it should reload component', () => {
    component['paramsSubscriber'] = jasmine.createSpyObj('paramsSubscriber', ['unsubscribe']);
    component.ngOnDestroy = jasmine.createSpy('ngOnDestroy');
    component.ngOnInit = jasmine.createSpy('ngOnInit');
    component.reloadComponent();

    expect(component['paramsSubscriber'].unsubscribe).toHaveBeenCalled();
    expect(component.ngOnDestroy).toHaveBeenCalled();
    expect(component.ngOnInit).toHaveBeenCalledWith(true);
  });
  describe('racingAutoseoData', () => {
    it('should asign data to autoSeoData Object,Outright to be true and publish data ', () => {
      component.eventEntity = { name: 'teamA v teamB', typeName: 'World Cup', categoryName: 'football', markets: [{ templateMarketName: 'Outright' }] } as ISportEvent;
      component['racingAutoseoData']();
      expect(component['autoSeoData']).toBeDefined();
      expect(component['autoSeoData']['isOutright']).toBeTrue();
      expect(component['autoSeoData']).toBeDefined();
      expect(component['autoSeoData']['name']).toEqual(component.eventEntity.name);
      expect(component['autoSeoData']['typeName']).toEqual(component.eventEntity.typeName);
      expect(component['autoSeoData']['categoryName']).toEqual(component.eventEntity.categoryName);
      expect(pubSubService.publish).toHaveBeenCalledWith('AUTOSEO_DATA_UPDATED', jasmine.any(Object));
    });
    it('should assign isOutright to false', () => {
      component.eventEntity = { name: 'teamA v teamB', typeName: 'World Cup', categoryName: 'football', markets: [{ templateMarketName: 'Match' }] } as ISportEvent;
      component.eventEntity.markets[0].templateMarketName = 'Match';
      component['racingAutoseoData']();
      expect(component['autoSeoData']['isOutright']).toBeFalse();
    });
  });

  describe('getEventsByTimeAndStatus', () => {
    it('should filter sportevents by selected day event', () => {
      component.eventEntity = {...sportEventMock} as any;
      const eventsData = [{...sportEventMock}] as any;
      const result = component.getEventsByTimeAndStatus(eventsData);
      result.subscribe(events => {
        expect(events.length).toBe(0);
      });
    });

    it('should filter sportevents by selected day event with drilldownTagNames', () => {
      component.eventEntity = {...sportEventMock} as any;
      const eventObj = {...sportEventMock};
      eventObj.markets[0]['drilldownTagNames'] = 'MKTFLAG_EPR_TEST';
      const eventsData = [{...eventObj}] as any;
      component.getEventsByTimeAndStatus(eventsData).subscribe(res =>{
        expect(res.length).toBeGreaterThan(0);
      });
    });

  });

});
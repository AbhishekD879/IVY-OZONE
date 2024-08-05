import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf, throwError, empty as emptyObservable } from 'rxjs';

import { SingleSportSectionComponent } from '@app/inPlay/components/singleSportSection/single-sport-section.component';
import { EVENT_TYPES } from '@app/inPlay/constants/event-types.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { IRequestParams } from '@app/inPlay/models/request.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportEvent } from '@core/models/sport-event.model';

describe('SingleSportSectionComponent', () => {
  let component: SingleSportSectionComponent;
  let pubsubService;
  let inPlayMainService;
  let coreToolService;
  let windowRef;
  let localeService;
  const competitionEvents = [{
    cashoutAvail: 'cashoutAvail',
    categoryCode: 'categoryCode',
    categoryId: 'categoryId',
    categoryName: 'categoryName',
    displayOrder: 'displayOrder',
    drilldownTagNames: 'drilldownTagNames',
    eventIsLive: 'eventIsLive',
    eventSortCode: 'eventSortCode',
    eventStatusCode: 'eventStatusCode',
    id: 123
  }];
  let changeDetectorRef, routingHelperService, activatedRoute, cmsService, stickyVirtualScrollerService;

  beforeEach(fakeAsync(() => {
    inPlayMainService = {
      unsubscribeForSportCompetitionUpdates: jasmine.createSpy('unsubscribeForSportCompetitionUpdates'),
      unsubscribeForEventsUpdates: jasmine.createSpy('unsubscribeForEventsUpdates'),
      unsubscribeForEventUpdates: jasmine.createSpy('unsubscribeForEventUpdates'),
      _getCompetitionData: jasmine.createSpy('_getCompetitionData').and.returnValue(observableOf(competitionEvents)),
      getTopLevelTypeParameter: jasmine.createSpy('getTopLevelTypeParameter'),
      subscribeForUpdates: jasmine.createSpy('subscribeForUpdates'),
      isCashoutAvailable: jasmine.createSpy('isCashoutAvailable').and.returnValue(true),
      getRibbonData: jasmine.createSpy().and.returnValue(observableOf({})),
      getUnformattedEventsCounter: jasmine.createSpy().and.returnValue({}),
      getSportConfigSafe: jasmine.createSpy().and.returnValue(observableOf({
        config: {
          tier: 1
        }
      })),
      getSportName: jasmine.createSpy().and.returnValue('someSport'),
      extendSectionWithSportInstance: jasmine.createSpy(),
      clearDeletedEventFromType: jasmine.createSpy('clearDeletedEventFromType'),
      checkAggregateMarkets: (requestParams: IRequestParams, competition: ITypeSegment, competitionEvents: ISportEvent[]) => {
        const aggregated = requestParams['marketSelector'] && requestParams['marketSelector'].split(',').length > 1;
        if(aggregated){
          const eventsList = [];
          competition.eventsIds.forEach(event => {
            const commonEvent = competitionEvents.filter(ev => ev.id == event);
            const marketsList = commonEvent.map(b => b.markets[0]);
            marketsList.forEach(market => {
              market.name = requestParams.marketSelector;
            });
            commonEvent[0].markets = marketsList;
            eventsList.push(commonEvent[0]);
          });
          return competition.events = eventsList;
        }
        else {
          return competition.events = competitionEvents;
        }
      }
    };

    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi,
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    routingHelperService = {
      formInplayUrl: jasmine.createSpy(),
      formCompetitionUrl: jasmine.createSpy(),
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };

    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy()
        }
      }
    };

    cmsService = {
      getCompetitions: jasmine.createSpy().and.callFake(() => observableOf({
        InitialClassIDs: '123,124',
        'A-ZClassIDs': '123,124'
      } as any)),
      getMarketSwitcherFlagValue: jasmine.createSpy('getMarketSwitcherFlagValue').and.callFake(() => observableOf(Boolean))
    };
    coreToolService = {
      uuid: jasmine.createSpy().and.returnValue('123')
    };

    stickyVirtualScrollerService = {
      stick: jasmine.createSpy('stick')
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
  }));

  beforeEach(fakeAsync(() => {
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new SingleSportSectionComponent(
      inPlayMainService,
      pubsubService,
      changeDetectorRef,
      routingHelperService,
      activatedRoute,
      cmsService,
      coreToolService,
      stickyVirtualScrollerService,
      windowRef,
      localeService);

    component.eventsBySports = {
      eventsByTypeName: []
    } as any;
    component.skeletonShow = [];
  }));

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(SingleSportSectionComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('subscription name should be defined', () => {
    expect(component['syncName']).toEqual('inplay-single-sport_123');
  });

  describe('formEdpUrl', () => {
    it('should create EDP url', () => {
      component.formEdpUrl(({ id: '1' } as any));

      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '1' });
    });

    it('should create Virtual url', () => {
      component['virtualScroll'] = true;
      component.formEdpUrl(({ id: '2' } as any));

      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '2' });
    });
  });

  describe('#ngOnInit', () => {
    const msgInPlayAdded = 'INPLAY_COMPETITION_ADDED:34:LIVE_EVENT';
    const msgInPlayRemoved = 'INPLAY_COMPETITION_REMOVED:34:LIVE_EVENT';

    beforeEach(() => {
      component['processInitialData'] = jasmine.createSpy();
      spyOn(component as any, 'calculateIsAllExpanded');
      component.sportName = 'someSport';
      component.eventsBySports = { categoryId: '34' } as any;
      inPlayMainService.getTopLevelTypeParameter.and.returnValue(EVENT_TYPES.LIVE_EVENT);
    });

    it('should subscribe on connect and pubsub', () => {
      component.ngOnInit();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay-single-sport_123', msgInPlayAdded, jasmine.any(Function));
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay-single-sport_123', msgInPlayRemoved, jasmine.any(Function));
      expect(component['processInitialData']).toHaveBeenCalled();
    });

    it('Should fetch event by sports EVENT_BY_SPORTS_SUBSCRIBE gets triggered', () => {
      component.filter = 'livenow';
      pubsubService.subscribe.and.callFake((subscriber, method, handler) => {
        if (method === `${pubSubApi.EVENT_BY_SPORTS_CHANNEL}_SINGLE`) {
          handler({livenow: {} , upcoming: {} } as any);
        }
      }),
      component.ngOnInit();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('EVENT_BY_SPORTS_SUBSCRIBE_livenow',
      `${pubSubApi.EVENT_BY_SPORTS_CHANNEL}_SINGLE`,jasmine.any(Function));
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should define subscriptionFlags, scrollSportUIdcand call ', () => {
      component.ngOnInit();
      expect(component.subscriptionFlags).toBeDefined();
      expect(component.scrollSportUId).toBe('123');
    });

    describe('connect INPLAY_COMPETITION_REMOVED handler', () => {
      beforeEach(() => {
        spyOn(component as any, 'loadCompetionSection').and.returnValue(observableOf({}));
        pubsubService.subscribe.and.callFake((a, b, cb) => {
          if (b === msgInPlayRemoved) {
            cb({
              categoryName: 'SomeSport',
              events: [{
                isStarted: true
              }]
            });
          }
        });
        component.eventsBySports['eventsByTypeName'] = [{
          categoryId: '34',
          typeId: 1,
          categoryName: 'SomeSport',
          events: [{
            isStarted: true
          }]
        }] as any;
        component.inner = true;
      });

      it('connect INPLAY_COMPETITION_REMOVED handler', fakeAsync(() => {
        component.filter = 'livenow';

        component.ngOnInit();

        expect(component.loadCompetionSection).toHaveBeenCalled();
        expect(component['calculateIsAllExpanded']).toHaveBeenCalled();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(component.expandedFlags['1']).toBeTruthy();
        expect(component.eventsBySports.eventsByTypeName[0].isExpanded).toBeTruthy();
        tick();
      }));

      it(`should Not loadCompetionSection if 'inner' is Falthy`, () => {
        component.inner = undefined;

        component.ngOnInit();

        expect(component.loadCompetionSection).not.toHaveBeenCalled();
      });

      it('when subscribed and the same sports', () => {
        component.subscriptionFlags = {
          1: true
        };
        component.eventsBySports = {
          eventsByTypeName: [
            {
              typeId: 1
            }
          ]
        } as any;
        component.ngOnInit();
        expect(component.loadCompetionSection).not.toHaveBeenCalled();
      });
    });

    it('handle connect INPLAY_COMPETITION_ADDED event when is inner', () => {
      component.inner = true;
      component.filter = 'livenow';
      component.virtualScroll = true;
      const addedCompetition = {
        typeId: 3,
        categoryName: 'SomeSport',
        events: [{
          isStarted: true
        }]
      } as any;

      pubsubService.subscribe.and.callFake((a, b, cb) => {
        if (b === msgInPlayAdded) {
          cb(addedCompetition);
        }
      });
      component.ngOnInit();
      expect(component['calculateIsAllExpanded']).toHaveBeenCalled();
      expect(component.expandedFlags['3']).toBeTruthy();
      expect(addedCompetition.isExpanded).toBeTruthy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('handle connect INPLAY_COMPETITION_ADDED event when is not inner', () => {
      component.inner = false;
      component['setExpandedFlags'] = jasmine.createSpy();
      const addedCompetition = {
        typeId: 3,
        categoryName: 'SomeSport',
        events: []
      } as any;
      pubsubService.subscribe.and.callFake((a, b, cb) => {

        if (b === msgInPlayAdded) {
          cb(addedCompetition);
        }
      });
      component.ngOnInit();
      expect(component['calculateIsAllExpanded']).toHaveBeenCalled();
      expect(inPlayMainService.subscribeForUpdates).not.toHaveBeenCalled();
      expect(addedCompetition.isExpanded).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('handle connect INPLAY_COMPETITION_ADDED event when is inner and virtual scroll is on', () => {
      component.filter = 'livenow';
      component.inner = true;
      component.virtualScroll = true;
      pubsubService.subscribe.and.callFake((a, b, cb) => {
        if (b === msgInPlayAdded) {
          cb({
            typeId: 3,
            categoryName: 'SomeSport',
            events: [{
              isStarted: true
            }]
          });
        }
      });
      component.ngOnInit();
      expect(component['calculateIsAllExpanded']).toHaveBeenCalled();
      expect(component.expandedFlags['3']).toBeTruthy();
      expect(inPlayMainService.subscribeForUpdates).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    describe('handle connect INPLAY_COMPETITION_ADDED', () => {

      beforeEach(() => {
        spyOn(component as any, 'setCompetitionPagesAvailability');

        cmsService.getCompetitions.and.returnValue(emptyObservable());

        component.filter = 'livenow';
      });

      it('event when is inner and virtual scroll is off', () => {
        component.inner = true;
        component.virtualScroll = false;
        pubsubService.subscribe.and.callFake((a, b, cb) => {
          if (b === msgInPlayAdded) {
            cb({
              typeId: 3,
              categoryName: 'SomeSport',
              events: [{
                isStarted: true
              }]
            });
          }
        });
        component.ngOnInit();
        expect(component['calculateIsAllExpanded']).toHaveBeenCalled();
        expect(component.expandedFlags['3']).toBeTruthy();
        expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalled();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it(`should remove section with empty events`, () => {
        const addedCompetition: any = {
          typeId: 3,
          categoryName: 'SomeDifferentSport',
          events: []
        };

        component.inner = true;
        component.eventsBySports.eventsByTypeName = [addedCompetition, { typeId: 4 }];

        pubsubService.subscribe.and.callFake((a, b, cb) => {
          if (b === msgInPlayAdded) { cb(addedCompetition); }
        });

        component.ngOnInit();

        expect(component.eventsBySports.eventsByTypeName).toEqual([{ typeId: 4 }] as any);
      });

      it('expanded competiiotn', () => {
        const eventsListMock = [{
          id: 123,
          isStarted: true
        }];

        component.inner = false;
        component.virtualScroll = false;
        component['expandedFlags']['3'] = true;

        pubsubService.subscribe.and.callFake((a, b, cb) => {
          if (b === msgInPlayAdded) {
            cb({
              typeId: 3,
              categoryName: 'SomeSport',
              events: eventsListMock
            });
          }
        });

        component.ngOnInit();
        expect(component['calculateIsAllExpanded']).toHaveBeenCalled();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalledWith(eventsListMock);
      });

      it('for COLLAPSED competition', () => {
        const eventsListMock = [{
          id: 123,
          isStarted: true
        }];

        component.inner = false;
        component.virtualScroll = false;
        component['expandedFlags']['3'] = false;

        pubsubService.subscribe.and.callFake((a, b, cb) => {
          if (b === msgInPlayAdded) {
            cb({
              typeId: 3,
              categoryName: 'SomeSport',
              events: eventsListMock
            });
          }
        });

        component.ngOnInit();
        expect(component['calculateIsAllExpanded']).toHaveBeenCalled();
        expect(inPlayMainService.subscribeForUpdates).not.toHaveBeenCalled();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it(' event when the same sport', () => {
        component.inner = true;
        pubsubService.subscribe.and.callFake((a, b, cb) => {
          if (b === msgInPlayAdded) {
            cb({
              typeId: 3,
              categoryName: 'SomeSport',
              events: [{
                isStarted: true
              }]
            });
          }
        });
        component.ngOnInit();
        expect(component['setCompetitionPagesAvailability']).toHaveBeenCalled();
      });
    });


    it('INPLAY_COMPETITION_REMOVED when no events in sections, has market selection and with different market name', () => {
      component.reloadData.emit = jasmine.createSpy('component[emit]');
      component['selectedMarketName'] = '2';
      component.eventsBySports = {
        categoryId: '16',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: []
      } as any;
      component.filter = 'livenow';
      component.ngOnInit();

      pubsubService.subscribe.and.callFake((a, b, cb) => {
        if (b === 'INPLAY_COMPETITION_REMOVED:16:LIVE_EVENT') {
          cb({
            categoryName: 'SomeOtherSport',
            events: [{
              isStarted: true
            }]
          });
        }
      });

      component.ngOnInit();

      expect(component.reloadData.emit).toHaveBeenCalledWith({
        additionalParams: { marketSelector: '1' },
        useCache: false
      });
    });

    it('INPLAY_COMPETITION_REMOVED when no events in sections, has market selection and with the same market name', () => {
      component.reloadData.emit = jasmine.createSpy('component[emit]');
      component['selectedMarketName'] = '1';
      component.eventsBySports = {
        categoryId: '34',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: []
      } as any;
      component.filter = 'livenow';

      pubsubService.subscribe.and.callFake((a, b, cb) => {
        if (b === msgInPlayRemoved) {
          cb({
            categoryName: 'SomeOtherSport',
            events: [{
              isStarted: true
            }]
          });
        }
      });
      component.ngOnInit();
      expect(component.reloadData.emit).not.toHaveBeenCalledWith({
        additionalParams: { marketSelector: '1' },
        useCache: false
      });
    });

    it('handle connect INPLAY_COMPETITION_REMOVED when no events in sections, has no market selection', () => {
      component.reloadData.emit = jasmine.createSpy('component[emit]');
      component.eventsBySports = {
        categoryId: '16',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: []
      } as any;

      pubsubService.subscribe.and.callFake((a, b, cb) => {
        if (b === 'INPLAY_COMPETITION_REMOVED') {
          cb({
            categoryName: 'SomeOtherSport',
            events: [{
              isStarted: true
            }]
          });
        }
      });
      component.ngOnInit();
      expect(component.reloadData.emit).not.toHaveBeenCalled();
    });
    it('ngOnInit case INPLAY_COMPETITION_UPDATED', () => {
      pubsubService.subscribe = jasmine.createSpy('ssubscribeync').and.callFake((a, b, cb) => {
        if (b == 'INPLAY_COMPETITION_UPDATED:34:LIVE_EVENT') {
          cb();
        }
      });
      component.ngOnInit();
      expect(pubsubService.subscribe).toHaveBeenCalled();
      expect(component.expandedFlags).toBeDefined();
      expect(component['processInitialData']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('ngOnInit', fakeAsync(() => {
      const mockSportInstance = { config: { tier: 1 } };
      component['extendSectionData'] = jasmine.createSpy();
      component.ngOnInit();

      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay-single-sport_123', msgInPlayAdded, jasmine.any(Function));
      expect(component.sportName).toEqual('someSport');
      expect(inPlayMainService.getSportConfigSafe).toHaveBeenCalledWith('someSport');
      tick();
      expect(component.sportInstance).toEqual(mockSportInstance as any);
      expect(component['extendSectionData']).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    }));

    it('should filter "Enhanced Multiples" type if eventsBySports exist', () => {
      component.eventsBySports = {} as any;
      component.ngOnInit();
      expect(component.eventsBySports).toEqual({} as any);

      component.eventsBySports.eventsByTypeName = [];
      component.ngOnInit();
      expect(component.eventsBySports.eventsByTypeName).toEqual([]);

      component.eventsBySports.eventsByTypeName = [{
        typeName: 'English Football',
        events: [{
          classId: '1'
        }]
      }, {
        typeName: 'Enhanced Multiples'
      }] as any;
      component.ngOnInit();

      expect(component.eventsBySports.eventsByTypeName).toEqual([{
        typeName: 'English Football',
        events: [{
          classId: '1'
        }],
        classId: '1'
      }] as any);
    });

    it('Should fetch event when live inplay event gets triggered', () => {
      let handler;
      pubsubService.subscribe.and.callFake((subscriber, method, cb) => {
        if (method === `WS_EVENT_LIVE_UPDATE`) {
          handler = cb;
        }
      });
      component.ngOnInit();
      handler();
      expect(pubsubService.subscribe).toHaveBeenCalledWith(`inplaySectionLiveUpdate_${component.filter}`,pubSubApi.WS_EVENT_LIVE_UPDATE, jasmine.any(Function));
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('Should fetch reloaded section inplay data when sport is selected', () => {
      let handler;
      const subscriberName = 'inplaySectionDataReLoad';
      pubsubService.subscribe.and.callFake((subscriber, method, cb) => {
        if (subscriber === `inplaySectionDataReLoad` && method === `INPLAY_DATA_RELOADED`) {
          handler = cb;
        }
      });
      component.ngOnInit();
      handler();
      expect(pubsubService.subscribe).toHaveBeenCalledWith(
        subscriberName,
        pubSubApi.INPLAY_DATA_RELOADED,
        jasmine.any(Function)
      );
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
      it('Should trigger change detection on the event update', () => {
        let handler;
        pubsubService.subscribe.and.callFake((subscriber, method, cb) => {
          if (method === `WS_EVENT_UPDATE`) {
            handler = cb;
          }
        });
        component.ngOnInit();
        handler();
        expect(pubsubService.subscribe).toHaveBeenCalledWith(
          `inplayEventUpdate_${component.filter}`,
          pubSubApi.WS_EVENT_UPDATE,
          jasmine.any(Function)
        );
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });
  });

  describe('#ngOnChanges', () => {
    let changes;

    beforeEach(() => {
      component['processInitialData'] = jasmine.createSpy();
      component['extendSectionData'] = jasmine.createSpy();
      changes = {
        eventsBySports: {
          currentValue: {
            eventsByTypeName: []
          }
        }
      };
    });
    it('should set expandedFlag', () => {
      component.ngOnChanges(changes as any);

      expect(Object.keys(changes).length).not.toEqual(0);
      expect(component['processInitialData']).toHaveBeenCalledWith(changes.eventsBySports.currentValue);
      expect(component['extendSectionData']).toHaveBeenCalledWith(true);
    });
    it('should not set expandedFlag 1', () => {
      changes = {
        eventsBySports: {
          currentValue: {}
        }
      };

      component.ngOnChanges(changes as any);
      expect(Object.keys(changes.eventsBySports.currentValue).length).toEqual(0);
      expect(component['processInitialData']).not.toHaveBeenCalled();
      expect(component['extendSectionData']).not.toHaveBeenCalled();
    });
    it('should not set expandedFlag 2', () => {
      changes = {
        eventsBySports: {}
      };

      component.ngOnChanges(changes as any);
      expect(component['processInitialData']).not.toHaveBeenCalled();
      expect(component['extendSectionData']).not.toHaveBeenCalled();
    });
    it('should not set expandedFlag 3', () => {
      changes = {};

      component.ngOnChanges(changes as any);
      expect(component['processInitialData']).not.toHaveBeenCalled();
      expect(component['extendSectionData']).not.toHaveBeenCalled();
    });
  });

  describe('#initMarketSelector', () => {
    it('should call markForCheck on market selector init', fakeAsync(() => {
      component.initMarketSelector();
      tick(0);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));
  });

  it('reloadSportData', () => {
    component.reloadData.emit = jasmine.createSpy();
    const options = {
      useCache: true,
      additionalParams: {
        topLevelType: 'type',
        categoryId: 'id'
      }
    } as any;
    component.reloadSportData(options);

    expect(component.reloadData.emit).toHaveBeenCalledWith(options);
  });

  describe('#setExpandedFlags', () => {
    let competitionSection;
    beforeEach(() => {
      competitionSection = {
        typeId: '123'
      } as any;
    });
    it('should set expandedFlag - true', () => {
      component['setExpandedFlag'](competitionSection, 1);
      expect(component.expandedFlags[123]).toBe(true);
    });
    it('should set expandedFlag - true', () => {
      component.expandedFlags[123] = false;
      component.expandedLeaguesCount = 2;
      component['setExpandedFlag'](competitionSection, 1);
      expect(component.expandedFlags[123]).toBe(true);
      expect(competitionSection.isExpanded).toBeTruthy();
    });
    it('should set expandedFlag - false', () => {
      component.expandedFlags[123] = true;
      component.expandedLeaguesCount = 2;
      component['setExpandedFlag'](competitionSection, 5);
      expect(component.expandedFlags[123]).toBe(false);
      expect(competitionSection.isExpanded).toBeFalsy();
    });
  });

  
  describe('#setExpandedFlags for HR', () => {
    let competitionSection;
    beforeEach(() => {
      competitionSection = {
        typeId: '123',
        events:[{id:'1234', startTime:'123', markets:[{id:'market1'}]}]
      } as any;
    });
    it('should set expandedFlag - true', () => {
      component.expandedFlags['1234'] = false;
      component['liveLabel'] = true;
      component['isHR'] = true;
      component.expandedLeaguesCount = 2;
      component['eventsBySports'] = {eventsByTypeName:[{},{}]as any} as any;
      component['HREvents'] =[{id:'1234', startTime:'123', markets:[{id:'market1'}]}];
      component['setExpandedFlag'](competitionSection, 1);
      expect(component.expandedFlags['1234']).toBe(true);
      expect(competitionSection.events[0].isExpanded).toBe(true);
      expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalledWith([jasmine.any(Object)]);
    });

    it('should set expandedFlag - false', () => {
      component['eventsBySports'] = { categoryId: 21, eventsByTypeName: [{ events: [{ id: '1234', startTime: '123' }] }] as any } as any;
      component.expandedFlags[123] = true;
      component.expandedLeaguesCount = 0;
      component['setExpandedFlag'](competitionSection, 1);
      expect(component['eventsBySports'].eventsByTypeName[0].events[0].isExpanded).toBeFalsy();
    });

    it('should not process HR', () => {
      component['isHR'] = true;
      competitionSection.events = null;      
      component['setExpandedFlag'](competitionSection, 1);
      expect(component['HREvents']).toEqual([]);
    });
  });
  describe('#processInitialData', () => {
    beforeEach(() => {
      component['setExpandedFlag'] = jasmine.createSpy();
    });
    it('when eventsByTypeName are defined', () => {
      component.eventsBySports = {
        eventsByTypeName: [{
          id: '112312312'
        }]
      } as any;
      component['processInitialData']();
      expect(component['setExpandedFlag']).toHaveBeenCalled();
    });
    it('when eventsByTypeName are not defined', () => {
      component.eventsBySports = undefined;
      component['processInitialData']();
      expect(component['setExpandedFlag']).not.toHaveBeenCalled();
    });
    it('when data is exist', () => {
      component.eventsBySports = undefined;
      component['processInitialData']({
        eventsByTypeName: [{
          typeId: '111'
        }]
      } as any);
      expect(component['setExpandedFlag']).toHaveBeenCalled();
    });
  });

  describe('handleOutput', () => {
    it('should execute filterEvents when output is reloadData', () => {
      component.handleOutput({ output: 'reloadData', value: 'someFilter' });
      component.reloadData.emit = jasmine.createSpy();
      const options = { value: 'someFilter' } as any;
      component.reloadSportData(options);
      expect(component.reloadData.emit).toHaveBeenCalledWith(options);
    });
    it('should execute filterEvents when output is selectedMarketName', () => {
      component.handleOutput({ output: 'selectedMarketName', value: 'someFilter' });
      expect(component.selectedMarketName).toBe('someFilter');
    });
    it('should passby when output is other than reloadData and selectedMarketName', () => {
      component.handleOutput({ output: 'someoutput', value: 'someFilter' });
      component.reloadData.emit = jasmine.createSpy();
      const options = {} as any;
      component.reloadSportData(options);
      expect(component.reloadData.emit).toHaveBeenCalledWith(options);
      expect(component.selectedMarketName).not.toBeDefined();
    });
  });

  describe('#toggleCompetitionSection', () => {
    const competitionSection = {
      typeId: '01',
      marketSelector: 'marketSelector',
      events: [
        {
          cashoutAvail: 'cashoutAvail',
          categoryCode: 'categoryCode',
          categoryId: 'categoryId'
        }
      ]
    } as any;
    const sectionsArray = [
      {
        typeId: '01',
        marketSelector: 'marketSelector',
        events: [
          {
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      },
      {
        typeId: '02',
        marketSelector: 'marketSelector',
        events: [
          {
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      }
    ] as any[];
    it('should test toggling of expand/collapse state of league section', fakeAsync(() => {
      component.expandedFlags = {
        '01': false,
        '02': false
      };
      component.competitionRequestInProcessFlags = {
        '01': false,
        '02': false
      };
      component.eventsBySports = {
        categoryCode: '01',
        categoryId: '02'
      } as any;
      component.filter = 'live';
      const requestParams = {
        categoryId: component.eventsBySports.categoryId,
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
        typeId: competitionSection.typeId,
        modifyMainMarkets: true
      };

      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);

      expect(component.competitionRequestInProcessFlags['01']).toBeFalsy();
      inPlayMainService._getCompetitionData(requestParams, component.eventsBySports.categoryCode)
        .subscribe((competition) => {
          expect(component.competitionRequestInProcessFlags[competitionSection.typeId]).toBeFalsy();
          expect(competitionSection.events).toEqual(competition);
          expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalledWith(competitionSection.events);
          expect(competitionSection.isExpanded).toBeTruthy();
          expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        });
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should call change detection when request is in progress', fakeAsync(() => {
      component.expandedFlags = {
        '01': false,
        '02': false
      };
      component.competitionRequestInProcessFlags = {
        '01': true,
        '02': true
      };
      component.eventsBySports = {
        categoryCode: '01',
        categoryId: '02'
      } as any;
      component.filter = 'live';

      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);

      expect(component.competitionRequestInProcessFlags['01']).toBeTruthy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should call change detection when request is in progress#1', fakeAsync(() => {
      component.expandedFlags = {
        '01': false,
        '02': false
      };
      component.competitionRequestInProcessFlags = {
        '01': true,
        '02': true
      };
      component.eventsBySports = {
        categoryCode: '01',
        categoryId: '02'
      } as any;
      component.filter = 'live';
      component.isHR = false;

      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);

      expect(component.competitionRequestInProcessFlags['01']).toBeTruthy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('when collapsing', () => {
      component.expandedFlags = {
        '01': true,
      };
      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);
      expect(inPlayMainService.unsubscribeForEventsUpdates).toHaveBeenCalled();
      expect(component.subscriptionFlags).toEqual({
        '01': false
      });
      expect(component.skeletonShow[0]).toBe(false);
    });

    it('when collapsing It with loadcompetition returing error', () => {
      component.expandedFlags = {
        '01': true,
      };
      component.loadCompetionSection = jasmine.createSpy().and.returnValue(observableOf({ error: 'error' }));
      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);
      expect(component.skeletonShow[0]).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('when collapsing It with loadcompetition returing error and expanded false', () => {
      component.expandedFlags = {
        '01': false,
      };
      component.loadCompetionSection = jasmine.createSpy().and.returnValue(throwError(''));
      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);
      expect(component.skeletonShow[0]).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('when user expand/collapse accordion rapidly', () => {
      component.loadCompetionSection = jasmine.createSpy().and.callFake(() => {
        // Emulate click accordion collapse before response;
        component.expandedFlags[competitionSection.typeId] = !component.expandedFlags[competitionSection.typeId];
        return observableOf({});
      });
      component.expandedFlags = {
        '01': false
      };
      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);
      expect(inPlayMainService.subscribeForUpdates).not.toHaveBeenCalled();
      expect(component.expandedFlags).toEqual({
        '01': false
      });
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('#toggleCompetitionSection with eventData', () => {
    beforeEach(()=>{
      component.eventsBySports = {
        categoryCode: '01',
        categoryId: '02',
        eventsByTypeName: [{
          showCashoutIcon: false,
          typeId: '01',
          competitionSection: {
            typeId: '01',
            marketSelector: 'marketSelector',
            events: [
              {
                cashoutAvail: 'cashoutAvail',
                categoryCode: 'categoryCode',
                categoryId: 'categoryId'
              }]
          }
        }]
      } as any;
    });
    const competitionSection = {
      typeId: '01',
      marketSelector: 'marketSelector',
      events: [
        {
          cashoutAvail: 'cashoutAvail',
          categoryCode: 'categoryCode',
          categoryId: 'categoryId'
        }
      ]
    } as any;
    const sectionsArray = 
      {
        id: '01',
        typeId: '01',
        marketSelector: 'marketSelector',
        events: [
          {
            typeId: '01',
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      } as any;
    it('should test toggling of expand/collapse state of league section', fakeAsync(() => {
      component.isHR = true;
      component.expandedFlags = {
        '01': false,
        '02': false
      };
      component.competitionRequestInProcessFlags = {
        '01': false,
        '02': false
      };
      component.filter = 'live';
      const requestParams = {
        categoryId: component.eventsBySports.categoryId,
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
        typeId: competitionSection.typeId,
        modifyMainMarkets: true
      };

      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);

      expect(component.competitionRequestInProcessFlags['01']).toBeFalsy();
      inPlayMainService._getCompetitionData(requestParams, component.eventsBySports.categoryCode)
        .subscribe((competition) => {
          expect(component.competitionRequestInProcessFlags[competitionSection.typeId]).toBeFalsy();
          expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalledWith([sectionsArray]);
          expect(sectionsArray.isExpanded).toBeTruthy();
          expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        });
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should call change detection when request is in progress', fakeAsync(() => {
      component.isHR = true;
      component.expandedFlags = {
        '01': false,
        '02': false
      };
      component.competitionRequestInProcessFlags = {
        '01': true,
        '02': true
      };
      component.filter = 'live';

      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);

      expect(component.competitionRequestInProcessFlags['01']).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('when collapsing', () => {
      component.isHR = true;
      component.expandedFlags = {
        '01': true,
      };
      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);
      expect(inPlayMainService.unsubscribeForEventUpdates).toHaveBeenCalled();
      expect(component.subscriptionFlags).toEqual({
        '01': false
      });
      expect(component.skeletonShow[0]).toBe(false);
    });

    it('when collapsing It with loadcompetition returing error', () => {
      component.isHR = true;
      component.expandedFlags = {
        '01': true,
      };
      component.loadCompetionSection = jasmine.createSpy().and.returnValue(observableOf({ error: 'error' }));
      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);
      expect(component.skeletonShow[0]).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('when collapsing It with loadcompetition returing error and expanded false', () => {
      component.isHR = true;
      component.expandedFlags = {
        '01': false,
      };
      component.loadCompetionSection = jasmine.createSpy().and.returnValue(throwError(''));
      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);
      expect(component.skeletonShow[0]).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('when user expand/collapse accordion rapidly', () => {
      component.isHR = true;
      component.loadCompetionSection = jasmine.createSpy().and.callFake(() => {
        // Emulate click accordion collapse before response;
        component.expandedFlags[competitionSection.typeId] = !component.expandedFlags[competitionSection.typeId];
        return observableOf({});
      });
      component.expandedFlags = {
        '01': false
      };
      component.toggleCompetitionSection(competitionSection, sectionsArray, 0);
      expect(inPlayMainService.subscribeForUpdates).not.toHaveBeenCalled();
      expect(component.expandedFlags).toEqual({
        '01': false
      });
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('checkIfMarketSelectorAvailable', () => {
    it('case if visible', () => {
      component.reloadData.emit = jasmine.createSpy('component[emit]');
      component.eventsBySports = {
        categoryId: '16',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: [{
          id: '112312312'
        }]
      } as any;
      component.categoryId = '16';
      component.inner = false;
      component.filter = 'livenow';
      component.checkIfMarketSelectorAvailable();
      const actualResult = component.isMarketSelectorVisible();
      expect(component.reloadData.emit).not.toHaveBeenCalledWith({
        additionalParams: { marketSelector: 'Match Betting' },
        useCache: false
      });
      expect(actualResult).toBe(true);
    });
    it('case if not visible', () => {
      component.reloadData.emit = jasmine.createSpy('component[emit]');
      component.eventsBySports = {
        categoryId: '123',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: []
      } as any;
      component.inner = false;
      component.filter = 'someFilter';
      component.checkIfMarketSelectorAvailable();
      expect(component.isMarketSelectorVisible()).toBe(false);
    });

    it('case if no events', () => {
      component.reloadData.emit = jasmine.createSpy('component[emit]');
      component.eventsBySports = {
        categoryId: '123',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: undefined
      } as any;
      component.inner = false;
      component.filter = 'someFilter';
      component.checkIfMarketSelectorAvailable();
      expect(component.isMarketSelectorVisible()).toBe(false);
    });
  });

  describe('#isMarketSelectorAvailable', () => {
    it('when no market selector options', () => {
      component.eventsBySports = {} as any;
      component.filter = 'livenow';
      component.checkIfMarketSelectorAvailable();

      expect(component.isMarketSelectorAvailable).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('when is inner', () => {
      component.inner = true;
      component.filter = 'livenow';
      component.eventsBySports = {
        categoryId: '16',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: [{
          id: '112312312'
        }]
      } as any;
      component.checkIfMarketSelectorAvailable();

      expect(component.isMarketSelectorAvailable).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('when is not football', () => {
      component.filter = 'livenow';
      component.eventsBySports = {
        categoryId: '43434',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: [{
          id: '112312312'
        }]
      } as any;
      component.checkIfMarketSelectorAvailable();

      expect(component.isMarketSelectorAvailable).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('when is not livenow filter', () => {
      component.filter = 'someFilter';
      component.eventsBySports = {
        categoryId: '43434',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: [{
          id: '112312312'
        }]
      } as any;
      component.checkIfMarketSelectorAvailable();

      expect(component.isMarketSelectorAvailable).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('when market selector should be present', () => {
      component.filter = 'livenow';
      component.eventsBySports = {
        categoryId: '16',
        marketSelectorOptions: ['1', '2'],
        eventsByTypeName: [{
          id: '112312312'
        }]
      } as any;
      component.categoryId = '16';
      component.checkIfMarketSelectorAvailable();

      expect(component.isMarketSelectorAvailable).toBe(true);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('#getSectionTitle', () => {
    it('should return one sport title', () => {
      const competitionSectionData = {
        typeName: 'Italian Serie B',
      } as any;
      const actualResult = component.getSectionTitle(competitionSectionData);
      expect(actualResult).toEqual(competitionSectionData.typeName);
    });

    it('should return empty string', () => {
      const competitionSectionData = {} as any;
      const actualResult = component.getSectionTitle(competitionSectionData);
      expect(actualResult).toEqual('');
    });
  });

  it('ngOnDestroy: should remove listeners', () => {
    component.eventsBySports = {} as any;
    component.filter = 'livenow';
    component.ngOnDestroy();

    expect(inPlayMainService.unsubscribeForSportCompetitionUpdates).toHaveBeenCalledWith(component.eventsBySports);
    expect(inPlayMainService.unsubscribeForEventsUpdates).toHaveBeenCalledWith(component.eventsBySports);
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplay-single-sport_123');
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('EVENT_BY_SPORTS_SUBSCRIBE_livenow');
    expect(component.eventsBySports.eventsByTypeName).toEqual([]);
    expect(stickyVirtualScrollerService.stick).toHaveBeenCalledWith(false, true);
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith(`inplaySectionLiveUpdate_${component.filter}`);
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplaySectionDataReLoad');
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith(`inplayEventUpdate_${component.filter}`);
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from marketSwitcherConfig', () => {
      component['marketSwitcherConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['marketSwitcherConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('check for isMarketSwitcherConfigured', () => {
    it('should set isMarketSwitcherConfigured to true if cmsService getMarketSwitcherFlagValue return true', () => {
      component.sportName = 'darts';
      cmsService.getMarketSwitcherFlagValue.subscribe = jasmine.createSpy('cmsService.getMarketSwitcherFlagValue')
        .and.callFake((flag) => {
          expect(cmsService.getMarketSwitcherFlagValue).toHaveBeenCalled();
          flag = true;
          expect(component.isMarketSwitcherConfigured).toBe(true);
          expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        });
    });
    it('should set isMarketSwitcherConfigured to false if cmsService getMarketSwitcherFlagValue return false', () => {
      component.sportName = 'darts';
      cmsService.getMarketSwitcherFlagValue.subscribe = jasmine.createSpy('cmsService.getMarketSwitcherFlagValue')
        .and.callFake((flag) => {
          expect(cmsService.getMarketSwitcherFlagValue).toHaveBeenCalled();
          flag = false;
          expect(component.isMarketSwitcherConfigured).toBe(false);
          expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        });
    });
  });

  describe('#showMoreSport', () => {
    let competitionSection;

    beforeEach(() => {
      competitionSection = [
        { typeId: 1 }, { typeId: 2 }
      ] as any;
      component.loadCompetionSection = jasmine.createSpy().and.returnValue(observableOf({}));
      component.toggleCompetitionSection = jasmine.createSpy();
      component.expandedLeaguesCount = 1;
      component.inner = true;
    });
    it('with virtual scroll', () => {
      component.virtualScroll = true;
      component.showMoreSport(competitionSection);
      expect(component.loadCompetionSection).toHaveBeenCalledWith({ typeId: 2, isExpanded: true } as any, competitionSection);
      expect(component.expandedFlags[2]).toBeTruthy();
      expect(component.isAllExpanded).toBeTruthy();
      expect(competitionSection[1].isExpanded).toBeTruthy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('without virtual scroll', () => {
      component.virtualScroll = false;
      component.showMoreSport(competitionSection);
      expect(component.loadCompetionSection).toHaveBeenCalledTimes(1);
      expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalledTimes(1);
      expect(component.expandedFlags[2]).toBeTruthy();
      expect(component.subscriptionFlags[2]).toBeTruthy();
      expect(component.isAllExpanded).toBeTruthy();
      expect(competitionSection[1].isExpanded).toBeTruthy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should not run any logic if is not inner', () => {
      component.inner = false;
      component.showMoreSport(competitionSection);
      expect(component.toggleCompetitionSection).not.toHaveBeenCalled();
      expect(component.loadCompetionSection).not.toHaveBeenCalled();
      expect(component.isAllExpanded).toBeFalsy();
    });
  });

  describe('#goToCompetition', () => {
    it('should redirect to competition', () => {
      component.goToCompetition({} as any);
      expect(routingHelperService.formCompetitionUrl).toHaveBeenCalled();
    });
  });

  describe('#setCompetitionPagesAvailability', () => {
    it('should set competitionsAvailability as false', () => {
      component.competitionsWithPages = {} as any;
      component.eventsBySports.eventsByTypeName = [{
        events: [{
          classId: 'someClassId'
        }]
      } as any];
      component.setCompetitionPagesAvailability();
      expect(component.competitionsAvailability).toEqual({
        someClassId: false
      } as any);
    });
  });

  describe('#loadCompetionSection', () => {
    it('when marketSelector is not present in competitionSection', () => {
      component.setCompetitionPagesAvailability = jasmine.createSpy();
      const competitionSections = [{ id: 1 }, { id: 2 }];
      inPlayMainService['_getCompetitionData'].and.returnValue(observableOf(competitionSections));
      const competitionSection = {
        typeId: '01',
        events: [
          {
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      } as any;
      const sectionsArray = [
        {
          typeId: '01',
          marketSelector: 'marketSelector',
          events: [
            {
              cashoutAvail: 'cashoutAvail',
              categoryCode: 'categoryCode',
              categoryId: 'categoryId'
            }
          ]
        },
        {
          typeId: '02',
          marketSelector: 'marketSelector',
          events: [
            {
              cashoutAvail: 'cashoutAvail',
              categoryCode: 'categoryCode',
              categoryId: 'categoryId'
            }
          ]
        }
      ] as any[];
      component.loadCompetionSection(competitionSection, sectionsArray, false).subscribe();
      expect(component.setCompetitionPagesAvailability).toHaveBeenCalled();
      expect(competitionSection.eventsIds).toEqual([1, 2]);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
    it('when competitionEvents is 0', () => {
      component.setCompetitionPagesAvailability = jasmine.createSpy();
      inPlayMainService['_getCompetitionData'].and.returnValue(observableOf([]));
      const competitionSection = {
        typeId: '01',
        events: [
          {
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      } as any;
      const sectionsArray = [
        {
          typeId: '01',
          marketSelector: 'marketSelector',
          events: [
            {
              cashoutAvail: 'cashoutAvail',
              categoryCode: 'categoryCode',
              categoryId: 'categoryId'
            }
          ]
        },
        {
          typeId: '02',
          marketSelector: 'marketSelector',
          events: [
            {
              cashoutAvail: 'cashoutAvail',
              categoryCode: 'categoryCode',
              categoryId: 'categoryId'
            }
          ]
        }
      ] as any[];
      component.loadCompetionSection(competitionSection, sectionsArray, false).subscribe();
      expect(sectionsArray).toBeDefined();
    });
    it('when competitionEvents is not 0', () => {
      component.setCompetitionPagesAvailability = jasmine.createSpy();
      const competitionSections = [{ id: 1 }, { id: 2 }];
      inPlayMainService['_getCompetitionData'].and.returnValue(observableOf(competitionSections));
      const competitionSection = {
        typeId: '01',
        events: [
          {
            id: 1,
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      } as any;
      const sectionsArray = {
        id: 1,
        cashoutAvail: 'cashoutAvail',
        categoryCode: 'categoryCode',
        categoryId: 'categoryId'
      } as any;
      component.loadCompetionSection(competitionSection, sectionsArray, false).subscribe();
      expect(competitionSection.events[0].isExpanded).toBeTrue();
      expect(competitionSection.events[0].competitionSection).toEqual(competitionSection);
    });
    describe('#prefetchNext', () => {
      beforeEach(() => {
        component.loadCompetionSection = jasmine.createSpy().and.returnValue(observableOf({}));
      });
      const competitionSection = {
        typeId: '01',
        marketSelector: 'marketSelector',
        events: [
          {
            cashoutAvail: 'cashoutAvail',
            categoryCode: 'categoryCode',
            categoryId: 'categoryId'
          }
        ]
      } as any;
      it('when isAllExpanded true', () => {
        component.isAllExpanded = true;
        component.expandedFlags = {
          '01': false
        };
        component.prefetchNext(competitionSection);
        expect(component.loadCompetionSection).toHaveBeenCalled();
        expect(component.expandedFlags['01']).toBeTruthy();
        expect(competitionSection.isExpanded).toBeTruthy();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });
      it('when isAllExpanded false', () => {
        component.isAllExpanded = false;
        component.prefetchNext(competitionSection);
        expect(component.loadCompetionSection).not.toHaveBeenCalled();
      });
      it('when isAllExpanded true and isExpanded true', () => {
        component.isAllExpanded = true;
        component.expandedFlags = {
          '01': true
        };
        component.prefetchNext(competitionSection);
        expect(component.loadCompetionSection).not.toHaveBeenCalled();
        expect(component.expandedFlags['01']).toBeTruthy();
      });
    });
  });

  describe('#handleLiveUpdatesSubscriptions', () => {
    beforeEach(() => {
      component.loadCompetionSection = jasmine.createSpy().and.returnValue(observableOf([]));
    });
    const competitionSection = {
      typeId: '01',
      marketSelector: 'marketSelector',
      events: [
        {
          cashoutAvail: 'cashoutAvail',
          categoryCode: 'categoryCode',
          categoryId: 'categoryId'
        }
      ]
    } as any;
    it('when event is visible with reloadData flag true and competition is not subscribed', () => {
      const event = {
        visible: true,
        reloadData: true
      } as any;
      component.handleLiveUpdatesSubscriptions(event, competitionSection);
      expect(component.loadCompetionSection).toHaveBeenCalled();
      expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalled();
      expect(component.subscriptionFlags['01']).toBeTruthy();
    });
    it('when event is visible with reloadData flag true and competition is subscribed', () => {
      const event = {
        visible: true,
        reloadData: true
      } as any;
      component.subscriptionFlags = {
        '01': true
      };
      component.handleLiveUpdatesSubscriptions(event, competitionSection);
      expect(component.loadCompetionSection).toHaveBeenCalled();
      expect(inPlayMainService.subscribeForUpdates).not.toHaveBeenCalled();
    });
    it('when event is visible with reloadData flag false and competition is not subscribed', () => {
      const event = {
        visible: true,
        reloadData: false
      } as any;
      component.handleLiveUpdatesSubscriptions(event, competitionSection);
      expect(component.loadCompetionSection).not.toHaveBeenCalled();
      expect(inPlayMainService.subscribeForUpdates).toHaveBeenCalled();
      expect(component.subscriptionFlags['01']).toBeTruthy();
    });
    it('when event is visible with reloadData flag false and competition is subscribed', () => {
      const event = {
        visible: true,
        reloadData: false
      } as any;
      component.subscriptionFlags['01'] = true;
      component.handleLiveUpdatesSubscriptions(event, competitionSection);
      expect(component.loadCompetionSection).not.toHaveBeenCalled();
      expect(inPlayMainService.subscribeForUpdates).not.toHaveBeenCalled();
      expect(component.subscriptionFlags['01']).toBeTruthy();
    });
    it('when event is not visible', () => {
      const event = {
        visible: false
      } as any;
      component.handleLiveUpdatesSubscriptions(event, competitionSection);
      expect(inPlayMainService.unsubscribeForEventsUpdates).toHaveBeenCalled();
      expect(component.subscriptionFlags['01']).toBeFalsy();
    });
  });

  describe('#isFirstMarketSelected', () => {
    it('should return true', () => {
      component.selectedMarketName = 'Match Betting';
      expect(component['isFirstMarketSelected']()).toBe(true);
    });
    it('should return false', () => {
      component.selectedMarketName = 'Main Market';
      expect(component['isFirstMarketSelected']()).toBe(true);
    });
    it('should return false', () => {
      component.selectedMarketName = '321';
      expect(component['isFirstMarketSelected']()).toBe(false);
    });
  });

  describe('#calculateIsAllExpanded', () => {
    it('should set isAllExpanded to true', () => {
      component.isAllExpanded = false;
      component.expandedFlags = [
        { isExpanded: true },
        { isExpanded: true }
      ];
      component['calculateIsAllExpanded']();
      expect(component.isAllExpanded).toBe(true);
    });
  });

  describe('#extendSectionData', () => {
    beforeEach(() => {
      component['setCompetitionPagesAvailability'] = jasmine.createSpy();
      component.eventsBySports = { test: 'any' } as any;
      component.sportInstance = { test: 'any' } as any;
    });

    it('should call extendSectionWithSportInstance and setCompetitionPagesAvailability', () => {
      component['extendSectionData'](true);

      expect(inPlayMainService.extendSectionWithSportInstance).toHaveBeenCalledWith(component.eventsBySports, component.sportInstance);
      expect(component['setCompetitionPagesAvailability']).toHaveBeenCalled();
    });

    it('should call extendSectionWithSportInstance but not setCompetitionPagesAvailability', () => {
      component['extendSectionData'](false);

      expect(inPlayMainService.extendSectionWithSportInstance).toHaveBeenCalledWith(component.eventsBySports, component.sportInstance);
      expect(component['setCompetitionPagesAvailability']).not.toHaveBeenCalled();
    });

    it('should not call extendSectionWithSportInstance and setCompetitionPagesAvailability when ' +
      'eventsBySports is undefined', () => {
        component.eventsBySports = undefined;
        component['extendSectionData'](true);

        expect(inPlayMainService.extendSectionWithSportInstance).not.toHaveBeenCalled();
        expect(component['setCompetitionPagesAvailability']).not.toHaveBeenCalled();
      });

    it('should not call extendSectionWithSportInstance and setCompetitionPagesAvailability when ' +
      'sportInstance is undefined', () => {
        component.sportInstance = undefined;
        component['extendSectionData'](true);

        expect(inPlayMainService.extendSectionWithSportInstance).not.toHaveBeenCalled();
        expect(component['setCompetitionPagesAvailability']).not.toHaveBeenCalled();
      });

    it('should not call extendSectionWithSportInstance and setCompetitionPagesAvailability ' +
      'when eventsBySports and sportInstance is undefined', () => {
        component.eventsBySports = undefined;
        component.sportInstance = undefined;
        component['extendSectionData'](true);

        expect(inPlayMainService.extendSectionWithSportInstance).not.toHaveBeenCalled();
        expect(component['setCompetitionPagesAvailability']).not.toHaveBeenCalled();
      });
  });

  describe('#trackByTypeId', () => {
    it('should return typeId', () => {
      const item = {
        typeId: '123'
      };
      expect(component['trackByTypeId'](1, item)).toEqual('123');
    });
  });

  describe('#trackByEventId', () => {
    it('should return id', () => {
      const item = {
        id: '123'
      };
      expect(component['trackByEventId'](1, item)).toEqual('1231');
    });
  });
});

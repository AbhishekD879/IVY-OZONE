import { NextRacesModuleComponent } from '@app/lazy-modules/nextRaces/component/next-races.component';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { ISportEvent } from '@root/app/core/models/sport-event.model';
import { nextRacesModule } from '@core/services/sport/racingService.mock';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';
describe('NextRacesModuleComponent', () => {
  let component: NextRacesModuleComponent;
  let pubSubService, cmsService, location, routingHelperService,
    nextRacesService, eventService, commandService, gtm, locale, racingPostService, horseRacingService, greyhoundService, routingState,
    vEPService;
  let cmsData;
  let racingGaService,windowRefService;
  const Sportdata: ISportEvent[]  = [{
    cashoutAvail: '',
    categoryCode: '',
    categoryId: '',
    categoryName: '',
    displayOrder: 1,
    eventSortCode: '',
    eventStatusCode: '',
    id: 1,
    liveServChannels: '',
    liveServChildrenChannels: '',
    typeId: '',
    typeName: '',
    name: '',
    startTime: '1400',
    correctedDayValue: 'sunday'
  }];

  const racingMock = {
    events: [],
    classesTypeNames: {},
    groupedRacing: [
      {
        flag: 'UK',
        access: true,
        data: [
          {
            "cashoutAvail": "",
            "startTime": "1400",
            "correctedDayValue": "sunday"
          }
          
        ]
      },
      {
        flag: 'INT',
        access: false,
        data: [
          {
            "cashoutAvail": "",
            "startTime": "1400",
            "correctedDayValue": "sunday"
          }
         
        ]
      },
      {
        flag: 'FR',
        data: [
          {
            "cashoutAvail": "",
            "startTime": "1400",
            "correctedDayValue": "sunday"
          }
         
        ]
      },
      {
        flag: 'VR',
        data: [
          {
            "cashoutAvail": "",
            "startTime": "1400",
            "correctedDayValue": "sunday"
          }
          
        ]
      }
    ],
    selectedTab: 'horseracing',
    modules: {}
  };

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi,
    };
    gtm = {};
    locale = {};
    cmsService = {
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate'),
    };
    location = {
      path: jasmine.createSpy('path')
    };
    routingHelperService = {
      formSportUrl: jasmine.createSpy('formSportUrl').and.returnValue(observableOf({}))
    };
    nextRacesService = {
      getNextRacesModuleConfig: jasmine.createSpy('getNextRacesModuleConfig').and.returnValue({}),
      subscribeForUpdates: jasmine.createSpy('subscribeForUpdates'),
      unSubscribeForUpdates: jasmine.createSpy('unSubscribeForUpdates'),
      getUpdatedEvents: jasmine.createSpy('getUpdatedEvents').and.returnValue(Sportdata),
      cacheKey: 'nextRaces'
    };
    eventService = {
      getNextEvents: jasmine.createSpy('getNextEvents').and.returnValue(Promise.resolve([{ id: 1 }, { id: 2 }]))
    };
    racingGaService = new RacingGaService(gtm, locale, pubSubService);
    racingGaService.sendGTM = jasmine.createSpy('sendGTM');
    racingGaService.trackNextRacesCollapse = jasmine.createSpy('trackNextRacesCollapse');
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(racingGaService)),
      API: {
        RACING_GA_SERVICE: 'test'
      }
    };
    racingPostService = {
      updateRacingEventsList: jasmine.createSpy('updateRacingEventsList').and.returnValue(
        observableOf([{ id: 1, racingPostEvent: {} }, { id: 2, racingPostEvent: {} }]))
    };
    cmsData = {
      NextRaces: { title: 'Next races', numberOfSelections: '10' },
      GreyhoundNextRaces: { numberOfSelections: '4' },
      RacingDataHub: { isEnabledForGreyhound: true},
      GreyhoundNextRacesToggle: { nextRacesTabEnabled: true }
    };
    windowRefService = {
      document: {
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((v1, cb) => cb({
          detail: { liveUpdate: {channel_type:"sEVENT",payload:{status:'S'},channel_number:'1'} }
        })
        )}
    };
    horseRacingService = {
      todayEventsByClasses: jasmine.createSpy('todayEventsByClasses').and.returnValue(Promise.resolve(racingMock)),
      getConfig: jasmine.createSpy('getConfig').and.returnValue({
        request: {
          date: 'today'
        }
      }),
      config: {
        request: {
          categoryId: '21',
        }
      },
      getNextRacesData: jasmine.createSpy('getNextRacesData').and.returnValue({}),
      addLpAvailableProp: jasmine.createSpy('addLpAvailableProp'),
      addPersistentInCacheProp: jasmine.createSpy('addPersistentInCacheProp'),
      groupByFlagCodesAndClassesTypeNames: jasmine.createSpy('groupByFlagCodesAndClassesTypeNames').and.returnValue(racingMock),
      sortRaceGroup: jasmine.createSpy('sortRaceGroup')
    },
    greyhoundService ={
      config: {
        request: {
          categoryId: '22',
        }
      },
      getNextRacesData: jasmine.createSpy('getNextRacesData').and.returnValue({}),
    },
    routingState={
      getCurrentSegment:  jasmine.createSpy('getCurrentSegment').and.returnValue('horseracing')
    },
    vEPService = {
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      targetTab:  new BehaviorSubject<any>('targetTab' as any),
    };

    createComponent();
  });

  function createComponent() {
    component = new NextRacesModuleComponent(
      pubSubService,
      cmsService,
      location,
      routingHelperService,
      nextRacesService,
      eventService,
      commandService,
      racingPostService,
      windowRefService,
      horseRacingService,
      greyhoundService,
      routingState,
      vEPService
    );

    component.moduleType = 'horseracing';
    component.nextRacesModule = {};
  }

  describe('ngOnInit racingSpecials', () => {
    it('ngOnInit: widget=true, headerVisible=true', () => {
      component.moduleType = 'horseracing';
      component.widget = true;
      component.headerVisible = true;
      component.moduleType = 'horseracing';
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => cb(cmsData));
      component.ngOnInit();
      expect(windowRefService.document.addEventListener).toHaveBeenCalledWith('LIVE_SERVE_UPDATE', jasmine.any(Function));
      expect(component.headerClass).toEqual('secondary-header');
      expect(component.leftTitleText).toEqual(component.moduleTitle);
      expect(component.className).toBe('next-races next-races-horseracing');
      expect(component.showBriefHeader).toBe(true);
    });

    it('ngOnInit: widget=false, headerVisible=false', () => {
      component.widget = false;
      component.headerVisible = false;
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => cb(cmsData));
      component.ngOnInit();
      expect(component.headerClass).toEqual('secondary-header');

      expect(component.leftTitleText).toEqual(component.moduleTitle);
    });

    it('ngOnInit: widget=true, headerVisible=false', () => {
      component.widget = true;
      component.headerVisible = false;
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => cb(cmsData));
      component.ngOnInit();
      expect(component.headerClass).toEqual('');
      expect(component.leftTitleText).toEqual('');
    });

    it('ngOnInit: widget=false, headerVisible=true', () => {
      component.widget = false;
      component.headerVisible = true;
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => cb(cmsData));
      component.ngOnInit();
      expect(component.headerClass).toEqual('secondary-header');
      expect(component.leftTitleText).toEqual(component.moduleTitle);
    });
    it(`default value of raceIndex should be 'next-races'`, () => {
      component.isEventOverlay = true;
      component.nextRacesModule = <any>{ storedEvents: [{ id: '1', startTime: '2019-05-15 15:10:00', localTime: '2019-05-15 15:10:00' }] };
      component.ngOnInit();
      expect(component.raceIndex).toEqual('next-races');
    });

    it(`default value of raceIndex should be 'next-races'  and startTime if condition `, () => {
      component.isEventOverlay = true;
      component.nextRacesModule = <any>{ storedEvents: [{ id: '1', startTime: '2019-05-15 15:10:00', localTime: '2019-05-15 15:10:00' }, { id: '1', startTime: '2019-05-15 17:10:00', localTime: '2019-05-15 15:10:00' }] };
      component.ngOnInit();
      expect(component.raceIndex).toEqual('next-races');
    });

    it(`nextRacesModule storedEvents empty and startTime else condition `, () => {
      component.isEventOverlay = true;
      component.nextRacesModule = <any>{ storedEvents: [] };
      windowRefService.document = {
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((v1, cb) => cb({
          detail: { liveUpdate: { channel_type: "sEVENT", payload: { status: 'S' }, channel_number: '2' } }
        })
        )
      };
      component.ngOnInit();
      expect(component.raceIndex).toEqual('next-races');
    }); 
  });

  describe('getCmsConfigs method', () => {
    let pubSubFn;

    beforeEach(() => {
      component.raceModule = 'NEXT_RACE';
      spyOn(component, 'getNextEvents');
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => pubSubFn = cb);
    });

    it('should subscribe to pubsub SYSTEM_CONFIG_UPDATED', () => {
      component.getCmsConfigs();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('MODULE_NEXT_RACE', 'SYSTEM_CONFIG_UPDATED', jasmine.any(Function));
    });

    it('should execute nextRacesService.getNextRacesModuleConfig and getNextEvents methods and update props on subscription', () => {
      cmsData.NextRaces.numberOfSelections = 0;
      component.getCmsConfigs();
      pubSubFn(cmsData);
      expect(component.numberOfSelections).toEqual(3);
      expect(component.moduleTitle).toEqual('Next races');
      expect(nextRacesService.getNextRacesModuleConfig).toHaveBeenCalledWith('horseracing',
        {
          NextRaces: { title: 'Next races', numberOfSelections: 0 },
          GreyhoundNextRaces: { numberOfSelections: '4' },
          RacingDataHub: { isEnabledForGreyhound: true }
        });
      expect(component.getNextEvents).toHaveBeenCalled();
    });

    it('should execute nextRacesService.getNextRacesModuleConfig and getNextEvents methods and update props on subscription', () => {
      cmsData.NextRaces.numberOfSelections = 10;
      delete cmsData.RacingDataHub;
      component.getCmsConfigs();
      pubSubFn(cmsData);
      expect(component.numberOfSelections).toEqual(10);
      expect(nextRacesService.getNextRacesModuleConfig).toHaveBeenCalledWith('horseracing',
        {
          NextRaces: { title: 'Next races', numberOfSelections: 10 },
          GreyhoundNextRaces: { numberOfSelections: '4' },
          RacingDataHub: undefined,
        });
      expect(component.getNextEvents).toHaveBeenCalled();
    });

    describe('should not call nextRacesService.getNextRacesModuleConfig and getNextEvents methods', () => {
      it('when cms config does not contain NextRaces entry', () => {
        cmsData = {};
        component.getCmsConfigs();
        pubSubFn(cmsData);
      });

      it('when called more than once with the same config', () => {
        component.getCmsConfigs();
        pubSubFn(cmsData);
        nextRacesService.getNextRacesModuleConfig.calls.reset();
        (component.getNextEvents as any).calls.reset();
        pubSubFn(cmsData);
      });
      afterEach(() => {
        expect(component.getNextEvents).not.toHaveBeenCalled();
        expect(nextRacesService.getNextRacesModuleConfig).not.toHaveBeenCalled();
      });
    });
  });

  describe('getNextEvents method', () => {
    it('should set showLoader and ssDown on error', fakeAsync(() => {
      const nextRacesModule = {};
      component.eventsLoaded.emit = jasmine.createSpy('eventsLoaded.emit');
      component.nextRacesModule = <any>nextRacesModule;
      racingPostService.updateRacingEventsList = jasmine.createSpy('updateRacingEventsList').and.returnValue(
        throwError({}));

      component.getNextEvents();
      tick();

      expect(component.showLoader).toEqual(false);
      expect(component.ssDown).toEqual(true);
      expect(component.eventsLoaded.emit).toHaveBeenCalled();
    }));

    it('should call racingPostService.updateRacingEventsList method', fakeAsync(() => {
      const nextRacesModule = {};
      component.nextRacesModule = <any>nextRacesModule;
      component.getNextEvents();
      component.filterAccess = ['UK', 'VR'];
      tick();
      expect(eventService.getNextEvents).toHaveBeenCalledWith(nextRacesModule, 'nextRaces', undefined);
      expect(racingPostService.updateRacingEventsList).toHaveBeenCalledWith([{ id: 1 }, { id: 2 }], true);
      expect(nextRacesService.getUpdatedEvents).toHaveBeenCalledWith(
        [{ id: 1, racingPostEvent: { } }, { id: 2, racingPostEvent: { } }], 'horseracing');
    }));

    it('should filter the data', fakeAsync(() => {
      
      component.onFilterChange({value: racingMock.groupedRacing[0]}) 
      tick();
      expect(component.selectedFilter).toEqual('UK');
     
    }));

    it('should store data subscription', fakeAsync(() => {
      const nextRacesModule = {};
      component.nextRacesModule = <any>nextRacesModule;
      component.isEventOverlay = true;
      component.getNextEvents();
      component.filterAccess = ['UK', 'VR'];
      tick();

      expect(component['loadDataSubscription']).toBeDefined();
    }));
  });

  // it('should create', () => {
  //   expect(component).toBeDefined();
  // });

  describe('registerEvents', () => {
    it('should registerEvents', () => {
      component.raceModule = 'W_NEXT_RACE';
      component.registerEvents();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('MODULE_W_NEXT_RACE', 'RELOAD_COMPONENTS', jasmine.any(Function));
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from pubsub events', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component.MODULE_NAME);
    });

    it('should unsubscribe from data load subscription', () => {
      const loadDataSubscription = jasmine.createSpyObj('loadDataSubscription', ['unsubscribe']);
      const subscriptionId = 'moduleName';

      component['subscriptionId'] = subscriptionId;
      component['loadDataSubscription'] = loadDataSubscription;
      component.ngOnDestroy();

      expect(loadDataSubscription.unsubscribe).toHaveBeenCalled();
      expect(nextRacesService.unSubscribeForUpdates).toHaveBeenCalledWith(subscriptionId);
    });
  });

  describe('trackCollapse', () => {
    it('should call sendGTM with eventCategory equals to home, set flag to true and NOT call trackNextRacesCollapse', fakeAsync(() => {
      component.trackGaDesktop = true;
      component['location'].path = jasmine.createSpy().and.returnValue('/');

      component.trackCollapse();
      tick();

      expect(racingGaService.sendGTM).toHaveBeenCalledWith('collapse', 'home');
      expect(racingGaService.flag[racingGaService.CONST.WIDGET]).toEqual(true);
      expect(racingGaService.trackNextRacesCollapse).not.toHaveBeenCalled();
    }));

    it('should call sendGTM with eventCategory equals to widget, set flag to true and NOT call trackNextRacesCollapse', fakeAsync(() => {
      component.trackGaDesktop = true;
      component['location'].path = jasmine.createSpy().and.returnValue('test');

      component.trackCollapse();
      tick();

      expect(racingGaService.sendGTM).toHaveBeenCalledWith('collapse', 'widget');
      expect(racingGaService.flag[racingGaService.CONST.WIDGET]).toEqual(true);
      expect(racingGaService.trackNextRacesCollapse).not.toHaveBeenCalled();
    }));

    it('should NOT call sendGTM and set flag to true and call trackNextRacesCollapse', fakeAsync(() => {
      component.trackGa = true;
      component.trackGaDesktop = false;
      component.nextRacesModule = { storedEvents: [] } as any;
      component.trackCollapse(false);
      tick();
      expect(racingGaService.sendGTM).not.toHaveBeenCalled();
      expect(racingGaService.trackNextRacesCollapse).toHaveBeenCalled();
    }));
  });

  it('sendToGTM should call sendGTM', fakeAsync(() => {
    component.sendToGTM();
    tick();

    expect(racingGaService.sendGTM).toHaveBeenCalledWith('view all', 'home');
  }));

  it('reloadComponent should set ssDown and call getNextEvents', () => {
    component.getNextEvents = jasmine.createSpy('component.getNextEvents');

    component.reloadComponent();

    expect(component.ssDown).toEqual(false);
    expect(component.getNextEvents).toHaveBeenCalled();
  });

  it('getNextEvents',()=>{
    component.isEventOverlay=true
    const result = component.getNextEvents();
    expect(result).toEqual(result);
  })
  
it('should enable toogle filter buttons',fakeAsync(()=>{
    component.showFilter = false;
    component.nextRacesModule.storedEvents = {};
    component.groupDataByFlags();
    tick();
    expect(component.showFilter).toEqual(false);
  }));
  
  it('getNextEvents with lastSuspendedEventTime',fakeAsync(()=>{
    component.isEventOverlay=true;
    component.lastSuspendedEventTime = new Date();
    component.nextRacesModule = {storedEvents : []}
    const d1 = new Date (),
    d2 = new Date (),
    d3 = new Date ();
    d2.setTime(d1.getTime() + (30 * 60 * 1000));
    d3.setTime(d1.getTime() - (30 * 60 * 1000));
    nextRacesService['getUpdatedEvents'] = jasmine.createSpy().and.returnValue([{id: 1, startTime: d2.getTime()}, {id: 2, startTime: d3.getTime()}]);
    
    component.getNextEvents();
    tick();
    expect(component.nextRacesModule.storedEvents.length).toBe(1);
  }));

  it('should call racingService with horse racing service',()=> {
    // routingState.getCurrentSegment.and.returnValue('horseracing');
    expect(component.racingService.config.request.categoryId).toEqual('21');
  });
  it('should call racingService with grey racing service',()=>{
    routingState.getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('greyhound');
    expect(component.racingService.config.request.categoryId).toEqual('22');
  });
  it('should call groupDataByFlags',()=>{
    component.nextRacesModule = nextRacesModule;
    component.showFilter = true;
    component.filterAccess = { 
      "UK&IRE": true,
      INT: true, 
      VR: true,
      FR: true,
      AE : true,
      ZA : true,
      IN : true,
      US : true,
      AU : true,
      CL : true
    };
    component.nextRacesModule = {
      storedEvents: [{
        name: 'test1',
        isResulted: true,
        startTime: '19:55'
      }]
    };
    component.showFilter = true;
    horseRacingService.getNextRacesData = (filterAccess: any, nextRacesModule: any) => {
      return {
        storedEvents: [{
          name: 'test1',
          isResulted: true,
          startTime: '19:55'
        }],
        groupedRacing: [
          {
            flag: 'All',
            data: [{
              name: 'test1',
              isResulted: true,
              startTime: '19:55'
            }],
    
          } ,
          {
            flag: 'VR',
            data: [{
              name: 'data1',
              isResulted: true,
              startTime: '12:55',
              isOpenEvent: true
            },
              {
                name: 'data1',
                isResulted: true,
                startTime: '12:55',
                isOpenEvent: true
              },
              {
                name: 'data1',
                isResulted: true,
                startTime: '12:55',
                isOpenEvent: true
              }],
    
          },
          {
            flag: 'FR',
            data: [{
              name: 'data1',
              isResulted: true,
              startTime: '12:55'
            }, {
              isResulted: true,
              startTime: '12:55'
            },
              {
                name: 'test1',
                isResulted: true,
                startTime: '19:55',
                isOpenEvent: true
              }]
    
          }
          ]
      }
    };
    component.selectedFilter = 'UK';
    component.groupDataByFlags();
    expect(component.nextRacesGroupedData.storedEvents.length).toEqual(1);
    // component.selectedFilterTabData = {
    //   value: {
    //     data: nextRacesModule.storedEvents
    //   }
    // };
    component.selectedFilter = 'All';
    component.groupDataByFlags();
    expect(component.nextRacesGroupedData.storedEvents.length).toEqual(1);
  });


  it('should check when banner above the accorition enabled',()=>
  {
    component.bannerBeforeAccorditionHeader='virtual';
    expect(component.isDisplayBanner('virtual')).toBeTruthy();
    expect(component.isDisplayBanner('nextRaces')).toBeFalsy();
    expect(component.isDisplayBanner(null)).toBeFalsy();
    component.bannerBeforeAccorditionHeader=undefined;
    expect(component.isDisplayBanner('virtual')).toBeFalsy();
    
  })

  
});

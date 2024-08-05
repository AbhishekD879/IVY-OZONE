import { NextRacesHomeComponent } from './next-races-home.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';

describe('#NextRacesHomeComponent', () => {
  let component: NextRacesHomeComponent;
  let nextRacesHomeService;
  let pubSubService;
  let cmsService;
  let eventService;
  let racingPostService;
  let cmsData;
  let updateEventService;
  let deviceService;
  let routingHelperService;
  let router;
  let horseRacingService;
  let greyhoundService;
  let routingState;
  let windowRefService;

  
  const racingMock = {
    events: [],
    classesTypeNames: {},
    groupedRacing: [
      {
        flag: 'UK',
        access: true,
        data: [
          {"id": "123",
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
            "id": "456",
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
            "id": "789",
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
            "id": "012",
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

  beforeEach(fakeAsync(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake(((a, b, cb) => cb && cb(cmsData))),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SYSTEM_CONFIG_UPDATED: 'SYSTEM_CONFIG_UPDATED',
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS',
        SCHEMA_DATA_UPDATED:'SCHEMA_DATA_UPDATED',
        SCHEMA_DATA_REMOVED:'SCHEMA_DATA_REMOVED',
        NEXT_RACES_DATA:'NEXT_RACES_DATA'
      }
    };
    eventService = {
      getNextEvents: jasmine.createSpy('getNextEvents').and.returnValue(Promise.resolve([{ id: 1 }, { id: 2 }]))
    };
    nextRacesHomeService = {
      unSubscribeForUpdates: jasmine.createSpy('unSubscribeForUpdates'),
      subscribeForUpdates: jasmine.createSpy('subscribeForUpdates'),
      getUpdatedEvents: jasmine.createSpy('getUpdatedEvents'),
      getNextRacesModuleConfig: jasmine.createSpy('getNextRacesModuleConfig').and.returnValue({}),
      sendGTM: jasmine.createSpy('sendGTM').and.returnValue(''),
      cacheKey: 'nextRaces'
    };
    cmsService = {
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate')
    };
    racingPostService = {
      updateRacingEventsList: jasmine.createSpy('updateRacingEventsList').and.returnValue(
        observableOf([{ id: 1, racingPostEvent: {} }, { id: 2, racingPostEvent: {} }]))
    };
    router = {
      url : jasmine.createSpy('url').and.returnValue('/horse-racing/featured')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('/horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/')
    };
    deviceService = {
      isRobot: jasmine.createSpy('isRobot').and.returnValue(true)
    };
    cmsData = {
      NextRaces: { title: 'Next races', numberOfSelections: '10' },
      GreyhoundNextRaces: { numberOfSelections: '4' },
      RacingDataHub: { isEnabledForGreyhound: true },
      GreyhoundNextRacesToggle: { nextRacesTabEnabled: true }
    };
    updateEventService = {};

    greyhoundService ={
      config: {
        request: {
          categoryId: '22',
        }
      },
      getNextRacesData: jasmine.createSpy('getNextRacesData').and.returnValue(Promise.resolve({}))
    },

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
      addLpAvailableProp: jasmine.createSpy('addLpAvailableProp'),
      addPersistentInCacheProp: jasmine.createSpy('addPersistentInCacheProp'),
      groupByFlagCodesAndClassesTypeNames: jasmine.createSpy('groupByFlagCodesAndClassesTypeNames').and.returnValue(racingMock),
      sortRaceGroup: jasmine.createSpy('sortRaceGroup'),
      getNextRacesData: jasmine.createSpy('getNextRacesData').and.returnValue({
        groupedRacing: [{flag: 'All', data: []}]
      })
    },
 
    routingState={
      getCurrentSegment:  jasmine.createSpy('getCurrentSegment').and.returnValue('horseracing')
    }

    windowRefService = {
      document: {
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((v1, cb) => cb({
          detail: { liveUpdate: {channel_type:"sEVENT",payload:{status:'S'},channel_number:'1'} }
        })
        )}
    };

    component = new NextRacesHomeComponent(
      pubSubService,
      cmsService,
      nextRacesHomeService,
      eventService,
      racingPostService,
      deviceService,
      routingHelperService,
      router,
      updateEventService,
      horseRacingService,
      greyhoundService,
      routingState,
      windowRefService
    );

    component.raceModule = 'NEXT_RACE';
    component.moduleType = 'horseracing';
    component.nextRacesModule = {};
  }));

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should get events for horce racing', () => {
      component.ngOnInit();

      expect(component.raceModule).toEqual('NEXT_RACE');
      expect(component.className).toEqual('next-races-horseracing');
      expect(component.showTimer).toEqual(true);
      expect(component.raceEvent).toEqual('Horse Racing');
      expect(cmsService.triggerSystemConfigUpdate).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(3);
    });

    it('should get events for grayhounds', () => {
      component.moduleType = 'greyhounds';
      component.ngOnInit();
      expect(component.raceEvent).toBe('Greyhounds');
    });
    
    it(`default value of raceIndex should be 'next-races'`, () => {
      component.moduleType = 'horseracing';
      component.nextRacesModule = <any>{ storedEvents: [{ id: '1', startTime: '2019-05-15 15:10:00', localTime: '2019-05-15 15:10:00' }] };
      component.registerEvents = () => {};
      component.getCmsConfigs = () => {};
      component.ngOnInit();
      expect(component.raceEvent).toBe('Horse Racing');
    });

    it(`default value of raceIndex should be 'next-races'  and startTime if condition `, () => {
      component.moduleType = 'horseracing';
      component.registerEvents = () => {};
      component.getCmsConfigs = () => {};
      component.nextRacesModule = <any>{ storedEvents: [{ id: '1', startTime: '2019-05-15 15:10:00', localTime: '2019-05-15 15:10:00' }, { id: '1', startTime: '2019-05-15 17:10:00', localTime: '2019-05-15 15:10:00' }] };
      component.ngOnInit();
      expect(component.raceEvent).toBe('Horse Racing');
    });
  });

  it('#ngOnDestroy', () => {
    component['eventsSubscription'] = { unsubscribe: jasmine.createSpy('unsubscribe') } as any;
    spyOn(component as any,'removeSchemaForGHNextRaces');
    component.ngOnDestroy();

    expect(nextRacesHomeService.unSubscribeForUpdates).toHaveBeenCalled();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('MODULE_NEXT_RACE');
    expect(component['eventsSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['removeSchemaForGHNextRaces']).toHaveBeenCalled();
  });

  it('#sendToGTM', () => {
    component.sendToGTM();

    expect(nextRacesHomeService.sendGTM).toHaveBeenCalledWith('view all', 'home');
  });

  describe('getCmsConfigs method', () => {
    let pubSubFn;

    beforeEach(() => {
      spyOn(component, 'getNextEvents');
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => pubSubFn = cb);
    });

    it('should subscribe to pubsub SYSTEM_CONFIG_UPDATED', () => {
      component.getCmsConfigs();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('MODULE_NEXT_RACE', 'SYSTEM_CONFIG_UPDATED', jasmine.any(Function));
    });

    it('should filter the data', fakeAsync(() => {
      
      component.onFilterChange(racingMock.groupedRacing[0]) 
      tick();
      expect(component.selectedFilter).toEqual('All');
     
    }));

    it('should execute nextRacesHomeService.getNextRacesModuleConfig and getNextEvents methods and update props on subscription', () => {
      component.getCmsConfigs();
      pubSubFn(cmsData);
      expect(component.moduleTitle).toEqual('Next races');
      expect(component.leftTitleText).toEqual('Next races');
      expect(nextRacesHomeService.getNextRacesModuleConfig).toHaveBeenCalledWith('horseracing',
        {
          NextRaces: { title: 'Next races', numberOfSelections: '10' },
          GreyhoundNextRaces: { numberOfSelections: '4' },
          RacingDataHub: { isEnabledForGreyhound: true},
        });
      expect(component.getNextEvents).toHaveBeenCalled();
    });

    it('should execute nextRacesHomeService.getNextRacesModuleConfig and getNextEvents methods and update props on subscription', () => {
      cmsData.NextRaces.numberOfSelections = 10;
      delete cmsData.RacingDataHub;
      component.getCmsConfigs();
      pubSubFn(cmsData);
      expect(nextRacesHomeService.getNextRacesModuleConfig).toHaveBeenCalledWith('horseracing',
        {
          NextRaces: { title: 'Next races', numberOfSelections: 10 },
          GreyhoundNextRaces: { numberOfSelections: '4' },
          RacingDataHub: undefined
        });
      expect(component.getNextEvents).toHaveBeenCalled();
    });

    describe('should not call nextRacesHomeService.getNextRacesModuleConfig and getNextEvents methods', () => {
      it('when cms config does not contain NextRaces entry', () => {
        cmsData = {};
        component.getCmsConfigs();
        pubSubFn(cmsData);
      });

      it('when called more than once with the same config', () => {
        component.getCmsConfigs();
        pubSubFn(cmsData);
        nextRacesHomeService.getNextRacesModuleConfig.calls.reset();
        (component.getNextEvents as any).calls.reset();
        pubSubFn(cmsData);
      });
      afterEach(() => {
        expect(component.getNextEvents).not.toHaveBeenCalled();
        expect(nextRacesHomeService.getNextRacesModuleConfig).not.toHaveBeenCalled();
      });
    });
  });

  describe('getNextEvents method', () => {
    it('should call racingPostService.updateRacingEventsList method', fakeAsync(() => {
      component.nextRacesModule.storedEvents = [{
        id: '1',
        name: "Catterick",
        categoryId: "19",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDayValue: "racing.today",
      }];
      component.getNextEvents();
      tick();
      expect(racingPostService.updateRacingEventsList).toHaveBeenCalledWith([{ id: 1 }, { id: 2 }], true);
      expect(nextRacesHomeService.getUpdatedEvents).toHaveBeenCalledWith(
        [{ id: 1, racingPostEvent: { } }, { id: 2, racingPostEvent: { } }], 'horseracing');
      expect(pubSubService.publish).toHaveBeenCalledWith('NEXT_RACES_DATA',[component.nextRacesModule.storedEvents]);
    }));

    describe('should toggle showLoader state', () => {
      let resolve = () => {}, reject = () => {};
      beforeEach(() => {
        component.nextRacesModule = {};
        component.showLoader = undefined;
        eventService.getNextEvents.and.returnValue(new Promise((...args) => { [resolve as any, reject] = args; }));

        component.getNextEvents();
        expect(component.showLoader).toEqual(true);
        spyOn(component['dataLoaded'], 'emit');
      });

      it('when event data load process completes', fakeAsync(() => { resolve(); }));
      it('when event data load process fails', fakeAsync(() => { reject(); }));
      afterEach(() => {
        expect(component.showLoader).toEqual(false);
        expect(component['dataLoaded']['emit']).toHaveBeenCalledWith(true);
      });
    });
  });


  it('should enable toogle filter buttons',fakeAsync(()=>{
    component.nextRacesModule.storedEvents = [];
    component.groupDataByFlags();
    tick();
    expect(component.showFilter).toEqual(false);
  }))
  it('should test nextRacesGroupedData',fakeAsync(()=>{
    component.nextRacesModule.storedEvents = [];
    component.showFilter = true;
    horseRacingService.getNextRacesData = (filterAccess: any, nextRacesModule: any) => {
      return {
        storedEvents: [],
        groupedRacing: [
          {flag: 'All', data: []},
          {flag: 'All', data: []},
        ]
      }
    };
    component.groupDataByFlags();
    tick();
    expect(component.nextRacesGroupedData.storedEvents).toEqual([]);
  }))
  it('should test storedEvents',fakeAsync(()=>{
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
    component.selectedFilter = 'All';
    component.groupDataByFlags();
    expect(component.nextRacesGroupedData.storedEvents.length).toEqual(1);
    component.selectedFilter = 'UK';
    component.groupDataByFlags();
    expect(component.nextRacesGroupedData.storedEvents.length).toEqual(1);
    tick();
  }));
  
  it('#registerEvents', () => {
    component.raceModule = 'NEXT_RACE';
    component.registerEvents();

    expect(pubSubService.subscribe).toHaveBeenCalledTimes(2);
    expect(pubSubService.subscribe).toHaveBeenCalledWith('MODULE_NEXT_RACE', 'RELOAD_COMPONENTS', jasmine.any(Function));
  });
  describe('removeSchemaForGHNextRaces', () => {
    it('should publish schema_removed with url', () => {
      component['schemaUrl'] = 'greyhound-racing/races/next';
      component.raceEvent = 'Greyhounds';
      environment.brand = 'ladbrokes';
      component['removeSchemaForGHNextRaces']();
      expect(pubSubService.publish).toHaveBeenCalledWith('SCHEMA_DATA_REMOVED', 'greyhound-racing/races/next');
    });


  it('should check filter change event', () => {
    const filter = {
      value : {
        flag : 'Bet Type',
        data: []
      }
    }
    component.onFilterChange(filter);
    expect(component.selectedFilter).toEqual('Bet Type');
    // expect(component.selectedFilterTabData).toEqual(filter);
  });
});

  it('should call racingService with horse racing service', () => {
    // routingState.getCurrentSegment.and.returnValue('horseracing');
    expect(component.racingService.config.request.categoryId).toEqual('21');
  });
  it('should call racingService with grey racing service', () => {
    routingState.getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('greyhound');
    expect(component.racingService.config.request.categoryId).toEqual('22');
  });
});

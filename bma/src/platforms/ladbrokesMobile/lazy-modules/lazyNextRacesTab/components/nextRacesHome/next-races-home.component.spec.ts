import { NextRacesHomeComponent } from './next-races-home.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';
describe('LadbrokesNextRacesHomeComponent', () => {
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
      sendGTM: jasmine.createSpy('sendGTM'),
      cacheKey: 'nextRaces'
    };
    cmsService = {
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate')
    };
    racingPostService = {
      updateRacingEventsList: jasmine.createSpy('updateRacingEventsList').and.returnValue(
        observableOf([{ id: 1, racingPostEvent: {} }, { id: 2, racingPostEvent: {} }]))
    };
    cmsData = {
      NextRaces: { title: 'Next races', numberOfSelections: '10' },
      GreyhoundNextRaces: { numberOfSelections: '4' },
      RacingDataHub: { isEnabledForGreyhound: true },
      GreyhoundNextRacesToggle: { nextRacesTabEnabled: true }
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
    updateEventService = {};
    greyhoundService ={
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
      getNextRacesData: jasmine.createSpy('getNextRacesData').and.returnValue(Promise.resolve({}))
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

  it('#ngOnInit', () => {
    spyOn(component as any,'schemaForGHNextRaces');
    component.ngOnInit();

    expect(component.raceModule).toEqual('NEXT_RACE');
    expect(component.className).toEqual('next-races-horseracing');
    expect(component.showTimer).toEqual(true);
    expect(component.raceEvent).toEqual('Horse Racing');
    expect(cmsService.triggerSystemConfigUpdate).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalledTimes(3);
    expect(component['schemaForGHNextRaces']).toHaveBeenCalled();
  });

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(nextRacesHomeService.unSubscribeForUpdates).toHaveBeenCalled();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('MODULE_NEXT_RACE');
  });

  it('#sendToGTM', () => {
    component.sendToGTM();

    expect(nextRacesHomeService.sendGTM).toHaveBeenCalledWith('view all', 'home');
  });

  describe('getCmsConfigs method', function () {
    let pubSubFn;

    beforeEach(() => {
      spyOn(component, 'getNextEvents');
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => pubSubFn = cb);
    });

    it('should subscribe to pubsub SYSTEM_CONFIG_UPDATED', () => {
      component.getCmsConfigs();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('MODULE_NEXT_RACE', 'SYSTEM_CONFIG_UPDATED', jasmine.any(Function));
    });

    it('should execute nextRacesHomeService.getNextRacesModuleConfig and getNextEvents methods and update props on subscription', () => {
      component.getCmsConfigs();
      pubSubFn(cmsData);
      expect(component.moduleTitle).toEqual('Next races');
      expect(component.leftTitleText).toEqual('Next races');
      expect(nextRacesHomeService.getNextRacesModuleConfig).toHaveBeenCalledWith('horseracing',
        {
          NextRaces: { title: 'Next races', numberOfSelections: '10' },
          GreyhoundNextRaces: { numberOfSelections: '4' },
          RacingDataHub: { isEnabledForGreyhound: true}
        });
      expect(component.getNextEvents).toHaveBeenCalled();
    });

    it('should execute nextRacesHomeService.getNextRacesModuleConfig and getNextEvents methods and update props on subscription', () => {
      component.moduleType = 'ladsbrokes';
      component.getCmsConfigs();
      pubSubFn(cmsData);
      expect(component.moduleTitle).toEqual('Next races');
      expect(component.leftTitleText).toEqual('Next races');
      expect(nextRacesHomeService.getNextRacesModuleConfig).toHaveBeenCalledWith('ladsbrokes',
        {
          NextRaces: { title: 'Next races', numberOfSelections: '10' },
          GreyhoundNextRaces: { numberOfSelections: '4' },
          RacingDataHub: { isEnabledForGreyhound: true}
        });
      expect(component.getNextEvents).toHaveBeenCalled();
    });
    it('should execute nextRacesHomeService.getNextRacesModuleConfig and getNextEvents methods and update props on subscription', () => {
      delete cmsData.RacingDataHub;
      component.getCmsConfigs();
      pubSubFn(cmsData);
      expect(nextRacesHomeService.getNextRacesModuleConfig).toHaveBeenCalledWith('horseracing',
      {
        NextRaces: { title: 'Next races', numberOfSelections: '10' },
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
      spyOn(component as any,'schemaForGHNextRaces');
      component.getNextEvents();
      tick();
      expect(racingPostService.updateRacingEventsList).toHaveBeenCalledWith([{ id: 1 }, { id: 2 }], true);
      expect(nextRacesHomeService.getUpdatedEvents).toHaveBeenCalledWith(
        [{ id: 1, racingPostEvent: { } }, { id: 2, racingPostEvent: { } }], 'horseracing');
    }));
  });

  it('#registerEvents', () => {
    component.raceModule = 'NEXT_RACE';
    component.registerEvents();

    expect(pubSubService.subscribe).toHaveBeenCalledTimes(2);
    expect(pubSubService.subscribe).toHaveBeenCalledWith('MODULE_NEXT_RACE', 'RELOAD_COMPONENTS', jasmine.any(Function));
  });
  describe('schemaForGHNextRaces', () => {
    it('should call pubsub.publish with events for GH next races', () => {
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => cb());
      component.raceEvent = 'Greyhounds';
      const races = [{
        id: '1',
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "s.today",
      }];
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => {
        if (command === 'NEXT_RACES_DATA') {
          cb(races);
        }
      });
      router.url = '/greyhound-racing/races/next';
      component['schemaForGHNextRaces']();
      expect(pubSubService.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, 'greyhound-racing/races/next']);
    });
    it('should not call pubsub.publish with events for GH router is null', () => {
      component.raceEvent = 'Greyhounds';
      const races = [{
        id: '1',
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "s.today",
      }];
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => {
        if (command === 'NEXT_RACES_DATA') {
          cb(races);
        }
      });
      component['router'] = null;
      component['schemaForGHNextRaces']();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/greyhound-racing/races/next']);
    });
    it('should not call pubsub.publish with events for GH null', () => {
      component.raceEvent = 'Greyhounds';
      const races = null;
      pubSubService.subscribe.and.callFake((subscriberName, command, cb) => {
        if (command === 'NEXT_RACES_DATA') {
          cb(races);
        }
      });
      router.url = '/greyhound-racing/races/next';
      component['schemaForGHNextRaces']();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/greyhound-racing/races/next']);
    });
  });
});

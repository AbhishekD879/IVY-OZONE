import { LadbrokesNextRacesModuleComponent } from '@ladbrokesDesktop/lazy-modules/nextRaces/component/next-races.component';
import { of as observableOf } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';
describe('NextRacesModuleComponent', () => {
  let component: LadbrokesNextRacesModuleComponent;
  let pubSubService, cmsService, location, routingHelperService,
    nextRacesService, eventService, commandService, racingPostService, germanSupportService,windowRefService, horseRacingService, greyhoundService, routingState,cmsData, vEPService;

  beforeEach(() => {
 
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi,};
      cmsService = {
        triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate')
      };
      cmsData = {
        NextRaces: { title: 'Next races', numberOfSelections: '10' },
        GreyhoundNextRaces: { numberOfSelections: '4' },
        RacingDataHub: { isEnabledForGreyhound: true},
        GreyhoundNextRacesToggle: { nextRacesTabEnabled: true }
      };
    location = {};
    routingHelperService = {
      formSportUrl: jasmine.createSpy('formSportUrl').and.returnValue(observableOf({}))
    };
    nextRacesService = {
      getNextRacesModuleConfig: jasmine.createSpy('getNextRacesModuleConfig').and.returnValue({}),
      unSubscribeForUpdates: jasmine.createSpy('unSubscribeForUpdates'),
    };
    eventService = {
      getNextEvents: jasmine.createSpy('getNextEvents').and.returnValue(Promise.resolve([{ id: 1 }, { id: 2 }]))
    };
    commandService = {};
    racingPostService = {};
    germanSupportService = {
      isGermanUser: jasmine.createSpy('isGermanUser').and.returnValue(true),
    };
    windowRefService = {
      document: {
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((v1, cb) => cb({
          detail: { liveUpdate: {channel_type:"sEVENT",payload:{status:'S'},channel_number:'1'} }
        })
        )}
    };
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
      getNextRacesData: jasmine.createSpy('getNextRacesData').and.returnValue(Promise.resolve({})),
      addLpAvailableProp: jasmine.createSpy('addLpAvailableProp'),
      addPersistentInCacheProp: jasmine.createSpy('addPersistentInCacheProp'),
      groupByFlagCodesAndClassesTypeNames: jasmine.createSpy('groupByFlagCodesAndClassesTypeNames').and.returnValue(racingMock),
      sortRaceGroup: jasmine.createSpy('sortRaceGroup')
    },
    greyhoundService ={
      getNextRacesData: jasmine.createSpy('getNextRacesData').and.returnValue(Promise.resolve({})),
    },
    routingState={
      getCurrentSegment:  jasmine.createSpy('getCurrentSegment').and.returnValue('horseracing')

    };

    vEPService = {
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      targetTab:  new BehaviorSubject<any>('targetTab' as any),
    }

    createComponent();
  });

  function createComponent() {
    component = new LadbrokesNextRacesModuleComponent(
      pubSubService,
      cmsService,
      location,
      routingHelperService,
      nextRacesService,
      eventService,
      commandService,
      racingPostService,
      germanSupportService,
      windowRefService,
      horseRacingService,
      greyhoundService,
      routingState,
      vEPService
    );
  }

  it('should create 1', () => {
    expect(component).toBeDefined();
  });
  it('should create 2', () => {
    const parentNgOnInit = spyOn(LadbrokesNextRacesModuleComponent.prototype['__proto__'], 'ngOnInit');
    pubSubService.subscribe.and.callFake((subscriberName, command, cb) => cb(cmsData));
    component.ngOnInit();
    expect(component.isGermanUser).toEqual(true);
    expect(parentNgOnInit).toHaveBeenCalled();
  });
  it('should create 3', () => {
    component.ngOnDestroy();
    // expect(pubSubService.subscribe).toHaveBeenCalledWith('MODULE_W_NEXT_RACE');
  expect(pubSubService.unsubscribe).toHaveBeenCalled();
  });
});
